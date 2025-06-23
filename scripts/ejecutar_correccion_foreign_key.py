#!/usr/bin/env python3
"""
Script para corregir el constraint de foreign key en asignaciones_materias
"""

import mysql.connector
import sys
import os

def conectar_db():
    """Conectar a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='control_asistencia',
            user='root',
            password='',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None

def corregir_foreign_key(connection):
    """Corregir el constraint de foreign key"""
    cursor = connection.cursor()
    
    try:
        print("🔧 Corrigiendo constraint de foreign key...")
        
        # Eliminar constraint existente si existe
        print("1. Eliminando constraint existente...")
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'asignaciones_materias' 
            AND CONSTRAINT_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        constraints = cursor.fetchall()
        for constraint in constraints:
            constraint_name = constraint[0]
            print(f"   Eliminando constraint: {constraint_name}")
            cursor.execute(f"ALTER TABLE asignaciones_materias DROP FOREIGN KEY {constraint_name}")
        
        # Agregar el constraint correcto
        print("2. Agregando constraint correcto...")
        cursor.execute("""
            ALTER TABLE asignaciones_materias 
            ADD CONSTRAINT asignaciones_materias_docente_fk 
            FOREIGN KEY (docente_id) REFERENCES docentes_base(id) 
            ON DELETE CASCADE ON UPDATE CASCADE
        """)
        
        # Verificar que se aplicó correctamente
        print("3. Verificando constraint...")
        cursor.execute("""
            SELECT 
                CONSTRAINT_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'asignaciones_materias' 
            AND CONSTRAINT_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Constraint creado correctamente:")
            print(f"   Nombre: {result[0]}")
            print(f"   Columna: {result[1]}")
            print(f"   Tabla referenciada: {result[2]}")
            print(f"   Columna referenciada: {result[3]}")
        else:
            print("❌ No se pudo verificar el constraint")
            return False
        
        connection.commit()
        print("✅ Constraint de foreign key corregido exitosamente")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error corrigiendo foreign key: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def main():
    """Función principal"""
    print("🔧 Iniciando corrección de foreign key constraint...")
    
    # Conectar a la base de datos
    connection = conectar_db()
    if not connection:
        sys.exit(1)
    
    try:
        # Corregir foreign key
        if corregir_foreign_key(connection):
            print("✅ Corrección completada exitosamente")
            print("\n📋 Resumen:")
            print("   - Foreign key constraint corregido")
            print("   - Ahora referencia docentes_base en lugar de docentes")
            print("   - Las asignaciones de materias deberían funcionar correctamente")
        else:
            print("❌ Error en la corrección")
            sys.exit(1)
            
    finally:
        connection.close()

if __name__ == "__main__":
    main()
