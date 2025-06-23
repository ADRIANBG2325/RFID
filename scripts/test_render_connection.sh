#!/bin/bash

echo "🧪 Probando conexión a Render..."

# URL de tu aplicación en Render (cambiar cuando tengas la real)
RENDER_URL="https://tu-rfid-system.onrender.com"

echo "📡 Probando endpoint de salud..."
curl -s "$RENDER_URL/health" | python -m json.tool

echo ""
echo "📊 Probando endpoint principal..."
curl -s "$RENDER_URL/" | python -m json.tool

echo ""
echo "🎓 Probando endpoint de carreras..."
curl -s "$RENDER_URL/carreras/" | python -m json.tool

echo ""
echo "✅ Pruebas completadas"
