#!/usr/bin/env python3
"""
Script seguro para migrar la base de datos paso a paso
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'control_asistencia',
    'user': 'User',
    'password': '12345678'
}

def execute_sql_safe(cursor, sql, description):
    """Ejecuta SQL de forma segura, manejando errores"""
    try:
        print(f"🔧 {description}...")
        cursor.execute(sql)
        print(f"✅ {description} - Completado")
        return True
    except Error as e:
        if "Duplicate column name" in str(e) or "already exists" in str(e):
            print(f"ℹ️  {description} - Ya existe, saltando...")
            return True
        else:
            print(f"❌ {description} - Error: {e}")
            return False

def main():
    print("🚀 Iniciando migración segura de base de datos...")
    
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conexión establecida")
        
        # PASO 1: Agregar columna activo a usuarios
        execute_sql_safe(
            cursor,
            "ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE",
            "Agregando columna 'activo' a usuarios"
        )
        
        execute_sql_safe(
            cursor,
            "UPDATE usuarios SET activo = TRUE WHERE activo IS NULL",
            "Actualizando usuarios existentes"
        )
        
        # PASO 2: Actualizar tabla carreras
        execute_sql_safe(
            cursor,
            "ALTER TABLE carreras ADD COLUMN codigo VARCHAR(20)",
            "Agregando columna 'codigo' a carreras"
        )
        
        execute_sql_safe(
            cursor,
            "ALTER TABLE carreras ADD COLUMN activa BOOLEAN DEFAULT TRUE",
            "Agregando columna 'activa' a carreras"
        )
        
        # Actualizar carreras existentes
        carreras_updates = [
            ("UPDATE carreras SET codigo = 'ISC', activa = TRUE WHERE nombre LIKE '%Sistemas%'", "Actualizando Ingeniería en Sistemas"),
            ("UPDATE carreras SET codigo = 'LOG', activa = TRUE WHERE nombre LIKE '%Logística%'", "Actualizando Logística"),
            ("UPDATE carreras SET codigo = 'TIC', activa = TRUE WHERE nombre LIKE '%Información%'", "Actualizando TIC"),
            ("UPDATE carreras SET codigo = 'MEC', activa = TRUE WHERE nombre LIKE '%Mecatrónica%'", "Actualizando Mecatrónica"),
            ("UPDATE carreras SET codigo = 'CIV', activa = TRUE WHERE nombre LIKE '%Civil%'", "Actualizando Ingeniería Civil")
        ]
        
        for sql, desc in carreras_updates:
            execute_sql_safe(cursor, sql, desc)
        
        # Insertar carreras faltantes
        carreras_insert = [
            ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Ingeniería en Sistemas', 'ISC', TRUE)", "Insertando Ingeniería en Sistemas"),
            ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Logística', 'LOG', TRUE)", "Insertando Logística"),
            ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Tecnologías de la Información', 'TIC', TRUE)", "Insertando TIC"),
            ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Mecatrónica', 'MEC', TRUE)", "Insertando Mecatrónica"),
            ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Ingeniería Civil', 'CIV', TRUE)", "Insertando Ingeniería Civil")
        ]
        
        for sql, desc in carreras_insert:
            execute_sql_safe(cursor, sql, desc)
        
        # PASO 3: Actualizar tabla materias
        execute_sql_safe(
            cursor,
            "ALTER TABLE materias ADD COLUMN codigo VARCHAR(20)",
            "Agregando columna 'codigo' a materias"
        )
        
        execute_sql_safe(
            cursor,
            "ALTER TABLE materias ADD COLUMN creditos INT DEFAULT 3",
            "Agregando columna 'creditos' a materias"
        )
        
        execute_sql_safe(
            cursor,
            "ALTER TABLE materias ADD COLUMN activa BOOLEAN DEFAULT TRUE",
            "Agregando columna 'activa' a materias"
        )
        
        execute_sql_safe(
            cursor,
            "UPDATE materias SET activa = TRUE WHERE activa IS NULL",
            "Actualizando materias existentes"
        )
        
        execute_sql_safe(
            cursor,
            "UPDATE materias SET creditos = 3 WHERE creditos IS NULL",
            "Actualizando créditos de materias"
        )
        
        # PASO 4: Crear nuevas tablas
        nuevas_tablas = [
            ("""CREATE TABLE IF NOT EXISTS docentes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT UNIQUE,
                especialidad VARCHAR(200),
                activo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )""", "Creando tabla docentes"),
            
            ("""CREATE TABLE IF NOT EXISTS docente_carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                docente_id INT,
                carrera_id INT,
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (docente_id) REFERENCES docentes(id),
                FOREIGN KEY (carrera_id) REFERENCES carreras(id)
            )""", "Creando tabla docente_carreras"),
            
            ("""CREATE TABLE IF NOT EXISTS asignaciones_materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                docente_id INT,
                materia_id INT,
                grupo VARCHAR(20) NOT NULL,
                dia_semana VARCHAR(20) NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                aula VARCHAR(50),
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (docente_id) REFERENCES docentes(id),
                FOREIGN KEY (materia_id) REFERENCES materias(id)
            )""", "Creando tabla asignaciones_materias"),
            
            ("""CREATE TABLE IF NOT EXISTS alumnos_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                matricula VARCHAR(100) UNIQUE NOT NULL,
                carrera VARCHAR(100) NOT NULL,
                semestre INT NOT NULL,
                grupo VARCHAR(10) NOT NULL,
                activo BOOLEAN DEFAULT TRUE
            )""", "Creando tabla alumnos_base"),
            
            ("""CREATE TABLE IF NOT EXISTS docentes_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                clave VARCHAR(100) UNIQUE NOT NULL,
                especialidad VARCHAR(200),
                activo BOOLEAN DEFAULT TRUE
            )""", "Creando tabla docentes_base")
        ]
        
        for sql, desc in nuevas_tablas:
            execute_sql_safe(cursor, sql, desc)
        
        # PASO 5: Insertar datos base
        docentes_base = [
            ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Juan Alberto Martinez Zamora', '123', 'Programación y Desarrollo')", "Insertando docente Juan Alberto"),
            ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Pedro Infante N', '456', 'Matemáticas y Estadística')", "Insertando docente Pedro"),
            ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('María González López', '789', 'Base de Datos')", "Insertando docente María"),
            ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Carlos Ruiz Hernández', '101', 'Redes y Seguridad')", "Insertando docente Carlos"),
            ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Ana Patricia Morales', '202', 'Logística y Operaciones')", "Insertando docente Ana")
        ]
        
        for sql, desc in docentes_base:
            execute_sql_safe(cursor, sql, desc)
        
        # PASO 6: Migrar datos de alumnos existentes
        execute_sql_safe(
            cursor,
            """INSERT IGNORE INTO alumnos_base (nombre, matricula, carrera, semestre, grupo)
               SELECT nombre, matricula, carrera, semestre, grupo 
               FROM alumnos""",
            "Migrando alumnos existentes"
        )
        
        # Confirmar cambios
        connection.commit()
        
        # Mostrar resumen
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n📋 Tablas disponibles: {', '.join(tables)}")
        
        cursor.execute("SELECT COUNT(*) FROM carreras")
        carreras_count = cursor.fetchone()[0]
        print(f"🎓 Carreras: {carreras_count}")
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = TRUE")
        usuarios_count = cursor.fetchone()[0]
        print(f"👥 Usuarios activos: {usuarios_count}")
        
        print("\n✅ ¡Migración completada exitosamente!")
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
