#!/usr/bin/env python3
"""
Script para probar login directamente
"""

import requests
import json

def probar_login(uid, contraseña):
    """Probar login con la API"""
    try:
        print(f"🔐 Probando login: {uid}")
        
        url = "http://localhost:8000/usuarios/login/"
        data = {
            "uid": uid,
            "contraseña": contraseña
        }
        
        response = requests.post(url, json=data)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso!")
            print(f"   Nombre: {result.get('nombre')}")
            print(f"   Rol: {result.get('rol')}")
            print(f"   Redirect: {result.get('redirect_url')}")
            return True
        else:
            error = response.json()
            print(f"❌ Login falló: {error.get('detail')}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando login: {e}")
        return False

def main():
    """Probar varios usuarios"""
    print("🔍 === PRUEBA DE LOGIN DIRECTO ===\n")
    
    usuarios_prueba = [
        ("ADMIN001", "admin123"),
        ("ALU001", "12345678"),
        ("ALU002", "12345678"),
        ("DOC001", "12345678"),
        ("TEST001", "12345678")
    ]
    
    for uid, contraseña in usuarios_prueba:
        probar_login(uid, contraseña)
        print()

if __name__ == "__main__":
    main()
