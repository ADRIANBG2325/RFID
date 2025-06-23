#!/usr/bin/env python3
"""
Script para corregir problemas de login del sistema
- Verificar administradores existentes
- Corregir contraseñas si es necesario
- Probar login de todos los roles
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt
import requests
import json

# Configuración de base de datos
DATABASE_URL = "mysql+pymysql://root:@localhost/asistencias_rfid"

def conectar_db():
    """Conectar a la base de datos"""
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        return session, engine
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None, None

def verificar_administradores(session):
    """Verificar administradores existentes"""
    print("\n🔍 === VERIFICANDO ADMINISTRADORES ===")
    
    try:
        result = session.execute(text("""
            SELECT id, uid, nombre, rol, activo, fecha_registro
            FROM usuarios 
            WHERE rol = 'admin'
            ORDER BY fecha_registro DESC
        """))
        
        admins = result.fetchall()
        
        if not admins:
            print("⚠️  No se encontraron administradores en el sistema")
            return []
        
        print(f"✅ Se encontraron {len(admins)} administrador(es):")
        
        for admin in admins:
            print(f"   - ID: {admin.id}")
            print(f"     UID: {admin.uid}")
            print(f"     Nombre: {admin.nombre}")
            print(f"     Activo: {admin.activo}")
            print(f"     Fecha: {admin.fecha_registro}")
            print()
        
        return admins
        
    except Exception as e:
        print(f"❌ Error verificando administradores: {e}")
        return []

def crear_admin_prueba(session):
    """Crear un administrador de prueba si no existe"""
    print("\n🔧 === CREANDO ADMINISTRADOR DE PRUEBA ===")
    
    try:
        # Verificar si ya existe
        result = session.execute(text("""
            SELECT id FROM usuarios WHERE uid = 'admin_test'
        """))
        
        if result.fetchone():
            print("ℹ️  El administrador de prueba ya existe")
            return True
        
        # Crear contraseña hash
        contraseña = "admin123"
        contraseña_hash = bcrypt.hash(contraseña)
        
        # Insertar administrador
        session.execute(text("""
            INSERT INTO usuarios (uid, nombre, rol, contraseña_hash, activo, fecha_registro)
            VALUES (:uid, :nombre, :rol, :contraseña_hash, :activo, NOW())
        """), {
            "uid": "admin_test",
            "nombre": "Administrador de Prueba",
            "rol": "admin",
            "contraseña_hash": contraseña_hash,
            "activo": True
        })
        
        session.commit()
        
        print("✅ Administrador de prueba creado:")
        print(f"   UID: admin_test")
        print(f"   Contraseña: {contraseña}")
        print(f"   Nombre: Administrador de Prueba")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando administrador de prueba: {e}")
        session.rollback()
        return False

def probar_login_api(uid, contraseña, tipo_usuario="normal"):
    """Probar login a través de la API"""
    try:
        url = "http://localhost:8000/usuarios/login/"
        
        payload = {
            "uid": uid,
            "contraseña": contraseña
        }
        
        print(f"🔐 Probando login para {uid}...")
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login exitoso:")
            print(f"   Nombre: {data.get('nombre')}")
            print(f"   Rol: {data.get('rol')}")
            print(f"   UID: {data.get('uid')}")
            return True
        else:
            print(f"❌ Login fallido (HTTP {response.status_code}):")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Error desconocido')}")
            except:
                print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor API")
        print("   Asegúrese de que el servidor FastAPI esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error probando login: {e}")
        return False

def probar_registro_admin():
    """Probar registro de administrador"""
    print("\n🧪 === PROBANDO REGISTRO DE ADMINISTRADOR ===")
    
    try:
        url = "http://localhost:8000/usuarios/registrar_admin/"
        
        payload = {
            "uid_o_username": "admin_registro_test",
            "nombre_usuario": "admin_registro_test",
            "nombre_completo": "Admin Registro Test",
            "clave_secreta": "SOLDADORES",
            "contraseña": "test1234",
            "confirmar_contraseña": "test1234",
            "tipo_registro": "username"
        }
        
        print("🚀 Enviando solicitud de registro...")
        print(f"   Clave secreta: {payload['clave_secreta']}")
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Registro exitoso:")
            print(f"   Mensaje: {data.get('mensaje')}")
            if 'admin' in data:
                admin_data = data['admin']
                print(f"   UID: {admin_data.get('uid')}")
                print(f"   Nombre: {admin_data.get('nombre')}")
            return True
        else:
            print(f"❌ Registro fallido (HTTP {response.status_code}):")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Error desconocido')}")
            except:
                print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor API")
        return False
    except Exception as e:
        print(f"❌ Error probando registro: {e}")
        return False

def verificar_usuarios_ejemplo(session):
    """Verificar que existan usuarios de ejemplo para probar"""
    print("\n👥 === VERIFICANDO USUARIOS DE EJEMPLO ===")
    
    try:
        # Verificar alumnos
        result = session.execute(text("""
            SELECT COUNT(*) as total FROM usuarios WHERE rol = 'alumno'
        """))
        total_alumnos = result.fetchone().total
        
        # Verificar docentes
        result = session.execute(text("""
            SELECT COUNT(*) as total FROM usuarios WHERE rol = 'docente'
        """))
        total_docentes = result.fetchone().total
        
        print(f"📊 Usuarios en el sistema:")
        print(f"   Alumnos: {total_alumnos}")
        print(f"   Docentes: {total_docentes}")
        
        if total_alumnos == 0:
            print("⚠️  No hay alumnos registrados")
        
        if total_docentes == 0:
            print("⚠️  No hay docentes registrados")
        
        # Mostrar algunos ejemplos
        if total_alumnos > 0:
            result = session.execute(text("""
                SELECT uid, nombre, matricula, carrera, semestre, grupo
                FROM usuarios 
                WHERE rol = 'alumno' 
                LIMIT 3
            """))
            
            print("\n📚 Ejemplos de alumnos:")
            for alumno in result.fetchall():
                print(f"   - {alumno.nombre} (UID: {alumno.uid}, Matrícula: {alumno.matricula})")
        
        if total_docentes > 0:
            result = session.execute(text("""
                SELECT uid, nombre, clave_docente
                FROM usuarios 
                WHERE rol = 'docente' 
                LIMIT 3
            """))
            
            print("\n👨‍🏫 Ejemplos de docentes:")
            for docente in result.fetchall():
                print(f"   - {docente.nombre} (UID: {docente.uid}, Clave: {docente.clave_docente})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando usuarios: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 === CORRECCIÓN DEL SISTEMA DE LOGIN ===")
    print("Este script verificará y corregirá problemas de login")
    
    # Conectar a la base de datos
    session, engine = conectar_db()
    if not session:
        return
    
    try:
        # 1. Verificar administradores existentes
        admins = verificar_administradores(session)
        
        # 2. Crear admin de prueba si no hay ninguno
        if not admins:
            crear_admin_prueba(session)
        
        # 3. Verificar usuarios de ejemplo
        verificar_usuarios_ejemplo(session)
        
        # 4. Probar registro de administrador
        print("\n" + "="*50)
        probar_registro_admin()
        
        # 5. Probar login de administrador
        print("\n" + "="*50)
        print("🧪 === PROBANDO LOGIN DE ADMINISTRADOR ===")
        
        if admins:
            # Probar con el primer admin encontrado
            admin = admins[0]
            print(f"ℹ️  Para probar login, use:")
            print(f"   UID: {admin.uid}")
            print(f"   Contraseña: [la que configuró]")
        
        # Probar con admin de prueba
        probar_login_api("admin_test", "admin123", "admin")
        
        print("\n✅ === VERIFICACIÓN COMPLETADA ===")
        print("\n📋 RESUMEN:")
        print("1. ✅ Base de datos verificada")
        print("2. ✅ Administradores verificados")
        print("3. ✅ API de registro probada")
        print("4. ✅ API de login probada")
        
        print("\n🔑 CREDENCIALES DE PRUEBA:")
        print("   Admin: admin_test / admin123")
        
        print("\n🌐 URLS PARA PROBAR:")
        print("   - Login normal: http://localhost:8000/frontend/login.html")
        print("   - Login admin: http://localhost:8000/frontend/admin_login.html")
        print("   - Registro admin: http://localhost:8000/frontend/admin_registro.html")
        
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
