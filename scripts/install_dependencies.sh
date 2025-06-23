#!/bin/bash
echo "🔧 Instalando dependencias del sistema..."

# Instalar mysql-connector-python
echo "📦 Instalando mysql-connector-python..."
pip3 install mysql-connector-python

# Verificar instalación
echo "✅ Verificando instalación..."
python3 -c "import mysql.connector; print('MySQL connector instalado correctamente')"

# Instalar otras dependencias si es necesario
echo "📦 Instalando dependencias adicionales..."
pip3 install pymysql
pip3 install sqlalchemy

echo "✅ ¡Todas las dependencias instaladas!"
