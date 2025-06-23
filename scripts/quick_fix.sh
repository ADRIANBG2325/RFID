#!/bin/bash
echo "🚀 Instalación rápida y migración..."

# Instalar dependencias
echo "📦 Instalando pymysql..."
pip3 install pymysql

# Ejecutar migración
echo "🔧 Ejecutando migración..."
python3 scripts/migrate_database_simple.py

# Verificar estado
echo "✅ Verificando estado del sistema..."
python3 scripts/test_connection.py

echo "🎉 ¡Proceso completado!"
