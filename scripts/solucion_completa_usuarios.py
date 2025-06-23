#!/usr/bin/env python3
"""
Solución completa para problemas de usuarios y tarjetas RFID
"""

import sys
import mysql.connector
from mysql.connector import Error
import bcrypt
import requests
import time

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'control_asistencia',
    'user': 'User',
    'password': '12345678'
}

def limpiar_y_recrear_bd():
    """Limpiar y recrear la base de datos completamente"""
    try:
        print("🗑️ Limpiando base de datos...")
        
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        # Eliminar y recrear base de datos
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        print(f"✅ Base de datos {DB_CONFIG['database']} recreada")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error recreando BD: {e}")
        return False

def crear_estructura_completa():
    """Crear estructura completa de tablas"""
    try:
        print("📋 Creando estructura de tablas...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Tabla usuarios (principal)
        cursor.execute("""
            CREATE TABLE usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uid VARCHAR(100) UNIQUE NOT NULL,
                rol ENUM('alumno', 'docente', 'admin') NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                matricula VARCHAR(100) NULL,
                clave_docente VARCHAR(100) NULL,
                carrera VARCHAR(100) NULL,
                semestre INT NULL,
                grupo VARCHAR(10) NULL,
                contraseña_hash VARCHAR(255) NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_uid (uid),
                INDEX idx_rol (rol),
                INDEX idx_matricula (matricula),
                INDEX idx_clave_docente (clave_docente)
            )
        """)
        
        # Tabla carreras
        cursor.execute("""
            CREATE TABLE carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL,
                codigo VARCHAR(20) UNIQUE NOT NULL,
                activa BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Tabla materias
        cursor.execute("""
            CREATE TABLE materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                codigo VARCHAR(20) NOT NULL,
                carrera_id INT NOT NULL,
                semestre INT NOT NULL,
                creditos INT DEFAULT 3,
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id),
                UNIQUE KEY unique_materia (nombre, carrera_id, semestre)
            )
        """)
        
        # Tabla alumnos_base
        cursor.execute("""
            CREATE TABLE alumnos_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                matricula VARCHAR(100) UNIQUE NOT NULL,
                carrera VARCHAR(100) NOT NULL,
                semestre INT NOT NULL,
                grupo VARCHAR(10) NOT NULL,
                activo BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Tabla docentes_base
        cursor.execute("""
            CREATE TABLE docentes_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                clave VARCHAR(100) UNIQUE NOT NULL,
                especialidad VARCHAR(200) NULL,
                activo BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Tabla docentes (relación con usuarios)
        cursor.execute("""
            CREATE TABLE docentes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT UNIQUE NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        print("✅ Estructura de tablas creada")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando estructura: {e}")
        return False

def insertar_datos_base():
    """Insertar datos base (carreras, alumnos, docentes)"""
    try:
        print("📊 Insertando datos base...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Insertar carreras
        carreras = [
            (1, "Ingeniería Industrial", "IND"),
            (2, "Ingeniería en Tecnologías de la Información y Comunicaciones", "TIC"),
            (3, "Ingeniería en Sistemas Computacionales", "ISC"),
            (4, "Ingeniería Mecatrónica", "MEC"),
            (5, "Ingeniería Civil", "CIV"),
            (6, "Licenciatura en Administración", "ADM"),
            (7, "Ingeniería Química", "QUI"),
            (8, "Ingeniería en Logística", "LOG")
        ]
        
        for carrera_id, nombre, codigo in carreras:
            cursor.execute("""
                INSERT INTO carreras (id, nombre, codigo, activa)
                VALUES (%s, %s, %s, %s)
            """, (carrera_id, nombre, codigo, True))
        
        print("✅ Carreras insertadas")
        
        # Insertar alumnos base
        alumnos = [
            ("Juan Carlos Pérez López", "20230001", "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301"),
            ("María Elena González Martínez", "20230002", "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301"),
            ("Roberto Miguel Jiménez Cruz", "20220001", "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2402"),
            ("Ana Patricia López Hernández", "20230003", "Ingeniería Industrial", 2, "1201"),
            ("Carlos Eduardo Martínez Sánchez", "20230004", "Ingeniería en Sistemas Computacionales", 5, "3501")
        ]
        
        for nombre, matricula, carrera, semestre, grupo in alumnos:
            cursor.execute("""
                INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, matricula, carrera, semestre, grupo, True))
        
        print("✅ Alumnos base insertados")
        
        # Insertar docentes base
        docentes = [
            ("Dr. Miguel Ángel Rodríguez Hernández", "DOC001", "Programación y Desarrollo de Software"),
            ("Ing. Laura Patricia Gómez Sánchez", "DOC002", "Redes y Telecomunicaciones"),
            ("M.C. José Luis Martínez Torres", "DOC003", "Base de Datos y Sistemas de Información"),
            ("Ing. Carmen Rosa Flores Díaz", "DOC004", "Matemáticas y Estadística"),
            ("Dr. Fernando Javier Cruz Morales", "DOC005", "Ingeniería de Software")
        ]
        
        for nombre, clave, especialidad in docentes:
            cursor.execute("""
                INSERT INTO docentes_base (nombre, clave, especialidad, activo)
                VALUES (%s, %s, %s, %s)
            """, (nombre, clave, especialidad, True))
        
        print("✅ Docentes base insertados")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error insertando datos base: {e}")
        return False

def crear_usuarios_sistema():
    """Crear usuarios del sistema con UIDs específicos"""
    try:
        print("👤 Creando usuarios del sistema...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Hash para contraseñas
        password_hash = bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        usuarios = [
            # Administrador con UID específico
            ("ADMIN001", "admin", "Administrador del Sistema", None, "ADMIN001", None, None, None, admin_hash),
            
            # Alumnos con UIDs de tarjetas RFID simuladas
            ("04 5C 8A 2A", "alumno", "Juan Carlos Pérez López", "20230001", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301", password_hash),
            ("04 7B 9C 3B", "alumno", "María Elena González Martínez", "20230002", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301", password_hash),
            ("04 8D 1E 4C", "alumno", "Roberto Miguel Jiménez Cruz", "20220001", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2402", password_hash),
            
            # Docentes con UIDs de tarjetas RFID simuladas
            ("04 9F 2A 5D", "docente", "Dr. Miguel Ángel Rodríguez Hernández", None, "DOC001", None, None, None, password_hash),
            ("04 1A 3B 6E", "docente", "Ing. Laura Patricia Gómez Sánchez", None, "DOC002", None, None, None, password_hash),
            ("04 2C 4D 7F", "docente", "M.C. José Luis Martínez Torres", None, "DOC003", None, None, None, password_hash),
            
            # Admin con UID de tarjeta para registro
            ("04 FF AA BB", "admin", "Admin con Tarjeta", None, "ADMIN_CARD", None, None, None, admin_hash),
        ]
        
        for uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, hash_pass in usuarios:
            cursor.execute("""
                INSERT INTO usuarios (uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, contraseña_hash, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, hash_pass, True))
            
            print(f"  ✅ {uid}: {nombre} ({rol})")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando usuarios: {e}")
        return False

def crear_registros_docentes():
    """Crear registros en tabla docentes para usuarios docentes"""
    try:
        print("👨‍🏫 Creando registros de docentes...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Obtener docentes usuarios
        cursor.execute("SELECT id, nombre FROM usuarios WHERE rol = 'docente'")
        docentes_usuarios = cursor.fetchall()
        
        for usuario_id, nombre in docentes_usuarios:
            cursor.execute("""
                INSERT INTO docentes (usuario_id, activo)
                VALUES (%s, %s)
            """, (usuario_id, True))
            print(f"  ✅ Registro docente: {nombre}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando registros docentes: {e}")
        return False

def simular_tarjetas_rfid():
    """Simular tarjetas RFID enviando UIDs al servidor"""
    try:
        print("📡 Simulando tarjetas RFID...")
        
        # Esperar a que el servidor esté listo
        print("⏳ Esperando servidor...")
        time.sleep(2)
        
        # UIDs de prueba
        uids_prueba = [
            "04 5C 8A 2A",  # Alumno Juan Carlos
            "04 7B 9C 3B",  # Alumno María Elena
            "04 9F 2A 5D",  # Docente Miguel
            "04 FF AA BB",  # Admin con tarjeta
            "ADMIN001"      # Admin por username
        ]
        
        for uid in uids_prueba:
            try:
                # Simular envío de UID al servidor
                response = requests.post(
                    "http://localhost:8000/usuarios/verificar_uid/",
                    json={"uid": uid},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("existe"):
                        usuario = data.get("usuario", {})
                        print(f"  ✅ {uid}: {usuario.get('nombre')} ({usuario.get('rol')})")
                    else:
                        print(f"  🆕 {uid}: Nuevo usuario")
                else:
                    print(f"  ❌ {uid}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️ {uid}: No se pudo conectar al servidor")
        
        return True
        
    except Exception as e:
        print(f"❌ Error simulando tarjetas: {e}")
        return False

def verificar_sistema_completo():
    """Verificar que todo el sistema funcione"""
    try:
        print("🔍 Verificando sistema completo...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Verificar carreras
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = TRUE")
        carreras_count = cursor.fetchone()[0]
        print(f"  📊 Carreras: {carreras_count}")
        
        # Verificar usuarios por rol
        cursor.execute("SELECT rol, COUNT(*) FROM usuarios WHERE activo = TRUE GROUP BY rol")
        roles = cursor.fetchall()
        for rol, count in roles:
            print(f"  👥 {rol}: {count} usuarios")
        
        # Verificar alumnos y docentes base
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = TRUE")
        alumnos_count = cursor.fetchone()[0]
        print(f"  👨‍🎓 Alumnos base: {alumnos_count}")
        
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = TRUE")
        docentes_count = cursor.fetchone()[0]
        print(f"  👨‍🏫 Docentes base: {docentes_count}")
        
        # Mostrar algunos usuarios con sus UIDs
        print("\n📋 Usuarios registrados:")
        cursor.execute("SELECT uid, nombre, rol FROM usuarios WHERE activo = TRUE ORDER BY rol, nombre")
        usuarios = cursor.fetchall()
        for uid, nombre, rol in usuarios:
            print(f"  {rol.upper()}: {uid} - {nombre}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error verificando sistema: {e}")
        return False

def main():
    """Función principal - Solución completa"""
    print("🔧 === SOLUCIÓN COMPLETA DE USUARIOS Y RFID ===\n")
    
    try:
        # 1. Limpiar y recrear base de datos
        if not limpiar_y_recrear_bd():
            print("❌ Error recreando BD")
            return False
        
        # 2. Crear estructura completa
        if not crear_estructura_completa():
            print("❌ Error creando estructura")
            return False
        
        # 3. Insertar datos base
        if not insertar_datos_base():
            print("❌ Error insertando datos base")
            return False
        
        # 4. Crear usuarios del sistema
        if not crear_usuarios_sistema():
            print("❌ Error creando usuarios")
            return False
        
        # 5. Crear registros de docentes
        if not crear_registros_docentes():
            print("❌ Error creando registros docentes")
            return False
        
        # 6. Verificar sistema
        if not verificar_sistema_completo():
            print("❌ Error verificando sistema")
            return False
        
        print("\n✅ === SOLUCIÓN COMPLETADA ===")
        
        print("\n🔐 Credenciales de acceso:")
        print("  👑 Admin (username): ADMIN001 / admin123")
        print("  👑 Admin (tarjeta): 04 FF AA BB / admin123")
        print("  👨‍🎓 Alumno: 04 5C 8A 2A / 12345678 (Juan Carlos)")
        print("  👨‍🎓 Alumno: 04 7B 9C 3B / 12345678 (María Elena)")
        print("  👨‍🏫 Docente: 04 9F 2A 5D / 12345678 (Dr. Miguel)")
        
        print("\n📡 UIDs de tarjetas RFID simuladas:")
        print("  - 04 5C 8A 2A (Alumno Juan Carlos)")
        print("  - 04 7B 9C 3B (Alumno María Elena)")
        print("  - 04 8D 1E 4C (Alumno Roberto)")
        print("  - 04 9F 2A 5D (Docente Miguel)")
        print("  - 04 1A 3B 6E (Docente Laura)")
        print("  - 04 FF AA BB (Admin con tarjeta)")
        
        print("\n🔄 Próximos pasos:")
        print("  1. Reiniciar servidor FastAPI")
        print("  2. Probar login con las credenciales")
        print("  3. Simular tarjetas RFID con los UIDs")
        print("  4. Registrar nuevos usuarios")
        
        # 7. Simular tarjetas RFID (opcional)
        print("\n📡 ¿Simular tarjetas RFID? (y/n): ", end="")
        respuesta = input().lower()
        if respuesta == 'y':
            simular_tarjetas_rfid()
        
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
