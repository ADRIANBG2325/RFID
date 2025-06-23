#!/usr/bin/env python3
"""
Debug específico para registro de administrador
"""

import mysql.connector
import bcrypt
import requests
import json

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'control_asistencia',
    'user': 'User',
    'password': '12345678'
}

def probar_hash_bcrypt():
    """Probar generación de hash bcrypt"""
    print("🔐 Probando generación de hash bcrypt...")
    
    password = "admin123"
    
    # Método 1: bcrypt directo
    hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"Hash 1: {hash1}")
    
    # Verificar
    check1 = bcrypt.checkpw(password.encode('utf-8'), hash1.encode('utf-8'))
    print(f"Verificación 1: {check1}")
    
    return hash1

def insertar_admin_directo():
    """Insertar administrador directamente en la BD"""
    try:
        print("👑 Insertando administrador directamente...")
        
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Generar hash
        password_hash = probar_hash_bcrypt()
        
        # Eliminar admin existente si existe
        cursor.execute("DELETE FROM usuarios WHERE uid = 'ADMIN_TEST'")
        
        # Insertar nuevo admin
        cursor.execute("""
            INSERT INTO usuarios (uid, rol, nombre, clave_docente, contraseña_hash, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("ADMIN_TEST", "admin", "Admin de Prueba", "ADMIN_TEST", password_hash, True))
        
        connection.commit()
        
        # Verificar inserción
        cursor.execute("SELECT * FROM usuarios WHERE uid = 'ADMIN_TEST'")
        admin = cursor.fetchone()
        
        if admin:
            print("✅ Admin insertado correctamente:")
            print(f"   ID: {admin[0]}")
            print(f"   UID: {admin[1]}")
            print(f"   Nombre: {admin[3]}")
            print(f"   Hash: {admin[7][:50]}...")
            
            # Probar login directo
            stored_hash = admin[7]
            login_ok = bcrypt.checkpw("admin123".encode('utf-8'), stored_hash.encode('utf-8'))
            print(f"   Login test: {login_ok}")
            
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_endpoint_registro():
    """Probar endpoint de registro de admin"""
    print("🌐 Probando endpoint de registro...")
    
    payload = {
        "uid_o_username": "ADMIN_API",
        "nombre_usuario": "admin_api",
        "nombre_completo": "Admin desde API",
        "clave_secreta": "SOLDADORES",
        "contraseña": "admin123",
        "confirmar_contraseña": "admin123",
        "tipo_registro": "username"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/usuarios/registrar_admin/",
            json=payload,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Registro exitoso:")
            print(json.dumps(data, indent=2))
        else:
            print("❌ Error en registro")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def verificar_estructura_tabla():
    """Verificar estructura de tabla usuarios"""
    try:
        print("📋 Verificando estructura de tabla usuarios...")
        
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("DESCRIBE usuarios")
        columns = cursor.fetchall()
        
        print("Columnas de la tabla usuarios:")
        for col in columns:
            print(f"  {col[0]}: {col[1]} {col[2]} {col[3]} {col[4]} {col[5]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔧 === DEBUG REGISTRO ADMINISTRADOR ===\n")
    
    # 1. Verificar estructura
    verificar_estructura_tabla()
    print()
    
    # 2. Insertar admin directo
    insertar_admin_directo()
    print()
    
    # 3. Probar endpoint
    probar_endpoint_registro()

if __name__ == "__main__":
    main()
