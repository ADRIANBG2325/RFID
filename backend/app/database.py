from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de MariaDB/MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://User:12345678@localhost/control_asistencia"
)

# Crear engine con configuración optimizada para MariaDB
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para debug SQL
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "charset": "utf8mb4",
        "autocommit": False
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crear_tablas():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

# Alias para compatibilidad
create_tables = crear_tablas

def test_connection():
    """Probar conexión a la base de datos"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Conexión a MariaDB exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando a MariaDB: {e}")
        return False
