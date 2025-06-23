#!/usr/bin/env python3
"""
Script para insertar usuarios básicos de forma simple
"""

import sys
import mysql.connector
from mysql.connector import Error
import bcrypt

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'control_asistencia',
    'user': 'User',
    'password': '12345678'
}

def crear_tablas_basicas():
    """Crear tablas básicas si no existen"""
    try:
        print("📋 Verificando/creando tablas básicas...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Crear tabla usuarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uid VARCHAR(100) UNIQUE NOT NULL,
                rol VARCHAR(50) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                matricula VARCHAR(100) NULL,
                clave_docente VARCHAR(100) NULL,
                carrera VARCHAR(100) NULL,
                semestre INT NULL,
                grupo VARCHAR(10) NULL,
                contraseña_hash VARCHAR(255) NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla carreras si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL,
                codigo VARCHAR(20) UNIQUE NOT NULL,
                activa BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Crear tabla alumnos_base si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alumnos_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                matricula VARCHAR(100) UNIQUE NOT NULL,
                carrera VARCHAR(100) NOT NULL,
                semestre INT NOT NULL,
                grupo VARCHAR(10) NOT NULL,
                activo BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Crear tabla docentes_base si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS docentes_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                clave VARCHAR(100) UNIQUE NOT NULL,
                especialidad VARCHAR(200) NULL,
                activo BOOLEAN DEFAULT TRUE
            )
        """)
        
        connection.commit()
        print("✅ Tablas verificadas/creadas")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def insertar_carreras():
    """Insertar carreras básicas"""
    try:
        print("🎓 Insertando carreras...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
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
            try:
                cursor.execute("""
                    INSERT INTO carreras (id, nombre, codigo, activa)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), codigo = VALUES(codigo)
                """, (carrera_id, nombre, codigo, True))
                print(f"  ✅ {carrera_id}. {nombre}")
            except Error as e:
                print(f"  ❌ Error con carrera {nombre}: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error insertando carreras: {e}")
        return False

def insertar_alumnos_base():
    """Insertar alumnos base"""
    try:
        print("👨‍🎓 Insertando alumnos base...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        alumnos = [
            ("Juan Carlos Pérez López", "20230001", "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301"),
            ("María Elena González Martínez", "20230002", "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301"),
            ("Roberto Miguel Jiménez Cruz", "20220001", "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2402"),
            ("Ana Patricia López Hernández", "20230003", "Ingeniería Industrial", 2, "1201"),
            ("Carlos Eduardo Martínez Sánchez", "20230004", "Ingeniería en Sistemas Computacionales", 5, "3501")
        ]
        
        for nombre, matricula, carrera, semestre, grupo in alumnos:
            try:
                cursor.execute("""
                    INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
                """, (nombre, matricula, carrera, semestre, grupo, True))
                print(f"  ✅ {matricula}: {nombre}")
            except Error as e:
                print(f"  ❌ Error con alumno {nombre}: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error insertando alumnos: {e}")
        return False

def insertar_docentes_base():
    """Insertar docentes base"""
    try:
        print("👨‍🏫 Insertando docentes base...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        docentes = [
            ("Dr. Miguel Ángel Rodríguez Hernández", "DOC001", "Programación y Desarrollo de Software"),
            ("Ing. Laura Patricia Gómez Sánchez", "DOC002", "Redes y Telecomunicaciones"),
            ("M.C. José Luis Martínez Torres", "DOC003", "Base de Datos y Sistemas de Información"),
            ("Ing. Carmen Rosa Flores Díaz", "DOC004", "Matemáticas y Estadística"),
            ("Dr. Fernando Javier Cruz Morales", "DOC005", "Ingeniería de Software")
        ]
        
        for nombre, clave, especialidad in docentes:
            try:
                cursor.execute("""
                    INSERT INTO docentes_base (nombre, clave, especialidad, activo)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
                """, (nombre, clave, especialidad, True))
                print(f"  ✅ {clave}: {nombre}")
            except Error as e:
                print(f"  ❌ Error con docente {nombre}: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error insertando docentes: {e}")
        return False

def insertar_usuarios():
    """Insertar usuarios de prueba"""
    try:
        print("👤 Insertando usuarios de prueba...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Hash para contraseña "12345678"
        password_hash = bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        usuarios = [
            # Administrador
            ("ADMIN001", "admin", "Administrador del Sistema", None, "ADMIN001", None, None, None, admin_hash),
            
            # Alumnos
            ("ALU001", "alumno", "Juan Carlos Pérez López", "20230001", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301", password_hash),
            ("ALU002", "alumno", "María Elena González Martínez", "20230002", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301", password_hash),
            ("ALU003", "alumno", "Roberto Miguel Jiménez Cruz", "20220001", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2402", password_hash),
            
            # Docentes
            ("DOC001", "docente", "Dr. Miguel Ángel Rodríguez Hernández", None, "DOC001", None, None, None, password_hash),
            ("DOC002", "docente", "Ing. Laura Patricia Gómez Sánchez", None, "DOC002", None, None, None, password_hash),
            ("DOC003", "docente", "M.C. José Luis Martínez Torres", None, "DOC003", None, None, None, password_hash),
        ]
        
        for uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, hash_pass in usuarios:
            try:
                cursor.execute("""
                    INSERT INTO usuarios (uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, contraseña_hash, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        nombre = VALUES(nombre),
                        contraseña_hash = VALUES(contraseña_hash),
                        activo = TRUE
                """, (uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, hash_pass, True))
                
                print(f"  ✅ {uid}: {nombre} ({rol})")
            except Error as e:
                print(f"  ❌ Error con usuario {uid}: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error insertando usuarios: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 === INSERCIÓN DE USUARIOS BÁSICOS ===\n")
    
    try:
        # 1. Crear tablas básicas
        if not crear_tablas_basicas():
            print("❌ Error creando tablas")
            return False
        
        # 2. Insertar carreras
        if not insertar_carreras():
            print("❌ Error insertando carreras")
            return False
        
        # 3. Insertar alumnos base
        if not insertar_alumnos_base():
            print("❌ Error insertando alumnos base")
            return False
        
        # 4. Insertar docentes base
        if not insertar_docentes_base():
            print("❌ Error insertando docentes base")
            return False
        
        # 5. Insertar usuarios
        if not insertar_usuarios():
            print("❌ Error insertando usuarios")
            return False
        
        print("\n✅ === INSERCIÓN COMPLETADA ===")
        print("\n🔐 Credenciales de prueba:")
        print("  👑 Admin: ADMIN001 / admin123")
        print("  👨‍🎓 Alumno: ALU001 / 12345678")
        print("  👨‍🎓 Alumno: ALU002 / 12345678")
        print("  👨‍🏫 Docente: DOC001 / 12345678")
        print("  👨‍🏫 Docente: DOC002 / 12345678")
        
        print("\n🔄 Próximos pasos:")
        print("  1. Reiniciar servidor FastAPI")
        print("  2. Probar login con las credenciales")
        print("  3. Verificar que aparezcan las carreras")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
