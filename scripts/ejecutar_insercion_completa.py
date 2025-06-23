#!/usr/bin/env python3
"""
Script para ejecutar la inserción completa de carreras, materias, alumnos y docentes
Ejecuta los scripts SQL en el orden correcto
"""

import mysql.connector
import os
import sys
from pathlib import Path

def conectar_db():
    """Conectar a la base de datos MySQL"""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Cambiar si tienes contraseña
            database='control_asistencias'
        )
        return conexion
    except mysql.connector.Error as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None

def ejecutar_script_sql(conexion, archivo_sql):
    """Ejecutar un archivo SQL"""
    try:
        cursor = conexion.cursor()
        
        # Leer el archivo SQL
        with open(archivo_sql, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        # Dividir por declaraciones (separadas por ;)
        declaraciones = [stmt.strip() for stmt in contenido.split(';') if stmt.strip()]
        
        print(f"📄 Ejecutando {archivo_sql}...")
        
        for i, declaracion in enumerate(declaraciones, 1):
            if declaracion.strip():
                try:
                    cursor.execute(declaracion)
                    print(f"   ✅ Declaración {i}/{len(declaraciones)} ejecutada")
                except mysql.connector.Error as e:
                    if "Duplicate entry" in str(e):
                        print(f"   ⚠️  Declaración {i}: Entrada duplicada (ignorada)")
                    else:
                        print(f"   ❌ Error en declaración {i}: {e}")
        
        conexion.commit()
        cursor.close()
        print(f"✅ {archivo_sql} ejecutado correctamente\n")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando {archivo_sql}: {e}")
        return False

def main():
    print("🚀 === INSERCIÓN COMPLETA DE DATOS ===\n")
    
    # Conectar a la base de datos
    conexion = conectar_db()
    if not conexion:
        sys.exit(1)
    
    # Directorio de scripts
    scripts_dir = Path(__file__).parent
    
    # Lista de scripts a ejecutar en orden
    scripts = [
        'insert_carreras_materias.sql',
        'insert_alumnos_docentes_ejemplo.sql'
    ]
    
    # Ejecutar scripts
    for script in scripts:
        archivo_script = scripts_dir / script
        
        if not archivo_script.exists():
            print(f"❌ Archivo no encontrado: {archivo_script}")
            continue
        
        if not ejecutar_script_sql(conexion, archivo_script):
            print(f"❌ Error ejecutando {script}. Deteniendo...")
            break
    
    # Mostrar resumen final
    try:
        cursor = conexion.cursor()
        
        print("📊 === RESUMEN FINAL ===")
        
        # Contar registros
        consultas = [
            ("Carreras", "SELECT COUNT(*) FROM carreras WHERE activa = TRUE"),
            ("Materias", "SELECT COUNT(*) FROM materias WHERE activa = TRUE"),
            ("Alumnos Base", "SELECT COUNT(*) FROM alumnos_base WHERE activo = TRUE"),
            ("Docentes Base", "SELECT COUNT(*) FROM docentes_base WHERE activo = TRUE"),
            ("Usuarios Registrados", "SELECT COUNT(*) FROM usuarios")
        ]
        
        for nombre, consulta in consultas:
            cursor.execute(consulta)
            resultado = cursor.fetchone()
            print(f"{nombre}: {resultado[0]}")
        
        print("\n📚 Materias por carrera:")
        cursor.execute("""
            SELECT 
                c.nombre as carrera,
                COUNT(m.id) as total_materias
            FROM carreras c
            LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
            WHERE c.activa = TRUE
            GROUP BY c.id, c.nombre
            ORDER BY c.nombre
        """)
        
        for carrera, total in cursor.fetchall():
            print(f"  • {carrera}: {total} materias")
        
        print("\n👥 Alumnos por carrera:")
        cursor.execute("""
            SELECT 
                carrera,
                COUNT(*) as total_alumnos
            FROM alumnos_base 
            WHERE activo = TRUE 
            GROUP BY carrera 
            ORDER BY carrera
        """)
        
        for carrera, total in cursor.fetchall():
            print(f"  • {carrera}: {total} alumnos")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error mostrando resumen: {e}")
    
    # Cerrar conexión
    conexion.close()
    print("\n✅ Inserción completa finalizada!")
    print("\n🎯 Próximos pasos:")
    print("1. Inicia el servidor backend: python backend/app/main.py")
    print("2. Abre el panel de administrador en el navegador")
    print("3. Registra usuarios usando las tarjetas RFID")
    print("4. Asigna materias a los docentes desde el panel admin")

if __name__ == "__main__":
    main()
