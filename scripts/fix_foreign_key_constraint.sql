-- Corregir el constraint de foreign key en asignaciones_materias
-- El error indica que está referenciando 'docentes' en lugar de 'docentes_base'

-- Primero, eliminar el constraint existente si existe
ALTER TABLE asignaciones_materias DROP FOREIGN KEY IF EXISTS asignaciones_materias_ibfk_1;

-- Agregar el constraint correcto que referencia docentes_base
ALTER TABLE asignaciones_materias 
ADD CONSTRAINT asignaciones_materias_docente_fk 
FOREIGN KEY (docente_id) REFERENCES docentes_base(id) 
ON DELETE CASCADE ON UPDATE CASCADE;

-- Verificar que la estructura sea correcta
DESCRIBE asignaciones_materias;

-- Mostrar los constraints actuales
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_NAME = 'asignaciones_materias' 
AND CONSTRAINT_SCHEMA = DATABASE();
