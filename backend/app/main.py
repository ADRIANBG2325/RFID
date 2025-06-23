from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import socketio
import logging
import uvicorn
from datetime import datetime
import os
import socket

from app.database import crear_tablas
from app.routers import usuarios, asistencias, materias, admin

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modificar la función get_local_ip para producción
def get_local_ip():
    """Obtener IP local del servidor - adaptado para producción"""
    # En producción (Render), usar la variable de entorno o localhost
    if os.getenv("RENDER"):
        return os.getenv("RENDER_EXTERNAL_HOSTNAME", "localhost")
    
    # Código existente para desarrollo local...
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        try:
            # Método 2: Usar hostname
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            if local_ip.startswith("127."):
                # Método 3: Buscar interfaces de red
                import subprocess
                result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
                if result.returncode == 0:
                    ips = result.stdout.strip().split()
                    for ip in ips:
                        if not ip.startswith("127.") and "." in ip:
                            return ip
            return local_ip
        except:
            return "localhost"

# Crear servidor Socket.IO con configuración para red local
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",  # Permitir todas las IPs de la red local
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# App de FastAPI
app = FastAPI(
    title="Control de Asistencias RFID", 
    version="1.0.0",
    description="Sistema de control de asistencias con RFID - Red Local"
)

# Configurar CORS para red local - MÁS PERMISIVO
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "https://*.onrender.com",  # Permitir dominios de Render
        "*"  # En desarrollo - restringir en producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    logger.info(f"📁 Sirviendo frontend desde: {frontend_path}")

# Variables globales para tracking
connected_clients = set()
rfid_readers = set()

# Eventos de Socket.IO
@sio.event
async def connect(sid, environ):
    connected_clients.add(sid)
    client_ip = environ.get('HTTP_X_FORWARDED_FOR', environ.get('REMOTE_ADDR', 'unknown'))
    logger.info(f"✅ Cliente conectado: {sid} desde IP: {client_ip} (Total: {len(connected_clients)})")
    
    # Enviar confirmación de conexión
    await sio.emit("connection_status", {
        "status": "connected", 
        "message": "Conectado al servidor exitosamente",
        "timestamp": str(datetime.now()),
        "server_ip": get_local_ip()
    }, room=sid)

@sio.event
async def disconnect(sid):
    connected_clients.discard(sid)
    rfid_readers.discard(sid)
    logger.info(f"❌ Cliente desconectado: {sid} (Total: {len(connected_clients)})")

@sio.event
async def ping(sid, data):
    """Manejar ping de clientes"""
    logger.info(f"🏓 Ping recibido de {sid}: {data}")
    
    # Identificar si es un lector RFID
    if isinstance(data, dict) and "RFID Reader" in str(data.get("message", "")):
        rfid_readers.add(sid)
        logger.info(f"📡 Lector RFID identificado: {sid}")
    
    await sio.emit("pong", {
        "message": "Server is alive", 
        "timestamp": str(datetime.now()),
        "clients_connected": len(connected_clients),
        "server_ip": get_local_ip()
    }, room=sid)

@sio.event
async def rfid_uid(sid, data):
    """Recibe UID desde el lector RFID"""
    try:
        # Extraer UID del data
        if isinstance(data, dict):
            uid = data.get("uid")
            source = data.get("source", "rfid_reader")
        else:
            uid = str(data)
            source = "legacy"
        
        logger.info(f"🎫 UID recibido de {sid} ({source}): {uid}")
        
        if uid:
            # Preparar respuesta
            response_data = {
                "uid": uid,
                "timestamp": str(datetime.now()),
                "source": source,
                "reader_id": sid
            }
            
            # Enviar a todos los clientes conectados (especialmente frontend)
            await sio.emit("respuesta_uid", response_data)
            logger.info(f"📤 UID retransmitido a {len(connected_clients)} clientes: {uid}")
            
            # Confirmar recepción al lector
            await sio.emit("uid_received", {
                "status": "success",
                "uid": uid,
                "message": "UID procesado correctamente",
                "timestamp": str(datetime.now())
            }, room=sid)
            
        else:
            logger.warning(f"⚠️ UID vacío recibido de {sid}")
            await sio.emit("uid_received", {
                "status": "error",
                "message": "UID vacío",
                "timestamp": str(datetime.now())
            }, room=sid)
            
    except Exception as e:
        logger.error(f"❌ Error procesando UID de {sid}: {e}")
        await sio.emit("uid_received", {
            "status": "error",
            "message": f"Error procesando UID: {str(e)}",
            "timestamp": str(datetime.now())
        }, room=sid)

# Montar Socket.IO con FastAPI
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)

# Incluir routers
app.include_router(usuarios.router)
app.include_router(asistencias.router)
app.include_router(materias.router)
app.include_router(admin.router)

# Endpoints adicionales
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "API funcionando correctamente",
        "timestamp": str(datetime.now()),
        "connected_clients": len(connected_clients),
        "rfid_readers": len(rfid_readers),
        "server_ip": get_local_ip()
    }

@app.get("/")
async def root():
    return {
        "message": "Control de Asistencias RFID API - Red Local",
        "server_ip": get_local_ip(),
        "docs": "/docs",
        "health": "/health",
        "frontend": "/static/index.html"
    }

@app.get("/network-info")
async def network_info():
    """Información de red para configuración"""
    local_ip = get_local_ip()
    return {
        "server_ip": local_ip,
        "api_url": f"http://{local_ip}:8000",
        "frontend_url": f"http://{local_ip}:8000/static/index.html",
        "websocket_url": f"ws://{local_ip}:8000/socket.io/",
        "connected_clients": len(connected_clients),
        "rfid_readers": len(rfid_readers)
    }

# Eventos de inicio
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Iniciando aplicación...")
    crear_tablas()
    logger.info("✅ Base de datos inicializada")
    
    if os.getenv("RENDER"):
        render_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'tu-app')}.onrender.com"
        logger.info(f"🌐 Servidor desplegado en Render:")
        logger.info(f"   - URL: {render_url}")
        logger.info(f"   - API Docs: {render_url}/docs")
    else:
        local_ip = get_local_ip()
        logger.info(f"🌐 Servidor local disponible en:")
        logger.info(f"   - Local: http://localhost:8000")
        logger.info(f"   - Red Local: http://{local_ip}:8000")

if __name__ == "__main__":
    uvicorn.run(
        "main:app_sio", 
        host="0.0.0.0",  # Escuchar en todas las interfaces
        port=8000, 
        reload=True,
        log_level="info"
    )
