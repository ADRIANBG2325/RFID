import socketio
import time
import logging
import sys
from datetime import datetime
import serial

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración - CAMBIAR ESTA URL POR LA DE TU RENDER
RENDER_URL = "https://tu-rfid-system.onrender.com"  # ⚠️ CAMBIAR POR TU URL REAL DE RENDER
SERIAL_PORT = "/dev/ttyACM0"  # Ajustar según tu sistema
BAUD_RATE = 9600
RECONNECT_DELAY = 5
MAX_RECONNECT_ATTEMPTS = 10

class RFIDCloudReader:
    def __init__(self):
        self.sio = socketio.Client(
            logger=True, 
            engineio_logger=True,
            ssl_verify=True
        )
        self.serial_connection = None
        self.is_connected = False
        self.reconnect_attempts = 0
        
        self.setup_socketio_events()
    
    def setup_socketio_events(self):
        @self.sio.event
        def connect():
            logger.info("✅ Conectado al servidor en la nube")
            self.is_connected = True
            self.reconnect_attempts = 0
        
        @self.sio.event
        def connect_error(data):
            logger.error(f"❌ Error de conexión: {data}")
            self.is_connected = False
        
        @self.sio.event
        def disconnect():
            logger.warning("🔌 Desconectado del servidor")
            self.is_connected = False
        
        @self.sio.event
        def pong(data):
            logger.info(f"🏓 Pong recibido: {data}")
        
        @self.sio.event
        def uid_received(data):
            logger.info(f"📨 Confirmación del servidor: {data}")
    
    def connect_to_cloud(self):
        """Conectar al servidor en la nube"""
        while self.reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
            try:
                logger.info(f"🔄 Conectando a {RENDER_URL}... (intento {self.reconnect_attempts + 1})")
                self.sio.connect(RENDER_URL, wait_timeout=15)
                return True
            except Exception as e:
                self.reconnect_attempts += 1
                logger.error(f"❌ Error conectando (intento {self.reconnect_attempts}): {e}")
                if self.reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
                    logger.info(f"⏳ Reintentando en {RECONNECT_DELAY} segundos...")
                    time.sleep(RECONNECT_DELAY)
        
        logger.error("❌ No se pudo conectar después de múltiples intentos")
        return False
    
    def setup_serial_connection(self):
        """Configurar conexión serial"""
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
            self.list_serial_ports()
            return False
    
    def list_serial_ports(self):
        """Listar puertos seriales disponibles"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            logger.info("💡 Puertos seriales disponibles:")
            for port in ports:
                logger.info(f"   - {port.device}: {port.description}")
        except ImportError:
            logger.warning("⚠️ No se puede listar puertos (instalar pyserial)")
    
    def send_uid_to_cloud(self, uid):
        """Enviar UID al servidor en la nube"""
        if not self.is_connected:
            logger.warning("⚠️ No conectado. Intentando reconectar...")
            if not self.connect_to_cloud():
                return False
        
        try:
            data = {
                "uid": uid,
                "timestamp": str(datetime.now()),
                "source": "local_rfid_reader",
                "location": "local_device"
            }
            
            self.sio.emit("rfid_uid", data)
            logger.info(f"📤 UID enviado a la nube: {uid}")
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
                        logger.info(f"🎫 UID leído: {uid}")
                        
                        # Validar formato básico
                        if len(uid) >= 8 and uid.replace(' ', '').isalnum():
                            if self.send_uid_to_cloud(uid):
                                logger.info(f"✅ UID enviado exitosamente: {uid}")
                            else:
                                logger.error(f"❌ Error enviando UID: {uid}")
                        else:
                            logger.warning(f"⚠️ UID con formato inválido: {uid}")
                
                time.sleep(0.1)
                
            except serial.SerialException as e:
                logger.error(f"❌ Error de conexión serial: {e}")
                logger.info("🔄 Intentando reconectar puerto serial...")
                time.sleep(2)
                if not self.setup_serial_connection():
                    logger.error("❌ No se pudo reconectar el puerto serial")
                    break
                    
            except UnicodeDecodeError as e:
                logger.warning(f"⚠️ Error decodificando datos: {e}")
                continue
                
            except KeyboardInterrupt:
                logger.info("🛑 Programa interrumpido por el usuario")
                break
                
            except Exception as e:
                logger.error(f"❌ Error inesperado: {e}")
                time.sleep(1)
    
    def run(self):
        """Ejecutar el lector RFID"""
        logger.info("🚀 Iniciando RFID Reader para la nube...")
        logger.info(f"🌐 Servidor destino: {RENDER_URL}")
        
        # Conectar a la nube
        if not self.connect_to_cloud():
            logger.error("❌ No se pudo conectar al servidor en la nube")
            return False
        
        # Configurar conexión serial
        if not self.setup_serial_connection():
            logger.error("❌ No se pudo configurar la conexión serial")
            return False
        
        # Enviar ping inicial
        try:
            self.sio.emit("ping", {
                "message": "RFID Reader conectado desde dispositivo local",
                "timestamp": str(datetime.now())
            })
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
                logger.info("🔌 Desconectado del servidor")
            except:
                pass

def main():
    if "tu-rfid-system" in RENDER_URL:
        logger.error("❌ DEBES CAMBIAR LA URL DE RENDER EN EL CÓDIGO")
        logger.error("   Edita la línea 15 y cambia 'tu-rfid-system' por el nombre real de tu app en Render")
        logger.error("   Ejemplo: https://rfid-control-abc123.onrender.com")
        return
    
    reader = RFIDCloudReader()
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
