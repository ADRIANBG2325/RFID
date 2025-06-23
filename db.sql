-- Insertar carreras
INSERT INTO carrera (nombre) VALUES 
('Ingeniería en sistemas'),
('Logistica'),
('Tics'),
('Mecateonica'),
('Civil');

-- Insertar alumnos base
INSERT INTO alumnobase (nombre, matricula, carrera, semestre, grupo) VALUES 
('Omar Anaya Martinez', '202323367', 'Ingeniería en sistemas', 4, '3402'),
('Laura J. Martinez Estevez', '202328344', 'Logistica', 4, '8402');

-- Insertar docentes base
INSERT INTO docentebase (nombre, clave) VALUES 
('Juan Alberto Martinez Zamora', '123'),
('Pedro Infante N', '456');
