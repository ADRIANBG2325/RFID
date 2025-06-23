-- =====================================================
-- CORRECCIÓN COMPLETA DE BASE DE DATOS
-- Sistema de Control de Asistencias RFID
-- =====================================================

-- Agregar columna activo a usuarios si no existe
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE;

-- Actualizar todos los usuarios existentes como activos
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;

-- Verificar y corregir numeración de carreras
UPDATE carreras SET id = 1 WHERE nombre = 'Ingeniería Industrial';
UPDATE carreras SET id = 2 WHERE nombre = 'Ingeniería en Tecnologías de la Información y Comunicaciones';
UPDATE carreras SET id = 3 WHERE nombre = 'Ingeniería en Sistemas Computacionales';
UPDATE carreras SET id = 4 WHERE nombre = 'Ingeniería Mecatrónica';
UPDATE carreras SET id = 5 WHERE nombre = 'Ingeniería Civil';
UPDATE carreras SET id = 6 WHERE nombre = 'Licenciatura en Administración';
UPDATE carreras SET id = 7 WHERE nombre = 'Ingeniería Química';
UPDATE carreras SET id = 8 WHERE nombre = 'Ingeniería en Logística';

-- Reiniciar secuencia de carreras
SELECT setval('carreras_id_seq', 8, true);

-- Verificar estructura de tablas críticas
DO $$
BEGIN
    -- Verificar tabla usuarios
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'usuarios' AND column_name = 'activo') THEN
        ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE;
    END IF;
    
    -- Verificar tabla alumnos_base
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                   WHERE table_name = 'alumnos_base') THEN
        CREATE TABLE alumnos_base (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            matricula VARCHAR(50) UNIQUE NOT NULL,
            carrera VARCHAR(255) NOT NULL,
            semestre INTEGER NOT NULL,
            grupo VARCHAR(10) NOT NULL,
            activo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
    
    -- Verificar tabla docentes_base
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                   WHERE table_name = 'docentes_base') THEN
        CREATE TABLE docentes_base (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            clave VARCHAR(50) UNIQUE NOT NULL,
            especialidad VARCHAR(255),
            activo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Insertar datos de ejemplo si las tablas están vacías
INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) 
SELECT * FROM (VALUES
    ('Juan Pérez García', '20240001', 'Ingeniería en Sistemas Computacionales', 3, '3301', true),
    ('María López Hernández', '20240002', 'Ingeniería Industrial', 2, '1201', true),
    ('Carlos Rodríguez Martín', '20240003', 'Ingeniería Civil', 4, '5401', true),
    ('Ana Sánchez Torres', '20240004', 'Licenciatura en Administración', 1, '6101', true),
    ('Luis González Ruiz', '20240005', 'Ingeniería Mecatrónica', 3, '4301', true)
) AS v(nombre, matricula, carrera, semestre, grupo, activo)
WHERE NOT EXISTS (SELECT 1 FROM alumnos_base LIMIT 1);

INSERT INTO docentes_base (nombre, clave, especialidad, activo)
SELECT * FROM (VALUES
    ('Dr. Roberto Martínez', 'DOC001', 'Sistemas Computacionales', true),
    ('Ing. Patricia Jiménez', 'DOC002', 'Ingeniería Industrial', true),
    ('M.C. Fernando Castro', 'DOC003', 'Ingeniería Civil', true),
    ('Lic. Carmen Morales', 'DOC004', 'Administración', true),
    ('Dr. Miguel Herrera', 'DOC005', 'Mecatrónica', true)
) AS v(nombre, clave, especialidad, activo)
WHERE NOT EXISTS (SELECT 1 FROM docentes_base LIMIT 1);

-- Verificar que todas las materias estén correctamente asignadas
SELECT 
    c.nombre as carrera,
    COUNT(m.id) as total_materias
FROM carreras c
LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = true
WHERE c.activa = true
GROUP BY c.id, c.nombre
ORDER BY c.id;

COMMIT;
