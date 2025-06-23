#!/usr/bin/env python3
"""
Script para diagnosticar problemas con usuarios
"""

import sys
import mysql.connector
from mysql.connector import Error
import bcrypt

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'control_asistencia',  # Nombre correcto de la BD
    'user': 'User',
    'password': '12345678'
}

def verificar_conexion():
    """Verificar conexión a la base de datos"""
    try:
        print("🔌 Verificando conexión a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✅ Conectado a la base de datos: {db_name}")
            
            cursor.close()
            connection.close()
            return True
        else:
            print("❌ No se pudo conectar a la base de datos")
            return False
            
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

def verificar_tablas():
    """Verificar que las tablas existan"""
    try:
        print("\n📋 Verificando tablas...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Verificar tabla usuarios
        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        if cursor.fetchone():
            print("✅ Tabla 'usuarios' existe")
            
            # Verificar estructura de la tabla usuarios
            cursor.execute("DESCRIBE usuarios")
            columnas = cursor.fetchall()
            print("📊 Estructura de tabla usuarios:")
            for columna in columnas:
                print(f"  - {columna[0]} ({columna[1]})")
        else:
            print("❌ Tabla 'usuarios' NO existe")
            return False
        
        # Verificar otras tablas importantes
        tablas_importantes = ['alumnos_base', 'docentes_base', 'carreras', 'materias']
        for tabla in tablas_importantes:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            if cursor.fetchone():
                print(f"✅ Tabla '{tabla}' existe")
            else:
                print(f"❌ Tabla '{tabla}' NO existe")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def verificar_usuarios():
    """Verificar usuarios en la base de datos"""
    try:
        print("\n👥 Verificando usuarios...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Contar usuarios totales
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        print(f"📊 Total de usuarios: {total_usuarios}")
        
        if total_usuarios == 0:
            print("❌ No hay usuarios en la base de datos")
            return False
        
        # Mostrar usuarios por rol
        cursor.execute("SELECT rol, COUNT(*) FROM usuarios GROUP BY rol")
        roles = cursor.fetchall()
        print("👥 Usuarios por rol:")
        for rol, count in roles:
            print(f"  - {rol}: {count} usuarios")
        
        # Mostrar algunos usuarios de ejemplo
        cursor.execute("SELECT uid, nombre, rol, activo FROM usuarios LIMIT 10")
        usuarios = cursor.fetchall()
        print("\n📋 Usuarios registrados:")
        for uid, nombre, rol, activo in usuarios:
            estado = "✅ Activo" if activo else "❌ Inactivo"
            print(f"  - {uid}: {nombre} ({rol}) - {estado}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error verificando usuarios: {e}")
        return False

def probar_login(uid, contraseña):
    """Probar login de un usuario específico"""
    try:
        print(f"\n🔐 Probando login: {uid}")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Buscar usuario
        cursor.execute("SELECT uid, nombre, rol, contraseña_hash, activo FROM usuarios WHERE uid = %s", (uid,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuario {uid} no encontrado")
            return False
        
        uid_db, nombre, rol, hash_db, activo = usuario
        print(f"✅ Usuario encontrado: {nombre} ({rol})")
        print(f"📊 Estado: {'Activo' if activo else 'Inactivo'}")
        
        if not activo:
            print("❌ Usuario inactivo")
            return False
        
        # Verificar contraseña
        if bcrypt.checkpw(contraseña.encode('utf-8'), hash_db.encode('utf-8')):
            print("✅ Contraseña correcta")
            return True
        else:
            print("❌ Contraseña incorrecta")
            print(f"Hash en BD: {hash_db[:50]}...")
            return False
        
    except Error as e:
        print(f"❌ Error probando login: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def crear_usuario_prueba():
    """Crear un usuario de prueba simple"""
    try:
        print("\n👤 Creando usuario de prueba...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Datos del usuario de prueba
        uid = "TEST001"
        nombre = "Usuario de Prueba"
        rol = "alumno"
        contraseña = "12345678"
        
        # Hash de la contraseña
        password_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Eliminar usuario si ya existe
        cursor.execute("DELETE FROM usuarios WHERE uid = %s", (uid,))
        
        # Insertar usuario
        cursor.execute("""
            INSERT INTO usuarios (uid, rol, nombre, matricula, contraseña_hash, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uid, rol, nombre, "TEST001", password_hash, True))
        
        connection.commit()
        print(f"✅ Usuario de prueba creado: {uid}")
        print(f"   Nombre: {nombre}")
        print(f"   Rol: {rol}")
        print(f"   Contraseña: {contraseña}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando usuario de prueba: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔍 === DIAGNÓSTICO DE USUARIOS ===\n")
    
    # 1. Verificar conexión
    if not verificar_conexion():
        print("❌ No se puede continuar sin conexión a la BD")
        return False
    
    # 2. Verificar tablas
    if not verificar_tablas():
        print("❌ Problemas con la estructura de tablas")
        return False
    
    # 3. Verificar usuarios existentes
    usuarios_ok = verificar_usuarios()
    
    # 4. Crear usuario de prueba
    if not crear_usuario_prueba():
        print("❌ No se pudo crear usuario de prueba")
        return False
    
    # 5. Probar login con usuario de prueba
    if not probar_login("TEST001", "12345678"):
        print("❌ Login de prueba falló")
        return False
    
    print("\n✅ === DIAGNÓSTICO COMPLETADO ===")
    print("🔧 Recomendaciones:")
    
    if not usuarios_ok:
        print("  1. Ejecutar script de inserción de usuarios")
        print("  2. Verificar configuración de base de datos")
    
    print("  3. Reiniciar servidor FastAPI")
    print("  4. Probar login con usuario TEST001 / 12345678")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
