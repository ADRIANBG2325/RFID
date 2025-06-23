#!/bin/bash

echo "🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA RFID"
echo "========================================"

# Verificar si Python está instalado
echo "📋 Verificando Python..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 encontrado: $(python3 --version)"
else
    echo "❌ Python3 no encontrado"
    exit 1
fi

# Verificar dependencias
echo "📋 Verificando dependencias..."
python3 -c "
try:
    import socketio
    import serial
    import requests
    print('✅ Todas las dependencias están instaladas')
except ImportError as e:
    print(f'❌ Falta dependencia: {e}')
    print('💡 Instalar con: pip3 install python-socketio pyserial requests')
    exit(1)
"

# Verificar puertos seriales
echo "📋 Verificando puertos seriales..."
python3 -c "
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
if ports:
    print('📡 Puertos seriales disponibles:')
    for port in ports:
        print(f'   - {port.device}: {port.description}')
else:
    print('⚠️ No se encontraron puertos seriales')
    print('💡 Conecte la Raspberry Pi Pico y verifique la conexión USB')
"

# Verificar si el backend está corriendo
echo "📋 Verificando backend..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend está corriendo"
    curl -s http://localhost:8000/health | python3 -m json.tool
else
    echo "❌ Backend no está corriendo"
    echo "💡 Iniciar con: cd backend && uvicorn app.main:app_sio --reload"
fi

# Ejecutar prueba de conexión
echo "📋 Ejecutando prueba de conexión..."
python3 test_rfid_connection.py

echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Si el backend no está corriendo, inícielo"
echo "2. Ejecute: python3 rfid_reader_debug.py"
echo "3. Seleccione modo simulación (2) para probar sin hardware"
echo "4. Si tiene hardware, conecte la Raspberry Pi Pico y seleccione modo 1"
