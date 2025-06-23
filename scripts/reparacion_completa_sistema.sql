-- =====================================================
-- SCRIPT DE REPARACIÓN COMPLETA DEL SISTEMA
-- =====================================================

-- Eliminar todas las tablas para empezar limpio
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS asistencias;
DROP TABLE IF EXISTS asignaciones_materias;
DROP TABLE IF EXISTS docente_carreras;
DROP TABLE IF EXISTS docentes;
DROP TABLE IF EXISTS grupos;
DROP TABLE IF EXISTS materias;
DROP TABLE IF EXISTS carreras;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS alumnos_base;
DROP TABLE IF EXISTS docentes_base;

SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- CREAR ESTRUCTURA DE TABLAS CORRECTA
-- =====================================================

-- Tabla de carreras
CREATE TABLE carreras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de materias
CREATE TABLE materias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    carrera_id INT NOT NULL,
    semestre INT NOT NULL,
    creditos INT DEFAULT 3,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id),
    UNIQUE KEY unique_materia_carrera (nombre, carrera_id, semestre)
);

-- Tabla de usuarios (alumnos, docentes, admins)
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uid VARCHAR(100) NOT NULL UNIQUE,
    rol ENUM('alumno', 'docente', 'admin') NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    matricula VARCHAR(100) NULL,
    clave_docente VARCHAR(100) NULL,
    carrera VARCHAR(100) NULL,
    semestre INT NULL,
    grupo VARCHAR(10) NULL,
    contraseña_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de docentes (información adicional)
CREATE TABLE docentes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de relación docente-carrera
CREATE TABLE docente_carreras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    docente_id INT NOT NULL,
    carrera_id INT NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id),
    UNIQUE KEY unique_docente_carrera (docente_id, carrera_id)
);

-- Tabla de asignaciones de materias (horarios)
CREATE TABLE asignaciones_materias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    docente_id INT NOT NULL,
    materia_id INT NOT NULL,
    grupo VARCHAR(20) NOT NULL,
    dia_semana ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    aula VARCHAR(50) NULL,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    UNIQUE KEY unique_horario (docente_id, dia_semana, hora_inicio, hora_fin)
);

-- Tabla de asistencias
CREATE TABLE asistencias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alumno_id INT NOT NULL,
    asignacion_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_registro TIME NOT NULL,
    estado ENUM('Presente', 'Ausente', 'Tardanza', 'Justificado') DEFAULT 'Presente',
    observaciones TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (asignacion_id) REFERENCES asignaciones_materias(id),
    UNIQUE KEY unique_asistencia_dia (alumno_id, asignacion_id, fecha)
);

-- Tabla base de alumnos (datos previos)
CREATE TABLE alumnos_base (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    matricula VARCHAR(100) NOT NULL UNIQUE,
    carrera VARCHAR(100) NOT NULL,
    semestre INT NOT NULL,
    grupo VARCHAR(10) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla base de docentes (datos previos)
CREATE TABLE docentes_base (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(100) NOT NULL UNIQUE,
    especialidad VARCHAR(200) NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de grupos
CREATE TABLE grupos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    carrera_id INT NOT NULL,
    semestre INT NOT NULL,
    numero_grupo INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id),
    UNIQUE KEY unique_grupo (carrera_id, semestre, numero_grupo)
);

-- =====================================================
-- INSERTAR DATOS DE CARRERAS
-- =====================================================

INSERT INTO carreras (id, nombre, codigo, activa) VALUES
(1, 'Ingeniería Industrial', 'II', TRUE),
(2, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 'ITIC', TRUE),
(3, 'Ingeniería en Sistemas Computacionales', 'ISC', TRUE),
(4, 'Ingeniería Mecatrónica', 'IM', TRUE),
(5, 'Ingeniería Civil', 'IC', TRUE),
(6, 'Licenciatura en Administración', 'LA', TRUE),
(7, 'Ingeniería Química', 'IQ', TRUE),
(8, 'Ingeniería en Logística', 'IL', TRUE);

-- =====================================================
-- INSERTAR MATERIAS POR CARRERA
-- =====================================================

-- Materias de Ingeniería Industrial (ID: 1)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Cálculo Diferencial', 'II-101', 1, 1, 5, TRUE),
('Álgebra Lineal', 'II-102', 1, 1, 4, TRUE),
('Química', 'II-103', 1, 1, 4, TRUE),
('Introducción a la Ingeniería Industrial', 'II-104', 1, 1, 3, TRUE),
('Taller de Herramientas Intelectuales', 'II-105', 1, 1, 4, TRUE),

('Cálculo Integral', 'II-201', 1, 2, 5, TRUE),
('Álgebra Lineal', 'II-202', 1, 2, 4, TRUE),
('Probabilidad y Estadística', 'II-203', 1, 2, 4, TRUE),
('Estática', 'II-204', 1, 2, 4, TRUE),
('Fundamentos de Investigación', 'II-205', 1, 2, 4, TRUE);

-- Materias de TICs (ID: 2)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Calculo Diferencial', 'ITIC-101', 2, 1, 5, TRUE),
('Fundamentos de Programacion', 'ITIC-102', 2, 1, 4, TRUE),
('Taller de Etica', 'ITIC-103', 2, 1, 4, TRUE),
('Matematicas Discretas', 'ITIC-104', 2, 1, 4, TRUE),
('Taller de Herramientas Intelectuales', 'ITIC-105', 2, 1, 4, TRUE),

('Calculo Integral', 'ITIC-201', 2, 2, 5, TRUE),
('Programacion Orientada a Objetos', 'ITIC-202', 2, 2, 4, TRUE),
('Contabilidad Financiera', 'ITIC-203', 2, 2, 4, TRUE),
('Algebra Lineal', 'ITIC-204', 2, 2, 4, TRUE),
('Fundamentos de Investigacion', 'ITIC-205', 2, 2, 4, TRUE),

('Calculo Vectorial', 'ITIC-301', 2, 3, 5, TRUE),
('Estructura de Datos', 'ITIC-302', 2, 3, 4, TRUE),
('Cultura Empresarial', 'ITIC-303', 2, 3, 4, TRUE),
('Investigacion de Operaciones', 'ITIC-304', 2, 3, 4, TRUE),
('Desarrollo Sustentable', 'ITIC-305', 2, 3, 4, TRUE),

('Ecuaciones Diferenciales', 'ITIC-401', 2, 4, 5, TRUE),
('Metodos Numericos', 'ITIC-402', 2, 4, 4, TRUE),
('Topicos Avanzados de Programacion', 'ITIC-403', 2, 4, 4, TRUE),
('Principios Electricos y Aplicaciones Digitales', 'ITIC-404', 2, 4, 4, TRUE),
('Probabilidad y Estadistica', 'ITIC-405', 2, 4, 4, TRUE);

-- Materias de ISC (ID: 3)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Cálculo Diferencial', 'ISC-101', 3, 1, 5, TRUE),
('Fundamentos de Programación', 'ISC-102', 3, 1, 4, TRUE),
('Matemáticas Discretas', 'ISC-103', 3, 1, 4, TRUE),
('Taller de Ética', 'ISC-104', 3, 1, 4, TRUE),
('Introducción a los Sistemas Computacionales', 'ISC-105', 3, 1, 3, TRUE),

('Cálculo Integral', 'ISC-201', 3, 2, 5, TRUE),
('Programación Orientada a Objetos', 'ISC-202', 3, 2, 4, TRUE),
('Contabilidad Financiera', 'ISC-203', 3, 2, 4, TRUE),
('Álgebra Lineal', 'ISC-204', 3, 2, 4, TRUE),
('Arquitectura de Computadoras', 'ISC-205', 3, 2, 4, TRUE);

-- =====================================================
-- INSERTAR ALUMNOS BASE DE EJEMPLO
-- =====================================================

INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) VALUES
-- Alumnos de TICs 3er semestre grupo 1 (código 2301)
('Juan Carlos Pérez López', '20230001', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),
('María Elena González Martínez', '20230002', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),
('Carlos Alberto Rodríguez Sánchez', '20230003', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),
('Ana Patricia Hernández García', '20230004', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),
('Luis Fernando Torres Morales', '20230005', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),

-- Alumnos de TICs 4to semestre grupo 2 (código 2402)
('Roberto Miguel Jiménez Cruz', '20220001', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, '2402', TRUE),
('Sandra Leticia Vargas Ruiz', '20220002', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, '2402', TRUE),
('Diego Alejandro Mendoza Silva', '20220003', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, '2402', TRUE),

-- Alumnos de ISC 2do semestre grupo 1 (código 3201)
('Fernanda Isabel Castillo Ramírez', '20240001', 'Ingeniería en Sistemas Computacionales', 2, '3201', TRUE),
('Andrés Eduardo Moreno Flores', '20240002', 'Ingeniería en Sistemas Computacionales', 2, '3201', TRUE),

-- Alumnos de Industrial 1er semestre grupo 1 (código 1101)
('Gabriela Monserrat Aguilar Vega', '20240101', 'Ingeniería Industrial', 1, '1101', TRUE),
('Héctor Daniel Ortega Campos', '20240102', 'Ingeniería Industrial', 1, '1101', TRUE);

-- =====================================================
-- INSERTAR DOCENTES BASE DE EJEMPLO
-- =====================================================

INSERT INTO docentes_base (nombre, clave, especialidad, activo) VALUES
('Dr. Miguel Ángel Rodríguez Hernández', 'DOC001', 'Matemáticas Aplicadas', TRUE),
('Ing. Laura Patricia Gómez Sánchez', 'DOC002', 'Programación y Desarrollo de Software', TRUE),
('M.C. José Luis Martínez Torres', 'DOC003', 'Redes y Telecomunicaciones', TRUE),
('Dra. Carmen Elena Vázquez Morales', 'DOC004', 'Bases de Datos y Sistemas de Información', TRUE),
('Ing. Ricardo Alejandro Pérez Jiménez', 'DOC005', 'Ingeniería de Software', TRUE),
('M.C. Ana Sofía Hernández García', 'DOC006', 'Inteligencia Artificial', TRUE),
('Dr. Fernando Gabriel López Cruz', 'DOC007', 'Seguridad Informática', TRUE),
('Ing. Mónica Isabel Ramírez Flores', 'DOC008', 'Desarrollo Web y Móvil', TRUE);

-- =====================================================
-- INSERTAR ADMINISTRADOR POR DEFECTO
-- =====================================================

INSERT INTO usuarios (uid, rol, nombre, clave_docente, contraseña_hash, activo) VALUES
('ADMIN001', 'admin', 'Administrador del Sistema', 'ADMIN_001', '$2b$12$LQv3c1yqBwlVHpPjrPyFUOeCjmVdEYM/f8zTdIVjuuB9LbJw8.9Aq', TRUE);
-- Contraseña: admin123

-- =====================================================
-- CREAR ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

CREATE INDEX idx_usuarios_uid ON usuarios(uid);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);
CREATE INDEX idx_usuarios_matricula ON usuarios(matricula);
CREATE INDEX idx_usuarios_clave_docente ON usuarios(clave_docente);
CREATE INDEX idx_asistencias_fecha ON asistencias(fecha);
CREATE INDEX idx_asistencias_alumno ON asistencias(alumno_id);
CREATE INDEX idx_asignaciones_dia ON asignaciones_materias(dia_semana);
CREATE INDEX idx_asignaciones_grupo ON asignaciones_materias(grupo);

-- =====================================================
-- VERIFICAR DATOS INSERTADOS
-- =====================================================

SELECT 'CARRERAS' as tabla, COUNT(*) as total FROM carreras WHERE activa = TRUE
UNION ALL
SELECT 'MATERIAS' as tabla, COUNT(*) as total FROM materias WHERE activa = TRUE
UNION ALL
SELECT 'ALUMNOS_BASE' as tabla, COUNT(*) as total FROM alumnos_base WHERE activo = TRUE
UNION ALL
SELECT 'DOCENTES_BASE' as tabla, COUNT(*) as total FROM docentes_base WHERE activo = TRUE
UNION ALL
SELECT 'USUARIOS' as tabla, COUNT(*) as total FROM usuarios WHERE activo = TRUE;

-- Mostrar carreras insertadas
SELECT id, nombre, codigo FROM carreras WHERE activa = TRUE ORDER BY id;

-- Mostrar materias de TICs
SELECT m.nombre, m.codigo, m.semestre, c.nombre as carrera 
FROM materias m 
JOIN carreras c ON m.carrera_id = c.id 
WHERE c.id = 2 AND m.activa = TRUE 
ORDER BY m.semestre, m.nombre;
