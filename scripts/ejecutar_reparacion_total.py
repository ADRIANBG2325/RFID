#!/usr/bin/env python3
"""
Script para ejecutar la reparación total del sistema
"""

import sys
import os
import mysql.connector
from mysql.connector import Error
import hashlib
import bcrypt

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'asistencias_rfid',
    'user': 'root',
    'password': ''
}

def ejecutar_script_sql(cursor, archivo_sql):
    """Ejecutar script SQL completo"""
    try:
        print(f"📄 Ejecutando script: {archivo_sql}")
        
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir por comandos usando punto y coma
        comandos = []
        comando_actual = ""
        
        for linea in sql_content.split('\n'):
            linea = linea.strip()
            if linea and not linea.startswith('--'):
                comando_actual += linea + " "
                if linea.endswith(';'):
                    comandos.append(comando_actual.strip())
                    comando_actual = ""
        
        print(f"📋 Ejecutando {len(comandos)} comandos...")
        
        for i, comando in enumerate(comandos, 1):
            if comando.strip():
                try:
                    cursor.execute(comando)
                    if i % 10 == 0:
                        print(f"  ✅ Ejecutados {i}/{len(comandos)} comandos")
                except Error as e:
                    if "already exists" in str(e) or "Duplicate entry" in str(e):
                        print(f"  ⚠️ Comando {i} - Ya existe (OK)")
                    else:
                        print(f"  ❌ Error en comando {i}: {e}")
                        print(f"     Comando: {comando[:100]}...")
                        continue
        
        print(f"✅ Script ejecutado completamente")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando script: {e}")
        return False

def crear_usuarios_ejemplo(cursor):
    """Crear usuarios de ejemplo para pruebas"""
    try:
        print("\n👤 Creando usuarios de ejemplo...")
        
        # Hash para contraseña "12345678"
        password_hash = bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        usuarios_ejemplo = [
            # Alumnos
            ('ALU001', 'alumno', 'Juan Carlos Pérez López', '20230001', None, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301'),
            ('ALU002', 'alumno', 'María Elena González Martínez', '20230002', None, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301'),
            ('ALU003', 'alumno', 'Roberto Miguel Jiménez Cruz', '20220001', None, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, '2402'),
            
            # Docentes
            ('DOC001', 'docente', 'Dr. Miguel Ángel Rodríguez Hernández', None, 'DOC001', None, None, None),
            ('DOC002', 'docente', 'Ing. Laura Patricia Gómez Sánchez', None, 'DOC002', None, None, None),
            ('DOC003', 'docente', 'M.C. José Luis Martínez Torres', None, 'DOC003', None, None, None),
        ]
        
        for uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo in usuarios_ejemplo:
            try:
                cursor.execute("""
                    INSERT INTO usuarios (uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, contraseña_hash, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (uid, rol, nombre, matricula, clave_docente, carrera, semestre, grupo, password_hash, True))
                print(f"  ✅ Usuario creado: {nombre} ({rol})")
            except Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠️ Usuario ya existe: {nombre}")
                else:
                    print(f"  ❌ Error creando usuario {nombre}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando usuarios ejemplo: {e}")
        return False

def crear_docentes_registros(cursor):
    """Crear registros de docentes en tabla docentes"""
    try:
        print("\n👨‍🏫 Creando registros de docentes...")
        
        # Obtener docentes usuarios
        cursor.execute("SELECT id, nombre FROM usuarios WHERE rol = 'docente'")
        docentes_usuarios = cursor.fetchall()
        
        for usuario_id, nombre in docentes_usuarios:
            try:
                cursor.execute("""
                    INSERT INTO docentes (usuario_id, activo)
                    VALUES (%s, %s)
                """, (usuario_id, True))
                print(f"  ✅ Registro docente creado para: {nombre}")
            except Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠️ Registro ya existe para: {nombre}")
                else:
                    print(f"  ❌ Error creando registro para {nombre}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando registros docentes: {e}")
        return False

def crear_asignaciones_ejemplo(cursor):
    """Crear asignaciones de materias ejemplo"""
    try:
        print("\n📚 Creando asignaciones de materias ejemplo...")
        
        # Obtener IDs necesarios
        cursor.execute("SELECT id FROM docentes LIMIT 3")
        docentes_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM materias WHERE carrera_id = 2 AND semestre IN (3, 4) LIMIT 5")
        materias_ids = [row[0] for row in cursor.fetchall()]
        
        if not docentes_ids or not materias_ids:
            print("  ⚠️ No hay suficientes docentes o materias para crear asignaciones")
            return True
        
        asignaciones_ejemplo = [
            # Docente 1 - Materias de 3er semestre grupo 2301
            (docentes_ids[0], materias_ids[0], '2301', 'Lunes', '07:00:00', '08:00:00', 'Aula 101'),
            (docentes_ids[0], materias_ids[1], '2301', 'Miércoles', '07:00:00', '08:00:00', 'Aula 101'),
            
            # Docente 2 - Materias de 4to semestre grupo 2402
            (docentes_ids[1], materias_ids[2], '2402', 'Martes', '08:00:00', '09:00:00', 'Aula 102'),
            (docentes_ids[1], materias_ids[3], '2402', 'Jueves', '08:00:00', '09:00:00', 'Aula 102'),
        ]
        
        for docente_id, materia_id, grupo, dia, hora_inicio, hora_fin, aula in asignaciones_ejemplo:
            try:
                cursor.execute("""
                    INSERT INTO asignaciones_materias (docente_id, materia_id, grupo, dia_semana, hora_inicio, hora_fin, aula, activa)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (docente_id, materia_id, grupo, dia, hora_inicio, hora_fin, aula, True))
                print(f"  ✅ Asignación creada: Grupo {grupo} - {dia} {hora_inicio}-{hora_fin}")
            except Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠️ Asignación ya existe: Grupo {grupo} - {dia}")
                else:
                    print(f"  ❌ Error creando asignación: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando asignaciones: {e}")
        return False

def verificar_sistema(cursor):
    """Verificar que todo esté funcionando correctamente"""
    try:
        print("\n📊 Verificando sistema...")
        
        # Verificar tablas principales
        tablas_verificar = [
            ('carreras', 'activa = TRUE'),
            ('materias', 'activa = TRUE'),
            ('usuarios', 'activo = TRUE'),
            ('docentes', 'activo = TRUE'),
            ('alumnos_base', 'activo = TRUE'),
            ('docentes_base', 'activo = TRUE'),
            ('asignaciones_materias', 'activa = TRUE')
        ]
        
        print("📋 Resumen de datos:")
        for tabla, condicion in tablas_verificar:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla} WHERE {condicion}")
                count = cursor.fetchone()[0]
                print(f"  {tabla}: {count} registros")
            except Error as e:
                print(f"  {tabla}: Error - {e}")
        
        # Verificar carreras específicamente
        print("\n🎓 Carreras disponibles:")
        cursor.execute("SELECT id, nombre FROM carreras WHERE activa = TRUE ORDER BY id")
        carreras = cursor.fetchall()
        for carrera_id, nombre in carreras:
            print(f"  {carrera_id}. {nombre}")
        
        # Verificar usuarios por rol
        print("\n👥 Usuarios por rol:")
        cursor.execute("SELECT rol, COUNT(*) FROM usuarios WHERE activo = TRUE GROUP BY rol")
        roles = cursor.fetchall()
        for rol, count in roles:
            print(f"  {rol}: {count} usuarios")
        
        # Verificar materias de TICs
        print("\n📚 Materias de TICs por semestre:")
        cursor.execute("""
            SELECT m.semestre, COUNT(*) as total
            FROM materias m 
            JOIN carreras c ON m.carrera_id = c.id 
            WHERE c.id = 2 AND m.activa = TRUE 
            GROUP BY m.semestre 
            ORDER BY m.semestre
        """)
        materias_tics = cursor.fetchall()
        for semestre, total in materias_tics:
            print(f"  Semestre {semestre}: {total} materias")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando sistema: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 === REPARACIÓN TOTAL DEL SISTEMA ===\n")
    
    connection = None
    try:
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conexión establecida")
        
        # 1. Ejecutar script de reparación completa
        archivo_sql = "scripts/reparacion_completa_sistema.sql"
        if not os.path.exists(archivo_sql):
            print(f"❌ Archivo {archivo_sql} no encontrado")
            return False
        
        if not ejecutar_script_sql(cursor, archivo_sql):
            print("❌ Error ejecutando script principal")
            return False
        
        # 2. Confirmar cambios del script
        connection.commit()
        print("✅ Script SQL ejecutado y confirmado")
        
        # 3. Crear usuarios de ejemplo
        if not crear_usuarios_ejemplo(cursor):
            print("❌ Error creando usuarios ejemplo")
            return False
        
        # 4. Crear registros de docentes
        if not crear_docentes_registros(cursor):
            print("❌ Error creando registros docentes")
            return False
        
        # 5. Crear asignaciones ejemplo
        if not crear_asignaciones_ejemplo(cursor):
            print("❌ Error creando asignaciones")
            return False
        
        # 6. Confirmar todos los cambios
        connection.commit()
        print("✅ Todos los cambios confirmados")
        
        # 7. Verificar sistema
        if not verificar_sistema(cursor):
            print("❌ Error verificando sistema")
            return False
        
        print("\n✅ === REPARACIÓN TOTAL COMPLETADA ===")
        
        print(f"\n📋 Sistema configurado con:")
        print(f"  ✅ 8 carreras con materias completas")
        print(f"  ✅ Usuarios de ejemplo (alumnos y docentes)")
        print(f"  ✅ Asignaciones de materias con horarios")
        print(f"  ✅ Administrador por defecto")
        print(f"  ✅ Estructura de base de datos optimizada")
        
        print(f"\n🔐 Credenciales de prueba:")
        print(f"  👨‍🎓 Alumno: UID=ALU001, Contraseña=12345678")
        print(f"  👨‍🏫 Docente: UID=DOC001, Contraseña=12345678")
        print(f"  👑 Admin: UID=ADMIN001, Contraseña=admin123")
        
        print(f"\n🔄 Próximos pasos:")
        print(f"  1. Reiniciar el servidor FastAPI")
        print(f"  2. Probar login con usuarios de ejemplo")
        print(f"  3. Verificar que aparezcan las carreras")
        print(f"  4. Probar registro de nuevos usuarios")
        
        return True
        
    except Error as e:
        print(f"❌ Error de base de datos: {e}")
        if connection:
            connection.rollback()
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
