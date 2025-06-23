#!/usr/bin/env python3
"""
Script para probar con el UID real que recibiste: D9B8FEA2
"""

import socketio
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_with_real_uid():
    """Probar con el UID real D9B8FEA2"""
    try:
        sio = socketio.Client()
        
        @sio.event
        def connect():
            logger.info("✅ Conectado al backend")
        
        @sio.event
        def uid_received(data):
            logger.info(f"📥 Confirmación del backend: {data}")
        
        @sio.event
        def respuesta_uid(data):
            logger.info(f"📤 UID retransmitido: {data}")
        
        # Conectar
        sio.connect("http://127.0.0.1:8000")
        
        # Enviar el UID real que recibiste
        real_uid = "D9B8FEA2"
        logger.info(f"📤 Enviando UID real: {real_uid}")
        
        sio.emit("rfid_uid", {
            "uid": real_uid,
            "timestamp": "2025-06-19 11:13:39.798590",
            "source": "test_script"
        })
        
        # Esperar respuesta
        time.sleep(3)
        
        sio.disconnect()
        logger.info("✅ Prueba completada")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Probando con UID real: D9B8FEA2")
    test_with_real_uid()
