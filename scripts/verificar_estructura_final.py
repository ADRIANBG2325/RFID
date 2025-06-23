#!/usr/bin/env python3
"""
Script para verificar que la estructura de la base de datos esté correcta
"""

import mysql.connector
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',
    'database': 'control_asistencia',
    'charset': 'utf8mb4'
}

def verificar_estructura():
    """Verificar la estructura completa de la base de datos"""
    try:
        print("🔧 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("🔍 Verificando estructura de la base de datos...")
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        print(f"\n📊 Tablas encontradas: {len(tablas)}")
        for tabla in tablas:
            print(f"  📋 {tabla}")
        
        # Verificar estructura de tabla usuarios
        print("\n👥 Estructura de tabla 'usuarios':")
        cursor.execute("DESCRIBE usuarios")
        columnas_usuarios = cursor.fetchall()
        for columna in columnas_usuarios:
            print(f"  📝 {columna[0]} - {columna[1]} - {columna[2]} - {columna[3]}")
        
        # Verificar estructura de tabla docentes
        if 'docentes' in tablas:
            print("\n👨‍🏫 Estructura de tabla 'docentes':")
            cursor.execute("DESCRIBE docentes")
            columnas_docentes = cursor.fetchall()
            for columna in columnas_docentes:
                print(f"  📝 {columna[0]} - {columna[1]} - {columna[2]} - {columna[3]}")
        
        # Verificar estructura de tabla asignaciones_materias
        if 'asignaciones_materias' in tablas:
            print("\n📋 Estructura de tabla 'asignaciones_materias':")
            cursor.execute("DESCRIBE asignaciones_materias")
            columnas_asignaciones = cursor.fetchall()
            for columna in columnas_asignaciones:
                print(f"  📝 {columna[0]} - {columna[1]} - {columna[2]} - {columna[3]}")
        
        # Contar registros en cada tabla
        print("\n📊 Conteo de registros:")
        for tabla in tablas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"  📋 {tabla}: {count} registros")
            except mysql.connector.Error as e:
                print(f"  ❌ Error contando {tabla}: {e}")
        
        # Verificar usuarios por rol
        print("\n👥 Usuarios por rol:")
        cursor.execute("SELECT rol, COUNT(*) FROM usuarios GROUP BY rol")
        roles = cursor.fetchall()
        for rol, count in roles:
            print(f"  👤 {rol}: {count} usuarios")
        
        # Verificar claves foráneas
        print("\n🔗 Verificando claves foráneas:")
        cursor.execute("""
            SELECT 
                TABLE_NAME,
                COLUMN_NAME,
                CONSTRAINT_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE REFERENCED_TABLE_SCHEMA = 'control_asistencia'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        claves_foraneas = cursor.fetchall()
        for fk in claves_foraneas:
            print(f"  🔗 {fk[0]}.{fk[1]} -> {fk[3]}.{fk[4]}")
        
        cursor.close()
        connection.close()
        
        print("\n✅ VERIFICACIÓN COMPLETADA")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def main():
    """Función principal"""
    print("🔍" + "="*60)
    print("    VERIFICACIÓN DE ESTRUCTURA DE BASE DE DATOS")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    verificar_estructura()

if __name__ == "__main__":
    main()
