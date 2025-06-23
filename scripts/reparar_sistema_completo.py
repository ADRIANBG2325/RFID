#!/usr/bin/env python3
"""
Reparación completa del sistema - Soluciona todos los problemas
"""

import sys
import mysql.connector
from mysql.connector import Error
import bcrypt
import requests
import time
import json

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'control_asistencia',
    'user': 'User',
    'password': '12345678'
}

def test_database_connection():
    """Probar conexión a la base de datos"""
    try:
        print("🔌 Probando conexión a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ Conectado a MySQL versión: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

def recrear_base_datos():
    """Recrear base de datos desde cero"""
    try:
        print("🗑️ Recreando base de datos...")
        
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        # Eliminar y recrear base de datos
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        print(f"✅ Base de datos {DB_CONFIG['database']} recreada")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error recreando BD: {e}")
        return False

def crear_tablas():
    """Crear todas las tablas necesarias"""
    try:
        print("📋 Creando tablas...")
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("  ✅ Tabla usuarios creada")
        
        # Tabla carreras
        cursor.execute("""
            CREATE TABLE carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL,
                codigo VARCHAR(20) UNIQUE NOT NULL,
                activa BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("  ✅ Tabla carreras creada")
        
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("  ✅ Tabla alumnos_base creada")
        
        # Tabla docentes_base
        cursor.execute("""
            CREATE TABLE docentes_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                clave VARCHAR(100) UNIQUE NOT NULL,
                especialidad VARCHAR(200) NULL,
                activo BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("  ✅ Tabla docentes_base creada")
        
        # Tabla docentes (relación)
        cursor.execute("""
            CREATE TABLE docentes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT UNIQUE NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("  ✅ Tabla docentes creada")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def insertar_datos_iniciales():
    """Insertar datos iniciales"""
    try:
        print("📊 Insertando datos iniciales...")
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
        
        print("  ✅ Carreras insertadas")
        
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
        
        print("  ✅ Alumnos base insertados")
        
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
        
        print("  ✅ Docentes base insertados")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error insertando datos: {e}")
        return False

def crear_usuarios_con_hash_correcto():
    """Crear usuarios con hash de contraseña correcto"""
    try:
        print("👤 Creando usuarios con hash correcto...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Generar hashes correctos
        def generar_hash(password):
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Contraseñas
        password_normal = generar_hash("12345678")
        password_admin = generar_hash("admin123")
        
        print(f"  🔐 Hash normal generado: {password_normal[:50]}...")
        print(f"  🔐 Hash admin generado: {password_admin[:50]}...")
        
        usuarios = [
            # Administradores
            ("ADMIN001", "admin", "Administrador Principal", None, "ADMIN001", None, None, None, password_admin),
            ("04FFAABB", "admin", "Admin con Tarjeta", None, "ADMIN_CARD", None, None, None, password_admin),
            
            # Alumnos con UIDs de tarjetas
            ("045C8A2A", "alumno", "Juan Carlos Pérez López", "20230001", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301", password_normal),
            ("047B9C3B", "alumno", "María Elena González Martínez", "20230002", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 3, "2301", password_normal),
            ("048D1E4C", "alumno", "Roberto Miguel Jiménez Cruz", "20220001", None, "Ingeniería en Tecnologías de la Información y Comunicaciones", 4, "2402", password_normal),
            
            # Docentes con UIDs de tarjetas
            ("049F2A5D", "docente", "Dr. Miguel Ángel Rodríguez Hernández", None, "DOC001", None, None, None, password_normal),
            ("041A3B6E", "docente", "Ing. Laura Patricia Gómez Sánchez", None, "DOC002", None, None, None, password_normal),
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
    """Crear registros en tabla docentes"""
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

def probar_login_directo():
    """Probar login directamente en la base de datos"""
    try:
        print("🔐 Probando login directo...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Probar algunos usuarios
        usuarios_prueba = [
            ("ADMIN001", "admin123"),
            ("045C8A2A", "12345678"),
            ("047B9C3B", "12345678"),
            ("049F2A5D", "12345678")
        ]
        
        for uid, password in usuarios_prueba:
            cursor.execute("SELECT uid, nombre, rol, contraseña_hash FROM usuarios WHERE uid = %s", (uid,))
            usuario = cursor.fetchone()
            
            if usuario:
                uid_db, nombre, rol, hash_db = usuario
                # Verificar contraseña
                if bcrypt.checkpw(password.encode('utf-8'), hash_db.encode('utf-8')):
                    print(f"  ✅ {uid}: {nombre} ({rol}) - Login OK")
                else:
                    print(f"  ❌ {uid}: {nombre} ({rol}) - Contraseña incorrecta")
            else:
                print(f"  ❌ {uid}: Usuario no encontrado")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error probando login: {e}")
        return False

def verificar_api_endpoints():
    """Verificar que los endpoints de la API funcionen"""
    try:
        print("🌐 Verificando endpoints de la API...")
        
        # Esperar a que el servidor esté listo
        print("  ⏳ Esperando servidor...")
        time.sleep(2)
        
        # Probar verificar UID
        test_uids = ["ADMIN001", "045C8A2A", "047B9C3B"]
        
        for uid in test_uids:
            try:
                response = requests.post(
                    "http://localhost:8000/usuarios/verificar_uid/",
                    json={"uid": uid},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("existe"):
                        usuario = data.get("usuario", {})
                        print(f"  ✅ API {uid}: {usuario.get('nombre')} ({usuario.get('rol')})")
                    else:
                        print(f"  🆕 API {uid}: Nuevo usuario")
                else:
                    print(f"  ❌ API {uid}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️ API {uid}: No se pudo conectar - {e}")
        
        # Probar login
        try:
            response = requests.post(
                "http://localhost:8000/usuarios/login/",
                json={"uid": "045C8A2A", "contraseña": "12345678"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Login API: {data.get('nombre')} - {data.get('mensaje')}")
            else:
                print(f"  ❌ Login API: Error {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️ Login API: No se pudo conectar - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando API: {e}")
        return False

def mostrar_resumen_final():
    """Mostrar resumen final del sistema"""
    try:
        print("📊 Resumen final del sistema...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Contar usuarios por rol
        cursor.execute("SELECT rol, COUNT(*) FROM usuarios WHERE activo = TRUE GROUP BY rol")
        roles = cursor.fetchall()
        
        print("\n👥 Usuarios por rol:")
        for rol, count in roles:
            print(f"  {rol.upper()}: {count} usuarios")
        
        # Mostrar usuarios con UIDs
        print("\n📋 Lista completa de usuarios:")
        cursor.execute("SELECT uid, nombre, rol FROM usuarios WHERE activo = TRUE ORDER BY rol, nombre")
        usuarios = cursor.fetchall()
        
        for uid, nombre, rol in usuarios:
            print(f"  {rol.upper()}: {uid} - {nombre}")
        
        # Mostrar carreras
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = TRUE")
        carreras_count = cursor.fetchone()[0]
        print(f"\n🎓 Carreras disponibles: {carreras_count}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error mostrando resumen: {e}")
        return False

def main():
    """Función principal - Reparación completa"""
    print("🔧 === REPARACIÓN COMPLETA DEL SISTEMA ===\n")
    
    try:
        # 1. Probar conexión
        if not test_database_connection():
            print("❌ No se puede conectar a la base de datos")
            return False
        
        # 2. Recrear base de datos
        if not recrear_base_datos():
            print("❌ Error recreando base de datos")
            return False
        
        # 3. Crear tablas
        if not crear_tablas():
            print("❌ Error creando tablas")
            return False
        
        # 4. Insertar datos iniciales
        if not insertar_datos_iniciales():
            print("❌ Error insertando datos iniciales")
            return False
        
        # 5. Crear usuarios con hash correcto
        if not crear_usuarios_con_hash_correcto():
            print("❌ Error creando usuarios")
            return False
        
        # 6. Crear registros de docentes
        if not crear_registros_docentes():
            print("❌ Error creando registros docentes")
            return False
        
        # 7. Probar login directo
        if not probar_login_directo():
            print("❌ Error probando login")
            return False
        
        # 8. Mostrar resumen
        if not mostrar_resumen_final():
            print("❌ Error mostrando resumen")
            return False
        
        print("\n✅ === REPARACIÓN COMPLETADA ===")
        
        print("\n🔐 CREDENCIALES DE ACCESO:")
        print("┌─────────────────────────────────────────────────────────┐")
        print("│ ADMINISTRADORES:                                        │")
        print("│  👑 UID: ADMIN001     | Contraseña: admin123           │")
        print("│  👑 UID: 04FFAABB     | Contraseña: admin123           │")
        print("│                                                         │")
        print("│ ALUMNOS:                                                │")
        print("│  👨‍🎓 UID: 045C8A2A     | Contraseña: 12345678           │")
        print("│  👨‍🎓 UID: 047B9C3B     | Contraseña: 12345678           │")
        print("│  👨‍🎓 UID: 048D1E4C     | Contraseña: 12345678           │")
        print("│                                                         │")
        print("│ DOCENTES:                                               │")
        print("│  👨‍🏫 UID: 049F2A5D     | Contraseña: 12345678           │")
        print("│  👨‍🏫 UID: 041A3B6E     | Contraseña: 12345678           │")
        print("└─────────────────────────────────────────────────────────┘")
        
        print("\n🔄 PRÓXIMOS PASOS:")
        print("1. Reiniciar el servidor FastAPI")
        print("2. Probar login con las credenciales")
        print("3. Verificar registro de administrador")
        print("4. Probar simulador de tarjetas RFID")
        
        # 9. Verificar API (opcional)
        print("\n📡 ¿Verificar endpoints de la API? (y/n): ", end="")
        try:
            respuesta = input().lower()
            if respuesta == 'y':
                verificar_api_endpoints()
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
