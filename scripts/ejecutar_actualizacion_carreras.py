#!/usr/bin/env python3
"""
Script para actualizar las carreras y materias correctas
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
                    print(f"  ⚠️ Warning en comando {i}: {e}")
                    continue
        
        return True
    except Exception as e:
        print(f"❌ Error ejecutando archivo {archivo_sql}: {e}")
        return False

def verificar_carreras(cursor):
    """Verificar que las carreras se insertaron correctamente"""
    try:
        cursor.execute("""
            SELECT id, nombre, codigo 
            FROM carreras 
            WHERE activa = TRUE 
            ORDER BY id
        """)
        
        carreras = cursor.fetchall()
        
        print(f"\n📋 Carreras registradas ({len(carreras)}):")
        for carrera in carreras:
            print(f"  {carrera[0]}. {carrera[1]} ({carrera[2]})")
        
        return len(carreras) > 0
    except Error as e:
        print(f"❌ Error verificando carreras: {e}")
        return False

def verificar_materias(cursor):
    """Verificar materias por carrera"""
    try:
        cursor.execute("""
            SELECT c.id, c.nombre, COUNT(m.id) as total_materias
            FROM carreras c
            LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
            WHERE c.activa = TRUE
            GROUP BY c.id, c.nombre
            ORDER BY c.id
        """)
        
        resultados = cursor.fetchall()
        
        print(f"\n📚 Materias por carrera:")
        total_materias = 0
        for resultado in resultados:
            print(f"  {resultado[0]}. {resultado[1]}: {resultado[2]} materias")
            total_materias += resultado[2]
        
        print(f"\n📊 Total de materias: {total_materias}")
        return total_materias > 0
    except Error as e:
        print(f"❌ Error verificando materias: {e}")
        return False

def insertar_alumnos_ejemplo(cursor):
    """Insertar algunos alumnos de ejemplo con códigos correctos"""
    try:
        print(f"\n👨‍🎓 Insertando alumnos de ejemplo...")
        
        alumnos_ejemplo = [
            # Carrera 2 (TICs) - Diferentes semestres y grupos
            ("Juan Carlos Pérez López", "20240001", "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301"),
            ("María Elena García Rodríguez", "20240002", "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2302"),
            ("Luis Fernando Martínez Sánchez", "20240003", "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2401"),
            ("Ana Sofía Hernández Torres", "20240004", "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2402"),
            
            # Carrera 3 (ISC)
            ("Carlos Eduardo López Morales", "20240005", "Ingeniería en Sistemas Computacionales", 5, "3501"),
            ("Diana Patricia Ruiz Jiménez", "20240006", "Ingeniería en Sistemas Computacionales", 5, "3502"),
            
            # Carrera 1 (Industrial)
            ("Roberto Miguel Flores Castro", "20240007", "Ingeniería Industrial", 2, "1201"),
            ("Alejandra Beatriz Mendoza Vargas", "20240008", "Ingeniería Industrial", 2, "1202"),
            
            # Carrera 4 (Mecatrónica)
            ("Fernando Javier Ramírez Ortega", "20240009", "Ingeniería Mecatrónica", 6, "4601"),
            ("Gabriela Monserrat Silva Delgado", "20240010", "Ingeniería Mecatrónica", 6, "4602"),
        ]
        
        # Limpiar tabla existente
        cursor.execute("DELETE FROM alumnos_base WHERE id > 0")
        
        for alumno in alumnos_ejemplo:
            cursor.execute("""
                INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo)
                VALUES (%s, %s, %s, %s, %s, TRUE)
            """, alumno)
            print(f"  ✅ Alumno insertado: {alumno[0]} - Grupo {alumno[4]}")
        
        print(f"✅ {len(alumnos_ejemplo)} alumnos de ejemplo insertados")
        return True
    except Error as e:
        print(f"❌ Error insertando alumnos: {e}")
        return False

def insertar_docentes_ejemplo(cursor):
    """Insertar algunos docentes de ejemplo"""
    try:
        print(f"\n👨‍🏫 Insertando docentes de ejemplo...")
        
        docentes_ejemplo = [
            ("Dr. Miguel Ángel Rodríguez Pérez", "DOC001", "Ingeniería de Software"),
            ("Mtra. Laura Patricia González Martínez", "DOC002", "Bases de Datos"),
            ("Ing. José Luis Hernández Sánchez", "DOC003", "Redes y Comunicaciones"),
            ("Dra. Carmen Elena López Torres", "DOC004", "Inteligencia Artificial"),
            ("Mtro. Ricardo Javier Morales Castro", "DOC005", "Programación"),
            ("Ing. Ana María Jiménez Ruiz", "DOC006", "Matemáticas Aplicadas"),
            ("Dr. Fernando Gabriel Silva Mendoza", "DOC007", "Ciberseguridad"),
            ("Mtra. Claudia Alejandra Vargas Flores", "DOC008", "Administración de Proyectos"),
        ]
        
        # Limpiar tabla existente
        cursor.execute("DELETE FROM docentes_base WHERE id > 0")
        
        for docente in docentes_ejemplo:
            cursor.execute("""
                INSERT INTO docentes_base (nombre, clave, especialidad, activo)
                VALUES (%s, %s, %s, TRUE)
            """, docente)
            print(f"  ✅ Docente insertado: {docente[0]} - {docente[1]}")
        
        print(f"✅ {len(docentes_ejemplo)} docentes de ejemplo insertados")
        return True
    except Error as e:
        print(f"❌ Error insertando docentes: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 === ACTUALIZACIÓN DE CARRERAS Y MATERIAS ===\n")
    
    connection = None
    try:
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conexión establecida")
        
        # Ejecutar script de actualización de carreras
        archivo_sql = "scripts/actualizar_carreras_correctas.sql"
        if not os.path.exists(archivo_sql):
            print(f"❌ Archivo no encontrado: {archivo_sql}")
            return False
        
        if not ejecutar_sql_desde_archivo(cursor, archivo_sql):
            print("❌ Error ejecutando script de carreras")
            return False
        
        # Confirmar cambios
        connection.commit()
        print("✅ Cambios de carreras y materias confirmados")
        
        # Verificar carreras
        if not verificar_carreras(cursor):
            print("❌ Error verificando carreras")
            return False
        
        # Verificar materias
        if not verificar_materias(cursor):
            print("❌ Error verificando materias")
            return False
        
        # Insertar datos de ejemplo
        if not insertar_alumnos_ejemplo(cursor):
            print("❌ Error insertando alumnos de ejemplo")
            return False
        
        if not insertar_docentes_ejemplo(cursor):
            print("❌ Error insertando docentes de ejemplo")
            return False
        
        # Confirmar todos los cambios
        connection.commit()
        print("\n✅ === ACTUALIZACIÓN COMPLETADA EXITOSAMENTE ===")
        
        print(f"\n📋 Resumen:")
        print(f"  ✅ Carreras actualizadas con IDs correctos")
        print(f"  ✅ Materias de TICs corregidas")
        print(f"  ✅ Alumnos de ejemplo con códigos de grupo correctos")
        print(f"  ✅ Docentes de ejemplo insertados")
        
        print(f"\n🔢 Códigos de grupo:")
        print(f"  Formato: XYZW")
        print(f"  X = Carrera (1-8)")
        print(f"  Y = Semestre (1-9)")
        print(f"  Z = Siempre 0")
        print(f"  W = Grupo (1-4)")
        print(f"  Ejemplo: 2301 = TICs, 3er semestre, grupo 1")
        
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
