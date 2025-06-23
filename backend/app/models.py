from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(100), unique=True, index=True)
    rol = Column(String(50))
    nombre = Column(String(100))
    matricula = Column(String(100), nullable=True)
    clave_docente = Column(String(100), nullable=True)
    carrera = Column(String(100), nullable=True)
    semestre = Column(Integer, nullable=True)
    grupo = Column(String(10), nullable=True)
    contraseña_hash = Column(String(255))
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    docente = relationship("Docente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    asistencias_alumno = relationship("Asistencia", foreign_keys="[Asistencia.alumno_id]", back_populates="alumno", cascade="all, delete-orphan")

class Carrera(Base):
    __tablename__ = "carreras"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    activa = Column(Boolean, default=True)
    
    # Relaciones - REMOVEMOS la relación con materias ya que usamos mapeo estático
    docente_carreras = relationship("DocenteCarrera", back_populates="carrera", cascade="all, delete-orphan")

# REMOVEMOS la clase Materia ya que usamos mapeo estático
# class Materia - NO LA NECESITAMOS

class Docente(Base):
    __tablename__ = "docentes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="docente")
    carreras = relationship("DocenteCarrera", back_populates="docente", cascade="all, delete-orphan")
    asignaciones = relationship("AsignacionMateria", back_populates="docente", cascade="all, delete-orphan")

class DocenteCarrera(Base):
    __tablename__ = "docente_carreras"
    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"))
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    activa = Column(Boolean, default=True)
    
    # Relaciones
    docente = relationship("Docente", back_populates="carreras")
    carrera = relationship("Carrera", back_populates="docente_carreras")

# CORREGIDO: AsignacionMateria sin relación problemática con Materia
class AsignacionMateria(Base):
    __tablename__ = "asignaciones_materias"
    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"))
    materia_id = Column(Integer)  # ID de materia del mapeo estático, NO ForeignKey
    carrera_id = Column(Integer)  # ID de carrera del mapeo estático
    semestre = Column(Integer)    # Semestre de la materia
    grupo = Column(String(20), nullable=False)
    dia_semana = Column(String(20), nullable=False)  # Lunes, Martes, etc.
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    aula = Column(String(50), nullable=True)
    activa = Column(Boolean, default=True)
    
    # Relaciones - SOLO con docente, NO con materia
    docente = relationship("Docente", back_populates="asignaciones")
    asistencias = relationship("Asistencia", back_populates="asignacion", cascade="all, delete-orphan")

class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("usuarios.id"))
    asignacion_id = Column(Integer, ForeignKey("asignaciones_materias.id"))
    fecha = Column(Date, nullable=False)
    hora_registro = Column(Time, nullable=False)
    estado = Column(String(20), default="Presente")  # Presente, Ausente, Tardanza, Justificado
    observaciones = Column(Text, nullable=True)
    
    # Relaciones
    alumno = relationship("Usuario", foreign_keys=[alumno_id], back_populates="asistencias_alumno")
    asignacion = relationship("AsignacionMateria", back_populates="asistencias")

# Tabla base para alumnos (datos previos)
class AlumnoBase(Base):
    __tablename__ = "alumnos_base"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    matricula = Column(String(100), unique=True, nullable=False)
    carrera = Column(String(100), nullable=False)
    semestre = Column(Integer, nullable=False)
    grupo = Column(String(10), nullable=False)
    activo = Column(Boolean, default=True)

# Tabla base para docentes (datos previos)
class DocenteBase(Base):
    __tablename__ = "docentes_base"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    clave = Column(String(100), unique=True, nullable=False)
    especialidad = Column(String(200), nullable=True)
    activo = Column(Boolean, default=True)

# Tabla para grupos específicos
class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, nullable=False)  # Ej: 3402
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    semestre = Column(Integer, nullable=False)
    numero_grupo = Column(Integer, nullable=False)  # 1, 2, 3, 4
    activo = Column(Boolean, default=True)
    
    # Relaciones
    carrera = relationship("Carrera")
