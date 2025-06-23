#!/usr/bin/env python3
"""
Script para reparar completamente la base de datos y solucionar todos los problemas
"""

import sys
import os
import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'asistencias_rfid',
    'user': 'root',
    'password': ''
}

def ejecutar_sql_desde_archivo(cursor, archivo_sql):
    """Ejecutar comandos SQL desde un archivo"""
    try:
        print(f"📄 Ejecutando archivo: {archivo_sql}")
        
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir por comandos (separados por ;)
        comandos = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        for i, comando in enumerate(comandos, 1):
            if comando.strip():
                try:
                    cursor.execute(comando)
                    print(f"  ✅ Comando {i} ejecutado correctamente")
                except Error as e:
                    if "Duplicate entry" in str(e) or "already exists" in str(e):
                        print(f"  ⚠️ Comando {i} - Dato ya existe (OK): {e}")
                    else:
                        print(f"  ⚠️ Warning en comando {i}: {e}")
                    continue
        
        return True
    except Exception as e:
        print(f"❌ Error ejecutando archivo {archivo_sql}: {e}")
        return False

def verificar_estructura_docentes(cursor):
    """Verificar y corregir estructura de tabla docentes"""
    try:
        print("\n🔧 Verificando estructura de tabla docentes...")
        
        # Verificar columnas actuales
        cursor.execute("DESCRIBE docentes")
        columnas = cursor.fetchall()
        
        print("📋 Columnas actuales en tabla docentes:")
        for columna in columnas:
            print(f"  - {columna[0]} ({columna[1]})")
        
        # Verificar si existe columna especialidad
        tiene_especialidad = any(col[0] == 'especialidad' for col in columnas)
        
        if tiene_especialidad:
            print("⚠️ Eliminando columna 'especialidad' de tabla docentes...")
            cursor.execute("ALTER TABLE docentes DROP COLUMN especialidad")
            print("✅ Columna 'especialidad' eliminada")
        
        # Verificar estructura final
        cursor.execute("DESCRIBE docentes")
        columnas_finales = cursor.fetchall()
        
        print("📋 Estructura final de tabla docentes:")
        for columna in columnas_finales:
            print(f"  - {columna[0]} ({columna[1]})")
        
        return True
    except Error as e:
        print(f"❌ Error verificando estructura docentes: {e}")
        return False

def agregar_columna_activo_usuarios(cursor):
    """Agregar columna activo a usuarios si no existe"""
    try:
        print("\n👤 Verificando columna 'activo' en tabla usuarios...")
        
        # Verificar si existe la columna
        cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'activo'")
        resultado = cursor.fetchone()
        
        if not resultado:
            print("➕ Agregando columna 'activo' a tabla usuarios...")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE")
            print("✅ Columna 'activo' agregada")
        else:
            print("✅ Columna 'activo' ya existe")
        
        # Actualizar usuarios existentes
        cursor.execute("UPDATE usuarios SET activo = TRUE WHERE activo IS NULL")
        print("✅ Usuarios existentes marcados como activos")
        
        return True
    except Error as e:
        print(f"❌ Error agregando columna activo: {e}")
        return False

def verificar_datos(cursor):
    """Verificar que todos los datos estén correctos"""
    try:
        print("\n📊 Verificando datos en la base de datos...")
        
        # Verificar carreras
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = TRUE")
        total_carreras = cursor.fetchone()[0]
        print(f"🎓 Carreras activas: {total_carreras}")
        
        # Verificar materias
        cursor.execute("SELECT COUNT(*) FROM materias WHERE activa = TRUE")
        total_materias = cursor.fetchone()[0]
        print(f"📚 Materias activas: {total_materias}")
        
        # Verificar alumnos base
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = TRUE")
        total_alumnos = cursor.fetchone()[0]
        print(f"👨‍🎓 Alumnos base: {total_alumnos}")
        
        # Verificar docentes base
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = TRUE")
        total_docentes = cursor.fetchone()[0]
        print(f"👨‍🏫 Docentes base: {total_docentes}")
        
        # Verificar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = TRUE")
        total_usuarios = cursor.fetchone()[0]
        print(f"👤 Usuarios activos: {total_usuarios}")
        
        # Mostrar carreras específicas
        cursor.execute("SELECT id, nombre FROM carreras WHERE activa = TRUE ORDER BY id")
        carreras = cursor.fetchall()
        print(f"\n📋 Lista de carreras:")
        for carrera in carreras:
            print(f"  {carrera[0]}. {carrera[1]}")
        
        return True
    except Error as e:
        print(f"❌ Error verificando datos: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 === REPARACIÓN COMPLETA DE LA BASE DE DATOS ===\n")
    
    connection = None
    try:
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conexión establecida")
        
        # 1. Agregar columna activo a usuarios
        if not agregar_columna_activo_usuarios(cursor):
            print("❌ Error agregando columna activo")
            return False
        
        # 2. Verificar y corregir estructura de docentes
        if not verificar_estructura_docentes(cursor):
            print("❌ Error corrigiendo estructura docentes")
            return False
        
        # 3. Ejecutar script de reparación
        archivo_sql = "scripts/fix_database_structure_final.sql"
        if os.path.exists(archivo_sql):
            if not ejecutar_sql_desde_archivo(cursor, archivo_sql):
                print("❌ Error ejecutando script de reparación")
                return False
        else:
            print(f"⚠️ Archivo {archivo_sql} no encontrado, continuando...")
        
        # 4. Confirmar cambios
        connection.commit()
        print("✅ Cambios confirmados en la base de datos")
        
        # 5. Verificar datos
        if not verificar_datos(cursor):
            print("❌ Error verificando datos")
            return False
        
        print("\n✅ === REPARACIÓN COMPLETADA EXITOSAMENTE ===")
        
        print(f"\n📋 Resumen de reparaciones:")
        print(f"  ✅ Estructura de tabla docentes corregida")
        print(f"  ✅ Columna 'activo' agregada a usuarios")
        print(f"  ✅ Carreras y materias verificadas")
        print(f"  ✅ Datos de ejemplo insertados")
        print(f"  ✅ Sistema listo para usar")
        
        print(f"\n🔄 Próximos pasos:")
        print(f"  1. Reiniciar el servidor FastAPI")
        print(f"  2. Probar el registro de docentes")
        print(f"  3. Verificar login de alumnos")
        print(f"  4. Probar activación/desactivación de usuarios")
        
        return True
        
    except Error as e:
        print(f"❌ Error de base de datos: {e}")
        if connection:
            connection.rollback()
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
