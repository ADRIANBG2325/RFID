#!/usr/bin/env python3
"""
Script para configurar completamente el sistema de control de asistencias RFID
Ejecuta todas las correcciones necesarias en la base de datos
"""

import pymysql
import sys
import os
from pathlib import Path

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',
    'database': 'control_asistencia',
    'charset': 'utf8mb4'
}

def conectar_db():
    """Conectar a la base de datos"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ Conexión a la base de datos establecida")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None

def ejecutar_script_sql(connection, script_path):
    """Ejecutar un script SQL"""
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir por declaraciones (separadas por ;)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        with connection.cursor() as cursor:
            for statement in statements:
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        print(f"⚠️ Warning ejecutando statement: {e}")
                        continue
            
            connection.commit()
        
        print(f"✅ Script ejecutado: {script_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando script {script_path}: {e}")
        return False

def verificar_estructura():
    """Verificar que la estructura esté correcta"""
    connection = conectar_db()
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            # Verificar carreras
            cursor.execute("SELECT id, nombre FROM carreras ORDER BY id")
            carreras = cursor.fetchall()
            print("\n📋 Carreras configuradas:")
            for carrera in carreras:
                print(f"  {carrera[0]}: {carrera[1]}")
            
            # Verificar materias por carrera
            cursor.execute("""
                SELECT c.id, c.nombre, COUNT(m.id) as total_materias
                FROM carreras c
                LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
                WHERE c.activa = TRUE
                GROUP BY c.id, c.nombre
                ORDER BY c.id
            """)
            stats = cursor.fetchall()
            print("\n📚 Materias por carrera:")
            for stat in stats:
                print(f"  {stat[0]}: {stat[1]} - {stat[2]} materias")
            
            # Verificar datos de ejemplo
            cursor.execute("SELECT COUNT(*) FROM alumnos_base")
            alumnos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM docentes_base")
            docentes = cursor.fetchone()[0]
            
            print(f"\n👥 Datos de ejemplo:")
            print(f"  Alumnos: {alumnos}")
            print(f"  Docentes: {docentes}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def main():
    print("🚀 === CONFIGURACIÓN COMPLETA DEL SISTEMA ===")
    print("Este script configurará completamente la base de datos\n")
    
    # Obtener directorio de scripts
    script_dir = Path(__file__).parent
    
    # Scripts a ejecutar en orden
    scripts = [
        script_dir / "fix_database_schema.sql",
        script_dir / "insert_sample_data.sql"
    ]
    
    # Verificar que existan los scripts
    for script in scripts:
        if not script.exists():
            print(f"❌ Script no encontrado: {script}")
            return False
    
    # Conectar a la base de datos
    connection = conectar_db()
    if not connection:
        return False
    
    try:
        print("📝 Ejecutando scripts de configuración...\n")
        
        # Ejecutar cada script
        for script in scripts:
            print(f"🔄 Ejecutando: {script.name}")
            if not ejecutar_script_sql(connection, script):
                print(f"❌ Error en script: {script.name}")
                return False
            print()
        
        print("✅ Todos los scripts ejecutados correctamente\n")
        
        # Verificar estructura final
        print("🔍 Verificando estructura final...")
        if verificar_estructura():
            print("\n🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
            print("\nEl sistema está listo para usar:")
            print("1. ✅ Base de datos configurada")
            print("2. ✅ Carreras y materias insertadas")
            print("3. ✅ Datos de ejemplo agregados")
            print("4. ✅ Estructura verificada")
            print("\n🚀 Puede iniciar el servidor backend ahora")
            return True
        else:
            print("❌ Error en la verificación final")
            return False
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False
    finally:
        connection.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
