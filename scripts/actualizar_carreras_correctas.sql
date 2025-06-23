-- =====================================================
-- ACTUALIZACIÓN CORRECTA DE CARRERAS Y MATERIAS
-- Sistema de Control de Asistencias RFID
-- =====================================================

-- Limpiar datos existentes
DELETE FROM materias WHERE id > 0;
DELETE FROM carreras WHERE id > 0;

-- =====================================================
-- INSERTAR CARRERAS CON IDs CORRECTOS
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
-- MATERIAS - INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIONES (ID: 2)
-- =====================================================

INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Cálculo diferencial', 'ITIC101', 2, 1, 5, TRUE),
('Fundamentos de programación', 'ITIC102', 2, 1, 5, TRUE),
('Matemáticas discretas I', 'ITIC103', 2, 1, 5, TRUE),
('Fundamentos de redes', 'ITIC104', 2, 1, 5, TRUE),
('Telecomunicaciones', 'ITIC105', 2, 1, 5, TRUE),
('Introducción a las TICs', 'ITIC106', 2, 1, 4, TRUE),

-- 2do Semestre
('Cálculo integral', 'ITIC201', 2, 2, 5, TRUE),
('Programación orientada a objetos', 'ITIC202', 2, 2, 5, TRUE),
('Matemáticas discretas II', 'ITIC203', 2, 2, 5, TRUE),
('Redes de comunicación', 'ITIC204', 2, 2, 5, TRUE),
('Probabilidad y estadística', 'ITIC205', 2, 2, 5, TRUE),
('Arquitectura de computadoras', 'ITIC206', 2, 2, 5, TRUE),

-- 3er Semestre
('Matemáticas aplicadas a comunicaciones', 'ITIC301', 2, 3, 5, TRUE),
('Estructura y organización de datos', 'ITIC302', 2, 3, 5, TRUE),
('Sistemas operativos I', 'ITIC303', 2, 3, 4, TRUE),
('Fundamentos de bases de datos', 'ITIC304', 2, 3, 5, TRUE),
('Electricidad y magnetismo', 'ITIC305', 2, 3, 5, TRUE),
('Álgebra lineal', 'ITIC306', 2, 3, 5, TRUE),

-- 4to Semestre
('Análisis de señales y sistemas de comunicación', 'ITIC401', 2, 4, 5, TRUE),
('Programación II', 'ITIC402', 2, 4, 5, TRUE),
('Sistemas operativos II', 'ITIC403', 2, 4, 4, TRUE),
('Taller de bases de datos', 'ITIC404', 2, 4, 4, TRUE),
('Circuitos eléctricos y electrónicos', 'ITIC405', 2, 4, 5, TRUE),
('Ingeniería de software', 'ITIC406', 2, 4, 5, TRUE),

-- 5to Semestre
('Fundamentos de investigación', 'ITIC501', 2, 5, 4, TRUE),
('Redes emergentes', 'ITIC502', 2, 5, 5, TRUE),
('Contabilidad y costos', 'ITIC503', 2, 5, 4, TRUE),
('Bases de datos distribuidas', 'ITIC504', 2, 5, 5, TRUE),
('Taller de ingeniería de software', 'ITIC505', 2, 5, 4, TRUE),
('Ciberseguridad', 'ITIC506', 2, 5, 5, TRUE),

-- 6to Semestre
('Taller de investigación I', 'ITIC601', 2, 6, 4, TRUE),
('Programación web', 'ITIC602', 2, 6, 5, TRUE),
('Administración general', 'ITIC603', 2, 6, 4, TRUE),
('Administración y seguridad de redes', 'ITIC604', 2, 6, 5, TRUE),
('Desarrollo de aplicaciones para dispositivos móviles', 'ITIC605', 2, 6, 5, TRUE),
('Interacción humano computadora', 'ITIC606', 2, 6, 4, TRUE),

-- 7mo Semestre
('Taller de investigación II', 'ITIC701', 2, 7, 4, TRUE),
('Negocios electrónicos I', 'ITIC702', 2, 7, 4, TRUE),
('Matemáticas para la toma de decisiones', 'ITIC703', 2, 7, 5, TRUE),
('Tecnología inalámbrica', 'ITIC704', 2, 7, 5, TRUE),
('Desarrollo de aplicaciones de realidad aumentada', 'ITIC705', 2, 7, 5, TRUE),
('Internet de las cosas', 'ITIC706', 2, 7, 5, TRUE),
('Desarrollo de emprendedores', 'ITIC707', 2, 7, 4, TRUE),

-- 8vo Semestre
('Administración de proyectos', 'ITIC801', 2, 8, 5, TRUE),
('Negocios electrónicos II', 'ITIC802', 2, 8, 4, TRUE),
('Desarrollo sustentable', 'ITIC803', 2, 8, 4, TRUE),
('Auditoría en tecnologías de la información', 'ITIC804', 2, 8, 5, TRUE),
('Ingeniería del conocimiento', 'ITIC805', 2, 8, 5, TRUE),
('Herramientas para el análisis de datos masivos (BIG DATA)', 'ITIC806', 2, 8, 5, TRUE),
('Cómputo en la nube', 'ITIC807', 2, 8, 5, TRUE),

-- 9no Semestre
('Taller de ética', 'ITIC901', 2, 9, 3, TRUE),
('Residencia profesional', 'ITIC902', 2, 9, 10, TRUE);

-- =====================================================
-- MATERIAS PARA OTRAS CARRERAS (EJEMPLOS BÁSICOS)
-- =====================================================

-- INGENIERÍA INDUSTRIAL (ID: 1)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Fundamentos de investigación', 'II101', 1, 1, 4, TRUE),
('Cálculo diferencial', 'II102', 1, 1, 5, TRUE),
('Química', 'II103', 1, 1, 4, TRUE),
('Dibujo industrial', 'II104', 1, 1, 4, TRUE),
('Taller de ética', 'II105', 1, 1, 3, TRUE),
('Introducción a la ingeniería industrial', 'II106', 1, 1, 4, TRUE);

-- INGENIERÍA EN SISTEMAS COMPUTACIONALES (ID: 3)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Cálculo diferencial', 'ISC101', 3, 1, 5, TRUE),
('Fundamentos de programación', 'ISC102', 3, 1, 5, TRUE),
('Matemáticas discretas', 'ISC103', 3, 1, 5, TRUE),
('Taller de ética', 'ISC104', 3, 1, 3, TRUE),
('Química', 'ISC105', 3, 1, 4, TRUE),
('Desarrollo sustentable', 'ISC106', 3, 1, 4, TRUE);

-- INGENIERÍA MECATRÓNICA (ID: 4)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Cálculo diferencial', 'IM101', 4, 1, 5, TRUE),
('Química', 'IM102', 4, 1, 4, TRUE),
('Dibujo asistido por computadora', 'IM103', 4, 1, 4, TRUE),
('Taller de ética', 'IM104', 4, 1, 3, TRUE),
('Fundamentos de investigación', 'IM105', 4, 1, 4, TRUE),
('Metodología y normalización', 'IM106', 4, 1, 4, TRUE);

-- INGENIERÍA CIVIL (ID: 5)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Cálculo diferencial', 'IC101', 5, 1, 5, TRUE),
('Química', 'IC102', 5, 1, 4, TRUE),
('Dibujo en ingeniería civil', 'IC103', 5, 1, 4, TRUE),
('Taller de ética', 'IC104', 5, 1, 3, TRUE),
('Fundamentos de investigación', 'IC105', 5, 1, 4, TRUE),
('Software en ingeniería civil', 'IC106', 5, 1, 4, TRUE);

-- LICENCIATURA EN ADMINISTRACIÓN (ID: 6)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Teoría general de la administración', 'LA101', 6, 1, 5, TRUE),
('Matemáticas aplicadas a la administración', 'LA102', 6, 1, 5, TRUE),
('Contabilidad general', 'LA103', 6, 1, 5, TRUE),
('Taller de ética', 'LA104', 6, 1, 3, TRUE),
('Fundamentos de investigación', 'LA105', 6, 1, 4, TRUE),
('Informática para la administración', 'LA106', 6, 1, 4, TRUE);

-- INGENIERÍA QUÍMICA (ID: 7)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Cálculo diferencial', 'IQ101', 7, 1, 5, TRUE),
('Química inorgánica', 'IQ102', 7, 1, 5, TRUE),
('Programación', 'IQ103', 7, 1, 4, TRUE),
('Taller de ética', 'IQ104', 7, 1, 3, TRUE),
('Fundamentos de investigación', 'IQ105', 7, 1, 4, TRUE),
('Dibujo asistido por computadora', 'IQ106', 7, 1, 4, TRUE);

-- INGENIERÍA EN LOGÍSTICA (ID: 8)
INSERT INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
('Introducción a la ingeniería logística', 'IL101', 8, 1, 4, TRUE),
('Cálculo diferencial', 'IL102', 8, 1, 5, TRUE),
('Química', 'IL103', 8, 1, 4, TRUE),
('Fundamentos de administración', 'IL104', 8, 1, 4, TRUE),
('Economía', 'IL105', 8, 1, 4, TRUE),
('Dibujo asistido por computadora', 'IL106', 8, 1, 4, TRUE);

-- =====================================================
-- VERIFICACIÓN FINAL
-- =====================================================

SELECT 
    c.id,
    c.nombre as carrera,
    COUNT(m.id) as total_materias
FROM carreras c
LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
WHERE c.activa = TRUE
GROUP BY c.id, c.nombre
ORDER BY c.id;
