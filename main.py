from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import socketio
import logging
import uvicorn
from datetime import datetime
import os
from pathlib import Path

from database import crear_tablas, get_db, Usuario, Administrador, Carrera, Materia, Asistencia
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class VerificarUID(BaseModel):
    uid: str

class RegistroUsuario(BaseModel):
    uid: str
    nombre: str
    apellido: str
    email: str
    rol: str
    carrera_id: int = None

class LoginUsuario(BaseModel):
    uid: str

# Crear servidor Socket.IO
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# App de FastAPI
app = FastAPI(
    title="Control de Asistencias RFID", 
    version="1.0.0",
    description="Sistema de control de asistencias con RFID"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Variables globales
connected_clients = set()
rfid_readers = set()

# Eventos de Socket.IO
@sio.event
async def connect(sid, environ):
    connected_clients.add(sid)
    client_ip = environ.get('HTTP_X_FORWARDED_FOR', environ.get('REMOTE_ADDR', 'unknown'))
    logger.info(f"✅ Cliente conectado: {sid} desde IP: {client_ip}")
    
    await sio.emit("connection_status", {
        "status": "connected", 
        "message": "Conectado al servidor exitosamente",
        "timestamp": str(datetime.now())
    }, room=sid)

@sio.event
async def disconnect(sid):
    connected_clients.discard(sid)
    rfid_readers.discard(sid)
    logger.info(f"❌ Cliente desconectado: {sid}")

@sio.event
async def ping(sid, data):
    logger.info(f"🏓 Ping recibido de {sid}: {data}")
    
    if isinstance(data, dict) and "RFID Reader" in str(data.get("message", "")):
        rfid_readers.add(sid)
        logger.info(f"📡 Lector RFID identificado: {sid}")
    
    await sio.emit("pong", {
        "message": "Server is alive", 
        "timestamp": str(datetime.now()),
        "clients_connected": len(connected_clients)
    }, room=sid)

@sio.event
async def rfid_uid(sid, data):
    """Recibe UID desde el lector RFID"""
    try:
        if isinstance(data, dict):
            uid = data.get("uid")
            source = data.get("source", "rfid_reader")
        else:
            uid = str(data)
            source = "legacy"
        
        logger.info(f"🎫 UID recibido de {sid} ({source}): {uid}")
        
        if uid:
            response_data = {
                "uid": uid,
                "timestamp": str(datetime.now()),
                "source": source,
                "reader_id": sid
            }
            
            # Enviar a todos los clientes
            await sio.emit("respuesta_uid", response_data)
            logger.info(f"📤 UID retransmitido a {len(connected_clients)} clientes: {uid}")
            
            await sio.emit("uid_received", {
                "status": "success",
                "uid": uid,
                "message": "UID procesado correctamente"
            }, room=sid)
        else:
            await sio.emit("uid_received", {
                "status": "error",
                "message": "UID vacío"
            }, room=sid)
            
    except Exception as e:
        logger.error(f"❌ Error procesando UID: {e}")
        await sio.emit("uid_received", {
            "status": "error",
            "message": f"Error: {str(e)}"
        }, room=sid)

# Montar Socket.IO
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)

# Endpoints de la API
@app.get("/")
async def root():
    return {
        "message": "Control de Asistencias RFID API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": str(datetime.now()),
        "connected_clients": len(connected_clients),
        "rfid_readers": len(rfid_readers)
    }

# Servir el frontend
@app.get("/app")
async def serve_frontend():
    static_path = Path(__file__).parent / "static" / "index.html"
    if static_path.exists():
        return FileResponse(static_path)
    return {"message": "Frontend no encontrado"}

# Endpoints de usuarios
@app.post("/usuarios/verificar_uid/")
async def verificar_uid(data: VerificarUID, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.uid == data.uid).first()
        
        if usuario:
            return {
                "existe": True,
                "nuevo": False,
                "usuario": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "email": usuario.email,
                    "rol": usuario.rol,
                    "carrera_id": usuario.carrera_id
                }
            }
        else:
            return {
                "existe": False,
                "nuevo": True,
                "usuario": None
            }
    except Exception as e:
        logger.error(f"Error verificando UID: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/usuarios/verificar_uid_admin/")
async def verificar_uid_admin(data: VerificarUID, db: Session = Depends(get_db)):
    try:
        admin = db.query(Administrador).filter(Administrador.uid == data.uid).first()
        
        if admin:
            return {
                "existe": True,
                "admin": {
                    "id": admin.id,
                    "nombre": admin.nombre,
                    "email": admin.email
                }
            }
        else:
            return {"existe": False, "admin": None}
    except Exception as e:
        logger.error(f"Error verificando UID admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/usuarios/registrar/")
async def registrar_usuario(usuario: RegistroUsuario, db: Session = Depends(get_db)):
    try:
        # Verificar si el UID ya existe
        existing = db.query(Usuario).filter(Usuario.uid == usuario.uid).first()
        if existing:
            raise HTTPException(status_code=400, detail="UID ya registrado")
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            uid=usuario.uid,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            rol=usuario.rol,
            carrera_id=usuario.carrera_id
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        return {
            "success": True,
            "message": "Usuario registrado exitosamente",
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "apellido": nuevo_usuario.apellido,
                "rol": nuevo_usuario.rol
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error registrando usuario: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/usuarios/login/")
async def login_usuario(data: LoginUsuario, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.uid == data.uid).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "success": True,
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "rol": usuario.rol,
                "carrera_id": usuario.carrera_id
            }
        }
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/carreras/")
async def obtener_carreras(db: Session = Depends(get_db)):
    try:
        carreras = db.query(Carrera).filter(Carrera.activa == True).all()
        return [
            {
                "id": carrera.id,
                "nombre": carrera.nombre,
                "codigo": carrera.codigo
            }
            for carrera in carreras
        ]
    except Exception as e:
        logger.error(f"Error obteniendo carreras: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Iniciando aplicación...")
    crear_tablas()
    logger.info("✅ Sistema iniciado correctamente")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app_sio",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
