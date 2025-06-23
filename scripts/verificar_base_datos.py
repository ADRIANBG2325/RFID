#!/usr/bin/env python3
"""
Script para verificar el estado de la base de datos
y mostrar información detallada del sistema
"""

import pymysql
import sys
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambiar si tienes contraseña
    'database': 'asistencias_rfid',
    'charset': 'utf8mb4'
}

def conectar_db():
    """Conectar a la base de datos"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ Conexión a base de datos exitosa")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a base de datos: {e}")
        return None

def verificar_estructura_tablas(cursor):
    """Verificar que todas las tablas necesarias existan"""
    print("\n🔍 VERIFICANDO ESTRUCTURA DE TABLAS:")
    
    tablas_requeridas = [
        'usuarios', 'carreras', 'materias', 'alumnos_base', 
        'docentes_base', 'docentes', 'asistencias'
    ]
    
    for tabla in tablas_requeridas:
        try:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            resultado = cursor.fetchone()
            if resultado:
                print(f"  ✅ Tabla '{tabla}' existe")
                
                # Verificar columnas críticas
                if tabla == 'usuarios':
                    cursor.execute("SHOW COLUMNS FROM usuarios")
                    columnas = [col[0] for col in cursor.fetchall()]
                    
                    columnas_requeridas = ['id', 'uid', 'rol', 'nombre', 'contraseña_hash', 'activo', 'fecha_registro']
                    for col in columnas_requeridas:
                        if col in columnas:
                            print(f"    ✅ Columna '{col}' existe")
                        else:
                            print(f"    ❌ Columna '{col}' FALTA")
                            
            else:
                print(f"  ❌ Tabla '{tabla}' NO EXISTE")
        except Exception as e:
            print(f"  ❌ Error verificando tabla '{tabla}': {e}")

def mostrar_estadisticas(cursor):
    """Mostrar estadísticas de la base de datos"""
    print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
    
    try:
        # Usuarios por rol
        cursor.execute("""
            SELECT rol, COUNT(*) as total 
            FROM usuarios 
            GROUP BY rol
        """)
        usuarios_por_rol = cursor.fetchall()
        
        print("  👥 Usuarios registrados:")
        total_usuarios = 0
        for rol, cantidad in usuarios_por_rol:
            print(f"    - {rol}: {cantidad}")
            total_usuarios += cantidad
        print(f"    TOTAL: {total_usuarios}")
        
        # Alumnos base
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = TRUE")
        alumnos_base = cursor.fetchone()[0]
        print(f"  👨‍🎓 Alumnos en base: {alumnos_base}")
        
        # Docentes base
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = TRUE")
        docentes_base = cursor.fetchone()[0]
        print(f"  👨‍🏫 Docentes en base: {docentes_base}")
        
        # Carreras
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = TRUE")
        carreras = cursor.fetchone()[0]
        print(f"  🎓 Carreras activas: {carreras}")
        
        # Materias
        cursor.execute("SELECT COUNT(*) FROM materias WHERE activa = TRUE")
        materias = cursor.fetchone()[0]
        print(f"  📚 Materias activas: {materias}")
        
    except Exception as e:
        print(f"  ❌ Error obteniendo estadísticas: {e}")

def mostrar_usuarios_detalle(cursor):
    """Mostrar detalle de usuarios registrados"""
    print("\n👤 USUARIOS REGISTRADOS:")
    
    try:
        cursor.execute("""
            SELECT id, uid, rol, nombre, matricula, clave_docente, activo
            FROM usuarios 
            ORDER BY rol, nombre
        """)
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("  ⚠️ No hay usuarios registrados")
            return
            
        for usuario in usuarios:
            id_user, uid, rol, nombre, matricula, clave_docente, activo = usuario
            estado = "✅ Activo" if activo else "❌ Inactivo"
            
            print(f"  ID: {id_user} | UID: {uid} | {rol.upper()}")
            print(f"    Nombre: {nombre}")
            if matricula:
                print(f"    Matrícula: {matricula}")
            if clave_docente:
                print(f"    Clave: {clave_docente}")
            print(f"    Estado: {estado}")
            print("    " + "-" * 40)
            
    except Exception as e:
        print(f"  ❌ Error obteniendo usuarios: {e}")

def verificar_admin_emergencia(cursor):
    """Verificar si existe el admin de emergencia"""
    print("\n🚨 VERIFICANDO ADMINISTRADOR DE EMERGENCIA:")
    
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM usuarios 
            WHERE rol = 'admin' AND uid = 'ADMIN_EMERGENCY'
        """)
        admin_emergencia = cursor.fetchone()[0]
        
        if admin_emergencia > 0:
            print("  ✅ Administrador de emergencia existe")
            print("  📋 Credenciales:")
            print("      UID: ADMIN_EMERGENCY")
            print("      Contraseña: admin123")
        else:
            print("  ⚠️ No se encontró administrador de emergencia")
            
        # Verificar si hay otros admins
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'admin'")
        total_admins = cursor.fetchone()[0]
        print(f"  📊 Total de administradores: {total_admins}")
        
    except Exception as e:
        print(f"  ❌ Error verificando admin: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🔍 VERIFICADOR DE BASE DE DATOS - SISTEMA RFID")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conectar a la base de datos
    connection = conectar_db()
    if not connection:
        sys.exit(1)
    
    try:
        cursor = connection.cursor()
        
        # Ejecutar verificaciones
        verificar_estructura_tablas(cursor)
        mostrar_estadisticas(cursor)
        verificar_admin_emergencia(cursor)
        mostrar_usuarios_detalle(cursor)
        
        print("\n" + "=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
    finally:
        connection.close()
        print("🔌 Conexión cerrada")

if __name__ == "__main__":
    main()
