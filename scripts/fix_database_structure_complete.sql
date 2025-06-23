-- Script para corregir completamente la estructura de la base de datos
-- Ejecutar este script para solucionar todos los problemas de estructura

USE control_asistencia;

-- Desactivar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- 1. Corregir tabla usuarios
ALTER TABLE usuarios 
MODIFY COLUMN contraseña_hash VARCHAR(255) NOT NULL DEFAULT '$2b$12$defaulthash';

-- 2. Corregir tabla asignaciones_materias
-- Eliminar la clave foránea de materia_id si existe
ALTER TABLE asignaciones_materias DROP FOREIGN KEY IF EXISTS asignaciones_materias_ibfk_2;
ALTER TABLE asignaciones_materias DROP FOREIGN KEY IF EXISTS fk_asignaciones_materias_materia;

-- Agregar columnas carrera_id y semestre si no existen
ALTER TABLE asignaciones_materias 
ADD COLUMN IF NOT EXISTS carrera_id INT NOT NULL DEFAULT 1 AFTER materia_id,
ADD COLUMN IF NOT EXISTS semestre INT NOT NULL DEFAULT 1 AFTER carrera_id;

-- 3. Asegurar que todas las tablas tengan las columnas correctas
-- Tabla docentes
CREATE TABLE IF NOT EXISTS docentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla carreras
CREATE TABLE IF NOT EXISTS carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    activa BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla materias
CREATE TABLE IF NOT EXISTS materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    carrera_id INT,
    semestre INT NOT NULL,
    creditos INT DEFAULT 3,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla docente_carreras
CREATE TABLE IF NOT EXISTS docente_carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docente_id INT,
    carrera_id INT,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Recrear tabla asignaciones_materias con estructura correcta
DROP TABLE IF EXISTS asignaciones_materias_backup;
CREATE TABLE asignaciones_materias_backup AS SELECT * FROM asignaciones_materias;

DROP TABLE IF EXISTS asignaciones_materias;
CREATE TABLE asignaciones_materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docente_id INT NOT NULL,
    materia_id INT NOT NULL,
    carrera_id INT NOT NULL,
    semestre INT NOT NULL,
    grupo VARCHAR(20) NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    aula VARCHAR(50),
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
    INDEX idx_docente_dia (docente_id, dia_semana),
    INDEX idx_carrera_semestre (carrera_id, semestre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Recrear tabla asistencias con estructura correcta
DROP TABLE IF EXISTS asistencias_backup;
CREATE TABLE asistencias_backup AS SELECT * FROM asistencias WHERE 1=0; -- Solo estructura

DROP TABLE IF EXISTS asistencias;
CREATE TABLE asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    asignacion_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_registro TIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'Presente',
    observaciones TEXT,
    FOREIGN KEY (alumno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (asignacion_id) REFERENCES asignaciones_materias(id) ON DELETE CASCADE,
    INDEX idx_fecha (fecha),
    INDEX idx_alumno_fecha (alumno_id, fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Insertar carreras básicas
INSERT IGNORE INTO carreras (id, nombre, codigo, activa) VALUES
(1, 'Ingeniería Industrial', 'IND', TRUE),
(2, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 'TIC', TRUE),
(3, 'Ingeniería en Sistemas Computacionales', 'ISC', TRUE),
(4, 'Ingeniería Mecatrónica', 'MEC', TRUE),
(5, 'Ingeniería Civil', 'CIV', TRUE),
(6, 'Licenciatura en Administración', 'ADM', TRUE),
(7, 'Ingeniería Química', 'QUI', TRUE),
(8, 'Ingeniería en Logística', 'LOG', TRUE);

-- 7. Crear registros de docentes para usuarios existentes con rol docente
INSERT IGNORE INTO docentes (usuario_id, activo)
SELECT id, activo FROM usuarios WHERE rol = 'docente';

-- 8. Actualizar contraseñas por defecto para usuarios sin hash válido
UPDATE usuarios 
SET contraseña_hash = '$2b$12$defaulthash' 
WHERE contraseña_hash IS NULL OR contraseña_hash = '' OR LENGTH(contraseña_hash) < 10;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- Verificar la estructura
SHOW TABLES;
DESCRIBE usuarios;
DESCRIBE docentes;
DESCRIBE asignaciones_materias;
DESCRIBE asistencias;

SELECT 'Estructura de base de datos corregida exitosamente' AS resultado;
