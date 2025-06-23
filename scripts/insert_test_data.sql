-- Crear datos de prueba para testing

-- Insertar carreras si no existen
INSERT IGNORE INTO carreras (nombre) VALUES 
('Ingeniería en sistemas'),
('Logistica'),
('Tics'),
('Mecateonica'),
('Civil');

-- Insertar alumnos base para pruebas
INSERT IGNORE INTO alumnos (nombre, matricula, carrera, semestre, grupo, contraseña_hash) VALUES 
('Omar Anaya Martinez', '202323367', 'Ingeniería en sistemas', 4, '3402', '$2b$12$dummy_hash'),
('Laura J. Martinez Estevez', '202328344', 'Logistica', 4, '8402', '$2b$12$dummy_hash'),
('Juan Pérez García', '202323001', 'Tics', 2, '2401', '$2b$12$dummy_hash'),
('María González López', '202323002', 'Civil', 3, '3301', '$2b$12$dummy_hash');

-- Insertar algunos docentes base para pruebas
INSERT IGNORE INTO usuarios (uid, rol, nombre, clave_docente, contraseña_hash) VALUES 
('DOCENTE001', 'docente', 'Juan Alberto Martinez Zamora', '123', '$2b$12$dummy_hash'),
('DOCENTE002', 'docente', 'Pedro Infante N', '456', '$2b$12$dummy_hash');
