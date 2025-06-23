-- Arreglar estructura de base de datos para solucionar todos los problemas

-- 1. Verificar y crear columna activo en usuarios si no existe
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE;

-- 2. Actualizar todos los usuarios existentes para que estén activos
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;

-- 3. Verificar estructura de tabla docentes
DESCRIBE docentes;

-- 4. Si la tabla docentes tiene columna especialidad, la eliminamos para que coincida con el modelo
-- ALTER TABLE docentes DROP COLUMN IF EXISTS especialidad;

-- 5. Asegurar que la tabla docentes tenga la estructura correcta
CREATE TABLE IF NOT EXISTS docentes_temp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 6. Migrar datos existentes si los hay
INSERT IGNORE INTO docentes_temp (usuario_id, activo)
SELECT usuario_id, TRUE FROM docentes WHERE usuario_id IS NOT NULL;

-- 7. Renombrar tablas
DROP TABLE IF EXISTS docentes_old;
RENAME TABLE docentes TO docentes_old;
RENAME TABLE docentes_temp TO docentes;

-- 8. Verificar que las carreras estén insertadas correctamente
SELECT COUNT(*) as total_carreras FROM carreras WHERE activa = TRUE;

-- 9. Si no hay carreras, insertarlas
INSERT IGNORE INTO carreras (id, nombre, codigo, activa) VALUES
(1, 'Ingeniería Industrial', 'IND', TRUE),
(2, 'Ingeniería en Tecnologías de la Información y Comunicaciones', 'TICS', TRUE),
(3, 'Ingeniería en Sistemas Computacionales', 'ISC', TRUE),
(4, 'Ingeniería Mecatrónica', 'MEC', TRUE),
(5, 'Ingeniería Civil', 'CIV', TRUE),
(6, 'Licenciatura en Administración', 'ADM', TRUE),
(7, 'Ingeniería Química', 'QUI', TRUE),
(8, 'Ingeniería en Logística', 'LOG', TRUE);

-- 10. Verificar materias de TICs
SELECT COUNT(*) as materias_tics FROM materias WHERE carrera_id = 2 AND activa = TRUE;

-- 11. Insertar materias de TICs si no existen
INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre TICs
('Calculo Diferencial', 'TICS-101', 2, 1, 5, TRUE),
('Algebra Lineal', 'TICS-102', 2, 1, 4, TRUE),
('Quimica', 'TICS-103', 2, 1, 4, TRUE),
('Introduccion a la Programacion', 'TICS-104', 2, 1, 5, TRUE),
('Taller de Etica', 'TICS-105', 2, 1, 3, TRUE),
('Fundamentos de Investigacion', 'TICS-106', 2, 1, 3, TRUE),

-- 2do Semestre TICs
('Calculo Integral', 'TICS-201', 2, 2, 5, TRUE),
('Algebra Superior', 'TICS-202', 2, 2, 4, TRUE),
('Fisica General', 'TICS-203', 2, 2, 4, TRUE),
('Programacion Orientada a Objetos', 'TICS-204', 2, 2, 5, TRUE),
('Contabilidad Financiera', 'TICS-205', 2, 2, 3, TRUE),
('Probabilidad y Estadistica', 'TICS-206', 2, 2, 4, TRUE),

-- 3er Semestre TICs
('Calculo Vectorial', 'TICS-301', 2, 3, 5, TRUE),
('Ecuaciones Diferenciales', 'TICS-302', 2, 3, 4, TRUE),
('Estructura de Datos', 'TICS-303', 2, 3, 5, TRUE),
('Cultura Empresarial', 'TICS-304', 2, 3, 3, TRUE),
('Investigacion de Operaciones', 'TICS-305', 2, 3, 4, TRUE),
('Desarrollo Sustentable', 'TICS-306', 2, 3, 3, TRUE);

-- 12. Crear algunos alumnos de ejemplo con códigos correctos
INSERT IGNORE INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) VALUES
('Juan Carlos Perez Lopez', '20240001', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2301', TRUE),
('Maria Elena Garcia Rodriguez', '20240002', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, '2302', TRUE),
('Luis Fernando Martinez Sanchez', '20240003', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, '2401', TRUE),
('Ana Sofia Hernandez Torres', '20240004', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, '2402', TRUE),
('Carlos Eduardo Lopez Morales', '20240005', 'Ingeniería en Sistemas Computacionales', 5, '3501', TRUE),
('Diana Patricia Ruiz Jimenez', '20240006', 'Ingeniería en Sistemas Computacionales', 5, '3502', TRUE),
('Roberto Miguel Flores Castro', '20240007', 'Ingeniería Industrial', 2, '1201', TRUE),
('Alejandra Beatriz Mendoza Vargas', '20240008', 'Ingeniería Industrial', 2, '1202', TRUE);

-- 13. Crear algunos docentes de ejemplo
INSERT IGNORE INTO docentes_base (nombre, clave, especialidad, activo) VALUES
('Dr. Miguel Angel Rodriguez Perez', 'DOC001', 'Ingeniería de Software', TRUE),
('Mtra. Laura Patricia Gonzalez Martinez', 'DOC002', 'Bases de Datos', TRUE),
('Ing. Jose Luis Hernandez Sanchez', 'DOC003', 'Redes y Comunicaciones', TRUE),
('Dra. Carmen Elena Lopez Torres', 'DOC004', 'Inteligencia Artificial', TRUE),
('Mtro. Ricardo Javier Morales Castro', 'DOC005', 'Programación', TRUE),
('Ing. Ana Maria Jimenez Ruiz', 'DOC006', 'Matemáticas Aplicadas', TRUE);

-- 14. Verificar que todo esté correcto
SELECT 'Carreras' as tabla, COUNT(*) as total FROM carreras WHERE activa = TRUE
UNION ALL
SELECT 'Materias', COUNT(*) FROM materias WHERE activa = TRUE
UNION ALL
SELECT 'Alumnos Base', COUNT(*) FROM alumnos_base WHERE activo = TRUE
UNION ALL
SELECT 'Docentes Base', COUNT(*) FROM docentes_base WHERE activo = TRUE
UNION ALL
SELECT 'Usuarios', COUNT(*) FROM usuarios WHERE activo = TRUE;
