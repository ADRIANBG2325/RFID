#!/usr/bin/env python3
"""
Script para recrear completamente la tabla materias
CUIDADO: Esto eliminará todos los datos existentes en la tabla materias
"""

import mysql.connector
import sys
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'User',
    'password': '12345678',
    'database': 'control_asistencia',
    'charset': 'utf8mb4'
}

def conectar_mysql():
    """Conectar a MySQL"""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexión a MySQL exitosa")
        return conexion
    except mysql.connector.Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None

def recrear_tabla_materias(cursor):
    """Recrear completamente la tabla materias"""
    print("\n🗑️  Eliminando tabla materias existente...")
    
    try:
        # Desactivar verificación de claves foráneas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Eliminar tabla si existe
        cursor.execute("DROP TABLE IF EXISTS materias")
        print("✅ Tabla materias eliminada")
        
        # Crear tabla nueva con estructura completa
        print("🏗️  Creando nueva tabla materias...")
        cursor.execute("""
            CREATE TABLE materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                codigo VARCHAR(20) NOT NULL,
                carrera_id INT,
                semestre INT NOT NULL,
                creditos INT DEFAULT 3,
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
                INDEX idx_carrera_semestre (carrera_id, semestre)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Reactivar verificación de claves foráneas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        print("✅ Nueva tabla materias creada")
        
        # Verificar estructura
        cursor.execute("DESCRIBE materias")
        columnas = cursor.fetchall()
        
        print("\n📋 Estructura de la nueva tabla:")
        for columna in columnas:
            print(f"  • {columna[0]} - {columna[1]}")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error recreando tabla: {e}")
        return False

def insertar_materias_completas_isc(cursor):
    """Insertar materias completas de ISC"""
    print("\n📚 Insertando materias completas de ISC...")
    
    # Obtener ID de ISC
    cursor.execute("SELECT id FROM carreras WHERE codigo = 'ISC'")
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ Carrera ISC no encontrada")
        return False
    
    carrera_id = resultado[0]
    
    materias_isc = [
        # 1er Semestre
        ('Cálculo diferencial', 'ISC101', carrera_id, 1, 5),
        ('Fundamentos de programación', 'ISC102', carrera_id, 1, 5),
        ('Desarrollo sustentable', 'ISC103', carrera_id, 1, 4),
        ('Matemáticas discretas', 'ISC104', carrera_id, 1, 5),
        ('Química', 'ISC105', carrera_id, 1, 4),
        ('Taller de ética', 'ISC106', carrera_id, 1, 3),
        
        # 2do Semestre
        ('Cálculo integral', 'ISC201', carrera_id, 2, 5),
        ('Programación orientada a objetos', 'ISC202', carrera_id, 2, 5),
        ('Taller de administración', 'ISC203', carrera_id, 2, 4),
        ('Álgebra lineal', 'ISC204', carrera_id, 2, 5),
        ('Probabilidad y estadística', 'ISC205', carrera_id, 2, 5),
        ('Física general', 'ISC206', carrera_id, 2, 4),
        
        # 3er Semestre
        ('Cálculo vectorial', 'ISC301', carrera_id, 3, 5),
        ('Estructura de datos', 'ISC302', carrera_id, 3, 5),
        ('Fundamentos de telecomunicaciones', 'ISC303', carrera_id, 3, 4),
        ('Investigación de operaciones', 'ISC304', carrera_id, 3, 5),
        ('Sistemas operativos I', 'ISC305', carrera_id, 3, 4),
        ('Principios eléctricos y aplicaciones digitales', 'ISC306', carrera_id, 3, 5),
        
        # 4to Semestre
        ('Ecuaciones diferenciales', 'ISC401', carrera_id, 4, 5),
        ('Métodos numéricos', 'ISC402', carrera_id, 4, 5),
        ('Tópicos avanzados de programación', 'ISC403', carrera_id, 4, 5),
        ('Fundamentos de bases de datos', 'ISC404', carrera_id, 4, 5),
        ('Taller de sistemas operativos', 'ISC405', carrera_id, 4, 4),
        ('Arquitectura de computadoras', 'ISC406', carrera_id, 4, 5),
        
        # 5to Semestre
        ('Lenguajes y autómatas I', 'ISC501', carrera_id, 5, 5),
        ('Redes computacionales', 'ISC502', carrera_id, 5, 5),
        ('Taller de base de datos', 'ISC503', carrera_id, 5, 4),
        ('Simulación', 'ISC504', carrera_id, 5, 5),
        ('Fundamentos de ingeniería de software', 'ISC505', carrera_id, 5, 4),
        ('Lenguaje de interfaz', 'ISC506', carrera_id, 5, 4),
        ('Contabilidad financiera', 'ISC507', carrera_id, 5, 4),
        
        # 6to Semestre
        ('Lenguajes y autómatas II', 'ISC601', carrera_id, 6, 5),
        ('Administración de redes', 'ISC602', carrera_id, 6, 5),
        ('Administración de bases de datos', 'ISC603', carrera_id, 6, 5),
        ('Programación web', 'ISC604', carrera_id, 6, 5),
        ('Ingeniería de software', 'ISC605', carrera_id, 6, 5),
        ('Sistemas programables', 'ISC606', carrera_id, 6, 5),
        
        # 7mo Semestre
        ('Programación lógica y funcional', 'ISC701', carrera_id, 7, 4),
        ('Comunicación y enrutamiento de redes de datos', 'ISC702', carrera_id, 7, 5),
        ('Taller de investigación I', 'ISC703', carrera_id, 7, 4),
        ('Desarrollo de aplicaciones para dispositivos móviles', 'ISC704', carrera_id, 7, 5),
        ('Gestión de proyectos de software', 'ISC705', carrera_id, 7, 4),
        ('Internet de las cosas', 'ISC706', carrera_id, 7, 4),
        ('Graficación', 'ISC707', carrera_id, 7, 4),
        
        # 8vo Semestre
        ('Inteligencia artificial', 'ISC801', carrera_id, 8, 5),
        ('Ciberseguridad', 'ISC802', carrera_id, 8, 5),
        ('Taller de investigación II', 'ISC803', carrera_id, 8, 4),
        ('Programación reactiva', 'ISC804', carrera_id, 8, 4),
        ('Sistemas distribuidos', 'ISC805', carrera_id, 8, 5),
        ('Cultura empresarial', 'ISC806', carrera_id, 8, 3),
        
        # 9no Semestre
        ('Residencias profesionales', 'ISC901', carrera_id, 9, 10)
    ]
    
    query = "INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES (%s, %s, %s, %s, %s, TRUE)"
    
    try:
        cursor.executemany(query, materias_isc)
        print(f"✅ {len(materias_isc)} materias de ISC insertadas")
        
        # Mostrar resumen por semestre
        cursor.execute("""
            SELECT semestre, COUNT(*) as total
            FROM materias 
            WHERE carrera_id = %s
            GROUP BY semestre
            ORDER BY semestre
        """, (carrera_id,))
        
        print("\n📊 Materias por semestre:")
        for semestre, total in cursor.fetchall():
            print(f"  • Semestre {semestre}: {total} materias")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error insertando materias: {e}")
        return False

def main():
    """Función principal"""
    print("🔧" + "="*60)
    print("    RECREACIÓN COMPLETA DE TABLA MATERIAS")
    print("="*60)
    print("⚠️  ADVERTENCIA: Esto eliminará todos los datos existentes en materias")
    
    respuesta = input("\n¿Continuar? (s/N): ").lower().strip()
    if respuesta != 's':
        print("❌ Operación cancelada")
        return
    
    conexion = conectar_mysql()
    if not conexion:
        sys.exit(1)
    
    cursor = conexion.cursor()
    
    try:
        # 1. Recrear tabla materias
        if not recrear_tabla_materias(cursor):
            print("❌ Error recreando tabla. Abortando...")
            return
        
        # 2. Insertar materias de ISC
        if not insertar_materias_completas_isc(cursor):
            print("❌ Error insertando materias. Abortando...")
            return
        
        # 3. Confirmar cambios
        conexion.commit()
        print("\n✅ RECREACIÓN COMPLETADA EXITOSAMENTE")
        print("\n🎉 Tabla materias lista con estructura completa!")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        conexion.rollback()
    
    finally:
        cursor.close()
        conexion.close()
        print("\n🔒 Conexión cerrada")

if __name__ == "__main__":
    main()
