#!/usr/bin/env python3
"""
Script para corregir el problema de login del administrador
"""

import mysql.connector
import bcrypt
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',
    'database': 'control_asistencia',
    'charset': 'utf8mb4'
}

def corregir_admin_login():
    """Corregir el login del administrador"""
    try:
        print("🔧 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("👤 Verificando usuarios administradores...")
        
        # Buscar administradores
        cursor.execute("SELECT id, uid, nombre, rol, contraseña_hash, activo FROM usuarios WHERE rol = 'admin'")
        admins = cursor.fetchall()
        
        print(f"📊 Administradores encontrados: {len(admins)}")
        
        for admin in admins:
            admin_id, uid, nombre, rol, password_hash, activo = admin
            print(f"\n👤 Admin: {nombre} (UID: {uid})")
            print(f"   Estado: {'Activo' if activo else 'Inactivo'}")
            print(f"   Hash actual: {password_hash[:50]}..." if password_hash else "   Sin contraseña")
            
            # Generar nuevo hash si es necesario
            if not password_hash or password_hash == '$2b$12$defaulthash':
                print("   🔑 Generando nueva contraseña...")
                
                # Generar hash para contraseña por defecto
                nueva_password = "admin123"  # Contraseña por defecto
                salt = bcrypt.gensalt()
                nuevo_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), salt).decode('utf-8')
                
                # Actualizar en la base de datos
                cursor.execute(
                    "UPDATE usuarios SET contraseña_hash = %s WHERE id = %s",
                    (nuevo_hash, admin_id)
                )
                
                print(f"   ✅ Nueva contraseña establecida: {nueva_password}")
                print(f"   🔐 Nuevo hash: {nuevo_hash[:50]}...")
            
            # Asegurar que esté activo
            if not activo:
                cursor.execute("UPDATE usuarios SET activo = TRUE WHERE id = %s", (admin_id,))
                print("   ✅ Usuario activado")
        
        connection.commit()
        
        # Verificar resultado final
        print("\n🔍 Verificación final:")
        cursor.execute("SELECT uid, nombre, rol, activo FROM usuarios WHERE rol = 'admin'")
        admins_final = cursor.fetchall()
        
        for uid, nombre, rol, activo in admins_final:
            estado = "✅ ACTIVO" if activo else "❌ INACTIVO"
            print(f"   👤 {nombre} (UID: {uid}) - {estado}")
        
        cursor.close()
        connection.close()
        
        print("\n✅ CORRECCIÓN DE LOGIN COMPLETADA")
        print("\n📝 Credenciales de administrador:")
        print("   UID: E950D8A2 (o el UID que aparece arriba)")
        print("   Contraseña: admin123")
        print("\n🔧 Reinicia el servidor FastAPI para aplicar cambios")
        
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo login: {e}")
        return False

def main():
    """Función principal"""
    print("🔑" + "="*60)
    print("    CORRECCIÓN DE LOGIN DE ADMINISTRADOR")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    corregir_admin_login()

if __name__ == "__main__":
    main()
