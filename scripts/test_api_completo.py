#!/usr/bin/env python3
"""
Script completo para verificar el 100% de funcionamiento del API
"""

import requests
import json
import time
from datetime import datetime

# Configuración del servidor
BASE_URL = "http://localhost:8000"

def test_health():
    """Verificar que el servidor esté funcionando"""
    print("🔍 Verificando estado del servidor...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servidor funcionando: {data['message']}")
            print(f"   Clientes conectados: {data.get('connected_clients', 0)}")
            return True
        else:
            print(f"❌ Servidor no responde correctamente: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_verificar_uid():
    """Probar verificación de UID"""
    print("\n🔍 Probando verificación de UID...")
    
    # UID de prueba
    test_uid = "TEST123456"
    
    try:
        response = requests.post(
            f"{BASE_URL}/usuarios/verificar_uid/",
            json={"uid": test_uid}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Verificación UID exitosa: {data}")
            return data
        else:
            print(f"❌ Error verificando UID: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en verificación UID: {e}")
        return None

def test_consultar_alumno():
    """Probar consulta de alumno"""
    print("\n🔍 Probando consulta de alumno...")
    
    # Matrícula de prueba (debe existir en alumnos_base)
    matricula_test = "20240001"
    
    try:
        response = requests.get(f"{BASE_URL}/usuarios/consultar_alumno/{matricula_test}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Consulta alumno exitosa: {data}")
            return data
        else:
            print(f"❌ Error consultando alumno: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en consulta alumno: {e}")
        return None

def test_consultar_docente():
    """Probar consulta de docente"""
    print("\n🔍 Probando consulta de docente...")
    
    # Clave de prueba (debe existir en docentes_base)
    clave_test = "DOC001"
    
    try:
        response = requests.get(f"{BASE_URL}/usuarios/consultar_docente/{clave_test}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Consulta docente exitosa: {data}")
            return data
        else:
            print(f"❌ Error consultando docente: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en consulta docente: {e}")
        return None

def test_registro_alumno():
    """Probar registro de alumno"""
    print("\n🔍 Probando registro de alumno...")
    
    # Datos de prueba
    uid_test = f"ALUMNO_TEST_{int(time.time())}"
    
    payload = {
        "uid": uid_test,
        "rol": "alumno",
        "identificador": "20240001",  # Matrícula que debe existir
        "contraseña": "test1234",
        "confirmar_contraseña": "test1234",
        "datos_usuario": {}
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/usuarios/registrar/",
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registro alumno exitoso: {data}")
            return data
        else:
            print(f"❌ Error registrando alumno: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error en registro alumno: {e}")
        return None

def test_registro_admin():
    """Probar registro de administrador"""
    print("\n🔍 Probando registro de administrador...")
    
    # Datos de prueba
    uid_test = f"ADMIN_TEST_{int(time.time())}"
    
    payload = {
        "uid_o_username": uid_test,
        "nombre_usuario": f"admin_test_{int(time.time())}",
        "nombre_completo": "Administrador de Prueba",
        "clave_secreta": "SOLDADORES",
        "contraseña": "admin123",
        "confirmar_contraseña": "admin123",
        "tipo_registro": "tarjeta"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/usuarios/registrar_admin/",
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registro admin exitoso: {data}")
            return data
        else:
            print(f"❌ Error registrando admin: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error en registro admin: {e}")
        return None

def test_login():
    """Probar login con usuario existente"""
    print("\n🔍 Probando login...")
    
    # Primero crear un usuario de prueba
    uid_test = f"LOGIN_TEST_{int(time.time())}"
    
    # Registrar usuario
    payload_registro = {
        "uid": uid_test,
        "rol": "alumno",
        "identificador": "20240001",
        "contraseña": "test1234",
        "confirmar_contraseña": "test1234",
        "datos_usuario": {}
    }
    
    try:
        # Registrar
        response_registro = requests.post(
            f"{BASE_URL}/usuarios/registrar/",
            json=payload_registro
        )
        
        if response_registro.status_code == 200:
            print("✅ Usuario de prueba registrado")
            
            # Intentar login
            payload_login = {
                "uid": uid_test,
                "contraseña": "test1234"
            }
            
            response_login = requests.post(
                f"{BASE_URL}/usuarios/login/",
                json=payload_login
            )
            
            print(f"Login Status Code: {response_login.status_code}")
            print(f"Login Response: {response_login.text}")
            
            if response_login.status_code == 200:
                data = response_login.json()
                print(f"✅ Login exitoso: {data}")
                return data
            else:
                print(f"❌ Error en login: {response_login.status_code}")
                return None
        else:
            print(f"❌ No se pudo registrar usuario de prueba: {response_registro.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error en test de login: {e}")
        return None

def test_admin_endpoints():
    """Probar endpoints de administrador"""
    print("\n🔍 Probando endpoints de administrador...")
    
    # Crear admin de prueba primero
    uid_admin = f"ADMIN_ENDPOINT_TEST_{int(time.time())}"
    
    payload_admin = {
        "uid_o_username": uid_admin,
        "nombre_usuario": f"admin_endpoint_{int(time.time())}",
        "nombre_completo": "Admin Endpoint Test",
        "clave_secreta": "SOLDADORES",
        "contraseña": "admin123",
        "confirmar_contraseña": "admin123",
        "tipo_registro": "tarjeta"
    }
    
    try:
        # Registrar admin
        response_admin = requests.post(
            f"{BASE_URL}/usuarios/registrar_admin/",
            json=payload_admin
        )
        
        if response_admin.status_code == 200:
            print("✅ Admin de prueba registrado")
            
            # Probar endpoints de admin
            endpoints_admin = [
                f"/admin/carreras/?uid={uid_admin}",
                f"/admin/usuarios/?uid={uid_admin}",
                f"/admin/estadisticas/?uid={uid_admin}"
            ]
            
            for endpoint in endpoints_admin:
                try:
                    response = requests.get(f"{BASE_URL}{endpoint}")
                    print(f"  {endpoint}: {response.status_code}")
                    if response.status_code != 200:
                        print(f"    Error: {response.text}")
                except Exception as e:
                    print(f"  {endpoint}: Error - {e}")
                    
        else:
            print(f"❌ No se pudo registrar admin de prueba: {response_admin.status_code}")
            
    except Exception as e:
        print(f"❌ Error en test de admin endpoints: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA COMPLETA DEL API - SISTEMA RFID")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Health Check", test_health),
        ("Verificar UID", test_verificar_uid),
        ("Consultar Alumno", test_consultar_alumno),
        ("Consultar Docente", test_consultar_docente),
        ("Registro Alumno", test_registro_alumno),
        ("Registro Admin", test_registro_admin),
        ("Login", test_login),
        ("Admin Endpoints", test_admin_endpoints)
    ]
    
    resultados = {}
    
    for nombre, test_func in tests:
        print(f"\n{'='*20} {nombre} {'='*20}")
        try:
            resultado = test_func()
            resultados[nombre] = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
            resultados[nombre] = "❌ ERROR"
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for nombre, resultado in resultados.items():
        print(f"{resultado} {nombre}")
    
    exitosos = sum(1 for r in resultados.values() if "✅" in r)
    total = len(resultados)
    
    print(f"\n🎯 Resultado: {exitosos}/{total} pruebas exitosas")
    
    if exitosos == total:
        print("🎉 ¡Todas las pruebas pasaron!")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar logs arriba.")

if __name__ == "__main__":
    main()
