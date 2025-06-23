#!/usr/bin/env python3
"""
Script para ejecutar verificación completa del sistema
"""

import subprocess
import sys
import os
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar resultado"""
    print(f"\n🔧 {descripcion}")
    print(f"   Comando: {comando}")
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print(f"   ✅ Exitoso")
            if resultado.stdout:
                print(f"   📤 Salida:\n{resultado.stdout}")
            return True
        else:
            print(f"   ❌ Error (código: {resultado.returncode})")
            if resultado.stderr:
                print(f"   📤 Error:\n{resultado.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA RFID")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Cambiar al directorio del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    
    # Lista de comandos a ejecutar
    comandos = [
        ("python scripts/verificar_y_corregir_db.py", "Verificar y corregir base de datos"),
        ("python scripts/insert_alumnos_docentes_ejemplo.sql", "Insertar datos de ejemplo (si es necesario)"),
        ("python scripts/test_api_completo.py", "Probar API completo"),
        ("python scripts/verificar_base_datos.py", "Verificación final de base de datos")
    ]
    
    resultados = []
    
    for comando, descripcion in comandos:
        resultado = ejecutar_comando(comando, descripcion)
        resultados.append((descripcion, "✅ EXITOSO" if resultado else "❌ FALLIDO"))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN COMPLETA")
    print("=" * 60)
    
    for descripcion, resultado in resultados:
        print(f"{resultado} {descripcion}")
    
    exitosos = sum(1 for _, r in resultados if "✅" in r)
    total = len(resultados)
    
    print(f"\n🎯 Resultado: {exitosos}/{total} verificaciones exitosas")
    
    if exitosos == total:
        print("🎉 ¡Sistema completamente verificado y funcionando!")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Iniciar el servidor: python backend/app/main.py")
        print("   2. Abrir frontend: http://localhost:8000")
        print("   3. Usar credenciales de emergencia si es necesario:")
        print("      UID: ADMIN_EMERGENCY")
        print("      Contraseña: admin123")
    else:
        print("⚠️ Algunas verificaciones fallaron. Revisar logs arriba.")

if __name__ == "__main__":
    main()
