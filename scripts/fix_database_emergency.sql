-- =====================================================
-- CORRECCIÓN DE EMERGENCIA - BASE DE DATOS
-- Sistema de Control de Asistencias RFID
-- =====================================================

-- 1. AGREGAR COLUMNAS FALTANTES A LA TABLA USUARIOS
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE;

-- 2. ACTUALIZAR USUARIOS EXISTENTES
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;
UPDATE usuarios SET fecha_registro = CURRENT_TIMESTAMP WHERE fecha_registro IS NULL;

-- 3. VERIFICAR SI HAY USUARIOS (SI NO, CREAR ADMIN DE EMERGENCIA)
DO $$
DECLARE
    user_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM usuarios WHERE rol = 'admin';
    
    IF user_count = 0 THEN
        -- Crear administrador de emergencia
        INSERT INTO usuarios (uid, rol, nombre, clave_docente, contraseña_hash, activo, fecha_registro)
        VALUES (
            'ADMIN_EMERGENCY', 
            'admin', 
            'Administrador de Emergencia', 
            'ADMIN_EMERGENCY',
            '$2b$12$LQv3c1yqBwlVHpPRrGkFUOdHvVp0jM1b3McTyNt7QdHJmOZFjOmjO', -- password: admin123
            TRUE,
            CURRENT_TIMESTAMP
        );
        
        RAISE NOTICE 'Administrador de emergencia creado - UID: ADMIN_EMERGENCY, Password: admin123';
    END IF;
END $$;

-- 4. VERIFICAR ESTRUCTURA DE TABLAS CRÍTICAS
CREATE TABLE IF NOT EXISTS alumnos_base (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    carrera VARCHAR(255) NOT NULL,
    semestre INTEGER NOT NULL,
    grupo VARCHAR(10) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS docentes_base (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    clave VARCHAR(50) UNIQUE NOT NULL,
    especialidad VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. INSERTAR DATOS DE EJEMPLO SI NO EXISTEN
INSERT INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) 
SELECT * FROM (VALUES
    ('Juan Pérez García', '20240001', 'Ingeniería en Sistemas Computacionales', 3, '3301', true),
    ('María López Hernández', '20240002', 'Ingeniería Industrial', 2, '1201', true),
    ('Carlos Rodríguez Martín', '20240003', 'Ingeniería Civil', 4, '5401', true),
    ('Ana Sánchez Torres', '20240004', 'Licenciatura en Administración', 1, '6101', true),
    ('Luis González Ruiz', '20240005', 'Ingeniería Mecatrónica', 3, '4301', true),
    ('Sofia Ramírez Cruz', '20240006', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 2, '2201', true),
    ('Diego Morales Vega', '20240007', 'Ingeniería Química', 1, '7101', true),
    ('Isabella Castro Luna', '20240008', 'Ingeniería en Logística', 3, '8301', true)
) AS v(nombre, matricula, carrera, semestre, grupo, activo)
WHERE NOT EXISTS (SELECT 1 FROM alumnos_base WHERE matricula = v.matricula);

INSERT INTO docentes_base (nombre, clave, especialidad, activo)
SELECT * FROM (VALUES
    ('Dr. Roberto Martínez', 'DOC001', 'Sistemas Computacionales', true),
    ('Ing. Patricia Jiménez', 'DOC002', 'Ingeniería Industrial', true),
    ('M.C. Fernando Castro', 'DOC003', 'Ingeniería Civil', true),
    ('Lic. Carmen Morales', 'DOC004', 'Administración', true),
    ('Dr. Miguel Herrera', 'DOC005', 'Mecatrónica', true),
    ('Ing. Laura Mendoza', 'DOC006', 'Tecnologías de la Información', true),
    ('Dr. Alejandro Ruiz', 'DOC007', 'Ingeniería Química', true),
    ('M.C. Gabriela Torres', 'DOC008', 'Logística', true)
) AS v(nombre, clave, especialidad, activo)
WHERE NOT EXISTS (SELECT 1 FROM docentes_base WHERE clave = v.clave);

-- 6. MOSTRAR RESUMEN
SELECT 
    'USUARIOS' as tabla,
    COUNT(*) as total,
    COUNT(CASE WHEN rol = 'admin' THEN 1 END) as admins,
    COUNT(CASE WHEN rol = 'docente' THEN 1 END) as docentes,
    COUNT(CASE WHEN rol = 'alumno' THEN 1 END) as alumnos
FROM usuarios
UNION ALL
SELECT 
    'ALUMNOS_BASE' as tabla,
    COUNT(*) as total,
    0 as admins,
    0 as docentes,
    COUNT(*) as alumnos
FROM alumnos_base
UNION ALL
SELECT 
    'DOCENTES_BASE' as tabla,
    COUNT(*) as total,
    0 as admins,
    COUNT(*) as docentes,
    0 as alumnos
FROM docentes_base;

COMMIT;
