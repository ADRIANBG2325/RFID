#!/usr/bin/env python3
"""
Script para verificar que todas las importaciones funcionen correctamente
"""

import sys
import os

# Agregar el directorio backend al path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

def verificar_importaciones():
    """Verificar que todas las importaciones funcionen"""
    try:
        print("🔍 Verificando importaciones...")
        
        # Verificar database
        print("📊 Verificando app.database...")
        from app.database import crear_tablas, get_db, test_connection
        print("✅ app.database importado correctamente")
        
        # Verificar models
        print("📋 Verificando app.models...")
        from app.models import Usuario, DocenteBase, AlumnoBase, Materia, Asistencia
        print("✅ app.models importado correctamente")
        
        # Verificar schemas
        print("📝 Verificando app.schemas...")
        from app.schemas import UsuarioCreate, UsuarioResponse, DocenteCreate, AlumnoCreate
        print("✅ app.schemas importado correctamente")
        
        # Verificar routers
        print("🛣️ Verificando routers...")
        from app.routers import usuarios, asistencias, materias, admin
        print("✅ Todos los routers importados correctamente")
        
        # Verificar main
        print("🚀 Verificando app.main...")
        from app.main import app
        print("✅ app.main importado correctamente")
        
        print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verificar_conexion_db():
    """Verificar conexión a la base de datos"""
    try:
        print("\n🔌 Verificando conexión a MariaDB...")
        from app.database import test_connection
        
        if test_connection():
            print("✅ Conexión a MariaDB exitosa")
            return True
        else:
            print("❌ Error conectando a MariaDB")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando conexión: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🔧 VERIFICACIÓN DEL SISTEMA")
    print("=" * 60)
    
    # Verificar importaciones
    importaciones_ok = verificar_importaciones()
    
    # Verificar conexión DB
    conexion_ok = verificar_conexion_db()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    print(f"Importaciones: {'✅ OK' if importaciones_ok else '❌ ERROR'}")
    print(f"Conexión DB:   {'✅ OK' if conexion_ok else '❌ ERROR'}")
    
    if importaciones_ok and conexion_ok:
        print("\n🎉 ¡Sistema listo para ejecutar!")
        print("\n🚀 Para iniciar el servidor:")
        print("   cd backend")
        print("   uvicorn app.main:app_sio --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n⚠️ Hay problemas que necesitan ser resueltos")
    
    return importaciones_ok and conexion_ok

if __name__ == "__main__":
    main()
