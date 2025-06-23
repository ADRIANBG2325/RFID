#!/bin/bash

# Script para iniciar todo el sistema de control de asistencias

echo "🚀 Iniciando Sistema de Control de Asistencias RFID"
echo "=================================================="

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar que las dependencias estén instaladas
echo "📦 Verificando dependencias..."
python3 -c "import fastapi, socketio, sqlalchemy, serial" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Faltan dependencias. Instalando..."
    pip3 install fastapi uvicorn python-socketio sqlalchemy pymysql pyserial passlib bcrypt
fi

# Iniciar el backend
echo "🔧 Iniciando backend..."
cd backend
python3 -m uvicorn app.main:app_sio --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Esperar a que el backend inicie
echo "⏳ Esperando que el backend inicie..."
sleep 5

# Verificar que el backend esté funcionando
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend iniciado correctamente"
else
    echo "❌ Error iniciando el backend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Iniciar el lector RFID
echo "📡 Iniciando lector RFID..."
cd ..
python3 rfid_reader.py &
RFID_PID=$!

echo ""
echo "✅ Sistema iniciado correctamente!"
echo "📋 Información del sistema:"
echo "   - Backend: http://localhost:8000"
echo "   - Frontend: Abrir frontend/index.html en el navegador"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Para detener el sistema, presione Ctrl+C"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🧹 Deteniendo sistema..."
    kill $BACKEND_PID 2>/dev/null
    kill $RFID_PID 2>/dev/null
    echo "✅ Sistema detenido"
    exit 0
}

# Capturar señal de interrupción
trap cleanup SIGINT SIGTERM

# Mantener el script corriendo
wait
