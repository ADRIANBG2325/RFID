from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date, time

# Configuración base para Pydantic V2
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# ==================== SCHEMAS DE USUARIO ====================
class UsuarioBase(BaseSchema):
    uid: Optional[str] = None
    rol: str
    nombre: str
    matricula: Optional[str] = None
    clave_docente: Optional[str] = None
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    grupo: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    fecha_registro: datetime

class UsuarioLogin(BaseSchema):
    uid: str
    contraseña: str

# ==================== SCHEMAS DE CARRERA ====================
class CarreraBase(BaseSchema):
    nombre: str
    codigo: str

class CarreraCreate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id: int
    activa: bool

# ==================== SCHEMAS DE DOCENTE ====================
class DocenteBase(BaseSchema):
    nombre: str
    clave: str
    especialidad: Optional[str] = None

class DocenteCreate(DocenteBase):
    pass

class DocenteResponse(DocenteBase):
    id: int
    activo: bool

# ==================== SCHEMAS DE ALUMNO ====================
class AlumnoBase(BaseSchema):
    nombre: str
    matricula: str
    carrera: str
    semestre: int
    grupo: str

class AlumnoCreate(AlumnoBase):
    pass

class AlumnoResponse(AlumnoBase):
    id: int
    activo: bool
    fecha_registro: Optional[datetime] = None

# ==================== SCHEMAS DE ASIGNACIÓN DE MATERIA ====================
class AsignacionMateriaBase(BaseSchema):
    docente_id: int
    materia_id: int
    carrera_id: int
    semestre: int
    grupo: str
    dia_semana: str
    hora_inicio: time
    hora_fin: time
    aula: Optional[str] = None

class AsignacionMateriaCreate(AsignacionMateriaBase):
    pass

class AsignacionMateriaResponse(AsignacionMateriaBase):
    id: int
    docente_nombre: str
    nombre: str  # Nombre de la materia
    activa: bool

# ==================== SCHEMAS DE ASISTENCIA ====================
class AsistenciaBase(BaseSchema):
    alumno_id: int
    asignacion_id: int
    fecha: date
    hora_registro: time
    estado: str = "Presente"
    observaciones: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    pass

class AsistenciaResponse(AsistenciaBase):
    id: int
    alumno_nombre: str
    materia_nombre: str

# ==================== SCHEMAS DE RESPUESTA RFID ====================
class RFIDResponse(BaseSchema):
    success: bool
    message: str
    usuario: Optional[UsuarioResponse] = None
    accion: Optional[str] = None

# ==================== SCHEMAS DE ESTADÍSTICAS ====================
class EstadisticasResponse(BaseSchema):
    total_usuarios: int
    total_docentes: int
    total_alumnos: int
    asistencias_hoy: int
    fecha: date
