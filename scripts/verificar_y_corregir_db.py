#!/usr/bin/env python3
"""
Script para verificar y corregir problemas en la base de datos
"""

import pymysql
import sys
from datetime import datetime
from passlib.hash import bcrypt

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambiar si tienes contraseña
    'database': 'asistencias_rfid',
    'charset': 'utf8mb4'
}

def conectar_db():
    """Conectar a la base de datos"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ Conexión a base de datos exitosa")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a base de datos: {e}")
        return None

def verificar_estructura_usuarios(cursor):
    """Verificar y corregir estructura de tabla usuarios"""
    print("\n🔍 VERIFICANDO ESTRUCTURA DE TABLA USUARIOS:")
    
    try:
        # Verificar si existe la tabla
        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        if not cursor.fetchone():
            print("❌ Tabla usuarios no existe")
            return False
        
        # Verificar columnas
        cursor.execute("SHOW COLUMNS FROM usuarios")
        columnas = {col[0]: col[1] for col in cursor.fetchall()}
        
        columnas_requeridas = {
            'id': 'int',
            'uid': 'varchar',
            'rol': 'varchar',
            'nombre': 'varchar',
            'contraseña_hash': 'varchar',
            'activo': 'tinyint',
            'fecha_registro': 'datetime'
        }
        
        for col, tipo in columnas_requeridas.items():
            if col in columnas:
                print(f"  ✅ Columna '{col}' existe")
            else:
                print(f"  ❌ Columna '{col}' FALTA - Agregando...")
                try:
                    if col == 'activo':
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN activo TINYINT(1) DEFAULT 1")
                    elif col == 'fecha_registro':
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP")
                    elif col == 'contraseña_hash':
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255)")
                    print(f"    ✅ Columna '{col}' agregada")
                except Exception as e:
                    print(f"    ❌ Error agregando columna '{col}': {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def crear_admin_emergencia(cursor):
    """Crear administrador de emergencia si no existe"""
    print("\n🚨 CREANDO ADMINISTRADOR DE EMERGENCIA:")
    
    try:
        # Verificar si ya existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE uid = 'ADMIN_EMERGENCY'")
        if cursor.fetchone()[0] > 0:
            print("  ✅ Administrador de emergencia ya existe")
            return True
        
        # Crear admin de emergencia
        contraseña_hash = bcrypt.hash("admin123")
        
        cursor.execute("""
            INSERT INTO usuarios (uid, rol, nombre, clave_docente, contraseña_hash, activo, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            'ADMIN_EMERGENCY',
            'admin',
            'Administrador de Emergencia',
            'ADMIN_EMERGENCY',
            contraseña_hash,
            1,
            datetime.now()
        ))
        
        print("  ✅ Administrador de emergencia creado")
        print("  📋 Credenciales:")
        print("      UID: ADMIN_EMERGENCY")
        print("      Contraseña: admin123")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error creando admin de emergencia: {e}")
        return False

def verificar_datos_base(cursor):
    """Verificar que existan datos base (alumnos y docentes)"""
    print("\n📊 VERIFICANDO DATOS BASE:")
    
    try:
        # Verificar alumnos_base
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = 1")
        alumnos_count = cursor.fetchone()[0]
        print(f"  👨‍🎓 Alumnos en base: {alumnos_count}")
        
        if alumnos_count == 0:
            print("  ⚠️ No hay alumnos en la base. Ejecute el script de inserción de datos.")
        
        # Verificar docentes_base
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = 1")
        docentes_count = cursor.fetchone()[0]
        print(f"  👨‍🏫 Docentes en base: {docentes_count}")
        
        if docentes_count == 0:
            print("  ⚠️ No hay docentes en la base. Ejecute el script de inserción de datos.")
        
        # Verificar carreras
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE activa = 1")
        carreras_count = cursor.fetchone()[0]
        print(f"  🎓 Carreras activas: {carreras_count}")
        
        if carreras_count == 0:
            print("  ⚠️ No hay carreras. Ejecute el script de inserción de datos.")
        
        return alumnos_count > 0 and docentes_count > 0 and carreras_count > 0
        
    except Exception as e:
        print(f"  ❌ Error verificando datos base: {e}")
        return False

def limpiar_usuarios_duplicados(cursor):
    """Limpiar usuarios duplicados"""
    print("\n🧹 LIMPIANDO USUARIOS DUPLICADOS:")
    
    try:
        # Buscar UIDs duplicados
        cursor.execute("""
            SELECT uid, COUNT(*) as count 
            FROM usuarios 
            GROUP BY uid 
            HAVING count > 1
        """)
        
        duplicados = cursor.fetchall()
        
        if not duplicados:
            print("  ✅ No hay usuarios duplicados")
            return True
        
        for uid, count in duplicados:
            print(f"  🔍 UID duplicado encontrado: {uid} ({count} veces)")
            
            # Mantener solo el más reciente
            cursor.execute("""
                DELETE FROM usuarios 
                WHERE uid = %s 
                AND id NOT IN (
                    SELECT * FROM (
                        SELECT MAX(id) FROM usuarios WHERE uid = %s
                    ) as temp
                )
            """, (uid, uid))
            
            print(f"    ✅ Duplicados eliminados para UID: {uid}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error limpiando duplicados: {e}")
        return False

def verificar_indices(cursor):
    """Verificar y crear índices necesarios"""
    print("\n📇 VERIFICANDO ÍNDICES:")
    
    try:
        # Verificar índice en UID
        cursor.execute("SHOW INDEX FROM usuarios WHERE Key_name = 'uid'")
        if not cursor.fetchall():
            print("  🔧 Creando índice en UID...")
            cursor.execute("CREATE UNIQUE INDEX uid ON usuarios(uid)")
            print("    ✅ Índice UID creado")
        else:
            print("  ✅ Índice UID existe")
        
        # Verificar índice en matrícula
        cursor.execute("SHOW INDEX FROM usuarios WHERE Key_name = 'matricula'")
        if not cursor.fetchall():
            print("  🔧 Creando índice en matrícula...")
            cursor.execute("CREATE INDEX matricula ON usuarios(matricula)")
            print("    ✅ Índice matrícula creado")
        else:
            print("  ✅ Índice matrícula existe")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error verificando índices: {e}")
        return False

def mostrar_estadisticas_finales(cursor):
    """Mostrar estadísticas finales"""
    print("\n📊 ESTADÍSTICAS FINALES:")
    
    try:
        # Usuarios por rol
        cursor.execute("SELECT rol, COUNT(*) FROM usuarios GROUP BY rol")
        usuarios_por_rol = cursor.fetchall()
        
        print("  👥 Usuarios registrados:")
        for rol, count in usuarios_por_rol:
            print(f"    - {rol}: {count}")
        
        # Total de usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        print(f"    TOTAL: {total_usuarios}")
        
        # Datos base
        cursor.execute("SELECT COUNT(*) FROM alumnos_base WHERE activo = 1")
        alumnos_base = cursor.fetchone()[0]
        print(f"  👨‍🎓 Alumnos disponibles: {alumnos_base}")
        
        cursor.execute("SELECT COUNT(*) FROM docentes_base WHERE activo = 1")
        docentes_base = cursor.fetchone()[0]
        print(f"  👨‍🏫 Docentes disponibles: {docentes_base}")
        
    except Exception as e:
        print(f"  ❌ Error obteniendo estadísticas: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🔧 VERIFICADOR Y CORRECTOR DE BASE DE DATOS")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conectar a la base de datos
    connection = conectar_db()
    if not connection:
        sys.exit(1)
    
    try:
        cursor = connection.cursor()
        
        # Ejecutar verificaciones y correcciones
        pasos = [
            ("Verificar estructura usuarios", lambda: verificar_estructura_usuarios(cursor)),
            ("Limpiar usuarios duplicados", lambda: limpiar_usuarios_duplicados(cursor)),
            ("Crear admin de emergencia", lambda: crear_admin_emergencia(cursor)),
            ("Verificar índices", lambda: verificar_indices(cursor)),
            ("Verificar datos base", lambda: verificar_datos_base(cursor))
        ]
        
        resultados = []
        
        for nombre, funcion in pasos:
            print(f"\n{'='*20} {nombre} {'='*20}")
            try:
                resultado = funcion()
                resultados.append((nombre, "✅ EXITOSO" if resultado else "⚠️ CON PROBLEMAS"))
                
                # Commit después de cada paso exitoso
                if resultado:
                    connection.commit()
                    
            except Exception as e:
                print(f"❌ Error en {nombre}: {e}")
                resultados.append((nombre, "❌ ERROR"))
                connection.rollback()
        
        # Mostrar estadísticas finales
        mostrar_estadisticas_finales(cursor)
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE VERIFICACIÓN Y CORRECCIÓN")
        print("=" * 60)
        
        for nombre, resultado in resultados:
            print(f"{resultado} {nombre}")
        
        exitosos = sum(1 for _, r in resultados if "✅" in r)
        total = len(resultados)
        
        print(f"\n🎯 Resultado: {exitosos}/{total} pasos completados exitosamente")
        
        if exitosos == total:
            print("🎉 ¡Base de datos verificada y corregida!")
            print("\n📋 CREDENCIALES DE EMERGENCIA:")
            print("   UID: ADMIN_EMERGENCY")
            print("   Contraseña: admin123")
        else:
            print("⚠️ Algunos pasos tuvieron problemas. Revisar logs arriba.")
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        connection.rollback()
    finally:
        connection.close()
        print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    main()
