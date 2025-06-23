#!/usr/bin/env python3
"""
Simulador de tarjetas RFID mejorado
"""

import requests
import time
import json
import sys

# Tarjetas RFID simuladas
TARJETAS_RFID = {
    "1": {"uid": "ADMIN001", "nombre": "Admin Principal", "tipo": "admin"},
    "2": {"uid": "04FFAABB", "nombre": "Admin con Tarjeta", "tipo": "admin"},
    "3": {"uid": "045C8A2A", "nombre": "Juan Carlos (Alumno)", "tipo": "alumno"},
    "4": {"uid": "047B9C3B", "nombre": "María Elena (Alumno)", "tipo": "alumno"},
    "5": {"uid": "048D1E4C", "nombre": "Roberto (Alumno)", "tipo": "alumno"},
    "6": {"uid": "049F2A5D", "nombre": "Dr. Miguel (Docente)", "tipo": "docente"},
    "7": {"uid": "041A3B6E", "nombre": "Ing. Laura (Docente)", "tipo": "docente"},
    "8": {"uid": "NUEVA001", "nombre": "Tarjeta Nueva", "tipo": "nueva"},
}

def mostrar_menu():
    """Mostrar menú de tarjetas"""
    print("\n📡 === SIMULADOR DE TARJETAS RFID ===")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ Seleccione una tarjeta para simular:                   │")
    print("├─────────────────────────────────────────────────────────┤")
    
    for key, tarjeta in TARJETAS_RFID.items():
        tipo_icon = {"admin": "👑", "alumno": "👨‍🎓", "docente": "👨‍🏫", "nueva": "🆕"}
        icon = tipo_icon.get(tarjeta["tipo"], "📱")
        print(f"│ {key}. {icon} {tarjeta['uid']:<12} - {tarjeta['nombre']:<25} │")
    
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 9. Probar login directo                                 │")
    print("│ 0. Salir                                                │")
    print("└─────────────────────────────────────────────────────────┘")

def enviar_uid_al_servidor(uid):
    """Enviar UID al servidor"""
    try:
        print(f"📡 Enviando UID: {uid}")
        
        # Verificar UID
        response = requests.post(
            "http://localhost:8000/usuarios/verificar_uid/",
            json={"uid": uid},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("existe"):
                usuario = data.get("usuario", {})
                print(f"✅ Usuario encontrado:")
                print(f"   Nombre: {usuario.get('nombre')}")
                print(f"   Rol: {usuario.get('rol')}")
                print(f"   UID: {usuario.get('uid') or uid}")
                if usuario.get('matricula'):
                    print(f"   Matrícula: {usuario.get('matricula')}")
                if usuario.get('carrera'):
                    print(f"   Carrera: {usuario.get('carrera')}")
                return True
            else:
                print(f"🆕 Usuario nuevo - UID disponible para registro")
                return True
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalle: {error_data.get('detail', 'Error desconocido')}")
            except:
                print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrese de que el servidor FastAPI esté ejecutándose en http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servidor no responde")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def probar_login_directo():
    """Probar login directo con credenciales"""
    print("\n🔐 === PRUEBA DE LOGIN DIRECTO ===")
    
    credenciales = [
        ("ADMIN001", "admin123", "Admin Principal"),
        ("04FFAABB", "admin123", "Admin con Tarjeta"),
        ("045C8A2A", "12345678", "Juan Carlos (Alumno)"),
        ("047B9C3B", "12345678", "María Elena (Alumno)"),
        ("049F2A5D", "12345678", "Dr. Miguel (Docente)")
    ]
    
    for uid, password, nombre in credenciales:
        try:
            print(f"\n🔐 Probando login: {nombre}")
            print(f"   UID: {uid}")
            print(f"   Contraseña: {password}")
            
            response = requests.post(
                "http://localhost:8000/usuarios/login/",
                json={"uid": uid, "contraseña": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Login exitoso: {data.get('mensaje')}")
                print(f"   👤 Usuario: {data.get('nombre')}")
                print(f"   🎭 Rol: {data.get('rol')}")
                print(f"   🔗 Redirección: {data.get('redirect_url')}")
            else:
                print(f"   ❌ Login fallido: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   📝 Error: {error_data.get('detail', 'Error desconocido')}")
                except:
                    print(f"   📝 Respuesta: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Pausa entre pruebas

def main():
    """Función principal del simulador"""
    print("🚀 Iniciando simulador de tarjetas RFID...")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n👆 Seleccione una opción: ").strip()
            
            if opcion == "0":
                print("👋 Saliendo del simulador...")
                break
            elif opcion == "9":
                probar_login_directo()
            elif opcion in TARJETAS_RFID:
                tarjeta = TARJETAS_RFID[opcion]
                print(f"\n📱 Simulando tarjeta: {tarjeta['nombre']}")
                print(f"   UID: {tarjeta['uid']}")
                
                if enviar_uid_al_servidor(tarjeta['uid']):
                    print("✅ Tarjeta simulada correctamente")
                else:
                    print("❌ Error simulando tarjeta")
            else:
                print("❌ Opción no válida")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo del simulador...")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        # Pausa antes del siguiente menú
        input("\n⏸️  Presione Enter para continuar...")

if __name__ == "__main__":
    main()
