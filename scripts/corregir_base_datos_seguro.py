#!/usr/bin/env python3
"""
Script mejorado para corregir la base de datos de forma segura
Maneja claves foráneas y errores de cursor correctamente
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
    'charset': 'utf8mb4',
    'autocommit': False
}

def ejecutar_comando_seguro(cursor, comando, descripcion=""):
    """Ejecutar un comando SQL de forma segura"""
    try:
        cursor.execute(comando)
        # Leer todos los resultados si los hay
        try:
            results = cursor.fetchall()
            if results:
                print(f"  📊 {descripcion}: {len(results)} resultados")
        except mysql.connector.Error:
            pass  # No hay resultados que leer
        
        print(f"  ✅ {descripcion}")
        return True
    except mysql.connector.Error as e:
        if "already exists" in str(e) or "Duplicate" in str(e):
            print(f"  ⚠️ {descripcion}: Ya existe (ignorado)")
            return True
        else:
            print(f"  ❌ {descripcion}: {e}")
            return False

def corregir_estructura_paso_a_paso():
    """Corregir la estructura de la base de datos paso a paso"""
    try:
        print("🔧 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        
        print("📋 Iniciando correcciones paso a paso...")
        
        # Paso 1: Desactivar verificación de claves foráneas
        print("\n🔧 Paso 1: Configuración inicial")
        cursor = connection.cursor()
        ejecutar_comando_seguro(cursor, "SET FOREIGN_KEY_CHECKS = 0", "Desactivar claves foráneas")
        ejecutar_comando_seguro(cursor, "SET SQL_MODE = ''", "Configurar modo SQL")
        connection.commit()
        cursor.close()
        
        # Paso 2: Verificar estructura actual
        print("\n🔍 Paso 2: Verificando estructura actual")
        cursor = connection.cursor()
        ejecutar_comando_seguro(cursor, "SHOW TABLES", "Listar tablas")
        cursor.close()
        
        # Paso 3: Corregir tabla usuarios
        print("\n👥 Paso 3: Corrigiendo tabla usuarios")
        cursor = connection.cursor()
        
        # Agregar columna contraseña_hash si no existe
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255) DEFAULT '$2b$12$defaulthash'")
            print("  ✅ Columna contraseña_hash agregada")
        except mysql.connector.Error as e:
            if "Duplicate column" in str(e):
                print("  ⚠️ Columna contraseña_hash ya existe")
            else:
                print(f"  ❌ Error agregando contraseña_hash: {e}")
        
        # Actualizar contraseñas vacías
        cursor.execute("UPDATE usuarios SET contraseña_hash = '$2b$12$defaulthash' WHERE contraseña_hash IS NULL OR contraseña_hash = ''")
        affected = cursor.rowcount
        print(f"  ✅ {affected} contraseñas actualizadas")
        
        connection.commit()
        cursor.close()
        
        # Paso 4: Crear tabla docentes si no existe
        print("\n👨‍🏫 Paso 4: Creando tabla docentes")
        cursor = connection.cursor()
        
        crear_docentes_sql = """
        CREATE TABLE IF NOT EXISTS docentes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT UNIQUE NOT NULL,
            activo BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_comando_seguro(cursor, crear_docentes_sql, "Crear tabla docentes")
        
        connection.commit()
        cursor.close()
        
        # Paso 5: Insertar docentes faltantes
        print("\n📝 Paso 5: Insertando docentes faltantes")
        cursor = connection.cursor()
        
        insertar_docentes_sql = """
        INSERT IGNORE INTO docentes (usuario_id, activo)
        SELECT id, activo FROM usuarios WHERE rol = 'docente'
        """
        cursor.execute(insertar_docentes_sql)
        affected = cursor.rowcount
        print(f"  ✅ {affected} docentes insertados")
        
        connection.commit()
        cursor.close()
        
        # Paso 6: Crear tabla carreras
        print("\n🎓 Paso 6: Creando tabla carreras")
        cursor = connection.cursor()
        
        crear_carreras_sql = """
        CREATE TABLE IF NOT EXISTS carreras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE NOT NULL,
            codigo VARCHAR(20) UNIQUE NOT NULL,
            activa BOOLEAN DEFAULT TRUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        ejecutar_comando_seguro(cursor, crear_carreras_sql, "Crear tabla carreras")
        
        connection.commit()
        cursor.close()
        
        # Paso 7: Insertar carreras básicas
        print("\n📚 Paso 7: Insertando carreras básicas")
        cursor = connection.cursor()
        
        carreras = [
            (1, 'Ingeniería Industrial', 'IND'),
            (2, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 'TIC'),
            (3, 'Ingeniería en Sistemas Computacionales', 'ISC'),
            (4, 'Ingeniería Mecatrónica', 'MEC'),
            (5, 'Ingeniería Civil', 'CIV'),
            (6, 'Licenciatura en Administración', 'ADM'),
            (7, 'Ingeniería Química', 'QUI'),
            (8, 'Ingeniería en Logística', 'LOG')
        ]
        
        for carrera_id, nombre, codigo in carreras:
            try:
                cursor.execute("INSERT IGNORE INTO carreras (id, nombre, codigo, activa) VALUES (%s, %s, %s, %s)", 
                             (carrera_id, nombre, codigo, True))
            except mysql.connector.Error as e:
                print(f"  ⚠️ Error insertando carrera {nombre}: {e}")
        
        connection.commit()
        print(f"  ✅ Carreras insertadas")
        cursor.close()
        
        # Paso 8: Corregir tabla asignaciones_materias
        print("\n📋 Paso 8: Corrigiendo tabla asignaciones_materias")
        cursor = connection.cursor()
        
        # Verificar si existe la tabla
        cursor.execute("SHOW TABLES LIKE 'asignaciones_materias'")
        tabla_existe = cursor.fetchone()
        
        if tabla_existe:
            # Agregar columnas faltantes
            try:
                cursor.execute("ALTER TABLE asignaciones_materias ADD COLUMN IF NOT EXISTS carrera_id INT NOT NULL DEFAULT 1")
                print("  ✅ Columna carrera_id agregada")
            except mysql.connector.Error as e:
                if "Duplicate column" in str(e):
                    print("  ⚠️ Columna carrera_id ya existe")
                else:
                    print(f"  ❌ Error agregando carrera_id: {e}")
            
            try:
                cursor.execute("ALTER TABLE asignaciones_materias ADD COLUMN IF NOT EXISTS semestre INT NOT NULL DEFAULT 1")
                print("  ✅ Columna semestre agregada")
            except mysql.connector.Error as e:
                if "Duplicate column" in str(e):
                    print("  ⚠️ Columna semestre ya existe")
                else:
                    print(f"  ❌ Error agregando semestre: {e}")
        else:
            # Crear tabla completa
            crear_asignaciones_sql = """
            CREATE TABLE asignaciones_materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                docente_id INT NOT NULL,
                materia_id INT NOT NULL,
                carrera_id INT NOT NULL DEFAULT 1,
                semestre INT NOT NULL DEFAULT 1,
                grupo VARCHAR(20) NOT NULL,
                dia_semana VARCHAR(20) NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                aula VARCHAR(50),
                activa BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            ejecutar_comando_seguro(cursor, crear_asignaciones_sql, "Crear tabla asignaciones_materias")
        
        connection.commit()
        cursor.close()
        
        # Paso 9: Corregir tabla asistencias
        print("\n📊 Paso 9: Corrigiendo tabla asistencias")
        cursor = connection.cursor()
        
        # Verificar si existe la tabla
        cursor.execute("SHOW TABLES LIKE 'asistencias'")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            crear_asistencias_sql = """
            CREATE TABLE asistencias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                alumno_id INT NOT NULL,
                asignacion_id INT NOT NULL,
                fecha DATE NOT NULL,
                hora_registro TIME NOT NULL,
                estado VARCHAR(20) DEFAULT 'Presente',
                observaciones TEXT,
                FOREIGN KEY (alumno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (asignacion_id) REFERENCES asignaciones_materias(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            ejecutar_comando_seguro(cursor, crear_asistencias_sql, "Crear tabla asistencias")
        
        connection.commit()
        cursor.close()
        
        # Paso 10: Reactivar claves foráneas
        print("\n🔒 Paso 10: Reactivando claves foráneas")
        cursor = connection.cursor()
        ejecutar_comando_seguro(cursor, "SET FOREIGN_KEY_CHECKS = 1", "Reactivar claves foráneas")
        connection.commit()
        cursor.close()
        
        # Paso 11: Verificación final
        print("\n🔍 Paso 11: Verificación final")
        cursor = connection.cursor()
        
        tablas_verificar = ['usuarios', 'docentes', 'carreras', 'asignaciones_materias', 'asistencias']
        
        for tabla in tablas_verificar:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"  📋 {tabla}: {count} registros")
            except mysql.connector.Error as e:
                print(f"  ❌ Error verificando {tabla}: {e}")
        
        cursor.close()
        connection.close()
        
        print("\n✅ CORRECCIÓN COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        try:
            connection.rollback()
            connection.close()
        except:
            pass
        return False

def main():
    """Función principal"""
    print("🚀" + "="*60)
    print("    CORRECCIÓN SEGURA DE LA BASE DE DATOS")
    print("="*60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if corregir_estructura_paso_a_paso():
        print("\n🎉 CORRECCIÓN COMPLETADA")
        print("\n📝 Próximos pasos:")
        print("1. Reiniciar el servidor FastAPI")
        print("2. Probar las funciones del panel de administración")
        print("3. Verificar que no hay errores HTTP 500")
        print("\n🔧 Para reiniciar FastAPI:")
        print("cd backend")
        print("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ CORRECCIÓN FALLIDA")
        print("Revisa los errores anteriores y ejecuta nuevamente")
        sys.exit(1)

if __name__ == "__main__":
    main()
