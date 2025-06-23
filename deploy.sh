#!/bin/bash

echo "🚀 Preparando despliegue para Render..."

# Crear directorio de despliegue
mkdir -p render-deploy
cd render-deploy

# Copiar archivos necesarios
cp ../main.py .
cp ../database.py .
cp ../requirements.txt .
cp ../Dockerfile .
cp ../render.yaml .
cp ../package.json .

# Crear directorio static y copiar frontend
mkdir -p static
cp ../static/index.html static/

echo "✅ Archivos preparados para despliegue"
echo "📁 Archivos en ./render-deploy/"
ls -la

echo ""
echo "🔗 Próximos pasos:"
echo "1. Sube estos archivos a un repositorio de GitHub"
echo "2. Ve a render.com y crea una nueva Web Service"
echo "3. Conecta tu repositorio de GitHub"
echo "4. Render detectará automáticamente la configuración"
echo "5. Agrega las variables de entorno necesarias"
