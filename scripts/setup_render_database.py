#!/usr/bin/env python3
"""
Script para configurar la base de datos de PostgreSQL en Render
"""
import os
import logging
from sqlalchemy import create_engine, text
from database import crear_tablas, crear_datos_iniciales

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL de tu base de datos en Render
DATABASE_URL = "postgresql://rfid_user:kCEZlaxvMEqBftLvcBJbFwo7EGhQohuj@dpg-d1clmfidbo4c73d02m80-a/rfid_db_xrv0"

def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"✅ Conexión exitosa a PostgreSQL")
            logger.info(f"📊 Versión: {version}")
            return True
    except Exception as e:
        logger.error(f"❌ Error conectando a la base de datos: {e}")
        return False

def setup_database():
    """Configurar la base de datos completa"""
    try:
        # Establecer la variable de entorno
        os.environ["DATABASE_URL"] = DATABASE_URL
        
        logger.info("🚀 Configurando base de datos en Render...")
        
        # Probar conexión
        if not test_connection():
            return False
        
        # Crear tablas
        logger.info("📋 Creando tablas...")
        crear_tablas()
        
        logger.info("✅ Base de datos configurada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error configurando base de datos: {e}")
        return False

def verify_setup():
    """Verificar que todo esté configurado correctamente"""
    try:
        engine = create_engine(DATABASE_URL)
        
        # Verificar tablas
        with engine.connect() as conn:
            tables = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)).fetchall()
            
            table_names = [table[0] for table in tables]
            logger.info(f"📋 Tablas encontradas: {table_names}")
            
            # Verificar datos iniciales
            carreras_count = conn.execute(text("SELECT COUNT(*) FROM carreras")).fetchone()[0]
            admin_count = conn.execute(text("SELECT COUNT(*) FROM administradores")).fetchone()[0]
            
            logger.info(f"🎓 Carreras: {carreras_count}")
            logger.info(f"👤 Administradores: {admin_count}")
            
            return len(table_names) > 0
            
    except Exception as e:
        logger.error(f"❌ Error verificando setup: {e}")
        return False

if __name__ == "__main__":
    logger.info("🔧 Iniciando configuración de base de datos para Render...")
    
    if setup_database():
        logger.info("✅ Configuración completada")
        
        if verify_setup():
            logger.info("✅ Verificación exitosa - Sistema listo para usar")
        else:
            logger.warning("⚠️ Verificación falló - revisar configuración")
    else:
        logger.error("❌ Configuración falló")
