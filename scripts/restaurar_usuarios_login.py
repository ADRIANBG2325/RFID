#!/usr/bin/env python3
"""
Script para restaurar el funcionamiento del login de usuarios
sin perder los datos existentes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt

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

def verificar_y_reparar_contraseñas(session):
    """Verificar que las contraseñas estén correctamente hasheadas"""
    print("\n🔧 === VERIFICANDO CONTRASEÑAS ===")
    
    try:
        # Buscar usuarios con contraseñas que podrían estar mal
        result = session.execute(text("""
            SELECT id, uid, nombre, rol, contraseña_hash
            FROM usuarios 
            WHERE activo = TRUE
            ORDER BY fecha_registro DESC
        """))
        
        usuarios = result.fetchall()
        
        if not usuarios:
            print("⚠️  No se encontraron usuarios")
            return
        
        print(f"🔍 Verificando {len(usuarios)} usuarios...")
        
        usuarios_reparados = 0
        
        for usuario in usuarios:
            id_usuario, uid, nombre, rol, contraseña_hash = usuario
            
            # Verificar si la contraseña parece estar hasheada correctamente
            if not contraseña_hash or len(contraseña_hash) < 50:
                print(f"⚠️  Usuario {nombre} ({uid}) tiene contraseña sospechosa")
                
                # Ofrecer reparar con contraseña por defecto
                if rol == "admin":
                    nueva_contraseña = "admin123"
                elif rol == "docente":
                    nueva_contraseña = "docente123"
                else:
                    nueva_contraseña = "alumno123"
                
                contraseña_hash_nueva = bcrypt.hash(nueva_contraseña)
                
                session.execute(text("""
                    UPDATE usuarios 
                    SET contraseña_hash = :hash 
                    WHERE id = :id
                """), {
                    "hash": contraseña_hash_nueva,
                    "id": id_usuario
                })
                
                print(f"✅ Contraseña reparada para {nombre} - Nueva contraseña: {nueva_contraseña}")
                usuarios_reparados += 1
        
        if usuarios_reparados > 0:
            session.commit()
            print(f"\n✅ {usuarios_reparados} contraseñas reparadas")
        else:
            print("\n✅ Todas las contraseñas están OK")
            
    except Exception as e:
        print(f"❌ Error verificando contraseñas: {e}")
        session.rollback()

def crear_usuario_prueba_si_no_existe(session):
    """Crear un usuario de prueba para verificar que el login funciona"""
    print("\n🧪 === CREANDO USUARIO DE PRUEBA ===")
    
    try:
        # Verificar si ya existe un usuario de prueba
        result = session.execute(text("""
            SELECT id FROM usuarios WHERE uid = 'test_login'
        """))
        
        if result.fetchone():
            print("ℹ️  Usuario de prueba ya existe")
            return
        
        # Crear usuario de prueba
        contraseña_hash = bcrypt.hash("test1234")
        
        session.execute(text("""
            INSERT INTO usuarios (uid, nombre, rol, contraseña_hash, activo, fecha_registro)
            VALUES (:uid, :nombre, :rol, :hash, :activo, NOW())
        """), {
            "uid": "test_login",
            "nombre": "Usuario de Prueba",
            "rol": "admin",
            "hash": contraseña_hash,
            "activo": True
        })
        
        session.commit()
        
        print("✅ Usuario de prueba creado:")
        print("   UID: test_login")
        print("   Contraseña: test1234")
        print("   Rol: admin")
        
    except Exception as e:
        print(f"❌ Error creando usuario de prueba: {e}")
        session.rollback()

def mostrar_usuarios_para_login(session):
    """Mostrar usuarios disponibles para hacer login"""
    print("\n👥 === USUARIOS DISPONIBLES PARA LOGIN ===")
    
    try:
        result = session.execute(text("""
            SELECT uid, nombre, rol, 
                   CASE 
                       WHEN rol = 'admin' THEN 'admin123'
                       WHEN rol = 'docente' THEN 'docente123'
                       ELSE 'alumno123'
                   END as contraseña_sugerida
            FROM usuarios 
            WHERE activo = TRUE
            ORDER BY rol, nombre
            LIMIT 10
        """))
        
        usuarios = result.fetchall()
        
        if not usuarios:
            print("⚠️  No hay usuarios disponibles")
            return
        
        print("🔑 Credenciales para probar login:")
        print("-" * 60)
        
        for uid, nombre, rol, contraseña in usuarios:
            print(f"👤 {nombre} ({rol.upper()})")
            print(f"   UID: {uid}")
            print(f"   Contraseña sugerida: {contraseña}")
            print()
        
        print("📝 NOTA: Si las contraseñas sugeridas no funcionan,")
        print("         use las contraseñas originales que configuró.")
        
    except Exception as e:
        print(f"❌ Error mostrando usuarios: {e}")

def main():
    """Función principal"""
    print("🔧 === RESTAURACIÓN DE LOGIN DE USUARIOS ===")
    print("Este script reparará problemas de login sin perder datos")
    
    # Conectar a la base de datos
    session, engine = conectar_db()
    if not session:
        return
    
    try:
        # Verificar y reparar contraseñas si es necesario
        verificar_y_reparar_contraseñas(session)
        
        # Crear usuario de prueba
        crear_usuario_prueba_si_no_existe(session)
        
        # Mostrar usuarios disponibles
        mostrar_usuarios_para_login(session)
        
        print("\n✅ === RESTAURACIÓN COMPLETADA ===")
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Reinicie el servidor FastAPI")
        print("2. Pruebe hacer login con las credenciales mostradas")
        print("3. Si sigue sin funcionar, revise los logs del servidor")
        
        print("\n🌐 URLs para probar:")
        print("   - Login normal: http://localhost:8000/frontend/login.html")
        print("   - Login admin: http://localhost:8000/frontend/admin_login.html")
        
    except Exception as e:
        print(f"❌ Error durante la restauración: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
