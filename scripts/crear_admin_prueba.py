#!/usr/bin/env python3
"""
Script para crear un administrador de prueba
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models
from passlib.hash import bcrypt
from datetime import datetime

def crear_admin_prueba():
    """Crear administrador de prueba"""
    print("🔧 Creando administrador de prueba...")
    
    # Crear sesión de base de datos
    db = Session(bind=engine)
    
    try:
        # Verificar si ya existe
        admin_existente = db.query(models.Usuario).filter(
            models.Usuario.uid == "admin123"
        ).first()
        
        if admin_existente:
            print("⚠️ Admin de prueba ya existe")
            print(f"   Nombre: {admin_existente.nombre}")
            print(f"   UID: {admin_existente.uid}")
            print(f"   Rol: {admin_existente.rol}")
            return
        
        # Crear nuevo admin
        contraseña_hash = bcrypt.hash("admin123")
        
        nuevo_admin = models.Usuario(
            uid="admin123",
            nombre="Administrador de Prueba",
            contraseña_hash=contraseña_hash,
            rol="admin",
            activo=True,
            fecha_registro=datetime.now()
        )
        
        db.add(nuevo_admin)
        db.commit()
        db.refresh(nuevo_admin)
        
        print("✅ Administrador de prueba creado exitosamente:")
        print(f"   UID: admin123")
        print(f"   Contraseña: admin123")
        print(f"   Nombre: {nuevo_admin.nombre}")
        print(f"   ID: {nuevo_admin.id}")
        
        # Crear también algunos usuarios de prueba
        crear_usuarios_prueba(db)
        
    except Exception as e:
        print(f"❌ Error creando admin: {e}")
        db.rollback()
    finally:
        db.close()

def crear_usuarios_prueba(db: Session):
    """Crear usuarios de prueba adicionales"""
    print("\n🔧 Creando usuarios de prueba adicionales...")
    
    usuarios_prueba = [
        {
            "uid": "alumno123",
            "nombre": "Alumno de Prueba",
            "contraseña": "alumno12",
            "rol": "alumno",
            "matricula": "2025001",
            "carrera": "Ingeniería en Sistemas Computacionales",
            "semestre": 2,
            "grupo": "2201"
        },
        {
            "uid": "docente123", 
            "nombre": "Docente de Prueba",
            "contraseña": "docent12",
            "rol": "docente",
            "clave_docente": "DOC001"
        }
    ]
    
    for usuario_data in usuarios_prueba:
        try:
            # Verificar si ya existe
            existente = db.query(models.Usuario).filter(
                models.Usuario.uid == usuario_data["uid"]
            ).first()
            
            if existente:
                print(f"⚠️ Usuario {usuario_data['uid']} ya existe")
                continue
            
            # Crear usuario
            contraseña_hash = bcrypt.hash(usuario_data["contraseña"])
            
            nuevo_usuario = models.Usuario(
                uid=usuario_data["uid"],
                nombre=usuario_data["nombre"],
                contraseña_hash=contraseña_hash,
                rol=usuario_data["rol"],
                matricula=usuario_data.get("matricula"),
                clave_docente=usuario_data.get("clave_docente"),
                carrera=usuario_data.get("carrera"),
                semestre=usuario_data.get("semestre"),
                grupo=usuario_data.get("grupo"),
                activo=True,
                fecha_registro=datetime.now()
            )
            
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)
            
            print(f"✅ Usuario creado: {usuario_data['uid']} / {usuario_data['contraseña']}")
            
        except Exception as e:
            print(f"❌ Error creando usuario {usuario_data['uid']}: {e}")
            db.rollback()

if __name__ == "__main__":
    crear_admin_prueba()
    print("\n🎯 Usuarios de prueba listos:")
    print("   Admin: admin123 / admin123")
    print("   Alumno: alumno123 / alumno12") 
    print("   Docente: docente123 / docent12")
    print("\n🌐 Acceder a: http://localhost:5500/frontend/admin_login.html")
