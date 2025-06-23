#!/usr/bin/env python3
"""
Script para probar los endpoints de la API después de las correcciones
"""

import requests
import json
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://localhost:8000"
ADMIN_UID = "E950D8A2"  # UID del administrador

def test_endpoint(method, endpoint, data=None, params=None):
    """Probar un endpoint específico"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, params=params)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        elif method == "PATCH":
            response = requests.patch(url, json=data, params=params)
        
        print(f"  {method} {endpoint}")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ ÉXITO")
            try:
                result = response.json()
                if isinstance(result, list):
                    print(f"  📊 Resultados: {len(result)} elementos")
                elif isinstance(result, dict):
                    if 'mensaje' in result:
                        print(f"  💬 {result['mensaje']}")
            except:
                pass
        else:
            print("  ❌ ERROR")
            try:
                error = response.json()
                print(f"  💬 {error.get('detail', 'Error desconocido')}")
            except:
                print(f"  💬 Error HTTP {response.status_code}")
        
        print()
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ EXCEPCIÓN: {e}")
        print()
        return False

def main():
    """Función principal para probar todos los endpoints"""
    print("🧪" + "="*60)
    print("    PRUEBA DE ENDPOINTS DE LA API")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Base URL: {API_BASE_URL}")
    print(f"👤 Admin UID: {ADMIN_UID}")
    
    # Parámetros comunes
    admin_params = {"uid": ADMIN_UID}
    
    print("\n🔍 Probando endpoints de consulta...")
    
    # Endpoints de consulta
    endpoints_consulta = [
        ("GET", "/admin/semestre_actual", None, admin_params),
        ("GET", "/admin/carreras/", None, admin_params),
        ("GET", "/admin/docentes_base/", None, admin_params),
        ("GET", "/admin/alumnos_base/", None, admin_params),
        ("GET", "/admin/materias_asignadas/", None, admin_params),
        ("GET", "/admin/asistencias_docentes/", None, admin_params),
        ("GET", "/admin/estadisticas/asistencias_hoy", None, admin_params),
    ]
    
    exitos_consulta = 0
    for method, endpoint, data, params in endpoints_consulta:
        if test_endpoint(method, endpoint, data, params):
            exitos_consulta += 1
    
    print(f"📊 Consultas exitosas: {exitos_consulta}/{len(endpoints_consulta)}")
    
    print("\n➕ Probando endpoints de creación...")
    
    # Probar creación de docente
    docente_data = {
        "nombre": "Dr. Prueba Test",
        "clave": "TEST001",
        "especialidad": "Pruebas Automatizadas"
    }
    
    docente_creado = test_endpoint("POST", "/admin/docentes_base/", docente_data, admin_params)
    
    # Probar creación de alumno
    alumno_data = {
        "nombre": "Alumno Prueba",
        "matricula": "TEST2025001",
        "carrera": "Ingeniería en Sistemas Computacionales",
        "semestre": 2,
        "grupo": "Grupo 1"
    }
    
    alumno_creado = test_endpoint("POST", "/admin/alumnos_base/", alumno_data, admin_params)
    
    # Probar asignación de materia (si se creó el docente)
    if docente_creado:
        # Primero obtener el ID del docente creado
        response = requests.get(f"{API_BASE_URL}/admin/docentes_base/", params=admin_params)
        if response.status_code == 200:
            docentes = response.json()
            docente_test = next((d for d in docentes if d['clave'] == 'TEST001'), None)
            
            if docente_test:
                asignacion_data = {
                    "docente_id": docente_test['id'],
                    "materia_id": 48,  # Métodos Numéricos
                    "carrera_id": 3,   # Ingeniería en Sistemas Computacionales
                    "semestre": 4,
                    "grupo": "Grupo 1",
                    "dia_semana": "Lunes",
                    "hora_inicio": "08:00",
                    "hora_fin": "10:00",
                    "aula": "Lab-01"
                }
                
                print("📋 Probando asignación de materia...")
                test_endpoint("POST", "/admin/asignar_materia/", asignacion_data, admin_params)
    
    print("\n🧹 Limpiando datos de prueba...")
    
    # Limpiar datos de prueba
    if docente_creado:
        response = requests.get(f"{API_BASE_URL}/admin/docentes_base/", params=admin_params)
        if response.status_code == 200:
            docentes = response.json()
            docente_test = next((d for d in docentes if d['clave'] == 'TEST001'), None)
            if docente_test:
                test_endpoint("DELETE", f"/admin/docentes_base/{docente_test['id']}", None, admin_params)
    
    if alumno_creado:
        response = requests.get(f"{API_BASE_URL}/admin/alumnos_base/", params=admin_params)
        if response.status_code == 200:
            alumnos = response.json()
            alumno_test = next((a for a in alumnos if a['matricula'] == 'TEST2025001'), None)
            if alumno_test:
                test_endpoint("DELETE", f"/admin/alumnos_base/{alumno_test['id']}", None, admin_params)
    
    print("✅ PRUEBAS COMPLETADAS")
    print("\n📝 Si todas las pruebas fueron exitosas, la API está funcionando correctamente")

if __name__ == "__main__":
    main()
