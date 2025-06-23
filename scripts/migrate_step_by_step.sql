-- Migración paso a paso para manejar tablas existentes
-- Ejecutar línea por línea o sección por sección

-- PASO 1: Agregar columnas faltantes a usuarios
ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE;
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;

-- PASO 2: Verificar y actualizar tabla carreras
-- Agregar columna codigo si no existe
ALTER TABLE carreras ADD COLUMN codigo VARCHAR(20);
ALTER TABLE carreras ADD COLUMN activa BOOLEAN DEFAULT TRUE;

-- Actualizar carreras existentes con códigos
UPDATE carreras SET codigo = 'ISC', activa = TRUE WHERE nombre = 'Ingeniería en Sistemas';
UPDATE carreras SET codigo = 'LOG', activa = TRUE WHERE nombre = 'Logística';
UPDATE carreras SET codigo = 'TIC', activa = TRUE WHERE nombre = 'Tecnologías de la Información';
UPDATE carreras SET codigo = 'MEC', activa = TRUE WHERE nombre = 'Mecatrónica';
UPDATE carreras SET codigo = 'CIV', activa = TRUE WHERE nombre = 'Ingeniería Civil';

-- Insertar carreras que no existen
INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES 
('Ingeniería en Sistemas', 'ISC', TRUE),
('Logística', 'LOG', TRUE),
('Tecnologías de la Información', 'TIC', TRUE),
('Mecatrónica', 'MEC', TRUE),
('Ingeniería Civil', 'CIV', TRUE);

-- PASO 3: Actualizar tabla materias
ALTER TABLE materias ADD COLUMN codigo VARCHAR(20);
ALTER TABLE materias ADD COLUMN creditos INT DEFAULT 3;
ALTER TABLE materias ADD COLUMN activa BOOLEAN DEFAULT TRUE;

-- Actualizar materias existentes
UPDATE materias SET activa = TRUE WHERE activa IS NULL;
UPDATE materias SET creditos = 3 WHERE creditos IS NULL;

-- PASO 4: Crear tabla docentes si no existe
CREATE TABLE IF NOT EXISTS docentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE,
    especialidad VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- PASO 5: Crear tabla docente_carreras
CREATE TABLE IF NOT EXISTS docente_carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docente_id INT,
    carrera_id INT,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (docente_id) REFERENCES docentes(id),
    FOREIGN KEY (carrera_id) REFERENCES carreras(id)
);

-- PASO 6: Crear tabla asignaciones_materias
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

-- PASO 7: Crear tablas base
CREATE TABLE IF NOT EXISTS alumnos_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    matricula VARCHAR(100) UNIQUE NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INT NOT NULL,
    grupo VARCHAR(10) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS docentes_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(100) UNIQUE NOT NULL,
    especialidad VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE
);
