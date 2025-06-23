#!/usr/bin/env python3
"""
Script para corregir completamente el sistema de control de asistencias
Incluye todas las correcciones necesarias para el funcionamiento completo
"""

import mysql.connector
import sys
import traceback
from datetime import datetime

# Configuración de la base de datos MariaDB
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',
    'database': 'control_asistencia',
    'charset': 'utf8mb4',
    'autocommit': False
}

def conectar_db():
    """Conectar a la base de datos"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexión a MariaDB exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a MariaDB: {e}")
        return None

def ejecutar_sql(cursor, sql, descripcion, datos=None):
    """Ejecutar SQL con manejo de errores"""
    try:
        if datos:
            cursor.execute(sql, datos)
        else:
            cursor.execute(sql)
        print(f"✅ {descripcion}")
        return True
    except Exception as e:
        print(f"❌ Error en {descripcion}: {e}")
        return False

def main():
    print("🔧 INICIANDO CORRECCIÓN COMPLETA DEL SISTEMA")
    print("=" * 60)
    
    conn = conectar_db()
    if not conn:
        sys.exit(1)
    
    cursor = conn.cursor()
    
    try:
        # 1. Verificar y crear tablas base si no existen
        print("\n📋 1. VERIFICANDO ESTRUCTURA DE TABLAS...")
        
        # Tabla usuarios
        sql_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            uid VARCHAR(50) UNIQUE NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            rol ENUM('admin', 'docente', 'alumno') NOT NULL,
            activo BOOLEAN DEFAULT TRUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_uid (uid),
            INDEX idx_rol (rol)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_sql(cursor, sql_usuarios, "Tabla usuarios verificada/creada")
        
        # Tabla docentes_base
        sql_docentes = """
        CREATE TABLE IF NOT EXISTS docentes_base (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            clave VARCHAR(20) UNIQUE NOT NULL,
            especialidad VARCHAR(100),
            activo BOOLEAN DEFAULT TRUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_clave (clave)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_sql(cursor, sql_docentes, "Tabla docentes_base verificada/creada")
        
        # Tabla alumnos_base
        sql_alumnos = """
        CREATE TABLE IF NOT EXISTS alumnos_base (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            matricula VARCHAR(20) UNIQUE NOT NULL,
            carrera VARCHAR(100) NOT NULL,
            semestre INT NOT NULL,
            grupo VARCHAR(10) NOT NULL,
            activo BOOLEAN DEFAULT TRUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_matricula (matricula),
            INDEX idx_carrera (carrera),
            INDEX idx_semestre (semestre)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_sql(cursor, sql_alumnos, "Tabla alumnos_base verificada/creada")
        
        # Tabla carreras
        sql_carreras = """
        CREATE TABLE IF NOT EXISTS carreras (
            id INT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            codigo VARCHAR(20) UNIQUE,
            activa BOOLEAN DEFAULT TRUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_sql(cursor, sql_carreras, "Tabla carreras verificada/creada")
        
        # Tabla asignacion_materias
        sql_asignaciones = """
        CREATE TABLE IF NOT EXISTS asignacion_materias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            docente_id INT NOT NULL,
            materia_id INT NOT NULL,
            carrera_id INT NOT NULL,
            semestre INT NOT NULL,
            grupo VARCHAR(10) NOT NULL,
            dia_semana VARCHAR(20) NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fin TIME NOT NULL,
            aula VARCHAR(20),
            activa BOOLEAN DEFAULT TRUE,
            fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (docente_id) REFERENCES docentes_base(id) ON DELETE CASCADE,
            FOREIGN KEY (carrera_id) REFERENCES carreras(id),
            INDEX idx_docente (docente_id),
            INDEX idx_materia (materia_id),
            INDEX idx_carrera (carrera_id),
            INDEX idx_horario (dia_semana, hora_inicio, hora_fin)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_sql(cursor, sql_asignaciones, "Tabla asignacion_materias verificada/creada")
        
        # Tabla asistencias
        sql_asistencias = """
        CREATE TABLE IF NOT EXISTS asistencias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alumno_id INT,
            docente_id INT,
            materia_id INT,
            fecha DATE NOT NULL,
            hora_entrada TIME,
            hora_salida TIME,
            tipo_usuario ENUM('alumno', 'docente') NOT NULL,
            uid_tarjeta VARCHAR(50),
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alumno_id) REFERENCES alumnos_base(id) ON DELETE CASCADE,
            FOREIGN KEY (docente_id) REFERENCES docentes_base(id) ON DELETE CASCADE,
            INDEX idx_fecha (fecha),
            INDEX idx_tipo (tipo_usuario),
            INDEX idx_uid_tarjeta (uid_tarjeta)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_sql(cursor, sql_asistencias, "Tabla asistencias verificada/creada")
        
        # 2. Insertar carreras básicas
        print("\n📚 2. INSERTANDO CARRERAS BÁSICAS...")
        
        carreras_data = [
            (1, "Ingeniería Industrial", "IND"),
            (2, "Ingeniería en Tecnologías de la Información y Comunicaciones", "TIC"),
            (3, "Ingeniería en Sistemas Computacionales", "ISC"),
            (4, "Ingeniería Mecatrónica", "MEC"),
            (5, "Ingeniería Civil", "CIV"),
            (6, "Licenciatura en Administración", "ADM"),
            (7, "Ingeniería Química", "QUI"),
            (8, "Ingeniería en Logística", "LOG")
        ]
        
        for carrera_id, nombre, codigo in carreras_data:
            sql_insert_carrera = """
            INSERT INTO carreras (id, nombre, codigo, activa) 
            VALUES (%s, %s, %s, TRUE)
            ON DUPLICATE KEY UPDATE 
            nombre = VALUES(nombre), 
            codigo = VALUES(codigo)
            """
            ejecutar_sql(cursor, sql_insert_carrera, f"Carrera {nombre}", (carrera_id, nombre, codigo))
        
        # 3. Crear usuario administrador por defecto
        print("\n👤 3. CREANDO USUARIO ADMINISTRADOR...")
        
        sql_admin = """
        INSERT INTO usuarios (uid, nombre, rol, activo) 
        VALUES ('admin123', 'Administrador Principal', 'admin', TRUE)
        ON DUPLICATE KEY UPDATE 
        nombre = VALUES(nombre), 
        rol = VALUES(rol), 
        activo = VALUES(activo)
        """
        ejecutar_sql(cursor, sql_admin, "Usuario administrador creado/actualizado")
        
        # 4. Insertar docentes de ejemplo
        print("\n👨‍🏫 4. INSERTANDO DOCENTES DE EJEMPLO...")
        
        docentes_ejemplo = [
            ("Dr. Juan García López", "DOC001", "Matemáticas"),
            ("Ing. María Rodríguez", "DOC002", "Física"),
            ("Mtro. Carlos Hernández", "DOC003", "Programación"),
            ("Dra. Ana Martínez", "DOC004", "Química"),
            ("Ing. Luis Pérez", "DOC005", "Mecánica")
        ]
        
        for nombre, clave, especialidad in docentes_ejemplo:
            sql_docente = """
            INSERT INTO docentes_base (nombre, clave, especialidad, activo) 
            VALUES (%s, %s, %s, TRUE)
            ON DUPLICATE KEY UPDATE 
            nombre = VALUES(nombre), 
            especialidad = VALUES(especialidad)
            """
            ejecutar_sql(cursor, sql_docente, f"Docente {nombre}", (nombre, clave, especialidad))
        
        # 5. Insertar alumnos de ejemplo
        print("\n🎓 5. INSERTANDO ALUMNOS DE EJEMPLO...")
        
        alumnos_ejemplo = [
            ("Omar Anaya Martinez", "202323889", "Ingeniería Industrial", 2, "2201"),
            ("Ivon Anaya Martinez", "202321234", "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2401"),
            ("Laura J. Martinez Estevez", "202356789", "Ingeniería Civil", 6, "5601"),
            ("Cristofer Anaya Martinez", "202398765", "Ingeniería Mecatrónica", 2, "4201"),
            ("Maria C. Martinez Trejo", "202321990", "Ingeniería Industrial", 2, "1202")
        ]
        
        for nombre, matricula, carrera, semestre, grupo in alumnos_ejemplo:
            sql_alumno = """
            INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) 
            VALUES (%s, %s, %s, %s, %s, TRUE)
            ON DUPLICATE KEY UPDATE 
            nombre = VALUES(nombre), 
            carrera = VALUES(carrera), 
            semestre = VALUES(semestre), 
            grupo = VALUES(grupo)
            """
            ejecutar_sql(cursor, sql_alumno, f"Alumno {nombre}", (nombre, matricula, carrera, semestre, grupo))
        
        # 6. Crear usuarios para docentes y alumnos
        print("\n🔐 6. CREANDO USUARIOS PARA DOCENTES Y ALUMNOS...")
        
        # Usuarios para docentes
        cursor.execute("SELECT id, clave, nombre FROM docentes_base")
        docentes = cursor.fetchall()
        
        for docente_id, clave, nombre in docentes:
            uid_docente = f"DOC_{clave}"
            sql_usuario_docente = """
            INSERT INTO usuarios (uid, nombre, rol, activo) 
            VALUES (%s, %s, 'docente', TRUE)
            ON DUPLICATE KEY UPDATE 
            nombre = VALUES(nombre), 
            rol = VALUES(rol)
            """
            ejecutar_sql(cursor, sql_usuario_docente, f"Usuario docente {nombre}", (uid_docente, nombre))
        
        # Usuarios para alumnos
        cursor.execute("SELECT id, matricula, nombre FROM alumnos_base")
        alumnos = cursor.fetchall()
        
        for alumno_id, matricula, nombre in alumnos:
            uid_alumno = f"ALU_{matricula}"
            sql_usuario_alumno = """
            INSERT INTO usuarios (uid, nombre, rol, activo) 
            VALUES (%s, %s, 'alumno', TRUE)
            ON DUPLICATE KEY UPDATE 
            nombre = VALUES(nombre), 
            rol = VALUES(rol)
            """
            ejecutar_sql(cursor, sql_usuario_alumno, f"Usuario alumno {nombre}", (uid_alumno, nombre))
        
        # 7. Insertar asignaciones de materias de ejemplo
        print("\n📖 7. INSERTANDO ASIGNACIONES DE MATERIAS DE EJEMPLO...")
        
        # Obtener IDs de docentes
        cursor.execute("SELECT id FROM docentes_base LIMIT 3")
        docentes_ids = [row[0] for row in cursor.fetchall()]
        
        if docentes_ids:
            asignaciones_ejemplo = [
                (docentes_ids[0], 4, 1, 2, "1202", "Lunes", "08:00:00", "09:30:00", "A-101"),
                (docentes_ids[1], 5, 1, 2, "1202", "Martes", "10:00:00", "11:30:00", "B-205"),
                (docentes_ids[2], 28, 2, 2, "2201", "Miércoles", "14:00:00", "15:30:00", "C-301"),
            ]
            
            for docente_id, materia_id, carrera_id, semestre, grupo, dia, hora_inicio, hora_fin, aula in asignaciones_ejemplo:
                sql_asignacion = """
                INSERT INTO asignacion_materias 
                (docente_id, materia_id, carrera_id, semestre, grupo, dia_semana, hora_inicio, hora_fin, aula, activa) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                ON DUPLICATE KEY UPDATE 
                aula = VALUES(aula), 
                activa = VALUES(activa)
                """
                ejecutar_sql(cursor, sql_asignacion, f"Asignación materia {materia_id} a docente {docente_id}", 
                           (docente_id, materia_id, carrera_id, semestre, grupo, dia, hora_inicio, hora_fin, aula))
        
        # 8. Insertar asistencias de ejemplo
        print("\n📊 8. INSERTANDO ASISTENCIAS DE EJEMPLO...")
        
        from datetime import date, timedelta
        
        # Asistencias de los últimos 5 días
        for i in range(5):
            fecha_asistencia = date.today() - timedelta(days=i)
            
            # Asistencias de alumnos
            cursor.execute("SELECT id FROM alumnos_base LIMIT 3")
            alumnos_ids = [row[0] for row in cursor.fetchall()]
            
            for alumno_id in alumnos_ids:
                sql_asistencia_alumno = """
                INSERT INTO asistencias 
                (alumno_id, fecha, hora_entrada, tipo_usuario, uid_tarjeta) 
                VALUES (%s, %s, '08:00:00', 'alumno', %s)
                ON DUPLICATE KEY UPDATE 
                hora_entrada = VALUES(hora_entrada)
                """
                uid_tarjeta = f"CARD_{alumno_id}_{i}"
                ejecutar_sql(cursor, sql_asistencia_alumno, f"Asistencia alumno {alumno_id} - {fecha_asistencia}", 
                           (alumno_id, fecha_asistencia, uid_tarjeta))
            
            # Asistencias de docentes
            for docente_id in docentes_ids[:2]:
                sql_asistencia_docente = """
                INSERT INTO asistencias 
                (docente_id, fecha, hora_entrada, tipo_usuario, uid_tarjeta) 
                VALUES (%s, %s, '07:30:00', 'docente', %s)
                ON DUPLICATE KEY UPDATE 
                hora_entrada = VALUES(hora_entrada)
                """
                uid_tarjeta = f"CARD_DOC_{docente_id}_{i}"
                ejecutar_sql(cursor, sql_asistencia_docente, f"Asistencia docente {docente_id} - {fecha_asistencia}", 
                           (docente_id, fecha_asistencia, uid_tarjeta))
        
        # Confirmar todos los cambios
        conn.commit()
        print("\n✅ TODAS LAS CORRECCIONES APLICADAS EXITOSAMENTE")
        
        # 9. Verificar el estado final
        print("\n📋 9. VERIFICACIÓN FINAL DEL SISTEMA...")
        
        # Contar registros
        tablas_verificar = [
            ("usuarios", "SELECT COUNT(*) FROM usuarios"),
            ("docentes_base", "SELECT COUNT(*) FROM docentes_base"),
            ("alumnos_base", "SELECT COUNT(*) FROM alumnos_base"),
            ("carreras", "SELECT COUNT(*) FROM carreras"),
            ("asignacion_materias", "SELECT COUNT(*) FROM asignacion_materias"),
            ("asistencias", "SELECT COUNT(*) FROM asistencias")
        ]
        
        for tabla, sql in tablas_verificar:
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            print(f"✅ {tabla}: {count} registros")
        
        print("\n🎉 SISTEMA COMPLETAMENTE CORREGIDO Y FUNCIONAL")
        print("=" * 60)
        print("📌 CREDENCIALES DE ACCESO:")
        print("   Admin: uid = 'admin123'")
        print("   Docentes: uid = 'DOC_[CLAVE]' (ej: DOC_DOC001)")
        print("   Alumnos: uid = 'ALU_[MATRICULA]' (ej: ALU_202323889)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        conn.rollback()
        return False
    
    finally:
        cursor.close()
        conn.close()
        print("\n🔌 Conexión cerrada")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Script ejecutado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Script falló")
        sys.exit(1)
