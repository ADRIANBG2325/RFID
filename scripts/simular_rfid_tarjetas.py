#!/usr/bin/env python3
"""
Simulador de tarjetas RFID para pruebas
"""

import socketio
import time
import sys

# UIDs de tarjetas simuladas
TARJETAS_RFID = {
    "04 5C 8A 2A": "Juan Carlos Pérez López (Alumno)",
    "04 7B 9C 3B": "María Elena González Martínez (Alumno)",
    "04 8D 1E 4C": "Roberto Miguel Jiménez Cruz (Alumno)",
    "04 9F 2A 5D": "Dr. Miguel Ángel Rodríguez Hernández (Docente)",
    "04 1A 3B 6E": "Ing. Laura Patricia Gómez Sánchez (Docente)",
    "04 2C 4D 7F": "M.C. José Luis Martínez Torres (Docente)",
    "04 FF AA BB": "Administrador con Tarjeta (Admin)",
    "ADMIN001": "Administrador del Sistema (Admin)"
}

def simular_lector_rfid():
    """Simular lector RFID enviando UIDs al servidor"""
    try:
        print("📡 === SIMULADOR DE TARJETAS RFID ===\n")
        
        # Conectar al servidor Socket.IO
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print("✅ Conectado al servidor")
            sio.emit("ping", {"message": "RFID Reader Simulator conectado"})
        
        @sio.event
        def disconnect():
            print("🔌 Desconectado del servidor")
        
        @sio.event
        def pong(data):
            print(f"🏓 Pong recibido: {data.get('message', '')}")
        
        @sio.event
        def uid_received(data):
            print(f"📥 Confirmación: {data.get('message', '')}")
        
        print("🔌 Conectando al servidor...")
        sio.connect("http://localhost:8000")
        
        print("\n📋 Tarjetas RFID disponibles:")
        for i, (uid, descripcion) in enumerate(TARJETAS_RFID.items(), 1):
            print(f"  {i}. {uid} - {descripcion}")
        
        while True:
            print(f"\n📡 Seleccione una tarjeta (1-{len(TARJETAS_RFID)}) o 'q' para salir: ", end="")
            opcion = input().strip()
            
            if opcion.lower() == 'q':
                break
            
            try:
                indice = int(opcion) - 1
                if 0 <= indice < len(TARJETAS_RFID):
                    uid = list(TARJETAS_RFID.keys())[indice]
                    descripcion = TARJETAS_RFID[uid]
                    
                    print(f"📤 Enviando UID: {uid}")
                    print(f"👤 Usuario: {descripcion}")
                    
                    # Enviar UID al servidor
                    sio.emit("rfid_uid", {
                        "uid": uid,
                        "source": "simulator",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    print("✅ UID enviado")
                    time.sleep(1)
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Ingrese un número válido")
        
        sio.disconnect()
        print("👋 Simulador cerrado")
        
    except Exception as e:
        print(f"❌ Error en simulador: {e}")

def enviar_uid_directo(uid):
    """Enviar un UID específico directamente"""
    try:
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print(f"📤 Enviando UID: {uid}")
            sio.emit("rfid_uid", {"uid": uid, "source": "direct"})
            time.sleep(1)
            sio.disconnect()
        
        sio.connect("http://localhost:8000")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error enviando UID: {e}")

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        # Modo directo: python simular_rfid_tarjetas.py "04 5C 8A 2A"
        uid = sys.argv[1]
        if uid in TARJETAS_RFID:
            print(f"📡 Enviando UID directo: {uid}")
            enviar_uid_directo(uid)
        else:
            print(f"❌ UID no reconocido: {uid}")
            print("UIDs disponibles:")
            for uid_disponible in TARJETAS_RFID.keys():
                print(f"  - {uid_disponible}")
    else:
        # Modo interactivo
        simular_lector_rfid()

if __name__ == "__main__":
    main()
