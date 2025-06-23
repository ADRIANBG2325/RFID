#!/usr/bin/env python3
"""
Script para probar el login del administrador
"""

import requests
import json
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Probar el login del administrador"""
    try:
        print("🧪 Probando login de administrador...")
        
        # Datos de login
        login_data = {
            "uid": "E950D8A2",
            "password": "admin123"
        }
        
        # Hacer petición de login
        response = requests.post(
            f"{API_BASE_URL}/usuarios/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN EXITOSO")
            print(f"   Nombre: {data.get('nombre')}")
            print(f"   Rol: {data.get('rol')}")
            print(f"   UID: {data.get('uid')}")
            print(f"   Mensaje: {data.get('mensaje')}")
            return True
        else:
            print("❌ LOGIN FALLIDO")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail')}")
            except:
                print(f"   Error HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrate de que FastAPI esté ejecutándose en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error probando login: {e}")
        return False

def test_admin_endpoints():
    """Probar endpoints de administrador"""
    try:
        print("\n🧪 Probando endpoints de administrador...")
        
        # Probar endpoint de carreras
        response = requests.get(
            f"{API_BASE_URL}/admin/carreras/",
            params={"uid": "E950D8A2"}
        )
        
        print(f"GET /admin/carreras/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data)} carreras obtenidas")
            return True
        else:
            try:
                error_data = response.json()
                print(f"   ❌ Error: {error_data.get('detail')}")
            except:
                print(f"   ❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def main():
    """Función principal"""
    print("🧪" + "="*60)
    print("    PRUEBA DE LOGIN DE ADMINISTRADOR")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Probar login
    login_ok = test_admin_login()
    
    if login_ok:
        # Probar endpoints
        test_admin_endpoints()
    
    print("\n📝 Si el login falla:")
    print("1. Ejecuta: python corregir_login_admin.py")
    print("2. Reinicia el servidor FastAPI")
    print("3. Vuelve a probar")

if __name__ == "__main__":
    main()
