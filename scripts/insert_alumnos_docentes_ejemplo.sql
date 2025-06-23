-- =====================================================
-- INSERCIÓN DE ALUMNOS Y DOCENTES DE EJEMPLO
-- Sistema de Control de Asistencias RFID
-- =====================================================

-- =====================================================
-- INSERTAR ALUMNOS BASE
-- =====================================================

INSERT IGNORE INTO alumnos_base (nombre, matricula, carrera, semestre, grupo, activo) VALUES
-- Ingeniería en Sistemas Computacionales
('Juan Carlos Pérez López', '20240001', 'Ingeniería en Sistemas Computacionales', 1, 'A', TRUE),
('María Elena García Rodríguez', '20240002', 'Ingeniería en Sistemas Computacionales', 1, 'A', TRUE),
('Luis Fernando Martínez Silva', '20240003', 'Ingeniería en Sistemas Computacionales', 2, 'A', TRUE),
('Ana Sofía Hernández Torres', '20240004', 'Ingeniería en Sistemas Computacionales', 2, 'B', TRUE),
('Carlos Eduardo Ramírez Flores', '20240005', 'Ingeniería en Sistemas Computacionales', 3, 'A', TRUE),
('Diana Patricia Morales Castro', '20240006', 'Ingeniería en Sistemas Computacionales', 3, 'A', TRUE),
('Roberto Alejandro Jiménez Vega', '20240007', 'Ingeniería en Sistemas Computacionales', 4, 'A', TRUE),
('Gabriela Monserrat Cruz Mendoza', '20240008', 'Ingeniería en Sistemas Computacionales', 4, 'B', TRUE),
('Fernando Javier Sánchez Ruiz', '20240009', 'Ingeniería en Sistemas Computacionales', 5, 'A', TRUE),
('Alejandra Isabel Vargas Ortega', '20240010', 'Ingeniería en Sistemas Computacionales', 5, 'A', TRUE),

-- Ingeniería Industrial
('Miguel Ángel Delgado Herrera', '20240011', 'Ingeniería Industrial', 1, 'A', TRUE),
('Paola Andrea Castillo Moreno', '20240012', 'Ingeniería Industrial', 1, 'A', TRUE),
('Sergio Daniel Aguilar Peña', '20240013', 'Ingeniería Industrial', 2, 'A', TRUE),
('Karla Vanessa Ramos Guerrero', '20240014', 'Ingeniería Industrial', 2, 'A', TRUE),
('Héctor Manuel Espinoza León', '20240015', 'Ingeniería Industrial', 3, 'A', TRUE),
('Claudia Berenice Medina Rojas', '20240016', 'Ingeniería Industrial', 3, 'B', TRUE),
('Arturo Emilio Contreras Valdez', '20240017', 'Ingeniería Industrial', 4, 'A', TRUE),
('Mónica Alejandra Fuentes Campos', '20240018', 'Ingeniería Industrial', 4, 'A', TRUE),
('Raúl Enrique Navarro Domínguez', '20240019', 'Ingeniería Industrial', 5, 'A', TRUE),
('Verónica Guadalupe Salinas Ibarra', '20240020', 'Ingeniería Industrial', 5, 'A', TRUE),

-- Ingeniería Mecatrónica
('Andrés Felipe Cordero Maldonado', '20240021', 'Ingeniería Mecatrónica', 1, 'A', TRUE),
('Natalia Estefanía Paredes Núñez', '20240022', 'Ingeniería Mecatrónica', 1, 'A', TRUE),
('Óscar Iván Mendoza Cabrera', '20240023', 'Ingeniería Mecatrónica', 2, 'A', TRUE),
('Brenda Yazmín Acosta Villanueva', '20240024', 'Ingeniería Mecatrónica', 2, 'A', TRUE),
('Javier Armando Téllez Sandoval', '20240025', 'Ingeniería Mecatrónica', 3, 'A', TRUE),
('Liliana Marisol Cervantes Ríos', '20240026', 'Ingeniería Mecatrónica', 3, 'A', TRUE),
('Gustavo Adolfo Pacheco Miranda', '20240027', 'Ingeniería Mecatrónica', 4, 'A', TRUE),
('Adriana Leticia Quintero Solís', '20240028', 'Ingeniería Mecatrónica', 4, 'A', TRUE),
('Rodrigo Sebastián Velázquez Cano', '20240029', 'Ingeniería Mecatrónica', 5, 'A', TRUE),
('Esmeralda Jazmín Ochoa Palacios', '20240030', 'Ingeniería Mecatrónica', 5, 'A', TRUE),

-- Ingeniería Civil
('Francisco Javier Morales Estrada', '20240031', 'Ingeniería Civil', 1, 'A', TRUE),
('Dulce María Reyes Barrera', '20240032', 'Ingeniería Civil', 1, 'A', TRUE),
('Emilio Gerardo Lozano Figueroa', '20240033', 'Ingeniería Civil', 2, 'A', TRUE),
('Rocío Esperanza Vázquez Montes', '20240034', 'Ingeniería Civil', 2, 'A', TRUE),
('Ignacio Rubén Herrera Galván', '20240035', 'Ingeniería Civil', 3, 'A', TRUE),
('Maribel Concepción Álvarez Trejo', '20240036', 'Ingeniería Civil', 3, 'A', TRUE),
('Enrique Mauricio Gutiérrez Peña', '20240037', 'Ingeniería Civil', 4, 'A', TRUE),
('Silvia Angélica Romero Chávez', '20240038', 'Ingeniería Civil', 4, 'A', TRUE),
('Armando Nicolás Carrillo Mejía', '20240039', 'Ingeniería Civil', 5, 'A', TRUE),
('Leticia Fernanda Molina Serrano', '20240040', 'Ingeniería Civil', 5, 'A', TRUE),

-- Licenciatura en Administración
('Ricardo Alonso Benítez Cortés', '20240041', 'Licenciatura en Administración', 1, 'A', TRUE),
('Yolanda Patricia Guerrero Soto', '20240042', 'Licenciatura en Administración', 1, 'A', TRUE),
('Mauricio Esteban Padilla Rosales', '20240043', 'Licenciatura en Administración', 2, 'A', TRUE),
('Cecilia Margarita Campos Herrera', '20240044', 'Licenciatura en Administración', 2, 'A', TRUE),
('Víctor Hugo Mendoza Arellano', '20240045', 'Licenciatura en Administración', 3, 'A', TRUE),
('Norma Alicia Peña Villaseñor', '20240046', 'Licenciatura en Administración', 3, 'A', TRUE),
('Jaime Arturo Flores Zamora', '20240047', 'Licenciatura en Administración', 4, 'A', TRUE),
('Gloria Esperanza Ruiz Medrano', '20240048', 'Licenciatura en Administración', 4, 'A', TRUE),
('Alfredo Jesús Ortega Vega', '20240049', 'Licenciatura en Administración', 5, 'A', TRUE),
('Carmen Leticia Jiménez Ávila', '20240050', 'Licenciatura en Administración', 5, 'A', TRUE),

-- Ingeniería Química
('Benjamín Eduardo Torres Maldonado', '20240051', 'Ingeniería Química', 1, 'A', TRUE),
('Mariana Guadalupe Silva Herrera', '20240052', 'Ingeniería Química', 1, 'A', TRUE),
('Cristian Alejandro Moreno Castillo', '20240053', 'Ingeniería Química', 2, 'A', TRUE),
('Fabiola Monserrat Rivas Delgado', '20240054', 'Ingeniería Química', 2, 'A', TRUE),
('Gerardo Antonio Vega Sandoval', '20240055', 'Ingeniería Química', 3, 'A', TRUE),
('Itzel Alejandra Cabrera Núñez', '20240056', 'Ingeniería Química', 3, 'A', TRUE),
('Horacio Ramón Espinoza Guerrero', '20240057', 'Ingeniería Química', 4, 'A', TRUE),
('Karina Beatriz Aguilar Morales', '20240058', 'Ingeniería Química', 4, 'A', TRUE),
('Leonardo Ismael Contreras Rojas', '20240059', 'Ingeniería Química', 5, 'A', TRUE),
('Melissa Fernanda Domínguez León', '20240060', 'Ingeniería Química', 5, 'A', TRUE),

-- Ingeniería en Logística
('Nicolás Efrén Salazar Campos', '20240061', 'Ingeniería en Logística', 1, 'A', TRUE),
('Olivia Esperanza Martín Vázquez', '20240062', 'Ingeniería en Logística', 1, 'A', TRUE),
('Pablo Ernesto Hernández Ibarra', '20240063', 'Ingeniería en Logística', 2, 'A', TRUE),
('Quetzalli Marisol Pérez Solano', '20240064', 'Ingeniería en Logística', 2, 'A', TRUE),
('Ramón Gilberto Rodríguez Fuentes', '20240065', 'Ingeniería en Logística', 3, 'A', TRUE),
('Susana Verónica García Mendoza', '20240066', 'Ingeniería en Logística', 3, 'A', TRUE),
('Tomás Aurelio López Cervantes', '20240067', 'Ingeniería en Logística', 4, 'A', TRUE),
('Úrsula Magdalena Martínez Ochoa', '20240068', 'Ingeniería en Logística', 4, 'A', TRUE),
('Valentín Rodrigo Sánchez Palacios', '20240069', 'Ingeniería en Logística', 5, 'A', TRUE),
('Wendy Alejandra Vargas Estrada', '20240070', 'Ingeniería en Logística', 5, 'A', TRUE),

-- Ingeniería en Tecnologías de la Información y Comunicaciones
('Xavier Emiliano Reyes Barrera', '20240071', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 1, 'A', TRUE),
('Yazmín Guadalupe Lozano Figueroa', '20240072', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 1, 'A', TRUE),
('Zacarías Humberto Vázquez Montes', '20240073', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 2, 'A', TRUE),
('Abigail Esperanza Herrera Galván', '20240074', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 2, 'A', TRUE),
('Bruno Maximiliano Álvarez Trejo', '20240075', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, 'A', TRUE),
('Camila Fernanda Gutiérrez Peña', '20240076', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 3, 'A', TRUE),
('Damián Sebastián Romero Chávez', '20240077', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, 'A', TRUE),
('Estefanía Monserrat Carrillo Mejía', '20240078', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 4, 'A', TRUE),
('Fabricio Alejandro Molina Serrano', '20240079', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 5, 'A', TRUE),
('Giselle Patricia Benítez Cortés', '20240080', 'Ingeniería en Tecnologías de la Información y Comunicaciones', 5, 'A', TRUE);

-- =====================================================
-- INSERTAR DOCENTES BASE
-- =====================================================

INSERT IGNORE INTO docentes_base (nombre, clave, especialidad, activo) VALUES
-- Docentes de Ingeniería en Sistemas Computacionales
('Dr. Juan Alberto Martínez Zamora', 'DOC001', 'Programación y Bases de Datos', TRUE),
('M.C. María Elena Rodríguez Vega', 'DOC002', 'Redes y Telecomunicaciones', TRUE),
('Ing. Carlos Eduardo Sánchez López', 'DOC003', 'Ingeniería de Software', TRUE),
('Dra. Ana Patricia Morales Cruz', 'DOC004', 'Inteligencia Artificial', TRUE),
('M.C. Roberto Alejandro Díaz Herrera', 'DOC005', 'Sistemas Operativos y Arquitectura', TRUE),
('Ing. Diana Gabriela Flores Mendoza', 'DOC006', 'Desarrollo Web y Móvil', TRUE),
('Dr. Fernando Javier Castro Ruiz', 'DOC007', 'Ciberseguridad', TRUE),
('M.C. Alejandra Isabel Vega Ortega', 'DOC008', 'Matemáticas Aplicadas', TRUE),

-- Docentes de Ingeniería Industrial
('Ing. Miguel Ángel Herrera Delgado', 'DOC009', 'Procesos Industriales', TRUE),
('M.C. Paola Andrea Moreno Castillo', 'DOC010', 'Administración de Operaciones', TRUE),
('Dr. Sergio Daniel Peña Aguilar', 'DOC011', 'Control de Calidad', TRUE),
('Ing. Karla Vanessa Guerrero Ramos', 'DOC012', 'Investigación de Operaciones', TRUE),
('M.C. Héctor Manuel León Espinoza', 'DOC013', 'Ergonomía y Seguridad Industrial', TRUE),
('Dra. Claudia Berenice Rojas Medina', 'DOC014', 'Logística y Cadena de Suministro', TRUE),
('Ing. Arturo Emilio Valdez Contreras', 'DOC015', 'Manufactura y Automatización', TRUE),
('M.C. Mónica Alejandra Campos Fuentes', 'DOC016', 'Gestión de Proyectos', TRUE),

-- Docentes de Ingeniería Mecatrónica
('Dr. Andrés Felipe Maldonado Cordero', 'DOC017', 'Robótica y Automatización', TRUE),
('M.C. Natalia Estefanía Núñez Paredes', 'DOC018', 'Control y Instrumentación', TRUE),
('Ing. Óscar Iván Cabrera Mendoza', 'DOC019', 'Manufactura Avanzada', TRUE),
('Dra. Brenda Yazmín Villanueva Acosta', 'DOC020', 'Mecatrónica Aplicada', TRUE),
('M.C. Javier Armando Sandoval Téllez', 'DOC021', 'Electrónica de Potencia', TRUE),
('Ing. Liliana Marisol Ríos Cervantes', 'DOC022', 'Sistemas Hidráulicos y Neumáticos', TRUE),
('Dr. Gustavo Adolfo Miranda Pacheco', 'DOC023', 'Diseño Mecánico', TRUE),
('M.C. Adriana Leticia Solís Quintero', 'DOC024', 'Microcontroladores', TRUE),

-- Docentes de Ingeniería Civil
('Ing. Francisco Javier Estrada Morales', 'DOC025', 'Estructuras y Construcción', TRUE),
('Arq. Dulce María Barrera Reyes', 'DOC026', 'Diseño y Planeación Urbana', TRUE),
('M.C. Emilio Gerardo Figueroa Lozano', 'DOC027', 'Hidráulica y Sanitaria', TRUE),
('Ing. Rocío Esperanza Montes Vázquez', 'DOC028', 'Geotecnia y Pavimentos', TRUE),
('Dr. Ignacio Rubén Galván Herrera', 'DOC029', 'Materiales de Construcción', TRUE),
('M.C. Maribel Concepción Trejo Álvarez', 'DOC030', 'Topografía y Cartografía', TRUE),
('Ing. Enrique Mauricio Peña Gutiérrez', 'DOC031', 'Administración de Obras', TRUE),
('Dra. Silvia Angélica Chávez Romero', 'DOC032', 'Ingeniería Ambiental', TRUE),

-- Docentes de Licenciatura en Administración
('Lic. Ricardo Alonso Cortés Benítez', 'DOC033', 'Administración General', TRUE),
('M.A. Yolanda Patricia Soto Guerrero', 'DOC034', 'Recursos Humanos', TRUE),
('C.P. Mauricio Esteban Rosales Padilla', 'DOC035', 'Finanzas y Contabilidad', TRUE),
('Mtra. Cecilia Margarita Herrera Campos', 'DOC036', 'Mercadotecnia', TRUE),
('Lic. Víctor Hugo Arellano Mendoza', 'DOC037', 'Derecho Empresarial', TRUE),
('M.A. Norma Alicia Villaseñor Peña', 'DOC038', 'Comportamiento Organizacional', TRUE),
('Dr. Jaime Arturo Zamora Flores', 'DOC039', 'Planeación Estratégica', TRUE),
('Mtra. Gloria Esperanza Medrano Ruiz', 'DOC040', 'Desarrollo Organizacional', TRUE),

-- Docentes de Ingeniería Química
('Dr. Benjamín Eduardo Maldonado Torres', 'DOC041', 'Procesos Químicos', TRUE),
('M.C. Mariana Guadalupe Herrera Silva', 'DOC042', 'Termodinámica y Transferencia', TRUE),
('Ing. Cristian Alejandro Castillo Moreno', 'DOC043', 'Reactores y Separación', TRUE),
('Dra. Fabiola Monserrat Delgado Rivas', 'DOC044', 'Ingeniería Ambiental', TRUE),
('M.C. Gerardo Antonio Sandoval Vega', 'DOC045', 'Control de Procesos', TRUE),
('Ing. Itzel Alejandra Núñez Cabrera', 'DOC046', 'Análisis Instrumental', TRUE),
('Dr. Horacio Ramón Guerrero Espinoza', 'DOC047', 'Fisicoquímica', TRUE),
('M.C. Karina Beatriz Morales Aguilar', 'DOC048', 'Seguridad Industrial', TRUE),

-- Docentes de Ingeniería en Logística
('Ing. Nicolás Efrén Campos Salazar', 'DOC049', 'Cadena de Suministro', TRUE),
('M.C. Olivia Esperanza Vázquez Martín', 'DOC050', 'Transporte y Distribución', TRUE),
('Lic. Pablo Ernesto Ibarra Hernández', 'DOC051', 'Gestión de Almacenes', TRUE),
('Mtra. Quetzalli Marisol Solano Pérez', 'DOC052', 'Comercio Internacional', TRUE),
('Ing. Ramón Gilberto Fuentes Rodríguez', 'DOC053', 'Investigación de Operaciones', TRUE),
('M.C. Susana Verónica Mendoza García', 'DOC054', 'Logística Inversa', TRUE),
('Dr. Tomás Aurelio Cervantes López', 'DOC055', 'Optimización de Procesos', TRUE),
('Ing. Úrsula Magdalena Ochoa Martínez', 'DOC056', 'Tecnologías de la Información', TRUE),

-- Docentes de Ingeniería en TIC
('M.C. Xavier Emiliano Barrera Reyes', 'DOC057', 'Desarrollo de Software', TRUE),
('Ing. Yazmín Guadalupe Figueroa Lozano', 'DOC058', 'Redes y Comunicaciones', TRUE),
('Dr. Zacarías Humberto Montes Vázquez', 'DOC059', 'Ciberseguridad', TRUE),
('M.C. Abigail Esperanza Galván Herrera', 'DOC060', 'Bases de Datos', TRUE),
('Ing. Bruno Maximiliano Trejo Álvarez', 'DOC061', 'Programación Web', TRUE),
('Dra. Camila Fernanda Peña Gutiérrez', 'DOC062', 'Inteligencia Artificial', TRUE),
('M.C. Damián Sebastián Chávez Romero', 'DOC063', 'Sistemas Distribuidos', TRUE),
('Ing. Estefanía Monserrat Mejía Carrillo', 'DOC064', 'Desarrollo Móvil', TRUE);

-- =====================================================
-- VERIFICACIÓN DE INSERCIÓN
-- =====================================================

-- Mostrar resumen de alumnos por carrera
SELECT 
    carrera,
    COUNT(*) as total_alumnos,
    GROUP_CONCAT(DISTINCT semestre ORDER BY semestre) as semestres_disponibles,
    GROUP_CONCAT(DISTINCT grupo ORDER BY grupo) as grupos_disponibles
FROM alumnos_base 
WHERE activo = TRUE 
GROUP BY carrera 
ORDER BY carrera;

-- Mostrar resumen de docentes por especialidad
SELECT 
    especialidad,
    COUNT(*) as total_docentes
FROM docentes_base 
WHERE activo = TRUE 
GROUP BY especialidad 
ORDER BY especialidad;

-- Mostrar totales generales
SELECT 
    'ALUMNOS' as tipo,
    COUNT(*) as total
FROM alumnos_base 
WHERE activo = TRUE
UNION ALL
SELECT 
    'DOCENTES' as tipo,
    COUNT(*) as total
FROM docentes_base 
WHERE activo = TRUE
UNION ALL
SELECT 
    'CARRERAS' as tipo,
    COUNT(*) as total
FROM carreras 
WHERE activa = TRUE
UNION ALL
SELECT 
    'MATERIAS' as tipo,
    COUNT(*) as total
FROM materias 
WHERE activa = TRUE;

-- Verificar que todas las carreras tengan alumnos
SELECT 
    c.nombre as carrera,
    COALESCE(COUNT(a.id), 0) as alumnos_registrados
FROM carreras c
LEFT JOIN alumnos_base a ON c.nombre = a.carrera AND a.activo = TRUE
WHERE c.activa = TRUE
GROUP BY c.id, c.nombre
ORDER BY c.nombre;
