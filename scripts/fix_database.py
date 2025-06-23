#!/usr/bin/env python3
"""
Script para arreglar y migrar la base de datos existente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from backend.app.database import SQLALCHEMY_DATABASE_URL

def main():
    print("🔧 Iniciando migración de base de datos...")
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Leer y ejecutar el script de migración
            with open('scripts/migrate_database.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Dividir el script en comandos individuales
            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            
            for i, command in enumerate(commands):
                if command.upper().startswith(('CREATE', 'ALTER', 'INSERT', 'UPDATE')):
                    try:
                        print(f"Ejecutando comando {i+1}/{len(commands)}: {command[:50]}...")
                        conn.execute(text(command))
                        conn.commit()
                    except Exception as e:
                        print(f"⚠️  Advertencia en comando {i+1}: {str(e)}")
                        continue
            
            print("✅ Migración completada exitosamente!")
            
            # Verificar que las tablas existen
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Tablas disponibles: {', '.join(tables)}")
            
            # Verificar columnas de usuarios
            result = conn.execute(text("DESCRIBE usuarios"))
            columns = [row[0] for row in result.fetchall()]
            print(f"👤 Columnas en usuarios: {', '.join(columns)}")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
