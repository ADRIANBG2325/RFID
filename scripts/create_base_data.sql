-- Crear datos base del sistema

-- Insertar carreras
INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES 
('Ingeniería en Sistemas Computacionales', 'ISC', 1),
('Logística', 'LOG', 1),
('Tecnologías de la Información y Comunicación', 'TIC', 1),
('Mecatrónica', 'MEC', 1),
('Ingeniería Civil', 'CIV', 1);

-- Insertar materias por carrera
-- Ingeniería en Sistemas (carrera_id = 1)
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES 
('Programación I', 'PROG1', 1, 1, 5, 1),
('Matemáticas Discretas', 'MATD1', 1, 1, 4, 1),
('Fundamentos de Programación', 'FUND1', 1, 1, 5, 1),
('Programación II', 'PROG2', 1, 2, 5, 1),
('Estructura de Datos', 'ESTD1', 1, 2, 5, 1),
('Base de Datos', 'BASD1', 1, 3, 5, 1),
('Programación Web', 'WEBP1', 1, 3, 5, 1),
('Sistemas Operativos', 'SISO1', 1, 4, 4, 1),
('Redes de Computadoras', 'REDC1', 1, 4, 4, 1),
('Ingeniería de Software', 'INGS1', 1, 5, 5, 1);

-- Logística (carrera_id = 2)
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES 
('Fundamentos de Logística', 'FUNL1', 2, 1, 4, 1),
('Matemáticas para Logística', 'MATL1', 2, 1, 4, 1),
('Gestión de Inventarios', 'GESI1', 2, 2, 4, 1),
('Cadena de Suministro', 'CASU1', 2, 2, 5, 1),
('Transporte y Distribución', 'TRDI1', 2, 3, 4, 1),
('Almacenes y Centros de Distribución', 'ALCD1', 2, 3, 4, 1),
('Logística Internacional', 'LOGI1', 2, 4, 5, 1),
('Gestión de Calidad', 'GECA1', 2, 4, 4, 1);

-- TIC (carrera_id = 3)
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES 
('Introducción a las TIC', 'ITIC1', 3, 1, 4, 1),
('Fundamentos de Redes', 'FUNR1', 3, 1, 4, 1),
('Administración de Sistemas', 'ADSI1', 3, 2, 5, 1),
('Seguridad Informática', 'SEGI1', 3, 2, 5, 1),
('Desarrollo de Aplicaciones', 'DEAP1', 3, 3, 5, 1),
('Gestión de Proyectos TIC', 'GPTI1', 3, 3, 4, 1),
('Infraestructura TIC', 'INTI1', 3, 4, 5, 1),
('Auditoría de Sistemas', 'AUSI1', 3, 4, 4, 1);

-- Insertar alumnos base
INSERT IGNORE INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) VALUES 
('Omar Anaya Martinez', '202323367', 'Ingeniería en Sistemas Computacionales', 4, '3402', 1),
('Laura J. Martinez Estevez', '202328344', 'Logística', 4, '8402', 1),
('Juan Pérez García', '202323001', 'Tecnologías de la Información y Comunicación', 2, '2401', 1),
('María González López', '202323002', 'Ingeniería Civil', 3, '3301', 1),
('Carlos Rodríguez Sánchez', '202323003', 'Mecatrónica', 1, '1501', 1),
('Ana Sofía Hernández', '202323004', 'Ingeniería en Sistemas Computacionales', 2, '2402', 1),
('Luis Fernando Torres', '202323005', 'Logística', 3, '3403', 1),
('Gabriela Morales Ruiz', '202323006', 'Tecnologías de la Información y Comunicación', 4, '4401', 1);

-- Insertar docentes base
INSERT IGNORE INTO docentes_base (nombre, clave, especialidad, activo) VALUES 
('Juan Alberto Martinez Zamora', '123', 'Programación y Desarrollo de Software', 1),
('Pedro Infante Navarro', '456', 'Redes y Sistemas Operativos', 1),
('María Elena Vásquez', '789', 'Base de Datos y Análisis de Sistemas', 1),
('Roberto Carlos Mendoza', '101', 'Logística y Cadena de Suministro', 1),
('Ana Patricia Jiménez', '102', 'Gestión de Calidad y Procesos', 1),
('Fernando Alejandro Cruz', '103', 'Seguridad Informática y Redes', 1),
('Claudia Esperanza Moreno', '104', 'Desarrollo Web y Aplicaciones Móviles', 1),
('Miguel Ángel Herrera', '105', 'Matemáticas y Estadística', 1);

-- Crear algunos horarios de ejemplo
-- Primero necesitamos que existan los docentes registrados como usuarios
-- Esto se hará después del registro manual

-- Crear usuario administrador por defecto (opcional)
-- INSERT IGNORE INTO usuarios (uid, rol, nombre, clave_docente, contraseña_hash, activo) VALUES 
-- ('ADMIN001', 'admin', 'Administrador Sistema', 'ADMIN', '$2b$12$dummy_hash_replace_after_registration', 1);
