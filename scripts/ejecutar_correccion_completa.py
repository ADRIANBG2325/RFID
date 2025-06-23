#!/usr/bin/env python3
"""
Script para ejecutar la corrección completa de la base de datos
"""

import mysql.connector
import sys
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',
    'database': 'control_asistencia',
    'charset': 'utf8mb4'
}

def ejecutar_script_sql():
    """Ejecutar el script SQL de corrección"""
    try:
        print("🔧 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("📋 Ejecutando correcciones de estructura...")
        
        # Leer y ejecutar el script SQL
        with open('scripts/fix_database_structure_complete.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Dividir en comandos individuales
        commands = sql_script.split(';')
        
        for i, command in enumerate(commands):
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"  ✅ Comando {i+1} ejecutado")
                except mysql.connector.Error as e:
                    if "already exists" in str(e) or "Duplicate" in str(e):
                        print(f"  ⚠️ Comando {i+1}: {e} (ignorado)")
                    else:
                        print(f"  ❌ Error en comando {i+1}: {e}")
        
        connection.commit()
        print("✅ Correcciones aplicadas exitosamente")
        
        # Verificar estructura
        print("\n🔍 Verificando estructura corregida...")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📊 Tablas encontradas: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📋 {table_name}: {count} registros")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Base de datos corregida exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando correcciones: {e}")
        return False

def main():
    """Función principal"""
    print("🚀" + "="*60)
    print("    CORRECCIÓN COMPLETA DE LA BASE DE DATOS")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if ejecutar_script_sql():
        print("\n✅ CORRECCIÓN COMPLETADA")
        print("\n📝 Próximos pasos:")
        print("1. Reiniciar el servidor FastAPI")
        print("2. Probar las funciones del panel de administración")
        print("3. Verificar que no hay errores HTTP 500")
    else:
        print("\n❌ CORRECCIÓN FALLIDA")
        sys.exit(1)

if __name__ == "__main__":
    main()
