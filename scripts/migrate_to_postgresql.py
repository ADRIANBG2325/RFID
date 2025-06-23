#!/usr/bin/env python3
"""
Script para migrar datos existentes de SQLite a PostgreSQL en Render
"""
import sqlite3
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Usuario, Administrador, Carrera, Materia, Asistencia, Base

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URLs de bases de datos
SQLITE_DB = "rfid_system.db"  # Tu base de datos local actual
POSTGRESQL_URL = "postgresql://rfid_user:kCEZlaxvMEqBftLvcBJbFwo7EGhQohuj@dpg-d1clmfidbo4c73d02m80-a/rfid_db_xrv0"

def migrate_data():
    """Migrar datos de SQLite a PostgreSQL"""
    try:
        # Conectar a PostgreSQL
        pg_engine = create_engine(POSTGRESQL_URL)
        Base.metadata.create_all(bind=pg_engine)
        PgSession = sessionmaker(bind=pg_engine)
        pg_session = PgSession()
        
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_conn.row_factory = sqlite3.Row
        cursor = sqlite_conn.cursor()
        
        logger.info("🚀 Iniciando migración de datos...")
        
        # Migrar carreras
        logger.info("🎓 Migrando carreras...")
        cursor.execute("SELECT * FROM carreras")
        carreras_data = cursor.fetchall()
        
        for row in carreras_data:
            carrera = Carrera(
                id=row['id'],
                nombre=row['nombre'],
                codigo=row['codigo'],
                activa=bool(row['activa'])
            )
            pg_session.merge(carrera)
        
        # Migrar administradores
        logger.info("👤 Migrando administradores...")
        cursor.execute("SELECT * FROM administradores")
        admin_data = cursor.fetchall()
        
        for row in admin_data:
            admin = Administrador(
                id=row['id'],
                uid=row['uid'],
                nombre=row['nombre'],
                email=row['email'],
                activo=bool(row['activo'])
            )
            pg_session.merge(admin)
        
        # Migrar usuarios
        logger.info("👥 Migrando usuarios...")
        cursor.execute("SELECT * FROM usuarios")
        usuarios_data = cursor.fetchall()
        
        for row in usuarios_data:
            usuario = Usuario(
                id=row['id'],
                uid=row['uid'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                rol=row['rol'],
                carrera_id=row['carrera_id'],
                activo=bool(row['activo'])
            )
            pg_session.merge(usuario)
        
        # Migrar materias
        logger.info("📚 Migrando materias...")
        try:
            cursor.execute("SELECT * FROM materias")
            materias_data = cursor.fetchall()
            
            for row in materias_data:
                materia = Materia(
                    id=row['id'],
                    nombre=row['nombre'],
                    codigo=row['codigo'],
                    carrera_id=row['carrera_id'],
                    docente_id=row.get('docente_id'),
                    activa=bool(row['activa'])
                )
                pg_session.merge(materia)
        except sqlite3.OperationalError:
            logger.warning("⚠️ Tabla materias no encontrada en SQLite")
        
        # Migrar asistencias
        logger.info("📋 Migrando asistencias...")
        try:
            cursor.execute("SELECT * FROM asistencias")
            asistencias_data = cursor.fetchall()
            
            for row in asistencias_data:
                asistencia = Asistencia(
                    id=row['id'],
                    usuario_id=row['usuario_id'],
                    materia_id=row.get('materia_id'),
                    tipo=row.get('tipo', 'entrada')
                )
                pg_session.merge(asistencia)
        except sqlite3.OperationalError:
            logger.warning("⚠️ Tabla asistencias no encontrada en SQLite")
        
        # Confirmar cambios
        pg_session.commit()
        logger.info("✅ Migración completada exitosamente")
        
        # Cerrar conexiones
        sqlite_conn.close()
        pg_session.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en migración: {e}")
        if 'pg_session' in locals():
            pg_session.rollback()
            pg_session.close()
        return False

def verify_migration():
    """Verificar que la migración fue exitosa"""
    try:
        engine = create_engine(POSTGRESQL_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Contar registros
        carreras_count = session.query(Carrera).count()
        usuarios_count = session.query(Usuario).count()
        admin_count = session.query(Administrador).count()
        
        logger.info("📊 Verificación de migración:")
        logger.info(f"   🎓 Carreras: {carreras_count}")
        logger.info(f"   👥 Usuarios: {usuarios_count}")
        logger.info(f"   👤 Administradores: {admin_count}")
        
        session.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error verificando migración: {e}")
        return False

if __name__ == "__main__":
    import os
    
    if not os.path.exists(SQLITE_DB):
        logger.error(f"❌ Base de datos SQLite no encontrada: {SQLITE_DB}")
        exit(1)
    
    logger.info("🔄 Iniciando migración SQLite → PostgreSQL...")
    
    if migrate_data():
        logger.info("✅ Migración exitosa")
        verify_migration()
    else:
        logger.error("❌ Migración falló")
