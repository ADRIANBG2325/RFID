import serial
import socketio
import time
import logging
import sys
import requests
from datetime import datetime
import threading

# Configurar logging más detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('rfid_reader.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuración
SERIAL_PORT = "/dev/ttyACM0"  # Cambiar según tu sistema
BAUD_RATE = 9600
BACKEND_URL = "http://127.0.0.1:8000"
RECONNECT_DELAY = 3  # segundos
MAX_RECONNECT_ATTEMPTS = 20

class RFIDReaderDebug:
    def __init__(self):
        self.sio = None
        self.serial_connection = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.should_run = True
        
    def test_backend_availability(self):
        """Probar si el backend está disponible"""
        try:
            logger.info("🔍 Probando disponibilidad del backend...")
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Backend HTTP está disponible")
                return True
            else:
                logger.error(f"❌ Backend respondió con código: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ No se puede conectar al backend - ¿Está ejecutándose?")
            return False
        except Exception as e:
            logger.error(f"❌ Error probando backend: {e}")
            return False
    
    def setup_socketio_client(self):
        """Configurar cliente Socket.IO con opciones detalladas"""
        try:
            logger.info("🔧 Configurando cliente Socket.IO...")
            
            self.sio = socketio.Client(
                logger=True,
                engineio_logger=True,
                reconnection=True,
                reconnection_attempts=5,
                reconnection_delay=2,
                reconnection_delay_max=10,
                timeout=20
            )
            
            @self.sio.event
            def connect():
                logger.info("✅ ¡CONECTADO AL BACKEND EXITOSAMENTE!")
                self.is_connected = True
                self.reconnect_attempts = 0
                # Enviar mensaje de prueba
                self.sio.emit("ping", {"message": "RFID Reader conectado", "timestamp": str(datetime.now())})
            
            @self.sio.event
            def connect_error(data):
                logger.error(f"❌ ERROR DE CONEXIÓN SOCKET.IO: {data}")
                self.is_connected = False
            
            @self.sio.event
            def disconnect():
                logger.warning("🔌 DESCONECTADO DEL BACKEND")
                self.is_connected = False
            
            @self.sio.event
            def pong(data):
                logger.info(f"🏓 Pong recibido del backend: {data}")
            
            logger.info("✅ Cliente Socket.IO configurado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error configurando Socket.IO: {e}")
            return False
    
    def connect_to_backend(self):
        """Conectar al backend con diagnóstico detallado"""
        logger.info(f"🔄 Intento de conexión #{self.reconnect_attempts + 1}")
        
        # Primero probar HTTP
        if not self.test_backend_availability():
            logger.error("❌ Backend no disponible via HTTP")
            return False
        
        try:
            logger.info(f"🔗 Conectando a {BACKEND_URL}...")
            
            # Intentar conexión con timeout específico
            self.sio.connect(
                BACKEND_URL, 
                wait_timeout=15,
                transports=['polling', 'websocket']
            )
            
            # Esperar un momento para confirmar conexión
            time.sleep(2)
            
            if self.sio.connected:
                logger.info("✅ Conexión Socket.IO establecida")
                return True
            else:
                logger.error("❌ Socket.IO no se conectó correctamente")
                return False
                
        except socketio.exceptions.ConnectionError as e:
            logger.error(f"❌ Error de conexión Socket.IO: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado conectando: {e}")
            return False
    
    def reconnect_loop(self):
        """Loop de reconexión con backoff"""
        while self.should_run and self.reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
            if self.is_connected:
                time.sleep(1)
                continue
                
            self.reconnect_attempts += 1
            logger.info(f"🔄 Intento de reconexión {self.reconnect_attempts}/{MAX_RECONNECT_ATTEMPTS}")
            
            if self.connect_to_backend():
                logger.info("✅ Reconexión exitosa")
                self.reconnect_attempts = 0
            else:
                delay = min(RECONNECT_DELAY * self.reconnect_attempts, 30)
                logger.info(f"⏳ Esperando {delay} segundos antes del siguiente intento...")
                time.sleep(delay)
        
        if self.reconnect_attempts >= MAX_RECONNECT_ATTEMPTS:
            logger.error("❌ Se agotaron los intentos de reconexión")
    
    def list_serial_ports(self):
        """Listar puertos seriales disponibles"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            logger.info("📡 Puertos seriales disponibles:")
            for port in ports:
                logger.info(f"   - {port.device}: {port.description}")
            return [port.device for port in ports]
        except Exception as e:
            logger.error(f"❌ Error listando puertos: {e}")
            return []
    
    def setup_serial_connection(self):
        """Configurar conexión serial con auto-detección"""
        # Primero intentar el puerto configurado
        ports_to_try = [SERIAL_PORT]
        
        # Agregar puertos detectados automáticamente
        detected_ports = self.list_serial_ports()
        for port in detected_ports:
            if port not in ports_to_try:
                ports_to_try.append(port)
        
        for port in ports_to_try:
            try:
                logger.info(f"🔌 Intentando conectar a {port}...")
                self.serial_connection = serial.Serial(
                    port, 
                    BAUD_RATE, 
                    timeout=1,
                    write_timeout=1
                )
                logger.info(f"✅ Conexión serial establecida en {port}")
                return True
                
            except serial.SerialException as e:
                logger.warning(f"⚠️ No se pudo conectar a {port}: {e}")
                continue
        
        logger.error("❌ No se pudo establecer conexión serial en ningún puerto")
        return False
    
    def send_uid_to_backend(self, uid):
        """Enviar UID al backend con reintentos"""
        if not self.is_connected:
            logger.warning("⚠️ No conectado al backend")
            return False
        
        try:
            payload = {
                "uid": uid, 
                "timestamp": str(datetime.now()),
                "source": "rfid_reader"
            }
            
            logger.info(f"📤 Enviando UID al backend: {uid}")
            self.sio.emit("rfid_uid", payload)
            logger.info(f"✅ UID enviado exitosamente: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando UID: {e}")
            self.is_connected = False
            return False
    
    def simulate_uid_input(self):
        """Simular entrada de UID para pruebas"""
        logger.info("🧪 Modo simulación activado")
        counter = 1
        
        while self.should_run:
            if self.is_connected:
                test_uid = f"TEST{counter:04d}"
                logger.info(f"🎫 Simulando UID: {test_uid}")
                self.send_uid_to_backend(test_uid)
                counter += 1
                time.sleep(10)  # Simular cada 10 segundos
            else:
                time.sleep(1)
    
    def read_rfid_loop(self):
        """Loop principal para leer RFID"""
        logger.info("🎫 Iniciando lectura de tarjetas RFID...")
        
        while self.should_run:
            try:
                if not self.serial_connection:
                    logger.warning("⚠️ Sin conexión serial, reintentando...")
                    if not self.setup_serial_connection():
                        time.sleep(5)
                        continue
                
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    
                    if line:
                        uid = line.upper()
                        logger.info(f"🎫 UID recibido desde hardware: {uid}")
                        
                        # Validar formato básico
                        if len(uid) >= 4 and uid.replace(' ', '').replace(':', '').isalnum():
                            if self.is_connected:
                                self.send_uid_to_backend(uid)
                            else:
                                logger.warning(f"⚠️ UID recibido pero no conectado al backend: {uid}")
                        else:
                            logger.warning(f"⚠️ UID con formato inválido: {uid}")
                
                time.sleep(0.1)
                
            except serial.SerialException as e:
                logger.error(f"❌ Error de conexión serial: {e}")
                self.serial_connection = None
                time.sleep(2)
                
            except UnicodeDecodeError as e:
                logger.warning(f"⚠️ Error decodificando datos: {e}")
                continue
                
            except Exception as e:
                logger.error(f"❌ Error inesperado en lectura RFID: {e}")
                time.sleep(1)
    
    def run(self):
        """Ejecutar el lector RFID"""
        logger.info("🚀 INICIANDO RFID READER CON DIAGNÓSTICO...")
        logger.info(f"Backend URL: {BACKEND_URL}")
        logger.info(f"Puerto Serial: {SERIAL_PORT}")
        
        # Configurar Socket.IO
        if not self.setup_socketio_client():
            logger.error("❌ No se pudo configurar Socket.IO")
            return False
        
        # Iniciar thread de reconexión
        reconnect_thread = threading.Thread(target=self.reconnect_loop, daemon=True)
        reconnect_thread.start()
        
        # Preguntar modo de operación
        print("\n" + "="*50)
        print("🎛️  MODO DE OPERACIÓN:")
        print("1. Hardware RFID (requiere Raspberry Pi Pico)")
        print("2. Simulación (para pruebas sin hardware)")
        print("="*50)
        
        try:
            choice = input("Seleccione modo (1 o 2): ").strip()
        except KeyboardInterrupt:
            logger.info("🛑 Programa interrumpido")
            return False
        
        if choice == "2":
            logger.info("🧪 Iniciando modo simulación...")
            self.simulate_uid_input()
        else:
            logger.info("🔌 Iniciando modo hardware...")
            if not self.setup_serial_connection():
                logger.error("❌ No se pudo configurar conexión serial")
                logger.info("💡 Pruebe el modo simulación (opción 2)")
                return False
            self.read_rfid_loop()
        
        return True
    
    def cleanup(self):
        """Limpiar recursos"""
        logger.info("🧹 Limpiando recursos...")
        self.should_run = False
        
        if self.serial_connection:
            try:
                self.serial_connection.close()
                logger.info("📡 Conexión serial cerrada")
            except:
                pass
        
        if self.sio and self.sio.connected:
            try:
                self.sio.disconnect()
                logger.info("🔌 Desconectado del backend")
            except:
                pass

def main():
    reader = RFIDReaderDebug()
    try:
        reader.run()
    except KeyboardInterrupt:
        logger.info("🛑 Programa interrumpido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
    finally:
        reader.cleanup()

if __name__ == "__main__":
    main()
