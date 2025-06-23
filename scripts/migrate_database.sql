-- Migración para actualizar la base de datos existente
-- Ejecutar este script para agregar las nuevas columnas

-- Agregar columna activo a usuarios si no existe
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE;

-- Actualizar usuarios existentes para que estén activos
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;

-- Crear tabla carreras si no existe
CREATE TABLE IF NOT EXISTS carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    activa BOOLEAN DEFAULT TRUE
);

-- Crear tabla materias si no existe
CREATE TABLE IF NOT EXISTS materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    carrera_id INT,
    semestre INT NOT NULL,
    creditos INT DEFAULT 3,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id)
);

-- Crear tabla docentes si no existe
CREATE TABLE IF NOT EXISTS docentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE,
    especialidad VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Crear tabla docente_carreras si no existe
CREATE TABLE IF NOT EXISTS docente_carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docente_id INT,
    carrera_id INT,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (docente_id) REFERENCES docentes(id),
    FOREIGN KEY (carrera_id) REFERENCES carreras(id)
);

-- Crear tabla asignaciones_materias si no existe
CREATE TABLE IF NOT EXISTS asignaciones_materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docente_id INT,
    materia_id INT,
    grupo VARCHAR(20) NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    aula VARCHAR(50),
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (docente_id) REFERENCES docentes(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);

-- Crear tabla alumnos_base si no existe
CREATE TABLE IF NOT EXISTS alumnos_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    matricula VARCHAR(100) UNIQUE NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INT NOT NULL,
    grupo VARCHAR(10) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Crear tabla docentes_base si no existe
CREATE TABLE IF NOT EXISTS docentes_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(100) UNIQUE NOT NULL,
    especialidad VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE
);

-- Actualizar tabla asistencias para nueva estructura
-- Primero crear la nueva tabla con la estructura correcta
CREATE TABLE IF NOT EXISTS asistencias_new (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT,
    asignacion_id INT,
    fecha DATE NOT NULL,
    hora_registro TIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'Presente',
    observaciones TEXT,
    FOREIGN KEY (alumno_id) REFERENCES usuarios(id),
    FOREIGN KEY (asignacion_id) REFERENCES asignaciones_materias(id)
);

-- Migrar datos existentes si la tabla asistencias existe
INSERT IGNORE INTO asistencias_new (alumno_id, fecha, hora_registro, estado)
SELECT 
    (SELECT id FROM usuarios WHERE matricula = (SELECT matricula FROM alumnos WHERE id = asistencias.alumno_id LIMIT 1) LIMIT 1) as alumno_id,
    fecha,
    hora,
    'Presente'
FROM asistencias 
WHERE EXISTS (SELECT 1 FROM alumnos WHERE id = asistencias.alumno_id);

-- Renombrar tablas (comentar si quieres mantener los datos antiguos)
-- DROP TABLE IF EXISTS asistencias;
-- RENAME TABLE asistencias_new TO asistencias;

-- Insertar carreras base
INSERT IGNORE INTO carreras (nombre, codigo) VALUES 
('Ingeniería en Sistemas', 'ISC'),
('Logística', 'LOG'),
('Tecnologías de la Información', 'TIC'),
('Mecatrónica', 'MEC'),
('Ingeniería Civil', 'CIV');

-- Insertar materias base para cada carrera
-- Ingeniería en Sistemas
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre) VALUES 
('Programación I', 'PROG1', (SELECT id FROM carreras WHERE codigo = 'ISC'), 1),
('Matemáticas I', 'MAT1', (SELECT id FROM carreras WHERE codigo = 'ISC'), 1),
('Fundamentos de Ingeniería', 'FUND1', (SELECT id FROM carreras WHERE codigo = 'ISC'), 1),
('Programación II', 'PROG2', (SELECT id FROM carreras WHERE codigo = 'ISC'), 2),
('Matemáticas II', 'MAT2', (SELECT id FROM carreras WHERE codigo = 'ISC'), 2),
('Estructura de Datos', 'ED', (SELECT id FROM carreras WHERE codigo = 'ISC'), 3),
('Base de Datos', 'BD', (SELECT id FROM carreras WHERE codigo = 'ISC'), 4),
('Ingeniería de Software', 'IS', (SELECT id FROM carreras WHERE codigo = 'ISC'), 5);

-- Logística
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre) VALUES 
('Fundamentos de Logística', 'FLOG', (SELECT id FROM carreras WHERE codigo = 'LOG'), 1),
('Matemáticas Aplicadas', 'MATA', (SELECT id FROM carreras WHERE codigo = 'LOG'), 1),
('Gestión de Inventarios', 'GI', (SELECT id FROM carreras WHERE codigo = 'LOG'), 2),
('Cadena de Suministro', 'CS', (SELECT id FROM carreras WHERE codigo = 'LOG'), 3),
('Transporte y Distribución', 'TD', (SELECT id FROM carreras WHERE codigo = 'LOG'), 4);

-- TIC
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre) VALUES 
('Introducción a TIC', 'ITIC', (SELECT id FROM carreras WHERE codigo = 'TIC'), 1),
('Redes de Computadoras', 'RC', (SELECT id FROM carreras WHERE codigo = 'TIC'), 2),
('Seguridad Informática', 'SI', (SELECT id FROM carreras WHERE codigo = 'TIC'), 3),
('Administración de Sistemas', 'AS', (SELECT id FROM carreras WHERE codigo = 'TIC'), 4);

-- Migrar datos de alumnos existentes a alumnos_base
INSERT IGNORE INTO alumnos_base (nombre, matricula, carrera, semestre, grupo)
SELECT nombre, matricula, carrera, semestre, grupo 
FROM alumnos 
WHERE EXISTS (SELECT 1 FROM alumnos);

-- Insertar docentes base de ejemplo
INSERT IGNORE INTO docentes_base (nombre, clave, especialidad) VALUES 
('Juan Alberto Martinez Zamora', '123', 'Programación y Desarrollo'),
('Pedro Infante N', '456', 'Matemáticas y Estadística'),
('María González López', '789', 'Base de Datos'),
('Carlos Ruiz Hernández', '101', 'Redes y Seguridad'),
('Ana Patricia Morales', '202', 'Logística y Operaciones');

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_usuarios_uid ON usuarios(uid);
CREATE INDEX IF NOT EXISTS idx_usuarios_matricula ON usuarios(matricula);
CREATE INDEX IF NOT EXISTS idx_usuarios_clave_docente ON usuarios(clave_docente);
CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON asistencias_new(fecha);
CREATE INDEX IF NOT EXISTS idx_asignaciones_dia ON asignaciones_materias(dia_semana);

COMMIT;
