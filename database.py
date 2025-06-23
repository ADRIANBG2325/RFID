import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rfid_user:kCEZlaxvMEqBftLvcBJbFwo7EGhQohuj@dpg-d1clmfidbo4c73d02m80-a/rfid_db_xrv0")

if not DATABASE_URL:
    # Fallback para desarrollo local
    DATABASE_URL = "sqlite:///./rfid_system.db"
    logger.warning("Usando SQLite para desarrollo local")
else:
    logger.info("✅ Usando PostgreSQL de Render")

# Ajustar URL para PostgreSQL en Render
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de base de datos
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(50), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    rol = Column(String(20), nullable=False)  # 'alumno' o 'docente'
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="usuarios")
    asistencias = relationship("Asistencia", back_populates="usuario")

class Administrador(Base):
    __tablename__ = "administradores"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(50), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

class Carrera(Base):
    __tablename__ = "carreras"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True, index=True)
    activa = Column(Boolean, default=True)
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="carrera")
    materias = relationship("Materia", back_populates="carrera")

class Materia(Base):
    __tablename__ = "materias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True, index=True)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    docente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    activa = Column(Boolean, default=True)
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="materias")
    docente = relationship("Usuario", foreign_keys=[docente_id])
    asistencias = relationship("Asistencia", back_populates="materia")

class Asistencia(Base):
    __tablename__ = "asistencias"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    tipo = Column(String(20), default="entrada")  # 'entrada' o 'salida'
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="asistencias")
    materia = relationship("Materia", back_populates="asistencias")

def crear_tablas():
    """Crear todas las tablas en la base de datos"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
        
        # Crear datos iniciales si no existen
        crear_datos_iniciales()
        
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")

def crear_datos_iniciales():
    """Crear datos iniciales para el sistema"""
    db = SessionLocal()
    try:
        # Verificar si ya existen datos
        if db.query(Carrera).count() == 0:
            # Crear carreras
            carreras = [
                Carrera(nombre="Ingeniería en Sistemas", codigo="ISI"),
                Carrera(nombre="Ingeniería Industrial", codigo="IIN"),
                Carrera(nombre="Administración de Empresas", codigo="ADE"),
            ]
            db.add_all(carreras)
            db.commit()
            logger.info("✅ Carreras iniciales creadas")
        
        # Crear administrador por defecto si no existe
        if db.query(Administrador).count() == 0:
            admin = Administrador(
                uid="ADMIN001",
                nombre="Administrador Sistema",
                email="admin@sistema.com"
            )
            db.add(admin)
            db.commit()
            logger.info("✅ Administrador por defecto creado")
            
    except Exception as e:
        logger.error(f"❌ Error creando datos iniciales: {e}")
        db.rollback()
    finally:
        db.close()

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
