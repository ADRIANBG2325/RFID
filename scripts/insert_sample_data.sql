-- =====================================================
-- INSERCIÓN DE DATOS DE EJEMPLO
-- Sistema de Control de Asistencias RFID
-- =====================================================

-- Insertar algunos alumnos de ejemplo con el formato de grupo correcto
INSERT IGNORE INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) VALUES
-- Ingeniería Industrial (carrera 1)
('Juan Pérez García', '20230001', 'Ingeniería Industrial', 4, '1401', TRUE),
('María López Hernández', '20230002', 'Ingeniería Industrial', 4, '1402', TRUE),
('Carlos Rodríguez Martín', '20230003', 'Ingeniería Industrial', 6, '1601', TRUE),

-- Ingeniería en TICs (carrera 2)
('Ana Sánchez Torres', '20230004', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),
('Luis González Ruiz', '20230005', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 5, '2501', TRUE),
('Elena Martínez Díaz', '20230006', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 7, '2701', TRUE),

-- Ingeniería en Sistemas (carrera 3)
('Roberto Fernández López', '20230007', 'Ingeniería en Sistemas Computacionales', 4, '3401', TRUE),
('Patricia Jiménez Morales', '20230008', 'Ingeniería en Sistemas Computacionales', 4, '3402', TRUE),
('Miguel Ángel Vargas Cruz', '20230009', 'Ingeniería en Sistemas Computacionales', 6, '3601', TRUE),

-- Ingeniería Mecatrónica (carrera 4)
('Sofía Ramírez Castillo', '20230010', 'Ingeniería Mecatrónica', 5, '4501', TRUE),
('Diego Herrera Vega', '20230011', 'Ingeniería Mecatrónica', 3, '4301', TRUE),
('Valeria Castro Mendoza', '20230012', 'Ingeniería Mecatrónica', 7, '4701', TRUE),

-- Ingeniería Civil (carrera 5)
('Fernando Morales Silva', '20230013', 'Ingeniería Civil', 4, '5401', TRUE),
('Gabriela Ortiz Ramos', '20230014', 'Ingeniería Civil', 6, '5601', TRUE),
('Andrés Delgado Peña', '20230015', 'Ingeniería Civil', 8, '5801', TRUE),

-- Licenciatura en Administración (carrera 6)
('Isabella Guerrero Flores', '20230016', 'Licenciatura en Administración', 3, '6301', TRUE),
('Sebastián Aguilar Romero', '20230017', 'Licenciatura en Administración', 5, '6501', TRUE),
('Camila Mendez Soto', '20230018', 'Licenciatura en Administración', 7, '6701', TRUE),

-- Ingeniería Química (carrera 7)
('Alejandro Ríos Navarro', '20230019', 'Ingeniería Química', 4, '7401', TRUE),
('Natalia Campos Herrera', '20230020', 'Ingeniería Química', 6, '7601', TRUE),
('Emilio Vázquez Luna', '20230021', 'Ingeniería Química', 8, '7801', TRUE),

-- Ingeniería en Logística (carrera 8)
('Daniela Paredes Jiménez', '20230022', 'Ingeniería en Logística', 3, '8301', TRUE),
('Mateo Salinas Cortés', '20230023', 'Ingeniería en Logística', 5, '8501', TRUE),
('Lucía Espinoza Reyes', '20230024', 'Ingeniería en Logística', 7, '8701', TRUE);

-- Insertar algunos docentes de ejemplo
INSERT IGNORE INTO docentes_base (nombre, clave, especialidad, activo) VALUES
('Dr. José Antonio Martínez', 'DOC001', 'Ingeniería Industrial', TRUE),
('Ing. María Elena Rodríguez', 'DOC002', 'Sistemas Computacionales', TRUE),
('Dr. Carlos Alberto Hernández', 'DOC003', 'Mecatrónica', TRUE),
('Ing. Ana Patricia López', 'DOC004', 'Ingeniería Civil', TRUE),
('Lic. Roberto González Vega', 'DOC005', 'Administración', TRUE),
('Dr. Laura Fernández Silva', 'DOC006', 'Ingeniería Química', TRUE),
('Ing. Miguel Ángel Torres', 'DOC007', 'Logística', TRUE),
('Ing. Sandra Morales Cruz', 'DOC008', 'Tecnologías de la Información', TRUE),
('Dr. Fernando Castillo Ruiz', 'DOC009', 'Matemáticas', TRUE),
('Ing. Gabriela Ramírez Díaz', 'DOC010', 'Física', TRUE);

-- Crear algunos grupos específicos
INSERT IGNORE INTO grupos (codigo, carrera_id, semestre, numero_group, activo) VALUES
('1401', 1, 4, 1, TRUE),
('1402', 1, 4, 2, TRUE),
('1601', 1, 6, 1, TRUE),
('2301', 2, 3, 1, TRUE),
('2501', 2, 5, 1, TRUE),
('2701', 2, 7, 1, TRUE),
('3401', 3, 4, 1, TRUE),
('3402', 3, 4, 2, TRUE),
('3601', 3, 6, 1, TRUE),
('4301', 4, 3, 1, TRUE),
('4501', 4, 5, 1, TRUE),
('4701', 4, 7, 1, TRUE),
('5401', 5, 4, 1, TRUE),
('5601', 5, 6, 1, TRUE),
('5801', 5, 8, 1, TRUE),
('6301', 6, 3, 1, TRUE),
('6501', 6, 5, 1, TRUE),
('6701', 6, 7, 1, TRUE),
('7401', 7, 4, 1, TRUE),
('7601', 7, 6, 1, TRUE),
('7801', 7, 8, 1, TRUE),
('8301', 8, 3, 1, TRUE),
('8501', 8, 5, 1, TRUE),
('8701', 8, 7, 1, TRUE);

-- Verificar inserción
SELECT 'Alumnos insertados:' as info, COUNT(*) as total FROM alumnos_base;
SELECT 'Docentes insertados:' as info, COUNT(*) as total FROM docentes_base;
SELECT 'Grupos creados:' as info, COUNT(*) as total FROM grupos;
SELECT 'Carreras disponibles:' as info, COUNT(*) as total FROM carreras;
SELECT 'Materias disponibles:' as info, COUNT(*) as total FROM materias;
