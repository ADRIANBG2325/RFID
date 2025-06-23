#!/usr/bin/env python3
"""
Script para verificar el estado del Sistema de Control de Asistencias RFID
"""

import mysql.connector
from mysql.connector import Error
import requests
import time

def verificar_base_datos():
    """Verificar conexión y datos en la base de datos"""
    print("🔍 VERIFICANDO BASE DE DATOS...")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='asistencias_rfid'
        )
        cursor = connection.cursor()
        
        # Verificar tablas principales
        tablas = ['carreras', 'materias', 'alumnos_base', 'docentes_base', 'usuarios']
        for tabla in tablas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"  ✅ {tabla}: {count} registros")
            except Error as e:
                print(f"  ❌ {tabla}: Error - {e}")
        
        # Verificar datos específicos
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = TRUE")
        carreras = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM materias WHERE activa = TRUE")
        materias = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = TRUE")
        alumnos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = TRUE")
        docentes = cursor.fetchone()[0]
        
        print(f"\n📊 RESUMEN DE DATOS:")
        print(f"  🎓 Carreras activas: {carreras}")
        print(f"  📚 Materias activas: {materias}")
        print(f"  👨‍🎓 Alumnos disponibles: {alumnos}")
        print(f"  👨‍🏫 Docentes disponibles: {docentes}")
        
        if carreras > 0 and materias > 0 and alumnos > 0 and docentes > 0:
            print("  ✅ Base de datos configurada correctamente")
            return True
        else:
            print("  ⚠️  Faltan datos en la base de datos")
            return False
            
    except Error as e:
        print(f"  ❌ Error de conexión: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def verificar_backend():
    """Verificar que el backend esté funcionando"""
    print("\n🔍 VERIFICANDO BACKEND...")
    
    try:
        # Intentar conectar al backend
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("  ✅ Backend respondiendo en http://localhost:8000")
            
            # Verificar endpoints principales
            endpoints = [
                "/usuarios/",
                "/admin/carreras/",
                "/admin/estadisticas/"
            ]
            
            for endpoint in endpoints:
                try:
                    resp = requests.get(f"http://localhost:8000{endpoint}", timeout=3)
                    if resp.status_code in [200, 422]:  # 422 es esperado sin parámetros
                        print(f"    ✅ {endpoint}: OK")
                    else:
                        print(f"    ⚠️  {endpoint}: Status {resp.status_code}")
                except:
                    print(f"    ❌ {endpoint}: No responde")
            
            return True
        else:
            print(f"  ❌ Backend responde con status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ❌ Backend no está ejecutándose")
        print("  💡 Ejecutar: cd backend && python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"  ❌ Error verificando backend: {e}")
        return False

def verificar_archivos():
    """Verificar que existan los archivos necesarios"""
    print("\n🔍 VERIFICANDO ARCHIVOS...")
    
    archivos_criticos = [
        "backend/app/main.py",
        "backend/app/models.py",
        "backend/app/database.py",
        "backend/app/routers/usuarios.py",
        "backend/app/routers/admin.py",
        "frontend/index.html",
        "frontend/admin_panel.html",
        "frontend/admin_login.html",
        "frontend/admin_registro.html",
        "db.sql"
    ]
    
    archivos_ok = 0
    for archivo in archivos_criticos:
        try:
            with open(archivo, 'r'):
                print(f"  ✅ {archivo}")
                archivos_ok += 1
        except FileNotFoundError:
            print(f"  ❌ {archivo}: No encontrado")
    
    print(f"\n📁 Archivos verificados: {archivos_ok}/{len(archivos_criticos)}")
    return archivos_ok == len(archivos_criticos)

def main():
    print("🔍 VERIFICACIÓN DEL SISTEMA DE ASISTENCIAS RFID")
    print("=" * 50)
    
    # Verificaciones
    db_ok = verificar_base_datos()
    archivos_ok = verificar_archivos()
    backend_ok = verificar_backend()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE VERIFICACIÓN:")
    print(f"  Base de datos: {'✅ OK' if db_ok else '❌ ERROR'}")
    print(f"  Archivos:      {'✅ OK' if archivos_ok else '❌ ERROR'}")
    print(f"  Backend:       {'✅ OK' if backend_ok else '❌ ERROR'}")
    
    if db_ok and archivos_ok and backend_ok:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("\n🚀 ACCESOS RÁPIDOS:")
        print("  • Frontend: file:///[ruta]/frontend/index.html")
        print("  • Admin Panel: file:///[ruta]/frontend/admin_login.html")
        print("  • Registro Admin: file:///[ruta]/frontend/admin_registro.html")
        print("  • Backend API: http://localhost:8000")
        print("  • Documentación API: http://localhost:8000/docs")
    else:
        print("\n⚠️  SISTEMA REQUIERE CONFIGURACIÓN")
        print("\n🔧 PASOS PARA SOLUCIONAR:")
        if not db_ok:
            print("  1. Ejecutar: python scripts/setup_completo_sistema.py")
        if not backend_ok:
            print("  2. Ejecutar: cd backend && python -m uvicorn app.main:app --reload")
        if not archivos_ok:
            print("  3. Verificar que todos los archivos estén presentes")

if __name__ == "__main__":
    main()
