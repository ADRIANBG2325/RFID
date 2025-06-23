#!/usr/bin/env python3
"""
Script específico para probar la conexión RFID al backend
"""

import socketio
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = "http://127.0.0.1:8000"

def test_backend_health():
    """Probar endpoint de salud"""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Backend saludable: {data}")
            return True
        else:
            logger.error(f"❌ Backend no saludable: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error probando backend: {e}")
        return False

def test_socketio_connection():
    """Probar conexión Socket.IO específicamente"""
    try:
        logger.info("🔍 Probando conexión Socket.IO...")
        
        sio = socketio.Client(logger=True, engineio_logger=True)
        connection_success = False
        
        @sio.event
        def connect():
            nonlocal connection_success
            logger.info("✅ ¡CONECTADO VIA SOCKET.IO!")
            connection_success = True
        
        @sio.event
        def connect_error(data):
            logger.error(f"❌ Error de conexión: {data}")
        
        @sio.event
        def pong(data):
            logger.info(f"🏓 Pong recibido: {data}")
        
        @sio.event
        def uid_received(data):
            logger.info(f"📥 Confirmación UID: {data}")
        
        # Intentar conexión
        sio.connect(BACKEND_URL, wait_timeout=10)
        
        if connection_success:
            # Enviar ping
            logger.info("📤 Enviando ping...")
            sio.emit("ping", {"message": "RFID Reader test connection"})
            time.sleep(2)
            
            # Simular UID
            test_uid = "TEST123456"
            logger.info(f"📤 Enviando UID de prueba: {test_uid}")
            sio.emit("rfid_uid", {"uid": test_uid, "source": "test"})
            time.sleep(2)
            
            # Obtener estado
            sio.emit("get_status", {})
            time.sleep(2)
            
            sio.disconnect()
            logger.info("✅ Prueba Socket.IO completada exitosamente")
            return True
        else:
            logger.error("❌ No se pudo establecer conexión Socket.IO")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error en prueba Socket.IO: {e}")
        return False

def main():
    print("🧪 DIAGNÓSTICO DE CONEXIÓN RFID")
    print("=" * 40)
    
    # Paso 1: Probar backend HTTP
    print("\n📋 Paso 1: Probando backend HTTP...")
    if not test_backend_health():
        print("❌ El backend no está disponible")
        print("💡 Asegúrese de que el backend esté ejecutándose:")
        print("   cd backend && uvicorn app.main:app_sio --reload")
        return False
    
    # Paso 2: Probar Socket.IO
    print("\n📋 Paso 2: Probando conexión Socket.IO...")
    if not test_socketio_connection():
        print("❌ La conexión Socket.IO falló")
        return False
    
    print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
    print("✅ El sistema está listo para el lector RFID")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
