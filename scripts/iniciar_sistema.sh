#!/bin/bash

# Script para iniciar el Sistema de Control de Asistencias RFID
# Ejecuta el backend y abre el frontend automáticamente

echo "🚀 INICIANDO SISTEMA DE CONTROL DE ASISTENCIAS RFID"
echo "=================================================="

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip no está instalado"
    exit 1
fi

# Cambiar al directorio del backend
cd backend

echo "📦 Instalando dependencias del backend..."
pip install -r requirements.txt

echo "🔧 Iniciando servidor backend..."
echo "Backend estará disponible en: http://localhost:8000"
echo "Documentación API en: http://localhost:8000/docs"
echo ""
echo "Para detener el servidor, presiona Ctrl+C"
echo ""

# Iniciar el servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
