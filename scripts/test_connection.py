#!/usr/bin/env python3
"""
Script para probar la conectividad del sistema
"""

import requests
import socketio
import time
import sys

def test_backend_http():
    """Probar conexión HTTP al backend"""
    try:
        print("🔍 Probando conexión HTTP al backend...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend HTTP funcionando correctamente")
            return True
        else:
            print(f"❌ Backend HTTP respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend HTTP: {e}")
        return False

def test_backend_socketio():
    """Probar conexión Socket.IO al backend"""
    try:
        print("🔍 Probando conexión Socket.IO al backend...")
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print("✅ Socket.IO conectado correctamente")
        
        @sio.event
        def connect_error(data):
            print(f"❌ Error de conexión Socket.IO: {data}")
        
        sio.connect("http://localhost:8000", wait_timeout=10)
        
        # Enviar ping de prueba
        sio.emit("ping", {"message": "Test connection"})
        time.sleep(2)
        
        sio.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Error conectando Socket.IO: {e}")
        return False

def test_rfid_simulation():
    """Simular envío de UID via Socket.IO"""
    try:
        print("🔍 Probando simulación de RFID...")
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print("✅ Conectado para simulación RFID")
            # Simular UID
            test_uid = "TEST123456789"
            sio.emit("rfid_uid", {"uid": test_uid})
            print(f"📤 UID de prueba enviado: {test_uid}")
        
        sio.connect("http://localhost:8000", wait_timeout=10)
        time.sleep(3)
        sio.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Error en simulación RFID: {e}")
        return False

def main():
    print("🧪 Iniciando pruebas de conectividad del sistema")
    print("=" * 50)
    
    tests = [
        ("Backend HTTP", test_backend_http),
        ("Backend Socket.IO", test_backend_socketio),
        ("Simulación RFID", test_rfid_simulation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("📊 Resumen de pruebas:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Todas las pruebas pasaron correctamente!")
        print("💡 El sistema está listo para usar")
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        print("💡 Verifique que el backend esté ejecutándose")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
