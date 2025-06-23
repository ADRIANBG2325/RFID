#!/usr/bin/env python3
"""
Script para configuración completa del Sistema de Control de Asistencias RFID
Ejecuta todos los scripts necesarios para inicializar el sistema
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error
import time

def print_step(step_num, description):
    """Imprimir paso con formato"""
    print(f"\n{'='*60}")
    print(f"PASO {step_num}: {description}")
    print(f"{'='*60}")

def execute_sql_file(cursor, file_path):
    """Ejecutar archivo SQL"""
    try:
        print(f"📄 Ejecutando: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir por declaraciones (separadas por ;)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Error as e:
                    if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                        print(f"⚠️  Advertencia en SQL: {e}")
        
        print(f"✅ Completado: {file_path}")
        return True
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    except Error as e:
        print(f"❌ Error ejecutando {file_path}: {e}")
        return False

def main():
    print("🚀 CONFIGURACIÓN COMPLETA DEL SISTEMA DE ASISTENCIAS RFID")
    print("=" * 60)
    
    # Configuración de base de datos
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Cambiar si tienes contraseña
        'database': 'asistencias_rfid'
    }
    
    try:
        # Conectar a la base de datos
        print_step(1, "CONECTANDO A LA BASE DE DATOS")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("✅ Conexión exitosa a la base de datos")
        
        # Paso 2: Crear estructura de base de datos
        print_step(2, "CREANDO ESTRUCTURA DE BASE DE DATOS")
        if execute_sql_file(cursor, "db.sql"):
            connection.commit()
            print("✅ Estructura de base de datos creada")
        
        # Paso 3: Insertar carreras y materias
        print_step(3, "INSERTANDO CARRERAS Y MATERIAS")
        if execute_sql_file(cursor, "scripts/insert_carreras_materias.sql"):
            connection.commit()
            print("✅ Carreras y materias insertadas")
        
        # Paso 4: Insertar alumnos y docentes de ejemplo
        print_step(4, "INSERTANDO ALUMNOS Y DOCENTES DE EJEMPLO")
        if execute_sql_file(cursor, "scripts/insert_alumnos_docentes_ejemplo.sql"):
            connection.commit()
            print("✅ Alumnos y docentes de ejemplo insertados")
        
        # Paso 5: Verificar datos
        print_step(5, "VERIFICANDO DATOS INSERTADOS")
        
        # Verificar carreras
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = TRUE")
        carreras_count = cursor.fetchone()[0]
        print(f"📊 Carreras activas: {carreras_count}")
        
        # Verificar materias
        cursor.execute("SELECT COUNT(*) FROM materias WHERE activa = TRUE")
        materias_count = cursor.fetchone()[0]
        print(f"📚 Materias activas: {materias_count}")
        
        # Verificar alumnos
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = TRUE")
        alumnos_count = cursor.fetchone()[0]
        print(f"👨‍🎓 Alumnos en base: {alumnos_count}")
        
        # Verificar docentes
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = TRUE")
        docentes_count = cursor.fetchone()[0]
        print(f"👨‍🏫 Docentes en base: {docentes_count}")
        
        # Mostrar resumen por carrera
        print("\n📋 RESUMEN POR CARRERA:")
        cursor.execute("""
            SELECT 
                c.nombre as carrera,
                COUNT(DISTINCT m.id) as materias,
                COUNT(DISTINCT a.id) as alumnos
            FROM carreras c
            LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
            LEFT JOIN alumnos_base a ON c.nombre = a.carrera AND a.activo = TRUE
            WHERE c.activa = TRUE
            GROUP BY c.id, c.nombre
            ORDER BY c.nombre
        """)
        
        resultados = cursor.fetchall()
        for carrera, materias, alumnos in resultados:
            print(f"  • {carrera}: {materias} materias, {alumnos} alumnos")
        
        print_step(6, "CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("🎉 El sistema está listo para usar!")
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Ejecutar el backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Abrir el frontend: Abrir frontend/index.html en el navegador")
        print("3. Registrar un administrador en: frontend/admin_registro.html")
        print("4. Acceder al panel de admin en: frontend/admin_login.html")
        
        print("\n🔑 CREDENCIALES DE PRUEBA:")
        print("- Para registrar admin, usar clave secreta: SOLDADORES")
        print("- Los alumnos y docentes pueden registrarse con sus matrículas/claves")
        
    except Error as e:
        print(f"❌ Error de base de datos: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error general: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔌 Conexión a base de datos cerrada")

if __name__ == "__main__":
    main()
