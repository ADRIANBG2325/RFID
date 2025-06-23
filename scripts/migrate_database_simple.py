#!/usr/bin/env python3
"""
Script simple para migrar usando pymysql (más compatible)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    print("❌ Error: pymysql no está instalado")
    print("🔧 Ejecuta: pip3 install pymysql")
    sys.exit(1)

def execute_sql_commands():
    """Ejecuta comandos SQL uno por uno"""
    
    # Configuración de conexión
    config = {
        'host': 'localhost',
        'user': 'User',
        'password': '12345678',
        'database': 'control_asistencia',
        'charset': 'utf8mb4'
    }
    
    # Comandos SQL a ejecutar
    commands = [
        # Paso 1: Agregar columnas a usuarios
        ("ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE", "Agregando columna activo a usuarios"),
        ("UPDATE usuarios SET activo = TRUE WHERE activo IS NULL", "Actualizando usuarios existentes"),
        
        # Paso 2: Agregar columnas a carreras
        ("ALTER TABLE carreras ADD COLUMN codigo VARCHAR(20)", "Agregando columna codigo a carreras"),
        ("ALTER TABLE carreras ADD COLUMN activa BOOLEAN DEFAULT TRUE", "Agregando columna activa a carreras"),
        
        # Paso 3: Actualizar carreras existentes
        ("UPDATE carreras SET codigo = 'ISC', activa = TRUE WHERE nombre LIKE '%Sistemas%'", "Actualizando Ingeniería en Sistemas"),
        ("UPDATE carreras SET codigo = 'LOG', activa = TRUE WHERE nombre LIKE '%Logística%'", "Actualizando Logística"),
        ("UPDATE carreras SET codigo = 'TIC', activa = TRUE WHERE nombre LIKE '%Información%'", "Actualizando TIC"),
        ("UPDATE carreras SET codigo = 'MEC', activa = TRUE WHERE nombre LIKE '%Mecatrónica%'", "Actualizando Mecatrónica"),
        ("UPDATE carreras SET codigo = 'CIV', activa = TRUE WHERE nombre LIKE '%Civil%'", "Actualizando Ingeniería Civil"),
        
        # Paso 4: Insertar carreras faltantes
        ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Ingeniería en Sistemas', 'ISC', TRUE)", "Insertando Ingeniería en Sistemas"),
        ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Logística', 'LOG', TRUE)", "Insertando Logística"),
        ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Tecnologías de la Información', 'TIC', TRUE)", "Insertando TIC"),
        ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Mecatrónica', 'MEC', TRUE)", "Insertando Mecatrónica"),
        ("INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES ('Ingeniería Civil', 'CIV', TRUE)", "Insertando Ingeniería Civil"),
        
        # Paso 5: Actualizar materias
        ("ALTER TABLE materias ADD COLUMN codigo VARCHAR(20)", "Agregando columna codigo a materias"),
        ("ALTER TABLE materias ADD COLUMN creditos INT DEFAULT 3", "Agregando columna creditos a materias"),
        ("ALTER TABLE materias ADD COLUMN activa BOOLEAN DEFAULT TRUE", "Agregando columna activa a materias"),
        ("UPDATE materias SET activa = TRUE WHERE activa IS NULL", "Actualizando materias existentes"),
        ("UPDATE materias SET creditos = 3 WHERE creditos IS NULL", "Actualizando créditos de materias"),
    ]
    
    # Tablas nuevas
    new_tables = [
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
        
        ("""CREATE TABLE IF NOT EXISTS docentes_base (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            clave VARCHAR(100) UNIQUE NOT NULL,
            especialidad VARCHAR(200),
            activo BOOLEAN DEFAULT TRUE
        )""", "Creando tabla docentes_base"),
    ]
    
    # Datos base
    base_data = [
        ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Juan Alberto Martinez Zamora', '123', 'Programación y Desarrollo')", "Insertando docente Juan Alberto"),
        ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Pedro Infante N', '456', 'Matemáticas y Estadística')", "Insertando docente Pedro"),
        ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('María González López', '789', 'Base de Datos')", "Insertando docente María"),
        ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Carlos Ruiz Hernández', '101', 'Redes y Seguridad')", "Insertando docente Carlos"),
        ("INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES ('Ana Patricia Morales', '202', 'Logística y Operaciones')", "Insertando docente Ana"),
    ]
    
    try:
        print("🚀 Iniciando migración de base de datos...")
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Conexión establecida")
        
        # Ejecutar comandos básicos
        for sql, desc in commands:
            try:
                print(f"🔧 {desc}...")
                cursor.execute(sql)
                print(f"✅ {desc} - Completado")
            except Exception as e:
                if "Duplicate column name" in str(e) or "already exists" in str(e):
                    print(f"ℹ️  {desc} - Ya existe, saltando...")
                else:
                    print(f"⚠️  {desc} - Error: {e}")
        
        # Crear tablas nuevas
        for sql, desc in new_tables:
            try:
                print(f"🔧 {desc}...")
                cursor.execute(sql)
                print(f"✅ {desc} - Completado")
            except Exception as e:
                print(f"⚠️  {desc} - Error: {e}")
        
        # Insertar datos base
        for sql, desc in base_data:
            try:
                print(f"🔧 {desc}...")
                cursor.execute(sql)
                print(f"✅ {desc} - Completado")
            except Exception as e:
                print(f"ℹ️  {desc} - Ya existe o error: {e}")
        
        # Confirmar cambios
        connection.commit()
        
        # Mostrar resumen
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n📋 Tablas disponibles: {', '.join(tables)}")
        
        cursor.execute("SELECT COUNT(*) FROM carreras")
        carreras_count = cursor.fetchone()[0]
        print(f"🎓 Carreras: {carreras_count}")
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]
        print(f"👥 Usuarios: {usuarios_count}")
        
        print("\n✅ ¡Migración completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    finally:
        if 'connection' in locals():
            connection.close()
            print("🔌 Conexión cerrada")
    
    return True

if __name__ == "__main__":
    success = execute_sql_commands()
    sys.exit(0 if success else 1)
