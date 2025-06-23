import serial
import socketio
import time
import logging
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modificar las constantes al inicio del archivo
SERIAL_PORT = "/dev/ttyACM0"  # Ajustar según tu sistema
BAUD_RATE = 9600

# URL del servidor - cambiar según donde despliegues
BACKEND_URL = "https://tu-app-name.onrender.com"  # Cambiar por tu URL de Render
# Para desarrollo local: BACKEND_URL = "http://127.0.0.1:8000"

RECONNECT_DELAY = 5
MAX_RECONNECT_ATTEMPTS = 10

# Agregar configuración adicional para HTTPS
class RFIDReader:
    def __init__(self):
        # Configuración para conexión HTTPS
        self.sio = socketio.Client(
            logger=True, 
            engineio_logger=True,
            ssl_verify=True  # Verificar certificados SSL en producción
        )
        self.serial_connection = None
        self.is_connected = False
        self.reconnect_attempts = 0
        
        # Configurar eventos de Socket.IO
        self.setup_socketio_events()
    
    def setup_socketio_events(self):
        @self.sio.event
        def connect():
            logger.info("✅ Conectado al backend exitosamente")
            self.is_connected = True
            self.reconnect_attempts = 0
        
        @self.sio.event
        def connect_error(data):
            logger.error(f"❌ Error de conexión al backend: {data}")
            self.is_connected = False
        
        @self.sio.event
        def disconnect():
            logger.warning("🔌 Desconectado del backend")
            self.is_connected = False
        
        @self.sio.event
        def pong(data):
            logger.info(f"🏓 Pong recibido: {data}")
    
    def connect_to_backend(self):
        """Conectar al backend con reintentos"""
        while self.reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
            try:
                logger.info(f"🔄 Intentando conectar al backend... (intento {self.reconnect_attempts + 1})")
                self.sio.connect(BACKEND_URL, wait_timeout=10)
                return True
            except Exception as e:
                self.reconnect_attempts += 1
                logger.error(f"❌ Error conectando (intento {self.reconnect_attempts}): {e}")
                if self.reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
                    logger.info(f"⏳ Reintentando en {RECONNECT_DELAY} segundos...")
                    time.sleep(RECONNECT_DELAY)
        
        logger.error("❌ No se pudo conectar al backend después de múltiples intentos")
        return False
    
    def setup_serial_connection(self):
        """Configurar conexión serial con la Raspberry Pi Pico"""
        try:
            self.serial_connection = serial.Serial(
                SERIAL_PORT, 
                BAUD_RATE, 
                timeout=1,
                write_timeout=1
            )
            logger.info(f"📡 Conexión serial establecida en {SERIAL_PORT}")
            return True
        except serial.SerialException as e:
            logger.error(f"❌ Error abriendo puerto serial {SERIAL_PORT}: {e}")
            logger.info("💡 Puertos disponibles:")
            self.list_serial_ports()
            return False
    
    def list_serial_ports(self):
        """Listar puertos seriales disponibles"""
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            logger.info(f"   - {port.device}: {port.description}")
    
    def send_uid_to_backend(self, uid):
        """Enviar UID al backend"""
        if not self.is_connected:
            logger.warning("⚠️ No conectado al backend. Intentando reconectar...")
            if not self.connect_to_backend():
                return False
        
        try:
            self.sio.emit("rfid_uid", {"uid": uid, "timestamp": str(datetime.now())})
            logger.info(f"📤 UID enviado al backend: {uid}")
            return True
        except Exception as e:
            logger.error(f"❌ Error enviando UID: {e}")
            self.is_connected = False
            return False
    
    def read_rfid_loop(self):
        """Loop principal para leer RFID"""
        logger.info("🎫 Iniciando lectura de tarjetas RFID...")
        
        while True:
            try:
                if self.serial_connection and self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    
                    if line:
                        uid = line.upper()
                        logger.info(f"🎫 UID recibido desde Pico: {uid}")
                        
                        # Validar formato de UID (básico)
                        if len(uid) >= 8 and uid.replace(' ', '').isalnum():
                            if self.send_uid_to_backend(uid):
                                logger.info(f"✅ UID procesado correctamente: {uid}")
                            else:
                                logger.error(f"❌ Error procesando UID: {uid}")
                        else:
                            logger.warning(f"⚠️ UID con formato inválido: {uid}")
                
                time.sleep(0.1)  # Pequeña pausa para no saturar el CPU
                
            except serial.SerialException as e:
                logger.error(f"❌ Error de conexión serial: {e}")
                logger.info("🔄 Intentando reconectar puerto serial...")
                time.sleep(2)
                if not self.setup_serial_connection():
                    logger.error("❌ No se pudo reconectar el puerto serial")
                    break
                    
            except UnicodeDecodeError as e:
                logger.warning(f"⚠️ Error decodificando datos del puerto serial: {e}")
                continue
                
            except KeyboardInterrupt:
                logger.info("🛑 Programa interrumpido por el usuario")
                break
                
            except Exception as e:
                logger.error(f"❌ Error inesperado: {e}")
                time.sleep(1)
    
    def run(self):
        """Ejecutar el lector RFID"""
        logger.info("🚀 Iniciando RFID Reader...")
        
        # Conectar al backend
        if not self.connect_to_backend():
            logger.error("❌ No se pudo conectar al backend. Saliendo...")
            return False
        
        # Configurar conexión serial
        if not self.setup_serial_connection():
            logger.error("❌ No se pudo configurar la conexión serial. Saliendo...")
            return False
        
        # Enviar ping inicial
        try:
            self.sio.emit("ping", {"message": "RFID Reader conectado"})
        except:
            pass
        
        # Iniciar loop de lectura
        try:
            self.read_rfid_loop()
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Limpiar recursos"""
        logger.info("🧹 Limpiando recursos...")
        
        if self.serial_connection:
            try:
                self.serial_connection.close()
                logger.info("📡 Conexión serial cerrada")
            except:
                pass
        
        if self.sio.connected:
            try:
                self.sio.disconnect()
                logger.info("🔌 Desconectado del backend")
            except:
                pass

def main():
    reader = RFIDReader()
    try:
        reader.run()
    except KeyboardInterrupt:
        logger.info("🛑 Programa interrumpido")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
    finally:
        reader.cleanup()

if __name__ == "__main__":
    main()
