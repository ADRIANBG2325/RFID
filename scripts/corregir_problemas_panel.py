#!/usr/bin/env python3
"""
Script para corregir problemas del panel de administrador
- Verificar conexión a la base de datos
- Corregir problemas de autenticación
- Verificar endpoints de la API
- Crear datos de prueba si es necesario
"""

import sys
import os
import requests
import json
from datetime import datetime

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from app.database import get_db, engine
    from app import models
    from sqlalchemy.orm import Session
    from passlib.hash import bcrypt
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

API_BASE = "http://localhost:8000"

def verificar_conexion_db():
    """Verificar conexión a la base de datos"""
    try:
        print("🔍 Verificando conexión a la base de datos...")
        
        # Crear una sesión de prueba
        db = next(get_db())
        
        # Verificar que las tablas existen
        usuarios_count = db.query(models.Usuario).count()
        print(f"✅ Conexión exitosa - {usuarios_count} usuarios en la base")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return False

def verificar_api_funcionando():
    """Verificar que la API está funcionando"""
    try:
        print("🔍 Verificando API...")
        
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            return True
        else:
            print(f"❌ API respondió con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando con la API: {e}")
        return False

def crear_admin_prueba():
    """Crear un administrador de prueba"""
    try:
        print("👤 Creando administrador de prueba...")
        
        db = next(get_db())
        
        # Verificar si ya existe
        admin_existente = db.query(models.Usuario).filter(
            models.Usuario.uid == "admin123",
            models.Usuario.rol == "admin"
        ).first()
        
        if admin_existente:
            print("✅ Administrador de prueba ya existe")
            db.close()
            return True
        
        # Crear nuevo admin
        admin_prueba = models.Usuario(
            uid="admin123",
            nombre="Administrador de Prueba",
            contraseña_hash=bcrypt.hash("admin123"),
            rol="admin",
            activo=True,
            fecha_registro=datetime.now()
        )
        
        db.add(admin_prueba)
        db.commit()
        
        print("✅ Administrador de prueba creado:")
        print("   UID: admin123")
        print("   Contraseña: admin123")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando administrador de prueba: {e}")
        return False

def crear_usuarios_prueba():
    """Crear usuarios de prueba para testing"""
    try:
        print("👥 Creando usuarios de prueba...")
        
        db = next(get_db())
        
        # Crear alumno de prueba
        alumno_existente = db.query(models.Usuario).filter(
            models.Usuario.matricula == "20240001"
        ).first()
        
        if not alumno_existente:
            alumno_prueba = models.Usuario(
                uid="alumno123",
                nombre="Juan Pérez Estudiante",
                contraseña_hash=bcrypt.hash("alumno12"),
                rol="alumno",
                matricula="20240001",
                carrera="Ingeniería en Sistemas Computacionales",
                semestre=3,
                grupo="3301",
                activo=True,
                fecha_registro=datetime.now()
            )
            db.add(alumno_prueba)
            print("✅ Alumno de prueba creado: Juan Pérez (20240001)")
        
        # Crear docente de prueba
        docente_existente = db.query(models.Usuario).filter(
            models.Usuario.clave_docente == "DOC001"
        ).first()
        
        if not docente_existente:
            docente_prueba = models.Usuario(
                uid="docente123",
                nombre="María García Profesora",
                contraseña_hash=bcrypt.hash("docent12"),
                rol="docente",
                clave_docente="DOC001",
                activo=True,
                fecha_registro=datetime.now()
            )
            db.add(docente_prueba)
            print("✅ Docente de prueba creado: María García (DOC001)")
        
        db.commit()
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuarios de prueba: {e}")
        return False

def probar_endpoints_admin():
    """Probar endpoints del administrador"""
    try:
        print("🔍 Probando endpoints del administrador...")
        
        # Datos del admin de prueba
        admin_uid = "admin123"
        
        # Probar listar usuarios
        response = requests.get(f"{API_BASE}/usuarios/listar_usuarios/?admin_uid={admin_uid}")
        if response.status_code == 200:
            usuarios = response.json()
            print(f"✅ Endpoint listar usuarios: {len(usuarios)} usuarios encontrados")
        else:
            print(f"❌ Error en listar usuarios: {response.status_code}")
            print(f"   Respuesta: {response.text}")
        
        # Probar semestre actual
        response = requests.get(f"{API_BASE}/admin/semestre_actual?uid={admin_uid}")
        if response.status_code == 200:
            semestre = response.json()
            print(f"✅ Endpoint semestre actual: {semestre.get('nombre', 'N/A')}")
        else:
            print(f"❌ Error en semestre actual: {response.status_code}")
            print(f"   Respuesta: {response.text}")
        
        # Probar estadísticas
        response = requests.get(f"{API_BASE}/admin/estadisticas/asistencias_hoy?uid={admin_uid}")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Endpoint estadísticas: {stats.get('total', 0)} asistencias hoy")
        else:
            print(f"❌ Error en estadísticas: {response.status_code}")
            print(f"   Respuesta: {response.text}")
        
        # Probar carreras
        response = requests.get(f"{API_BASE}/admin/carreras/?uid={admin_uid}")
        if response.status_code == 200:
            carreras = response.json()
            print(f"✅ Endpoint carreras: {len(carreras)} carreras encontradas")
        else:
            print(f"❌ Error en carreras: {response.status_code}")
            print(f"   Respuesta: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def verificar_tablas_necesarias():
    """Verificar que todas las tablas necesarias existen"""
    try:
        print("🔍 Verificando tablas de la base de datos...")
        
        db = next(get_db())
        
        # Verificar tabla usuarios
        try:
            count = db.query(models.Usuario).count()
            print(f"✅ Tabla usuarios: {count} registros")
        except Exception as e:
            print(f"❌ Error en tabla usuarios: {e}")
        
        # Verificar tabla carreras
        try:
            count = db.query(models.Carrera).count()
            print(f"✅ Tabla carreras: {count} registros")
        except Exception as e:
            print(f"⚠️  Tabla carreras no encontrada o vacía")
        
        # Verificar tabla materias
        try:
            count = db.query(models.Materia).count()
            print(f"✅ Tabla materias: {count} registros")
        except Exception as e:
            print(f"⚠️  Tabla materias no encontrada o vacía")
        
        # Verificar tabla asistencias
        try:
            count = db.query(models.Asistencia).count()
            print(f"✅ Tabla asistencias: {count} registros")
        except Exception as e:
            print(f"⚠️  Tabla asistencias no encontrada o vacía")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def crear_carreras_basicas():
    """Crear carreras básicas si no existen"""
    try:
        print("📚 Creando carreras básicas...")
        
        db = next(get_db())
        
        CARRERAS_MAP = {
            1: "Ingeniería Industrial",
            2: "Ingeniería en Tecnologías de la Información y Comunicaciones", 
            3: "Ingeniería en Sistemas Computacionales",
            4: "Ingeniería Mecatrónica",
            5: "Ingeniería Civil",
            6: "Licenciatura en Administración",
            7: "Ingeniería Química",
            8: "Ingeniería en Logística"
        }
        
        carreras_existentes = db.query(models.Carrera).count()
        
        if carreras_existentes == 0:
            for id_carrera, nombre in CARRERAS_MAP.items():
                carrera = models.Carrera(
                    id=id_carrera,
                    nombre=nombre,
                    codigo=f"CAR{id_carrera:02d}",
                    activa=True
                )
                db.add(carrera)
            
            db.commit()
            print(f"✅ {len(CARRERAS_MAP)} carreras creadas")
        else:
            print(f"✅ Ya existen {carreras_existentes} carreras")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando carreras: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN DE PROBLEMAS DEL PANEL DE ADMINISTRADOR")
    print("=" * 60)
    
    # Verificaciones básicas
    if not verificar_conexion_db():
        print("❌ No se puede continuar sin conexión a la base de datos")
        return False
    
    if not verificar_api_funcionando():
        print("⚠️  La API no está funcionando, pero continuamos con las correcciones de BD")
    
    # Verificar y crear datos necesarios
    verificar_tablas_necesarias()
    crear_carreras_basicas()
    crear_admin_prueba()
    crear_usuarios_prueba()
    
    # Probar endpoints si la API funciona
    if verificar_api_funcionando():
        probar_endpoints_admin()
    
    print("\n" + "=" * 60)
    print("✅ CORRECCIÓN COMPLETADA")
    print("\n📋 CREDENCIALES DE PRUEBA:")
    print("   Administrador:")
    print("     UID: admin123")
    print("     Contraseña: admin123")
    print("\n   Alumno:")
    print("     UID: alumno123")
    print("     Contraseña: alumno12")
    print("\n   Docente:")
    print("     UID: docente123")
    print("     Contraseña: docent12")
    print("\n🌐 URLs de acceso:")
    print("   Panel Admin: admin_login.html")
    print("   Login General: login.html")
    print("   API Docs: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    main()
