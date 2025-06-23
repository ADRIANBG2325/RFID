#!/usr/bin/env python3
"""
Script para crear la estructura completa de la base de datos
Verifica y crea todas las tablas necesarias antes de insertar datos
"""

import mysql.connector
import sys
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',  # Cambiar si tienes contraseña
    'database': 'control_asistencia',  # Nota: sin 's' al final
    'charset': 'utf8mb4'
}

def conectar_mysql():
    """Conectar a MySQL"""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexión a MySQL exitosa")
        return conexion
    except mysql.connector.Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None

def crear_base_datos_si_no_existe():
    """Crear la base de datos si no existe"""
    try:
        config_sin_db = DB_CONFIG.copy()
        del config_sin_db['database']
        
        conexion = mysql.connector.connect(**config_sin_db)
        cursor = conexion.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Base de datos verificada/creada")
        
        cursor.close()
        conexion.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def crear_estructura_tablas(cursor):
    """Crear todas las tablas necesarias"""
    print("\n🏗️  Creando estructura de tablas...")
    
    tablas = {
        'usuarios': """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uid VARCHAR(100) UNIQUE,
                rol VARCHAR(50),
                nombre VARCHAR(100),
                matricula VARCHAR(100) UNIQUE,
                clave_docente VARCHAR(100),
                carrera VARCHAR(100),
                semestre INT,
                grupo VARCHAR(10),
                contraseña_hash VARCHAR(255),
                activo BOOLEAN DEFAULT TRUE,
                INDEX idx_uid (uid),
                INDEX idx_matricula (matricula),
                INDEX idx_clave_docente (clave_docente)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'carreras': """
            CREATE TABLE IF NOT EXISTS carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL,
                codigo VARCHAR(20) UNIQUE NOT NULL,
                activa BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'materias': """
            CREATE TABLE IF NOT EXISTS materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                codigo VARCHAR(20) NOT NULL,
                carrera_id INT,
                semestre INT NOT NULL,
                creditos INT DEFAULT 3,
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
                INDEX idx_carrera_semestre (carrera_id, semestre)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'docentes': """
            CREATE TABLE IF NOT EXISTS docentes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT UNIQUE,
                especialidad VARCHAR(200),
                activo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'docente_carreras': """
            CREATE TABLE IF NOT EXISTS docente_carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                docente_id INT,
                carrera_id INT,
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'asignaciones_materias': """
            CREATE TABLE IF NOT EXISTS asignaciones_materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                docente_id INT,
                materia_id INT,
                grupo VARCHAR(20) NOT NULL,
                dia_semana VARCHAR(20) NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                aula VARCHAR(50),
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
                FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
                INDEX idx_dia_hora (dia_semana, hora_inicio)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'asistencias': """
            CREATE TABLE IF NOT EXISTS asistencias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                alumno_id INT,
                asignacion_id INT,
                fecha DATE NOT NULL,
                hora_registro TIME NOT NULL,
                estado VARCHAR(20) DEFAULT 'Presente',
                observaciones TEXT,
                FOREIGN KEY (alumno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (asignacion_id) REFERENCES asignaciones_materias(id) ON DELETE CASCADE,
                INDEX idx_fecha (fecha),
                INDEX idx_alumno_fecha (alumno_id, fecha)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'alumnos_base': """
            CREATE TABLE IF NOT EXISTS alumnos_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                matricula VARCHAR(100) UNIQUE NOT NULL,
                carrera VARCHAR(100) NOT NULL,
                semestre INT NOT NULL,
                grupo VARCHAR(10) NOT NULL,
                activo BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'docentes_base': """
            CREATE TABLE IF NOT EXISTS docentes_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                clave VARCHAR(100) UNIQUE NOT NULL,
                especialidad VARCHAR(200),
                activo BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    }
    
    try:
        # Desactivar verificación de claves foráneas temporalmente
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        for nombre_tabla, sql in tablas.items():
            print(f"  📋 Creando tabla: {nombre_tabla}")
            cursor.execute(sql)
        
        # Reactivar verificación de claves foráneas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        print("✅ Estructura de tablas creada exitosamente")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def verificar_estructura(cursor):
    """Verificar que todas las tablas y columnas existan"""
    print("\n🔍 Verificando estructura de la base de datos...")
    
    tablas_requeridas = [
        'usuarios', 'carreras', 'materias', 'docentes', 
        'docente_carreras', 'asignaciones_materias', 
        'asistencias', 'alumnos_base', 'docentes_base'
    ]
    
    try:
        cursor.execute("SHOW TABLES")
        tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]
        
        print(f"📊 Tablas encontradas: {len(tablas_existentes)}")
        
        for tabla in tablas_requeridas:
            if tabla in tablas_existentes:
                print(f"  ✅ {tabla}")
                
                # Verificar columnas específicas para materias
                if tabla == 'materias':
                    cursor.execute(f"DESCRIBE {tabla}")
                    columnas = [col[0] for col in cursor.fetchall()]
                    columnas_requeridas = ['id', 'nombre', 'codigo', 'carrera_id', 'semestre', 'creditos', 'activa']
                    
                    for col in columnas_requeridas:
                        if col in columnas:
                            print(f"    ✅ Columna: {col}")
                        else:
                            print(f"    ❌ Columna faltante: {col}")
                            return False
            else:
                print(f"  ❌ {tabla} - FALTANTE")
                return False
        
        print("✅ Estructura verificada correctamente")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def insertar_carreras(cursor):
    """Insertar todas las carreras"""
    print("\n📚 Insertando carreras...")
    
    carreras = [
        ('Ingeniería en Sistemas Computacionales', 'ISC'),
        ('Ingeniería Industrial', 'II'),
        ('Ingeniería Mecatrónica', 'IM'),
        ('Ingeniería Civil', 'IC'),
        ('Licenciatura en Administración', 'LA'),
        ('Ingeniería Química', 'IQ'),
        ('Ingeniería en Logística', 'IL'),
        ('Ingeniería en Tecnologías de la Información y Comunicaciones', 'ITIC')
    ]
    
    query = "INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES (%s, %s, TRUE)"
    
    try:
        cursor.executemany(query, carreras)
        print(f"✅ {len(carreras)} carreras insertadas")
        return True
    except mysql.connector.Error as e:
        print(f"❌ Error insertando carreras: {e}")
        return False

def insertar_materias_isc(cursor):
    """Insertar materias de Ingeniería en Sistemas"""
    print("\n📖 Insertando materias de ISC...")
    
    # Obtener ID de la carrera ISC
    cursor.execute("SELECT id FROM carreras WHERE codigo = 'ISC'")
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ Carrera ISC no encontrada")
        return False
    
    carrera_id = resultado[0]
    
    materias = [
        # 1er Semestre
        ('Cálculo diferencial', 'ISC101', carrera_id, 1, 5),
        ('Fundamentos de programación', 'ISC102', carrera_id, 1, 5),
        ('Desarrollo sustentable', 'ISC103', carrera_id, 1, 4),
        ('Matemáticas discretas', 'ISC104', carrera_id, 1, 5),
        ('Química', 'ISC105', carrera_id, 1, 4),
        ('Taller de ética', 'ISC106', carrera_id, 1, 3),
        
        # 2do Semestre
        ('Cálculo integral', 'ISC201', carrera_id, 2, 5),
        ('Programación orientada a objetos', 'ISC202', carrera_id, 2, 5),
        ('Taller de administración', 'ISC203', carrera_id, 2, 4),
        ('Álgebra lineal', 'ISC204', carrera_id, 2, 5),
        ('Probabilidad y estadística', 'ISC205', carrera_id, 2, 5),
        ('Física general', 'ISC206', carrera_id, 2, 4),
        
        # 3er Semestre
        ('Cálculo vectorial', 'ISC301', carrera_id, 3, 5),
        ('Estructura de datos', 'ISC302', carrera_id, 3, 5),
        ('Fundamentos de telecomunicaciones', 'ISC303', carrera_id, 3, 4),
        ('Investigación de operaciones', 'ISC304', carrera_id, 3, 5),
        ('Sistemas operativos I', 'ISC305', carrera_id, 3, 4),
        ('Principios eléctricos y aplicaciones digitales', 'ISC306', carrera_id, 3, 5),
        
        # 4to Semestre
        ('Ecuaciones diferenciales', 'ISC401', carrera_id, 4, 5),
        ('Métodos numéricos', 'ISC402', carrera_id, 4, 5),
        ('Tópicos avanzados de programación', 'ISC403', carrera_id, 4, 5),
        ('Fundamentos de bases de datos', 'ISC404', carrera_id, 4, 5),
        ('Taller de sistemas operativos', 'ISC405', carrera_id, 4, 4),
        ('Arquitectura de computadoras', 'ISC406', carrera_id, 4, 5),
        
        # 5to Semestre
        ('Lenguajes y autómatas I', 'ISC501', carrera_id, 5, 5),
        ('Redes computacionales', 'ISC502', carrera_id, 5, 5),
        ('Taller de base de datos', 'ISC503', carrera_id, 5, 4),
        ('Simulación', 'ISC504', carrera_id, 5, 5),
        ('Fundamentos de ingeniería de software', 'ISC505', carrera_id, 5, 4),
        ('Lenguaje de interfaz', 'ISC506', carrera_id, 5, 4),
        ('Contabilidad financiera', 'ISC507', carrera_id, 5, 4),
        
        # 6to Semestre
        ('Lenguajes y autómatas II', 'ISC601', carrera_id, 6, 5),
        ('Administración de redes', 'ISC602', carrera_id, 6, 5),
        ('Administración de bases de datos', 'ISC603', carrera_id, 6, 5),
        ('Programación web', 'ISC604', carrera_id, 6, 5),
        ('Ingeniería de software', 'ISC605', carrera_id, 6, 5),
        ('Sistemas programables', 'ISC606', carrera_id, 6, 5),
        
        # 7mo Semestre
        ('Programación lógica y funcional', 'ISC701', carrera_id, 7, 4),
        ('Comunicación y enrutamiento de redes de datos', 'ISC702', carrera_id, 7, 5),
        ('Taller de investigación I', 'ISC703', carrera_id, 7, 4),
        ('Desarrollo de aplicaciones para dispositivos móviles', 'ISC704', carrera_id, 7, 5),
        ('Gestión de proyectos de software', 'ISC705', carrera_id, 7, 4),
        ('Internet de las cosas', 'ISC706', carrera_id, 7, 4),
        ('Graficación', 'ISC707', carrera_id, 7, 4),
        
        # 8vo Semestre
        ('Inteligencia artificial', 'ISC801', carrera_id, 8, 5),
        ('Ciberseguridad', 'ISC802', carrera_id, 8, 5),
        ('Taller de investigación II', 'ISC803', carrera_id, 8, 4),
        ('Programación reactiva', 'ISC804', carrera_id, 8, 4),
        ('Sistemas distribuidos', 'ISC805', carrera_id, 8, 5),
        ('Cultura empresarial', 'ISC806', carrera_id, 8, 3),
        
        # 9no Semestre
        ('Residencias profesionales', 'ISC901', carrera_id, 9, 10)
    ]
    
    query = "INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES (%s, %s, %s, %s, %s, TRUE)"
    
    try:
        cursor.executemany(query, materias)
        print(f"✅ {len(materias)} materias de ISC insertadas")
        return True
    except mysql.connector.Error as e:
        print(f"❌ Error insertando materias de ISC: {e}")
        return False

def mostrar_resumen(cursor):
    """Mostrar resumen de la base de datos"""
    print("\n" + "="*50)
    print("📊 RESUMEN DE LA BASE DE DATOS")
    print("="*50)
    
    try:
        cursor.execute("SELECT COUNT(*) FROM carreras")
        total_carreras = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM materias")
        total_materias = cursor.fetchone()[0]
        
        print(f"🎓 Total de carreras: {total_carreras}")
        print(f"📚 Total de materias: {total_materias}")
        
        # Detalle por carrera
        cursor.execute("""
            SELECT 
                c.codigo,
                c.nombre,
                COUNT(m.id) as total_materias
            FROM carreras c
            LEFT JOIN materias m ON c.id = m.carrera_id
            GROUP BY c.id, c.codigo, c.nombre
            ORDER BY c.codigo
        """)
        
        print("\n📋 DETALLE POR CARRERA:")
        for codigo, nombre, total in cursor.fetchall():
            print(f"• {codigo}: {total} materias")
        
    except mysql.connector.Error as e:
        print(f"❌ Error mostrando resumen: {e}")

def main():
    """Función principal"""
    print("🚀" + "="*60)
    print("    CREACIÓN DE ESTRUCTURA COMPLETA DE BASE DE DATOS")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Base de datos: {DB_CONFIG['database']}")
    
    # Crear base de datos si no existe
    if not crear_base_datos_si_no_existe():
        sys.exit(1)
    
    # Conectar a MySQL
    conexion = conectar_mysql()
    if not conexion:
        sys.exit(1)
    
    cursor = conexion.cursor()
    
    try:
        # 1. Crear estructura de tablas
        if not crear_estructura_tablas(cursor):
            print("❌ Error creando estructura. Abortando...")
            return
        
        # 2. Verificar estructura
        if not verificar_estructura(cursor):
            print("❌ Estructura incompleta. Abortando...")
            return
        
        # 3. Insertar carreras
        if not insertar_carreras(cursor):
            print("❌ Error insertando carreras. Abortando...")
            return
        
        # 4. Insertar materias de ISC
        if not insertar_materias_isc(cursor):
            print("❌ Error insertando materias. Abortando...")
            return
        
        # 5. Confirmar cambios
        conexion.commit()
        print("\n✅ ESTRUCTURA Y DATOS CREADOS EXITOSAMENTE")
        
        # 6. Mostrar resumen
        mostrar_resumen(cursor)
        
        print("\n🎉 ¡Base de datos lista!")
        print("\n📝 Ahora puedes ejecutar el script completo de inserción de materias")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        conexion.rollback()
    
    finally:
        cursor.close()
        conexion.close()
        print("\n🔒 Conexión cerrada")

if __name__ == "__main__":
    main()
