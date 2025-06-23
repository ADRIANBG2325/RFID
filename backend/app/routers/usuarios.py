from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
from passlib.hash import bcrypt
import re
import logging
from datetime import datetime, time
from datetime import timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MAPEO CORRECTO DE CARRERAS
CARRERAS_MAP = {
   1: "Ingeniería Industrial",
   2: "Ingeniería en Tecnologías de la Información y Comunicaciones", 
   3: "Ingeniería en Sistemas Computacionales",
   4: "Ingeniería Mecatrónica",
   5: "Ingeniería Civil",
   6: "Licenciatura en Administración",
   7: "Ingeniería Química",
   8: "Ingeniería en Logística"
}

def validar_contraseña(contraseña: str) -> dict:
   """Validar contraseña según los criterios establecidos"""
   errores = []
   
   if len(contraseña) != 8:
       errores.append(f"La contraseña debe tener exactamente 8 caracteres (actual: {len(contraseña)})")
   
   if not re.search(r'\d', contraseña):
       errores.append("La contraseña debe contener al menos un número")
   
   if not re.search(r'[a-zA-Z]', contraseña):
       errores.append("La contraseña debe contener al menos una letra")
   
   if ' ' in contraseña:
       errores.append("La contraseña no debe contener espacios")
   
   return {
       "valida": len(errores) == 0,
       "errores": errores
   }

def obtener_semestre_actual():
    """Determinar el semestre actual basado en las fechas corregidas"""
    ahora = datetime.now()
    mes = ahora.month
    dia = ahora.day
    año = ahora.year
    
    # Semestre 1: Febrero a Julio (2025-1) - Solo semestres pares
    # Semestre 2: Agosto a Febrero del siguiente año (2025-2) - Solo semestres impares
    
    if (mes == 2 and dia >= 1) or (mes >= 3 and mes <= 7):
        # Semestre 1: Febrero - Julio
        return {
            "numero": 1,
            "codigo": f"{año}-1",
            "nombre": f"Semestre {año}-1",
            "semestres_permitidos": [2, 4, 6, 8]  # Solo semestres pares
        }
    elif mes >= 8 or mes <= 1:
        # Semestre 2: Agosto - Febrero del siguiente año
        año_semestre = año if mes >= 8 else año - 1
        return {
            "numero": 2,
            "codigo": f"{año_semestre}-2",
            "nombre": f"Semestre {año_semestre}-2",
            "semestres_permitidos": [1, 3, 5, 7, 9]  # Solo semestres impares
        }
    
    # Período de transición
    return {
        "numero": 0,
        "codigo": "Transición",
        "nombre": "Período de Transición",
        "semestres_permitidos": []
    }

def verificar_horario_alumno(usuario_id: int, db: Session) -> dict:
    """Verificar si el alumno puede iniciar sesión según su horario de clases"""
    try:
        ahora = datetime.now()
        hora_actual = ahora.time()
        dia_actual = ahora.strftime("%A")
        
        # Mapear días al español
        dias_map = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }
        dia_espanol = dias_map.get(dia_actual, dia_actual)
        
        # Obtener el grupo del alumno
        usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if not usuario or not usuario.grupo:
            return {"puede_acceder": True, "mensaje": "Sin restricciones de horario"}
        
        # Buscar clases del alumno en el día actual
        query = text("""
            SELECT am.hora_inicio, am.hora_fin, m.nombre as materia_nombre
            FROM asignaciones_materias am
            JOIN materias m ON am.materia_id = m.id
            WHERE am.grupo = :grupo 
            AND am.dia_semana = :dia
            AND am.activa = TRUE
            ORDER BY am.hora_inicio
        """)
        
        result = db.execute(query, {
            "grupo": usuario.grupo,
            "dia": dia_espanol
        })
        
        clases_hoy = result.fetchall()
        
        if not clases_hoy:
            return {"puede_acceder": True, "mensaje": "No tiene clases hoy"}
        
        # Verificar cada clase
        for clase in clases_hoy:
            hora_inicio, hora_fin, materia = clase
            
            # Calcular ventana de restricción: desde inicio de clase hasta 15 minutos después
            inicio_restriccion = hora_inicio
            fin_restriccion = (datetime.combine(ahora.date(), hora_inicio) + 
                             timedelta(minutes=15)).time()
            
            # Verificar si está en período de restricción
            if inicio_restriccion <= hora_actual <= fin_restriccion:
                return {
                    "puede_acceder": False,
                    "mensaje": f"No puede acceder durante la clase de {materia} ({hora_inicio.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}). Intente después de las {fin_restriccion.strftime('%H:%M')}",
                    "clase_actual": {
                        "materia": materia,
                        "hora_inicio": hora_inicio.strftime('%H:%M'),
                        "hora_fin": hora_fin.strftime('%H:%M'),
                        "puede_acceder_despues": fin_restriccion.strftime('%H:%M')
                    }
                }
        
        return {"puede_acceder": True, "mensaje": "Fuera del horario de clases"}
        
    except Exception as e:
        logger.error(f"Error verificando horario del alumno: {e}")
        # En caso de error, permitir acceso para no bloquear al usuario
        return {"puede_acceder": True, "mensaje": "Error verificando horario, acceso permitido"}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verificando contraseña: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

@router.post("/login")
async def login_usuario(
    login_data: dict,
    db: Session = Depends(get_db)
):
    """Autenticar usuario (alumno, docente o admin)"""
    try:
        uid = login_data.get("uid")
        password = login_data.get("password", "")
        
        if not uid:
            raise HTTPException(
                status_code=400,
                detail="UID es requerido"
            )
        
        logger.info(f"Intento de login para UID: {uid}")
        
        # Buscar usuario por UID
        usuario = db.query(models.Usuario).filter(
            models.Usuario.uid == uid,
            models.Usuario.activo == True
        ).first()
        
        if not usuario:
            logger.warning(f"Usuario no encontrado: {uid}")
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )
        
        # Para administradores, verificar contraseña si se proporciona
        if usuario.rol == "admin":
            if password:
                # Si se proporciona contraseña, verificarla
                if not verify_password(password, usuario.contraseña_hash):
                    logger.warning(f"Contraseña incorrecta para admin: {uid}")
                    raise HTTPException(
                        status_code=401,
                        detail="Credenciales inválidas"
                    )
            else:
                # Si no se proporciona contraseña para admin, permitir acceso
                # (compatibilidad con sistema RFID)
                logger.info(f"Login de admin sin contraseña (RFID): {uid}")
        
        # Para alumnos y docentes, el UID es suficiente (sistema RFID)
        logger.info(f"Login exitoso para {usuario.rol}: {usuario.nombre}")
        
        # Preparar datos de respuesta según el rol
        response_data = {
            "uid": usuario.uid,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "activo": usuario.activo,
            "mensaje": f"Bienvenido {usuario.nombre}"
        }
        
        # Agregar datos específicos según el rol
        if usuario.rol == "alumno":
            response_data.update({
                "matricula": usuario.uid,
                "carrera": usuario.carrera,
                "semestre": usuario.semestre,
                "grupo": usuario.grupo
            })
        elif usuario.rol == "docente":
            response_data.update({
                "clave_docente": usuario.uid
            })
        elif usuario.rol == "admin":
            response_data.update({
                "permisos": "administrador"
            })
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@router.post("/register")
async def registrar_usuario(
    registro_data: dict,
    db: Session = Depends(get_db)
):
    """Registrar nuevo usuario"""
    try:
        uid = registro_data.get("uid")
        nombre = registro_data.get("nombre")
        rol = registro_data.get("rol")
        password = registro_data.get("password", "")
        
        if not all([uid, nombre, rol]):
            raise HTTPException(
                status_code=400,
                detail="UID, nombre y rol son requeridos"
            )
        
        if rol not in ["alumno", "docente", "admin"]:
            raise HTTPException(
                status_code=400,
                detail="Rol debe ser: alumno, docente o admin"
            )
        
        # Verificar que no exista el usuario
        usuario_existente = db.query(models.Usuario).filter(
            models.Usuario.uid == uid
        ).first()
        
        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )
        
        # Generar hash de contraseña
        password_hash = get_password_hash(password) if password else get_password_hash("default123")
        
        # Crear nuevo usuario
        nuevo_usuario = models.Usuario(
            uid=uid,
            nombre=nombre,
            rol=rol,
            contraseña_hash=password_hash,
            activo=True,
            fecha_registro=datetime.now()
        )
        
        # Agregar datos específicos según el rol
        if rol == "alumno":
            nuevo_usuario.carrera = registro_data.get("carrera")
            nuevo_usuario.semestre = registro_data.get("semestre")
            nuevo_usuario.grupo = registro_data.get("grupo")
        elif rol == "docente":
            nuevo_usuario.clave_docente = uid
        
        db.add(nuevo_usuario)
        db.flush()  # Para obtener el ID
        
        # Crear registro en tabla específica si es docente
        if rol == "docente":
            docente_registro = models.Docente(
                usuario_id=nuevo_usuario.id,
                activo=True
            )
            db.add(docente_registro)
        
        db.commit()
        db.refresh(nuevo_usuario)
        
        logger.info(f"Usuario registrado: {nombre} ({rol})")
        
        return {
            "uid": nuevo_usuario.uid,
            "nombre": nuevo_usuario.nombre,
            "rol": nuevo_usuario.rol,
            "mensaje": "Usuario registrado exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error registrando usuario: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error registrando usuario"
        )

@router.get("/verificar/{uid}")
async def verificar_usuario(
    uid: str,
    db: Session = Depends(get_db)
):
    """Verificar si un usuario existe y está activo"""
    try:
        usuario = db.query(models.Usuario).filter(
            models.Usuario.uid == uid,
            models.Usuario.activo == True
        ).first()
        
        if not usuario:
            return {
                "existe": False,
                "mensaje": "Usuario no encontrado"
            }
        
        return {
            "existe": True,
            "uid": usuario.uid,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "activo": usuario.activo
        }
        
    except Exception as e:
        logger.error(f"Error verificando usuario: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error verificando usuario"
        )

@router.patch("/{uid}/toggle")
async def toggle_usuario_estado(
    uid: str,
    toggle_data: dict,
    db: Session = Depends(get_db)
):
    """Activar o desactivar un usuario"""
    try:
        activo = toggle_data.get("activo")
        if activo is None:
            raise HTTPException(
                status_code=400,
                detail="Campo 'activo' es requerido"
            )
        
        usuario = db.query(models.Usuario).filter(
            models.Usuario.uid == uid
        ).first()
        
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        
        usuario.activo = activo
        db.commit()
        
        accion = "activado" if activo else "desactivado"
        logger.info(f"Usuario {usuario.nombre} {accion}")
        
        return {
            "uid": usuario.uid,
            "nombre": usuario.nombre,
            "activo": usuario.activo,
            "mensaje": f"Usuario {accion} exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error cambiando estado del usuario: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error cambiando estado del usuario"
        )

# CONSULTAR ALUMNO - CORREGIDO
@router.get("/consultar_alumno/{matricula}")
def consultar_alumno(matricula: str, db: Session = Depends(get_db)):
    """Consultar información de un alumno por matrícula"""
    try:
        logger.info(f"Consultando alumno con matrícula: '{matricula}'")
        
        # Buscar en la tabla alumnos
        query = text("""
            SELECT a.nombre, a.matricula, a.carrera, a.semestre, a.grupo
            FROM alumnos a
            WHERE a.matricula = :matricula
            AND a.activo = TRUE
        """)
        
        result = db.execute(query, {"matricula": matricula})
        alumno = result.fetchone()
        
        if not alumno:
            logger.warning(f"Alumno no encontrado: '{matricula}'")
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        logger.info(f"Alumno encontrado: {alumno.nombre}")
        
        return {
            "nombre": alumno.nombre,
            "matricula": alumno.matricula,
            "carrera": alumno.carrera,
            "semestre": alumno.semestre,
            "grupo": alumno.grupo
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error consultando alumno: {e}")
        raise HTTPException(status_code=500, detail="Error consultando alumno")

# CONSULTAR DOCENTE - CORREGIDO
@router.get("/consultar_docente/{clave}")
def consultar_docente(clave: str, db: Session = Depends(get_db)):
    """Consultar información de un docente por clave"""
    try:
        logger.info(f"Consultando docente con clave: '{clave}'")
        
        # Buscar en la tabla docentes
        query = text("""
            SELECT d.nombre, d.clave, d.especialidad
            FROM docentes d
            WHERE d.clave = :clave
            AND d.activo = TRUE
        """)
        
        result = db.execute(query, {"clave": clave})
        docente = result.fetchone()
        
        if not docente:
            logger.warning(f"Docente no encontrado: '{clave}'")
            raise HTTPException(status_code=404, detail="Docente no encontrado")
        
        logger.info(f"Docente encontrado: {docente.nombre}")
        
        return {
            "nombre": docente.nombre,
            "clave": docente.clave,
            "especialidad": docente.especialidad
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error consultando docente: {e}")
        raise HTTPException(status_code=500, detail="Error consultando docente")

# Verificar UID - MEJORADO
@router.post("/verificar_uid/")
def verificar_uid(data: dict = Body(...), db: Session = Depends(get_db)):
   uid = data.get("uid")
   if not uid:
       raise HTTPException(status_code=400, detail="UID no proporcionado")

   try:
       logger.info(f"Verificando UID: '{uid}'")
       
       # Buscar usuario por UID
       usuario = db.query(models.Usuario).filter(models.Usuario.uid == uid).first()
       
       if usuario:
           logger.info(f"Usuario encontrado: {usuario.nombre} ({usuario.rol})")
           return {
               "existe": True,
               "nuevo": False,
               "usuario": {
                   "id": usuario.id,
                   "nombre": usuario.nombre,
                   "rol": usuario.rol,
                   "matricula": usuario.matricula,
                   "clave_docente": usuario.clave_docente,
                   "carrera": usuario.carrera,
                   "semestre": usuario.semestre,
                   "grupo": usuario.grupo,
                   "activo": usuario.activo
               }
           }
       else:
           logger.info(f"Usuario no encontrado: '{uid}'")
           return {
               "existe": False,
               "nuevo": True
           }
           
   except Exception as e:
       logger.error(f"Error verificando UID: {e}")
       return {
           "existe": False,
           "nuevo": True
       }

# Verificar UID ESPECÍFICO PARA ADMINISTRADOR - CORREGIDO
@router.post("/verificar_uid_admin/")
def verificar_uid_admin(data: dict = Body(...), db: Session = Depends(get_db)):
   uid = data.get("uid")
   if not uid:
       raise HTTPException(status_code=400, detail="UID no proporcionado")

   try:
       logger.info(f"Verificando UID admin: '{uid}'")
       
       # Buscar SOLO administradores con este UID
       admin = db.query(models.Usuario).filter(
           models.Usuario.uid == uid,
           models.Usuario.rol == "admin"
       ).first()
       
       if admin:
           logger.info(f"Admin encontrado: {admin.nombre}")
           return {
               "existe": True,
               "admin": {
                   "id": admin.id,
                   "nombre": admin.nombre,
                   "uid": admin.uid
               }
           }
       else:
           # Verificar si el UID ya está usado por otro rol
           usuario_existente = db.query(models.Usuario).filter(models.Usuario.uid == uid).first()
           if usuario_existente:
               logger.warning(f"UID usado por {usuario_existente.rol}: {usuario_existente.nombre}")
               return {
                   "existe": False,
                   "error": f"Este UID ya está registrado como {usuario_existente.rol}: {usuario_existente.nombre}"
               }
           else:
               logger.info(f"UID disponible para admin: '{uid}'")
               return {
                   "existe": False,
                   "disponible": True
               }
           
   except Exception as e:
       logger.error(f"Error verificando UID admin: {e}")
       return {
           "existe": False,
           "error": "Error verificando UID"
       }

# Verificar username para admin - CORREGIDO
@router.post("/verificar_username_admin/")
def verificar_username_admin(data: dict = Body(...), db: Session = Depends(get_db)):
   username = data.get("username")
   if not username:
       raise HTTPException(status_code=400, detail="Username no proporcionado")

   try:
       logger.info(f"Verificando username admin: '{username}'")
       
       # Buscar por UID (que puede ser username) o clave_docente
       usuario_existente = db.query(models.Usuario).filter(
           (models.Usuario.uid == username) | 
           (models.Usuario.clave_docente == username)
       ).first()
       
       if usuario_existente:
           logger.warning(f"Username ya usado: {usuario_existente.nombre} ({usuario_existente.rol})")
           return {
               "existe": True,
               "error": f"Username ya está en uso por {usuario_existente.nombre} ({usuario_existente.rol})"
           }
       else:
           logger.info(f"Username disponible: '{username}'")
           return {
               "existe": False,
               "disponible": True
           }
           
   except Exception as e:
       logger.error(f"Error verificando username: {e}")
       return {
           "existe": False,
           "error": "Error verificando username"
       }

# REGISTRO ESPECIAL PARA ADMINISTRADOR - COMPLETAMENTE CORREGIDO
@router.post("/registrar_admin/")
def registrar_admin(data: dict = Body(...), db: Session = Depends(get_db)):
   try:
       logger.info("=== INICIO REGISTRO ADMINISTRADOR ===")
       logger.info(f"Datos recibidos: {data}")
       
       # Extraer datos
       uid_o_username = data.get("uid_o_username")
       nombre_usuario = data.get("nombre_usuario", "")
       nombre_completo = data.get("nombre_completo", "")
       contraseña = data.get("contraseña")
       confirmar = data.get("confirmar_contraseña")
       clave_secreta = data.get("clave_secreta")
       tipo_registro = data.get("tipo_registro", "tarjeta")

       logger.info(f"Tipo: {tipo_registro}")
       logger.info(f"UID/Username: '{uid_o_username}'")
       logger.info(f"Nombre usuario: '{nombre_usuario}'")
       logger.info(f"Nombre completo: '{nombre_completo}'")

       # Validaciones básicas
       if not uid_o_username:
           logger.error("UID/Username faltante")
           raise HTTPException(status_code=400, detail="UID o Username es requerido")
       
       if not contraseña:
           logger.error("Contraseña faltante")
           raise HTTPException(status_code=400, detail="Contraseña es requerida")
       
       if contraseña != confirmar:
           logger.error("Contraseñas no coinciden")
           raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")
       
       # Validar contraseña
       validacion = validar_contraseña(contraseña)
       if not validacion["valida"]:
           logger.error(f"Contraseña inválida: {validacion['errores']}")
           raise HTTPException(status_code=400, detail=f"Contraseña inválida: {', '.join(validacion['errores'])}")
       
       # Verificar clave secreta
       if clave_secreta.strip().upper() != "SOLDADORES":
           logger.error(f"Clave secreta incorrecta: '{clave_secreta}' (esperada: 'SOLDADORES')")
           raise HTTPException(status_code=403, detail="Clave secreta incorrecta")

       # Determinar nombre final
       if tipo_registro == "tarjeta":
           if not nombre_completo:
               logger.error("Nombre completo faltante para registro con tarjeta")
               raise HTTPException(status_code=400, detail="Nombre completo es requerido para registro con tarjeta")
           nombre_final = nombre_completo
           uid_final = uid_o_username
       else:  # manual
           if not nombre_usuario:
               logger.error("Nombre de usuario faltante para registro manual")
               raise HTTPException(status_code=400, detail="Nombre de usuario es requerido para registro manual")
           nombre_final = nombre_usuario
           uid_final = uid_o_username

       logger.info(f"Nombre final: '{nombre_final}'")
       logger.info(f"UID final: '{uid_final}'")

       # Verificar si ya existe
       usuario_existente = db.query(models.Usuario).filter(
           models.Usuario.uid == uid_final
       ).first()
       
       if usuario_existente:
           logger.error(f"Usuario ya existe: {usuario_existente.nombre}")
           raise HTTPException(status_code=400, detail=f"Ya existe un usuario con este UID: {usuario_existente.nombre}")

       # Crear administrador
       contraseña_hash = bcrypt.hash(contraseña)
       
       nuevo_admin = models.Usuario(
           uid=uid_final,
           nombre=nombre_final,
           contraseña_hash=contraseña_hash,
           rol="admin",
           activo=True,
           fecha_registro=datetime.now()
       )
       
       logger.info(f"Creando admin: {nuevo_admin.nombre} con UID: {nuevo_admin.uid}")
       
       db.add(nuevo_admin)
       db.commit()
       db.refresh(nuevo_admin)
       
       logger.info(f"✅ Admin creado exitosamente: ID {nuevo_admin.id}")
       
       return {
           "mensaje": "Administrador registrado exitosamente",
           "admin": {
               "id": nuevo_admin.id,
               "nombre": nuevo_admin.nombre,
               "uid": nuevo_admin.uid,
               "rol": nuevo_admin.rol
           }
       }
       
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"❌ Error registrando admin: {e}")
       db.rollback()
       raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# LOGIN PARA USUARIOS NORMALES - MEJORADO CON RESTRICCIÓN DE HORARIO
@router.post("/login/")
def login_usuario(data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        logger.info("=== INICIO LOGIN USUARIO ===")
        
        uid = data.get("uid")
        contraseña = data.get("contraseña")
        
        logger.info(f"UID: '{uid}'")
        
        if not uid or not contraseña:
            logger.error("Credenciales faltantes")
            raise HTTPException(status_code=400, detail="UID y contraseña son requeridos")
        
        # Buscar usuario por UID (TODOS los roles)
        usuario = db.query(models.Usuario).filter(models.Usuario.uid == uid).first()
        
        if not usuario:
            logger.error(f"Usuario no encontrado: '{uid}'")
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        logger.info(f"Usuario encontrado: {usuario.nombre} ({usuario.rol})")
        
        # Verificar contraseña
        if not bcrypt.verify(contraseña, usuario.contraseña_hash):
            logger.error("Contraseña incorrecta")
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        if not usuario.activo:
            logger.error("Usuario inactivo")
            raise HTTPException(status_code=401, detail="Cuenta desactivada")
        
        # VALIDACIÓN DE HORARIO SOLO PARA ALUMNOS
        if usuario.rol == "alumno":
            verificacion_horario = verificar_horario_alumno(usuario.id, db)
            if not verificacion_horario["puede_acceder"]:
                logger.warning(f"Acceso denegado por horario: {verificacion_horario['mensaje']}")
                raise HTTPException(
                    status_code=403, 
                    detail={
                        "tipo": "restriccion_horario",
                        "mensaje": verificacion_horario["mensaje"],
                        "clase_actual": verificacion_horario.get("clase_actual")
                    }
                )
        
        logger.info(f"✅ Login exitoso: {usuario.nombre} ({usuario.rol})")
        
        # Determinar URL de redirección según el rol
        redirect_urls = {
            "admin": "admin_panel.html",
            "docente": "docente_panel.html", 
            "alumno": "alumno_panel.html"
        }
        
        return {
            "mensaje": "Login exitoso",
            "id": usuario.id,
            "uid": usuario.uid,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "matricula": usuario.matricula,
            "clave_docente": usuario.clave_docente,
            "carrera": usuario.carrera,
            "semestre": usuario.semestre,
            "grupo": usuario.grupo,
            "redirect_url": redirect_urls.get(usuario.rol, "index.html")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en login: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Registrar usuario normal - MEJORADO
@router.post("/registrar/")
def registrar_usuario(data: dict = Body(...), db: Session = Depends(get_db)):
   try:
       logger.info("=== INICIO REGISTRO USUARIO ===")
       logger.info(f"Datos recibidos: {data}")
       
       # Extraer datos
       uid = data.get("uid")
       rol = data.get("rol")
       identificador = data.get("identificador")
       contraseña = data.get("contraseña")
       confirmar = data.get("confirmar_contraseña")
       datos_usuario = data.get("datos_usuario", {})

       # Validaciones básicas
       if not uid or not rol or not identificador or not contraseña:
           raise HTTPException(status_code=400, detail="Datos básicos faltantes")
       
       if contraseña != confirmar:
           raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")
       
       # Validar contraseña
       validacion = validar_contraseña(contraseña)
       if not validacion["valida"]:
           raise HTTPException(status_code=400, detail=f"Contraseña inválida: {', '.join(validacion['errores'])}")
       
       # Verificar si ya existe
       usuario_existente = db.query(models.Usuario).filter(models.Usuario.uid == uid).first()
       if usuario_existente:
           raise HTTPException(status_code=400, detail=f"Ya existe un usuario con este UID: {usuario_existente.nombre}")

       # Crear usuario
       contraseña_hash = bcrypt.hash(contraseña)
       
       nuevo_usuario = models.Usuario(
           uid=uid,
           nombre=datos_usuario.get("nombre"),
           contraseña_hash=contraseña_hash,
           rol=rol,
           matricula=datos_usuario.get("matricula") if rol == "alumno" else None,
           clave_docente=datos_usuario.get("clave") if rol == "docente" else None,
           carrera=datos_usuario.get("carrera") if rol == "alumno" else None,
           semestre=int(datos_usuario.get("semestre")) if rol == "alumno" and datos_usuario.get("semestre") else None,
           grupo=datos_usuario.get("grupo") if rol == "alumno" else None,
           activo=True,
           fecha_registro=datetime.now()
       )
       
       db.add(nuevo_usuario)
       db.commit()
       db.refresh(nuevo_usuario)
       
       logger.info(f"✅ Usuario creado: {nuevo_usuario.nombre} ({nuevo_usuario.rol})")
       
       return {
           "mensaje": "Usuario registrado correctamente",
           "usuario": {
               "id": nuevo_usuario.id,
               "nombre": nuevo_usuario.nombre,
               "uid": nuevo_usuario.uid,
               "rol": nuevo_usuario.rol
           }
       }
       
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"❌ Error registrando usuario: {e}")
       db.rollback()
       raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# Listar usuarios (para admin) - MEJORADO
@router.get("/listar_usuarios/")
def listar_usuarios(admin_uid: str, db: Session = Depends(get_db)):
   try:
       logger.info(f"Listando usuarios - Admin UID: {admin_uid}")
       
       # Verificar que quien solicita es admin
       admin = db.query(models.Usuario).filter(
           models.Usuario.uid == admin_uid,
           models.Usuario.rol == "admin"
       ).first()
       
       if not admin:
           raise HTTPException(status_code=403, detail="Acceso denegado: Se requieren permisos de administrador")
       
       # Obtener todos los usuarios
       usuarios = db.query(models.Usuario).all()
       
       usuarios_lista = []
       for usuario in usuarios:
           usuarios_lista.append({
               "id": usuario.id,
               "uid": usuario.uid,
               "nombre": usuario.nombre,
               "rol": usuario.rol,
               "matricula": usuario.matricula,
               "clave_docente": usuario.clave_docente,
               "carrera": usuario.carrera,
               "semestre": usuario.semestre,
               "grupo": usuario.grupo,
               "activo": usuario.activo,
               "fecha_registro": usuario.fecha_registro.isoformat() if usuario.fecha_registro else None
           })
       
       logger.info(f"✅ {len(usuarios_lista)} usuarios listados")
       return usuarios_lista
       
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"❌ Error listando usuarios: {e}")
       raise HTTPException(status_code=500, detail="Error interno del servidor")

# Obtener información del semestre actual
@router.get("/semestre_actual/")
def obtener_info_semestre():
   """Obtener información del semestre académico actual"""
   try:
       semestre = obtener_semestre_actual()
       return semestre
   except Exception as e:
       logger.error(f"Error obteniendo semestre actual: {e}")
       raise HTTPException(status_code=500, detail="Error obteniendo información del semestre")

# Obtener información de carreras
@router.get("/carreras/")
def obtener_carreras():
   """Obtener lista de carreras disponibles"""
   try:
       carreras = []
       for id_carrera, nombre_carrera in CARRERAS_MAP.items():
           carreras.append({
               "id": id_carrera,
               "nombre": nombre_carrera
           })
       
       return carreras
   except Exception as e:
       logger.error(f"Error obteniendo carreras: {e}")
       raise HTTPException(status_code=500, detail="Error obteniendo carreras")
