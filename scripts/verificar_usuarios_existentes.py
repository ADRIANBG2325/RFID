#!/usr/bin/env python3
"""
Script para verificar que los usuarios existentes sigan funcionando
después de los cambios en los modelos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
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

def verificar_usuarios_en_db(session):
    """Verificar usuarios directamente en la base de datos"""
    print("\n🔍 === VERIFICANDO USUARIOS EN BASE DE DATOS ===")
    
    try:
        # Contar usuarios por rol
        result = session.execute(text("""
            SELECT rol, COUNT(*) as total, 
                   GROUP_CONCAT(CONCAT(nombre, ' (', uid, ')') SEPARATOR ', ') as usuarios
            FROM usuarios 
            WHERE activo = TRUE
            GROUP BY rol
            ORDER BY rol
        """))
        
        usuarios_por_rol = result.fetchall()
        
        if not usuarios_por_rol:
            print("⚠️  No se encontraron usuarios activos")
            return False
        
        print("📊 Usuarios encontrados:")
        total_usuarios = 0
        
        for rol, cantidad, usuarios in usuarios_por_rol:
            print(f"\n🔹 {rol.upper()}: {cantidad} usuario(s)")
            if usuarios:
                usuarios_lista = usuarios.split(', ')
                for usuario in usuarios_lista[:3]:  # Mostrar máximo 3
                    print(f"   - {usuario}")
                if len(usuarios_lista) > 3:
                    print(f"   ... y {len(usuarios_lista) - 3} más")
            total_usuarios += cantidad
        
        print(f"\n📈 TOTAL: {total_usuarios} usuarios activos")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando usuarios: {e}")
        return False

def probar_login_usuarios(session):
    """Probar login con algunos usuarios existentes"""
    print("\n🧪 === PROBANDO LOGIN DE USUARIOS ===")
    
    try:
        # Obtener algunos usuarios para probar
        result = session.execute(text("""
            SELECT uid, nombre, rol 
            FROM usuarios 
            WHERE activo = TRUE 
            ORDER BY fecha_registro DESC 
            LIMIT 5
        """))
        
        usuarios_prueba = result.fetchall()
        
        if not usuarios_prueba:
            print("⚠️  No hay usuarios para probar")
            return
        
        print("🔐 Usuarios disponibles para probar login:")
        for i, (uid, nombre, rol) in enumerate(usuarios_prueba, 1):
            print(f"   {i}. {nombre} ({rol}) - UID: {uid}")
        
        print("\n💡 Para probar login, use las credenciales:")
        print("   - UID: [el mostrado arriba]")
        print("   - Contraseña: [la que configuró al registrar]")
        
        # Intentar verificar UID con la API
        if usuarios_prueba:
            uid_prueba = usuarios_prueba[0][0]
            print(f"\n🔍 Verificando UID '{uid_prueba}' con la API...")
            
            try:
                response = requests.post(
                    "http://localhost:8000/usuarios/verificar_uid/",
                    json={"uid": uid_prueba},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("existe"):
                        usuario = data.get("usuario", {})
                        print(f"✅ API responde correctamente:")
                        print(f"   - Nombre: {usuario.get('nombre')}")
                        print(f"   - Rol: {usuario.get('rol')}")
                        print(f"   - Activo: {usuario.get('activo')}")
                    else:
                        print("❌ API dice que el usuario no existe")
                else:
                    print(f"❌ API respondió con error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("⚠️  No se puede conectar a la API (servidor no está corriendo)")
            except Exception as e:
                print(f"❌ Error probando API: {e}")
        
    except Exception as e:
        print(f"❌ Error obteniendo usuarios para prueba: {e}")

def verificar_estructura_tablas(session):
    """Verificar que las tablas críticas existan"""
    print("\n🏗️  === VERIFICANDO ESTRUCTURA DE TABLAS ===")
    
    tablas_criticas = [
        "usuarios", "carreras", "materias", "docentes", 
        "asignaciones_materias", "asistencias"
    ]
    
    try:
        for tabla in tablas_criticas:
            result = session.execute(text(f"SHOW TABLES LIKE '{tabla}'"))
            if result.fetchone():
                print(f"✅ Tabla '{tabla}' existe")
                
                # Verificar algunas columnas críticas
                if tabla == "usuarios":
                    result = session.execute(text("DESCRIBE usuarios"))
                    columnas = [row[0] for row in result.fetchall()]
                    columnas_requeridas = ["id", "uid", "nombre", "rol", "contraseña_hash", "activo"]
                    
                    for col in columnas_requeridas:
                        if col in columnas:
                            print(f"   ✅ Columna '{col}' OK")
                        else:
                            print(f"   ❌ Columna '{col}' FALTA")
            else:
                print(f"❌ Tabla '{tabla}' NO EXISTE")
                
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")

def main():
    """Función principal"""
    print("🔍 === VERIFICACIÓN DE USUARIOS EXISTENTES ===")
    print("Verificando que los usuarios sigan funcionando después de los cambios...")
    
    # Conectar a la base de datos
    session, engine = conectar_db()
    if not session:
        return
    
    try:
        # Verificar estructura de tablas
        verificar_estructura_tablas(session)
        
        # Verificar usuarios en la base de datos
        usuarios_ok = verificar_usuarios_en_db(session)
        
        if usuarios_ok:
            # Probar login de usuarios
            probar_login_usuarios(session)
            
            print("\n✅ === VERIFICACIÓN COMPLETADA ===")
            print("Los usuarios existentes deberían seguir funcionando.")
            print("\n🔧 Si hay problemas de login:")
            print("1. Verifique que el servidor FastAPI esté corriendo")
            print("2. Pruebe con las credenciales mostradas arriba")
            print("3. Revise los logs del servidor para errores específicos")
        else:
            print("\n❌ === PROBLEMA DETECTADO ===")
            print("No se encontraron usuarios o hay problemas con la base de datos.")
            
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
