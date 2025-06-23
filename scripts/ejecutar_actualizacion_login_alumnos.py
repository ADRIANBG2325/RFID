#!/usr/bin/env python3
"""
Script para actualizar el sistema de login de alumnos con restricciones de horario
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de base de datos
DATABASE_URL = "mysql+pymysql://root:@localhost/sistema_asistencias"

def main():
    """Función principal para actualizar el sistema"""
    try:
        logger.info("🚀 Iniciando actualización del sistema de login de alumnos...")
        
        # Crear conexión a la base de datos
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        logger.info("✅ Conexión a base de datos establecida")
        
        # 1. Verificar estructura de tablas necesarias
        logger.info("📋 Verificando estructura de tablas...")
        
        # Verificar tabla asignaciones_materias
        result = db.execute(text("""
            SELECT COUNT(*) as count 
            FROM information_schema.tables 
            WHERE table_schema = 'sistema_asistencias' 
            AND table_name = 'asignaciones_materias'
        """))
        
        if result.fetchone().count == 0:
            logger.warning("⚠️ Tabla asignaciones_materias no existe, creándola...")
            
            db.execute(text("""
                CREATE TABLE asignaciones_materias (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    docente_id INT NOT NULL,
                    materia_id INT NOT NULL,
                    grupo INT NOT NULL,
                    dia_semana VARCHAR(20) NOT NULL,
                    hora_inicio TIME NOT NULL,
                    hora_fin TIME NOT NULL,
                    aula VARCHAR(50),
                    activa BOOLEAN DEFAULT TRUE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (docente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
                    INDEX idx_grupo_dia (grupo, dia_semana),
                    INDEX idx_docente (docente_id),
                    INDEX idx_materia (materia_id)
                )
            """))
            
            logger.info("✅ Tabla asignaciones_materias creada")
        else:
            logger.info("✅ Tabla asignaciones_materias existe")
        
        # 2. Insertar algunas asignaciones de ejemplo para testing
        logger.info("📚 Insertando asignaciones de ejemplo...")
        
        # Verificar si ya hay asignaciones
        result = db.execute(text("SELECT COUNT(*) as count FROM asignaciones_materias"))
        if result.fetchone().count == 0:
            
            # Obtener algunos docentes y materias para crear asignaciones de ejemplo
            docentes = db.execute(text("""
                SELECT id, nombre FROM usuarios WHERE rol = 'docente' LIMIT 3
            """)).fetchall()
            
            materias = db.execute(text("""
                SELECT id, nombre FROM materias LIMIT 5
            """)).fetchall()
            
            if docentes and materias:
                # Crear algunas asignaciones de ejemplo
                asignaciones_ejemplo = [
                    (docentes[0].id, materias[0].id, 1101, "Lunes", "08:00", "10:00", "A-101"),
                    (docentes[0].id, materias[1].id, 1101, "Miércoles", "10:00", "12:00", "A-102"),
                    (docentes[1].id, materias[2].id, 1102, "Martes", "14:00", "16:00", "B-201"),
                    (docentes[1].id, materias[3].id, 1102, "Jueves", "16:00", "18:00", "B-202"),
                    (docentes[2].id, materias[4].id, 2101, "Viernes", "09:00", "11:00", "C-301"),
                ]
                
                for asignacion in asignaciones_ejemplo:
                    db.execute(text("""
                        INSERT INTO asignaciones_materias 
                        (docente_id, materia_id, grupo, dia_semana, hora_inicio, hora_fin, aula)
                        VALUES (:docente_id, :materia_id, :grupo, :dia, :inicio, :fin, :aula)
                    """), {
                        "docente_id": asignacion[0],
                        "materia_id": asignacion[1], 
                        "grupo": asignacion[2],
                        "dia": asignacion[3],
                        "inicio": asignacion[4],
                        "fin": asignacion[5],
                        "aula": asignacion[6]
                    })
                
                logger.info(f"✅ {len(asignaciones_ejemplo)} asignaciones de ejemplo creadas")
            else:
                logger.warning("⚠️ No hay docentes o materias para crear asignaciones de ejemplo")
        else:
            logger.info("✅ Ya existen asignaciones en la base de datos")
        
        # 3. Verificar que los alumnos tengan grupos asignados
        logger.info("👥 Verificando grupos de alumnos...")
        
        result = db.execute(text("""
            SELECT COUNT(*) as count 
            FROM usuarios 
            WHERE rol = 'alumno' AND (grupo IS NULL OR grupo = '')
        """))
        
        alumnos_sin_grupo = result.fetchone().count
        if alumnos_sin_grupo > 0:
            logger.warning(f"⚠️ {alumnos_sin_grupo} alumnos sin grupo asignado")
            
            # Asignar grupos por defecto basados en carrera y semestre
            db.execute(text("""
                UPDATE usuarios 
                SET grupo = CONCAT(
                    CASE carrera
                        WHEN 'Ingeniería Industrial' THEN '1'
                        WHEN 'Ingeniería en Tecnologías de la Información y Comunicaciones' THEN '2'
                        WHEN 'Ingeniería en Sistemas Computacionales' THEN '3'
                        WHEN 'Ingeniería Mecatrónica' THEN '4'
                        WHEN 'Ingeniería Civil' THEN '5'
                        WHEN 'Licenciatura en Administración' THEN '6'
                        WHEN 'Ingeniería Química' THEN '7'
                        WHEN 'Ingeniería en Logística' THEN '8'
                        ELSE '1'
                    END,
                    COALESCE(semestre, 1),
                    '01'
                )
                WHERE rol = 'alumno' AND (grupo IS NULL OR grupo = '')
            """))
            
            logger.info("✅ Grupos asignados automáticamente a alumnos")
        else:
            logger.info("✅ Todos los alumnos tienen grupo asignado")
        
        # 4. Crear función para verificar horarios (stored procedure)
        logger.info("🔧 Creando función de verificación de horarios...")
        
        # Eliminar función si existe
        db.execute(text("DROP FUNCTION IF EXISTS verificar_horario_alumno"))
        
        # Crear nueva función
        db.execute(text("""
            CREATE FUNCTION verificar_horario_alumno(
                p_grupo INT,
                p_dia VARCHAR(20),
                p_hora TIME
            ) RETURNS JSON
            READS SQL DATA
            DETERMINISTIC
            BEGIN
                DECLARE v_result JSON;
                DECLARE v_count INT DEFAULT 0;
                DECLARE v_materia VARCHAR(255);
                DECLARE v_hora_inicio TIME;
                DECLARE v_hora_fin TIME;
                DECLARE v_hora_limite TIME;
                
                -- Buscar clases activas en el horario
                SELECT COUNT(*), 
                       MAX(m.nombre),
                       MAX(am.hora_inicio),
                       MAX(am.hora_fin)
                INTO v_count, v_materia, v_hora_inicio, v_hora_fin
                FROM asignaciones_materias am
                JOIN materias m ON am.materia_id = m.id
                WHERE am.grupo = p_grupo 
                AND am.dia_semana = p_dia
                AND am.activa = TRUE
                AND p_hora >= am.hora_inicio
                AND p_hora <= ADDTIME(am.hora_inicio, '00:15:00');
                
                IF v_count > 0 THEN
                    SET v_hora_limite = ADDTIME(v_hora_inicio, '00:15:00');
                    SET v_result = JSON_OBJECT(
                        'puede_acceder', FALSE,
                        'mensaje', CONCAT('No puede acceder durante la clase de ', v_materia, 
                                        ' (', TIME_FORMAT(v_hora_inicio, '%H:%i'), ' - ', 
                                        TIME_FORMAT(v_hora_fin, '%H:%i'), '). Intente después de las ', 
                                        TIME_FORMAT(v_hora_limite, '%H:%i')),
                        'clase_actual', JSON_OBJECT(
                            'materia', v_materia,
                            'hora_inicio', TIME_FORMAT(v_hora_inicio, '%H:%i'),
                            'hora_fin', TIME_FORMAT(v_hora_fin, '%H:%i'),
                            'puede_acceder_despues', TIME_FORMAT(v_hora_limite, '%H:%i')
                        )
                    );
                ELSE
                    SET v_result = JSON_OBJECT(
                        'puede_acceder', TRUE,
                        'mensaje', 'Fuera del horario de clases'
                    );
                END IF;
                
                RETURN v_result;
            END
        """))
        
        logger.info("✅ Función de verificación de horarios creada")
        
        # 5. Crear tabla de logs de acceso
        logger.info("📝 Creando tabla de logs de acceso...")
        
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS logs_acceso (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                tipo_acceso ENUM('login', 'logout', 'intento_fallido', 'restriccion_horario') NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                mensaje TEXT,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                INDEX idx_usuario_fecha (usuario_id, fecha_hora),
                INDEX idx_tipo_fecha (tipo_acceso, fecha_hora)
            )
        """))
        
        logger.info("✅ Tabla de logs de acceso creada")
        
        # 6. Insertar configuración del sistema
        logger.info("⚙️ Configurando parámetros del sistema...")
        
        # Crear tabla de configuración si no existe
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS configuracion_sistema (
                id INT AUTO_INCREMENT PRIMARY KEY,
                clave VARCHAR(100) UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                descripcion TEXT,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """))
        
        # Insertar configuraciones por defecto
        configuraciones = [
            ('restriccion_horario_alumnos', 'true', 'Activar restricción de horario para alumnos'),
            ('minutos_restriccion_clase', '15', 'Minutos de restricción después del inicio de clase'),
            ('semestre_actual', '2025-1', 'Semestre académico actual'),
            ('periodo_semestre_1', 'febrero-julio', 'Período del primer semestre'),
            ('periodo_semestre_2', 'agosto-febrero', 'Período del segundo semestre'),
            ('semestres_permitidos_1', '2,4,6,8', 'Semestres permitidos en período 1 (pares)'),
            ('semestres_permitidos_2', '1,3,5,7,9', 'Semestres permitidos en período 2 (impares)')
        ]
        
        for clave, valor, descripcion in configuraciones:
            db.execute(text("""
                INSERT INTO configuracion_sistema (clave, valor, descripcion)
                VALUES (:clave, :valor, :descripcion)
                ON DUPLICATE KEY UPDATE 
                valor = VALUES(valor),
                descripcion = VALUES(descripcion)
            """), {"clave": clave, "valor": valor, "descripcion": descripcion})
        
        logger.info("✅ Configuraciones del sistema actualizadas")
        
        # 7. Commit de todos los cambios
        db.commit()
        logger.info("💾 Cambios guardados en la base de datos")
        
        # 8. Verificar el estado final
        logger.info("🔍 Verificando estado final del sistema...")
        
        # Contar elementos importantes
        stats = {}
        
        result = db.execute(text("SELECT COUNT(*) as count FROM usuarios WHERE rol = 'alumno'"))
        stats['alumnos'] = result.fetchone().count
        
        result = db.execute(text("SELECT COUNT(*) as count FROM usuarios WHERE rol = 'docente'"))
        stats['docentes'] = result.fetchone().count
        
        result = db.execute(text("SELECT COUNT(*) as count FROM asignaciones_materias WHERE activa = TRUE"))
        stats['asignaciones'] = result.fetchone().count
        
        result = db.execute(text("SELECT COUNT(*) as count FROM usuarios WHERE rol = 'alumno' AND grupo IS NOT NULL"))
        stats['alumnos_con_grupo'] = result.fetchone().count
        
        logger.info("📊 Estado final del sistema:")
        logger.info(f"   👥 Alumnos: {stats['alumnos']}")
        logger.info(f"   👨‍🏫 Docentes: {stats['docentes']}")
        logger.info(f"   📚 Asignaciones activas: {stats['asignaciones']}")
        logger.info(f"   🎯 Alumnos con grupo: {stats['alumnos_con_grupo']}")
        
        # 9. Mostrar información sobre el uso
        logger.info("\n" + "="*60)
        logger.info("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*60)
        logger.info("\n📋 NUEVAS FUNCIONALIDADES:")
        logger.info("   🔒 Restricción de horario para alumnos")
        logger.info("   ⏰ Validación de horarios de clase")
        logger.info("   📝 Logs de acceso detallados")
        logger.info("   ⚙️ Configuración flexible del sistema")
        logger.info("\n🎯 COMPORTAMIENTO:")
        logger.info("   • Los alumnos NO pueden iniciar sesión durante sus clases")
        logger.info("   • Restricción activa desde el inicio hasta 15 min después")
        logger.info("   • Los docentes pueden acceder sin restricciones")
        logger.info("   • Los administradores pueden acceder sin restricciones")
        logger.info("\n🔧 CONFIGURACIÓN:")
        logger.info("   • Semestres pares (2,4,6,8) en período Feb-Jul")
        logger.info("   • Semestres impares (1,3,5,7,9) en período Ago-Feb")
        logger.info("   • Grupos asignados automáticamente por carrera")
        logger.info("\n" + "="*60)
        
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Error durante la actualización: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
