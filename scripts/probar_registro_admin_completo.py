#!/usr/bin/env python3
"""
Prueba completa del registro de administrador
"""

import requests
import json
import time

def probar_registro_admin():
    """Probar diferentes escenarios de registro de admin"""
    
    print("🧪 === PRUEBA COMPLETA REGISTRO ADMIN ===\n")
    
    # Escenarios de prueba
    escenarios = [
        {
            "nombre": "Admin con tarjeta",
            "payload": {
                "uid_o_username": "ADMIN_TARJETA",
                "nombre_usuario": "admin_tarjeta",
                "nombre_completo": "Administrador con Tarjeta",
                "clave_secreta": "SOLDADORES",
                "contraseña": "admin123",
                "confirmar_contraseña": "admin123",
                "tipo_registro": "tarjeta"
            }
        },
        {
            "nombre": "Admin solo username",
            "payload": {
                "uid_o_username": "ADMIN_USER",
                "nombre_usuario": "ADMIN_USER",
                "nombre_completo": "Administrador Username",
                "clave_secreta": "SOLDADORES",
                "contraseña": "admin123",
                "confirmar_contraseña": "admin123",
                "tipo_registro": "username"
            }
        },
        {
            "nombre": "Admin mínimo",
            "payload": {
                "uid_o_username": "ADMIN_MIN",
                "clave_secreta": "SOLDADORES",
                "contraseña": "admin123",
                "confirmar_contraseña": "admin123"
            }
        }
    ]
    
    for i, escenario in enumerate(escenarios, 1):
        print(f"🧪 Escenario {i}: {escenario['nombre']}")
        print(f"   Payload: {json.dumps(escenario['payload'], indent=2)}")
        
        try:
            response = requests.post(
                "http://localhost:8000/usuarios/registrar_admin/",
                json=escenario['payload'],
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Éxito: {data.get('mensaje')}")
                usuario = data.get('usuario', {})
                print(f"   👤 Usuario: {usuario.get('nombre')} (UID: {usuario.get('uid')})")
            else:
                try:
                    error_data = response.json()
                    print(f"   ❌ Error: {error_data.get('detail', 'Error desconocido')}")
                except:
                    print(f"   ❌ Error: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
        
        print()
        time.sleep(1)

def probar_login_admins():
    """Probar login de los admins creados"""
    
    print("🔐 === PRUEBA LOGIN ADMINS ===\n")
    
    admins_prueba = [
        ("ADMIN_TARJETA", "admin123"),
        ("ADMIN_USER", "admin123"),
        ("ADMIN_MIN", "admin123"),
        ("ADMIN001", "admin123"),  # Del script anterior
        ("04FFAABB", "admin123")   # Del script anterior
    ]
    
    for uid, password in admins_prueba:
        print(f"🔐 Probando login: {uid}")
        
        try:
            response = requests.post(
                "http://localhost:8000/usuarios/login/",
                json={"uid": uid, "contraseña": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Login exitoso: {data.get('nombre')} ({data.get('rol')})")
            else:
                try:
                    error_data = response.json()
                    print(f"   ❌ Login fallido: {error_data.get('detail')}")
                except:
                    print(f"   ❌ Login fallido: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)

def main():
    print("🚀 Iniciando pruebas completas...\n")
    
    # Esperar servidor
    print("⏳ Esperando servidor...")
    time.sleep(2)
    
    # Probar registros
    probar_registro_admin()
    
    # Probar logins
    probar_login_admins()
    
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main()
