-- =====================================================
-- INSERCIÓN COMPLETA DE CARRERAS Y MATERIAS
-- Sistema de Control de Asistencias RFID
-- =====================================================

-- Limpiar datos existentes (opcional)
-- DELETE FROM materias WHERE id > 0;
-- DELETE FROM carreras WHERE id > 0;

-- =====================================================
-- INSERTAR CARRERAS
-- =====================================================

INSERT IGNORE INTO carreras (nombre, codigo, activa) VALUES
('Ingeniería en Sistemas Computacionales', 'ISC', TRUE),
('Ingeniería Industrial', 'II', TRUE),
('Ingeniería Mecatrónica', 'IM', TRUE),
('Ingeniería Civil', 'IC', TRUE),
('Licenciatura en Administración', 'LA', TRUE),
('Ingeniería Química', 'IQ', TRUE),
('Ingeniería en Logística', 'IL', TRUE),
('Ingeniería en Tecnologías de la Información y Comunicaciones', 'ITIC', TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA EN SISTEMAS COMPUTACIONALES
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Cálculo diferencial', 'ISC101', 1, 1, 5, TRUE),
('Fundamentos de programación', 'ISC102', 1, 1, 5, TRUE),
('Desarrollo sustentable', 'ISC103', 1, 1, 4, TRUE),
('Matemáticas discretas', 'ISC104', 1, 1, 5, TRUE),
('Química', 'ISC105', 1, 1, 4, TRUE),
('Taller de ética', 'ISC106', 1, 1, 3, TRUE),

-- 2do Semestre
('Cálculo integral', 'ISC201', 1, 2, 5, TRUE),
('Programación orientada a objetos', 'ISC202', 1, 2, 5, TRUE),
('Taller de administración', 'ISC203', 1, 2, 4, TRUE),
('Álgebra lineal', 'ISC204', 1, 2, 5, TRUE),
('Probabilidad y estadística', 'ISC205', 1, 2, 5, TRUE),
('Física general', 'ISC206', 1, 2, 4, TRUE),

-- 3er Semestre
('Cálculo vectorial', 'ISC301', 1, 3, 5, TRUE),
('Estructura de datos', 'ISC302', 1, 3, 5, TRUE),
('Fundamentos de telecomunicaciones', 'ISC303', 1, 3, 4, TRUE),
('Investigación de operaciones', 'ISC304', 1, 3, 5, TRUE),
('Sistemas operativos I', 'ISC305', 1, 3, 4, TRUE),
('Principios eléctricos y aplicaciones digitales', 'ISC306', 1, 3, 5, TRUE),

-- 4to Semestre
('Ecuaciones diferenciales', 'ISC401', 1, 4, 5, TRUE),
('Métodos numéricos', 'ISC402', 1, 4, 5, TRUE),
('Tópicos avanzados de programación', 'ISC403', 1, 4, 5, TRUE),
('Fundamentos de bases de datos', 'ISC404', 1, 4, 5, TRUE),
('Taller de sistemas operativos', 'ISC405', 1, 4, 4, TRUE),
('Arquitectura de computadoras', 'ISC406', 1, 4, 5, TRUE),
('Taller de ética', 'ISC407', 1, 4, 3, TRUE),

-- 5to Semestre
('Lenguajes y autómatas I', 'ISC501', 1, 5, 5, TRUE),
('Redes computacionales', 'ISC502', 1, 5, 5, TRUE),
('Taller de base de datos', 'ISC503', 1, 5, 4, TRUE),
('Simulación', 'ISC504', 1, 5, 5, TRUE),
('Fundamentos de ingeniería de software', 'ISC505', 1, 5, 4, TRUE),
('Lenguaje de interfaz', 'ISC506', 1, 5, 4, TRUE),
('Contabilidad financiera', 'ISC507', 1, 5, 4, TRUE),

-- 6to Semestre
('Lenguajes y autómatas II', 'ISC601', 1, 6, 5, TRUE),
('Administración de redes', 'ISC602', 1, 6, 5, TRUE),
('Administración de bases de datos', 'ISC603', 1, 6, 5, TRUE),
('Programación web', 'ISC604', 1, 6, 5, TRUE),
('Ingeniería de software', 'ISC605', 1, 6, 5, TRUE),
('Sistemas programables', 'ISC606', 1, 6, 5, TRUE),

-- 7mo Semestre
('Programación lógica y funcional', 'ISC701', 1, 7, 4, TRUE),
('Comunicación y enrutamiento de redes de datos', 'ISC702', 1, 7, 5, TRUE),
('Taller de investigación I', 'ISC703', 1, 7, 4, TRUE),
('Desarrollo de aplicaciones para dispositivos móviles', 'ISC704', 1, 7, 5, TRUE),
('Gestión de proyectos de software', 'ISC705', 1, 7, 4, TRUE),
('Internet de las cosas', 'ISC706', 1, 7, 4, TRUE),
('Graficación', 'ISC707', 1, 7, 4, TRUE),

-- 8vo Semestre
('Inteligencia artificial', 'ISC801', 1, 8, 5, TRUE),
('Ciberseguridad', 'ISC802', 1, 8, 5, TRUE),
('Taller de investigación II', 'ISC803', 1, 8, 4, TRUE),
('Programación reactiva', 'ISC804', 1, 8, 4, TRUE),
('Sistemas distribuidos', 'ISC805', 1, 8, 5, TRUE),
('Cultura empresarial', 'ISC806', 1, 8, 3, TRUE),

-- 9no Semestre
('Residencias profesionales', 'ISC901', 1, 9, 10, TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA INDUSTRIAL
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Fundamentos de investigación', 'II101', 2, 1, 4, TRUE),
('Taller de ética', 'II102', 2, 1, 3, TRUE),
('Cálculo diferencial', 'II103', 2, 1, 5, TRUE),
('Taller de herramientas intelectuales', 'II104', 2, 1, 4, TRUE),
('Química', 'II105', 2, 1, 4, TRUE),
('Dibujo industrial', 'II106', 2, 1, 4, TRUE),

-- 2do Semestre
('Electricidad y electrónica industrial', 'II201', 2, 2, 5, TRUE),
('Propiedades de materiales', 'II202', 2, 2, 4, TRUE),
('Cálculo integral', 'II203', 2, 2, 5, TRUE),
('Análisis de la realidad nacional', 'II204', 2, 2, 4, TRUE),
('Taller de liderazgo', 'II205', 2, 2, 3, TRUE),

-- 3er Semestre
('Metodología y normalización', 'II301', 2, 3, 4, TRUE),
('Álgebra lineal', 'II302', 2, 3, 5, TRUE),
('Cálculo vectorial', 'II303', 2, 3, 5, TRUE),
('Economía', 'II304', 2, 3, 4, TRUE),
('Estadística inferencial I', 'II305', 2, 3, 5, TRUE),
('Estudio de trabajo I', 'II306', 2, 3, 5, TRUE),

-- 4to Semestre
('Proceso de fabricación', 'II401', 2, 4, 5, TRUE),
('Física', 'II402', 2, 4, 4, TRUE),
('Algoritmos y lenguajes de programación', 'II403', 2, 4, 5, TRUE),
('Investigación de operaciones I', 'II404', 2, 4, 5, TRUE),
('Estadística inferencial II', 'II405', 2, 4, 5, TRUE),
('Estudio de trabajo II', 'II406', 2, 4, 5, TRUE),

-- 5to Semestre
('Administración de proyectos', 'II501', 2, 5, 4, TRUE),
('Gestión de costos', 'II502', 2, 5, 4, TRUE),
('Administración de operaciones I', 'II503', 2, 5, 5, TRUE),
('Investigación de operaciones II', 'II504', 2, 5, 5, TRUE),
('Control estadístico de la calidad', 'II505', 2, 5, 5, TRUE),
('Ergonomía', 'II506', 2, 5, 4, TRUE),

-- 6to Semestre
('Taller de investigación I', 'II601', 2, 6, 4, TRUE),
('Investigación económica', 'II602', 2, 6, 4, TRUE),
('Administración de operaciones II', 'II603', 2, 6, 5, TRUE),
('Simulación', 'II604', 2, 6, 5, TRUE),
('Administración del mantenimiento', 'II605', 2, 6, 4, TRUE),
('Mercadotecnia', 'II606', 2, 6, 4, TRUE),

-- 7mo Semestre
('Taller de investigación II', 'II701', 2, 7, 4, TRUE),
('Planeación financiera', 'II702', 2, 7, 4, TRUE),
('Planeación y diseño de instalaciones', 'II703', 2, 7, 5, TRUE),
('Sistema de manufactura', 'II704', 2, 7, 5, TRUE),
('Logística y cadenas de suministro', 'II705', 2, 7, 5, TRUE),
('Gestión de los sistemas de calidad', 'II706', 2, 7, 4, TRUE),

-- 8vo Semestre
('Formulación y evaluación de proyectos', 'II801', 2, 8, 5, TRUE),
('Relaciones industriales', 'II802', 2, 8, 4, TRUE),

-- 9no Semestre
('Residencias profesionales', 'II901', 2, 9, 10, TRUE),
('Especialidad', 'II902', 2, 9, 5, TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA MECATRÓNICA
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Química', 'IM101', 3, 1, 4, TRUE),
('Cálculo diferencial', 'IM102', 3, 1, 5, TRUE),
('Taller de ética', 'IM103', 3, 1, 3, TRUE),
('Dibujo asistido por computadora', 'IM104', 3, 1, 4, TRUE),
('Metodología y normalización', 'IM105', 3, 1, 4, TRUE),
('Fundamentos de investigación', 'IM106', 3, 1, 4, TRUE),

-- 2do Semestre
('Cálculo integral', 'IM201', 3, 2, 5, TRUE),
('Álgebra lineal', 'IM202', 3, 2, 5, TRUE),
('Ciencia e ingeniería de los materiales', 'IM203', 3, 2, 4, TRUE),
('Estadística y control de calidad', 'IM204', 3, 2, 5, TRUE),
('Programación básica', 'IM205', 3, 2, 4, TRUE),
('Administración y contabilidad', 'IM206', 3, 2, 4, TRUE),

-- 3er Semestre
('Cálculo vectorial', 'IM301', 3, 3, 5, TRUE),
('Procesos de fabricación', 'IM302', 3, 3, 5, TRUE),
('Electromagnetismo', 'IM303', 3, 3, 5, TRUE),
('Estática', 'IM304', 3, 3, 5, TRUE),
('Métodos numéricos', 'IM305', 3, 3, 5, TRUE),
('Desarrollo sustentable', 'IM306', 3, 3, 4, TRUE),

-- 4to Semestre
('Ecuaciones diferenciales', 'IM401', 3, 4, 5, TRUE),
('Fundamentos de termodinámica', 'IM402', 3, 4, 5, TRUE),
('Mecánica de materiales', 'IM403', 3, 4, 5, TRUE),
('Dinámica', 'IM404', 3, 4, 5, TRUE),
('Análisis de circuitos electrónicos', 'IM405', 3, 4, 5, TRUE),
('Electrónica analógica', 'IM406', 3, 4, 5, TRUE),

-- 5to Semestre
('Máquinas eléctricas', 'IM501', 3, 5, 5, TRUE),
('Mecanismos', 'IM502', 3, 5, 5, TRUE),
('Análisis de fluidos', 'IM503', 3, 5, 5, TRUE),
('Electrónica digital', 'IM504', 3, 5, 5, TRUE),
('Programación avanzada', 'IM505', 3, 5, 4, TRUE),
('Circuitos hidráulicos y neumáticos', 'IM506', 3, 5, 5, TRUE),

-- 6to Semestre
('Electrónica de potencia aplicada', 'IM601', 3, 6, 5, TRUE),
('Instrumentación', 'IM602', 3, 6, 5, TRUE),
('Diseño de elementos mecánicos', 'IM603', 3, 6, 5, TRUE),
('Vibraciones mecánicas', 'IM604', 3, 6, 5, TRUE),
('Dinámica de sistemas', 'IM605', 3, 6, 5, TRUE),

-- 7mo Semestre
('Mantenimiento', 'IM701', 3, 7, 4, TRUE),
('Manufactura avanzada', 'IM702', 3, 7, 5, TRUE),
('Microcontroladores', 'IM703', 3, 7, 5, TRUE),
('Control', 'IM704', 3, 7, 5, TRUE),
('Manufactura integrada por computadora', 'IM705', 3, 7, 5, TRUE),
('Diseño avanzado y manufactura', 'IM706', 3, 7, 5, TRUE),

-- 8vo Semestre
('Formulación y evaluación de proyectos', 'IM801', 3, 8, 5, TRUE),
('Controladores lógicos programables', 'IM802', 3, 8, 5, TRUE),
('Robótica', 'IM803', 3, 8, 5, TRUE),
('Control robótico', 'IM804', 3, 8, 5, TRUE),
('Automatización industrial', 'IM805', 3, 8, 5, TRUE),
('Instrumentación avanzada', 'IM806', 3, 8, 5, TRUE),

-- 9no Semestre
('Residencia profesional', 'IM901', 3, 9, 10, TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA CIVIL
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Fundamentos de investigación', 'IC101', 4, 1, 4, TRUE),
('Cálculo diferencial', 'IC102', 4, 1, 5, TRUE),
('Taller de ética', 'IC103', 4, 1, 3, TRUE),
('Química', 'IC104', 4, 1, 4, TRUE),
('Software en ingeniería civil', 'IC105', 4, 1, 4, TRUE),
('Dibujo en ingeniería civil', 'IC106', 4, 1, 4, TRUE),
('Tutorías', 'IC107', 4, 1, 1, TRUE),
('Taller de matemáticas I', 'IC108', 4, 1, 3, TRUE),

-- 2do Semestre
('Cálculo vectorial', 'IC201', 4, 2, 5, TRUE),
('Geología', 'IC202', 4, 2, 4, TRUE),
('Probabilidad y estadística', 'IC203', 4, 2, 5, TRUE),
('Topografía', 'IC204', 4, 2, 5, TRUE),
('Materiales y procesos constructivos', 'IC205', 4, 2, 5, TRUE),
('Cálculo integral', 'IC206', 4, 2, 5, TRUE),
('Tutorías II', 'IC207', 4, 2, 1, TRUE),
('Taller de matemáticas II', 'IC208', 4, 2, 3, TRUE),

-- 3er Semestre
('Estática', 'IC301', 4, 3, 5, TRUE),
('Ecuaciones diferenciales', 'IC302', 4, 3, 5, TRUE),
('Álgebra lineal', 'IC303', 4, 3, 5, TRUE),
('Carreteras', 'IC304', 4, 3, 5, TRUE),
('Tecnología del concreto', 'IC305', 4, 3, 5, TRUE),
('Sistemas de transporte', 'IC306', 4, 3, 4, TRUE),
('Tutorías III', 'IC307', 4, 3, 1, TRUE),

-- 4to Semestre
('Fundamentos de mecánica de los medios continuos', 'IC401', 4, 4, 5, TRUE),
('Métodos numéricos', 'IC402', 4, 4, 5, TRUE),
('Mecánica de suelos', 'IC403', 4, 4, 5, TRUE),
('Maquinaria pesada y movimiento de tierra', 'IC404', 4, 4, 5, TRUE),
('Dinámica', 'IC405', 4, 4, 5, TRUE),
('Modelos de optimización de recursos', 'IC406', 4, 4, 4, TRUE),
('Tutorías IV', 'IC407', 4, 4, 1, TRUE),

-- 5to Semestre
('Mecánica de materiales', 'IC501', 4, 5, 5, TRUE),
('Desarrollo sustentable', 'IC502', 4, 5, 4, TRUE),
('Mecánica de suelos aplicada', 'IC503', 4, 5, 5, TRUE),
('Costos y presupuestos', 'IC504', 4, 5, 4, TRUE),
('Taller de investigación I', 'IC505', 4, 5, 4, TRUE),
('Hidráulica básica', 'IC506', 4, 5, 5, TRUE),
('Servicio social', 'IC507', 4, 5, 1, TRUE),

-- 6to Semestre
('Análisis estructural', 'IC601', 4, 6, 5, TRUE),
('Instalaciones de los edificios', 'IC602', 4, 6, 4, TRUE),
('Diseño y construcción de pavimentos', 'IC603', 4, 6, 5, TRUE),
('Administración de la construcción', 'IC604', 4, 6, 4, TRUE),
('Hidrología superficial', 'IC605', 4, 6, 5, TRUE),
('Hidráulica de canales', 'IC606', 4, 6, 5, TRUE),
('Servicio social', 'IC607', 4, 6, 1, TRUE),

-- 7mo Semestre
('Análisis estructural avanzado', 'IC701', 4, 7, 5, TRUE),
('Diseño de elementos de concreto reforzado', 'IC702', 4, 7, 5, TRUE),
('Taller de investigación II', 'IC703', 4, 7, 4, TRUE),
('Abastecimiento de agua', 'IC704', 4, 7, 5, TRUE),
('Topografía de obras', 'IC705', 4, 7, 4, TRUE),
('Normatividad y seguridad en la construcción', 'IC706', 4, 7, 4, TRUE),
('Planeación y control de obra', 'IC707', 4, 7, 4, TRUE),

-- 8vo Semestre
('Diseño estructural de cimentaciones', 'IC801', 4, 8, 5, TRUE),
('Diseño de elementos de acero', 'IC802', 4, 8, 5, TRUE),
('Formulación y evaluación de proyectos', 'IC803', 4, 8, 5, TRUE),
('Alcantarillado', 'IC804', 4, 8, 5, TRUE),
('Construcción pesada', 'IC805', 4, 8, 5, TRUE),
('Construcción de estructuras de concreto', 'IC806', 4, 8, 5, TRUE),
('Construcción de estructuras de acero', 'IC807', 4, 8, 5, TRUE),

-- 9no Semestre
('Residencia profesional', 'IC901', 4, 9, 10, TRUE);

-- =====================================================
-- MATERIAS - LICENCIATURA EN ADMINISTRACIÓN
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Teoría general de la administración', 'LA101', 5, 1, 5, TRUE),
('Informática para la administración', 'LA102', 5, 1, 4, TRUE),
('Taller de ética', 'LA103', 5, 1, 3, TRUE),
('Fundamentos de investigación', 'LA104', 5, 1, 4, TRUE),
('Matemáticas aplicadas a la administración', 'LA105', 5, 1, 5, TRUE),
('Contabilidad general', 'LA106', 5, 1, 5, TRUE),

-- 2do Semestre
('Función administrativa I', 'LA201', 5, 2, 5, TRUE),
('Estadística para la administración I', 'LA202', 5, 2, 5, TRUE),
('Derecho laboral y seguridad social', 'LA203', 5, 2, 4, TRUE),
('Comunicación corporativa', 'LA204', 5, 2, 4, TRUE),
('Taller de desarrollo humano', 'LA205', 5, 2, 3, TRUE),
('Costos de manufactura', 'LA206', 5, 2, 5, TRUE),

-- 3er Semestre
('Función administrativa II', 'LA301', 5, 3, 5, TRUE),
('Estadística para la administración II', 'LA302', 5, 3, 5, TRUE),
('Derecho empresarial', 'LA303', 5, 3, 4, TRUE),
('Comportamiento organizacional', 'LA304', 5, 3, 4, TRUE),
('Dinámica social', 'LA305', 5, 3, 4, TRUE),
('Contabilidad general', 'LA306', 5, 3, 5, TRUE),

-- 4to Semestre
('Gestión estratégica del capital humano I', 'LA401', 5, 4, 5, TRUE),
('Procesos estructurales', 'LA402', 5, 4, 4, TRUE),
('Métodos cuantitativos para la administración', 'LA403', 5, 4, 5, TRUE),
('Fundamentos de mercadotecnia', 'LA404', 5, 4, 4, TRUE),
('Economía empresarial', 'LA405', 5, 4, 4, TRUE),
('Matemáticas financieras', 'LA406', 5, 4, 5, TRUE),

-- 5to Semestre
('Gestión estratégica del capital humano II', 'LA501', 5, 5, 5, TRUE),
('Derecho fiscal', 'LA502', 5, 5, 4, TRUE),
('Mezcla de mercadotecnia', 'LA503', 5, 5, 5, TRUE),
('Macroeconomía', 'LA504', 5, 5, 4, TRUE),
('Administración financiera I', 'LA505', 5, 5, 5, TRUE),
('Desarrollo sustentable', 'LA506', 5, 5, 4, TRUE),

-- 6to Semestre
('Gestión de la retribución', 'LA601', 5, 6, 4, TRUE),
('Producción', 'LA602', 5, 6, 5, TRUE),
('Taller de investigación I', 'LA603', 5, 6, 4, TRUE),
('Sistema de información de mercadotecnia', 'LA604', 5, 6, 4, TRUE),
('Innovación y emprendedurismo', 'LA605', 5, 6, 4, TRUE),
('Administración financiera II', 'LA606', 5, 6, 5, TRUE),

-- 7mo Semestre
('Plan de negocios', 'LA701', 5, 7, 5, TRUE),
('Procesos de dirección', 'LA702', 5, 7, 5, TRUE),
('Taller de investigación II', 'LA703', 5, 7, 4, TRUE),
('Administración de la calidad', 'LA704', 5, 7, 4, TRUE),
('Economía internacional', 'LA705', 5, 7, 4, TRUE),
('Diagnósticos y evaluación empresarial', 'LA706', 5, 7, 5, TRUE),

-- 8vo Semestre
('Consulta empresarial', 'LA801', 5, 8, 5, TRUE),
('Formulación y evaluación de proyectos', 'LA802', 5, 8, 5, TRUE),
('Desarrollo organizacional', 'LA803', 5, 8, 4, TRUE),

-- 9no Semestre
('Residencia profesional', 'LA901', 5, 9, 10, TRUE),
('Especialidad', 'LA902', 5, 9, 5, TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA QUÍMICA
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Taller de ética', 'IQ101', 6, 1, 3, TRUE),
('Fundamentos de investigación', 'IQ102', 6, 1, 4, TRUE),
('Cálculo diferencial', 'IQ103', 6, 1, 5, TRUE),
('Química inorgánica', 'IQ104', 6, 1, 5, TRUE),
('Programación', 'IQ105', 6, 1, 4, TRUE),
('Dibujo asistido por computadora', 'IQ106', 6, 1, 4, TRUE),

-- 2do Semestre
('Álgebra lineal', 'IQ201', 6, 2, 5, TRUE),
('Mecánica clásica', 'IQ202', 6, 2, 5, TRUE),
('Cálculo integral', 'IQ203', 6, 2, 5, TRUE),
('Química orgánica I', 'IQ204', 6, 2, 5, TRUE),
('Termodinámica', 'IQ205', 6, 2, 5, TRUE),
('Química analítica', 'IQ206', 6, 2, 5, TRUE),

-- 3er Semestre
('Análisis de datos experimentales', 'IQ301', 6, 3, 4, TRUE),
('Electricidad, magnetismo y óptica', 'IQ302', 6, 3, 5, TRUE),
('Cálculo vectorial', 'IQ303', 6, 3, 5, TRUE),
('Química orgánica II', 'IQ304', 6, 3, 5, TRUE),
('Balance de materia y energía', 'IQ305', 6, 3, 5, TRUE),
('Gestión de calidad', 'IQ306', 6, 3, 4, TRUE),

-- 4to Semestre
('Métodos numéricos', 'IQ401', 6, 4, 5, TRUE),
('Ecuaciones diferenciales', 'IQ402', 6, 4, 5, TRUE),
('Mecanismo de transferencia', 'IQ403', 6, 4, 5, TRUE),
('Ingeniería ambiental', 'IQ404', 6, 4, 4, TRUE),
('Fisicoquímica I', 'IQ405', 6, 4, 5, TRUE),
('Análisis instrumental', 'IQ406', 6, 4, 5, TRUE),

-- 5to Semestre
('Taller de investigación I', 'IQ501', 6, 5, 4, TRUE),
('Procesos de separación I', 'IQ502', 6, 5, 5, TRUE),
('Laboratorio integral I', 'IQ503', 6, 5, 4, TRUE),
('Reactores químicos', 'IQ504', 6, 5, 5, TRUE),

-- 6to Semestre
('Taller de investigación I', 'IQ601', 6, 6, 4, TRUE),
('Procesos de separación II', 'IQ602', 6, 6, 5, TRUE),
('Laboratorio integral I', 'IQ603', 6, 6, 4, TRUE),
('Reactores químicos', 'IQ604', 6, 6, 5, TRUE),

-- 7mo Semestre
('Taller de administración', 'IQ701', 6, 7, 4, TRUE),
('Taller de investigación II', 'IQ702', 6, 7, 4, TRUE),
('Procesos de separación III', 'IQ703', 6, 7, 5, TRUE),
('Salud y seguridad en el trabajo', 'IQ704', 6, 7, 4, TRUE),
('Laboratorio integral II', 'IQ705', 6, 7, 4, TRUE),

-- 8vo Semestre
('Laboratorio integral III', 'IQ801', 6, 8, 4, TRUE),
('Instrumentación y control', 'IQ802', 6, 8, 5, TRUE),
('Ingeniería de proyectos', 'IQ803', 6, 8, 5, TRUE),
('Simulación de procesos', 'IQ804', 6, 8, 5, TRUE),

-- 9no Semestre
('Residencia profesional', 'IQ901', 6, 9, 10, TRUE),
('Especialidad', 'IQ902', 6, 9, 5, TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA EN LOGÍSTICA
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Introducción a la ingeniería logística', 'IL101', 7, 1, 4, TRUE),
('Cálculo diferencial', 'IL102', 7, 1, 5, TRUE),
('Química', 'IL103', 7, 1, 4, TRUE),
('Fundamentos de administración', 'IL104', 7, 1, 4, TRUE),
('Dibujo asistido por computadora', 'IL105', 7, 1, 4, TRUE),
('Economía', 'IL106', 7, 1, 4, TRUE),

-- 2do Semestre
('Taller de ética', 'IL201', 7, 2, 3, TRUE),
('Cálculo integral', 'IL202', 7, 2, 5, TRUE),
('Probabilidad y estadística', 'IL203', 7, 2, 5, TRUE),
('Desarrollo humano y organización', 'IL204', 7, 2, 4, TRUE),
('Contabilidad y costos', 'IL205', 7, 2, 5, TRUE),

-- 3er Semestre
('Cadena de suministro', 'IL301', 7, 3, 5, TRUE),
('Álgebra lineal', 'IL302', 7, 3, 5, TRUE),
('Estadística inferencial I', 'IL303', 7, 3, 5, TRUE),
('Fundamentos de derecho', 'IL304', 7, 3, 4, TRUE),
('Mecánica clásica', 'IL305', 7, 3, 5, TRUE),
('Finanzas', 'IL306', 7, 3, 4, TRUE),

-- 4to Semestre
('Compras', 'IL401', 7, 4, 5, TRUE),
('Tipología del producto', 'IL402', 7, 4, 4, TRUE),
('Estadística inferencial II', 'IL403', 7, 4, 5, TRUE),
('Entorno económico', 'IL404', 7, 4, 4, TRUE),
('Tópicos de ingeniería mecánica', 'IL405', 7, 4, 5, TRUE),
('Bases de datos', 'IL406', 7, 4, 4, TRUE),

-- 5to Semestre
('Almacenes', 'IL501', 7, 5, 5, TRUE),
('Inventarios', 'IL502', 7, 5, 5, TRUE),
('Investigación de operaciones I', 'IL503', 7, 5, 5, TRUE),
('Higiene y seguridad', 'IL504', 7, 5, 4, TRUE),
('Procesos de fabricación y manejo de materiales', 'IL505', 7, 5, 5, TRUE),
('Mercadotecnia', 'IL506', 7, 5, 4, TRUE),

-- 6to Semestre
('Tráfico y transporte', 'IL601', 7, 6, 5, TRUE),
('Cultura de calidad', 'IL602', 7, 6, 4, TRUE),
('Investigación de operaciones II', 'IL603', 7, 6, 5, TRUE),
('Desarrollo sustentable', 'IL604', 7, 6, 4, TRUE),
('Taller de investigación I', 'IL605', 7, 6, 4, TRUE),
('Empaque, envase y embalaje', 'IL606', 7, 6, 4, TRUE),

-- 7mo Semestre
('Servicio al cliente', 'IL701', 7, 7, 4, TRUE),
('Programación de procesos productivos', 'IL702', 7, 7, 5, TRUE),
('Modelos de simulación y logística', 'IL703', 7, 7, 5, TRUE),
('Legislación aduanera', 'IL704', 7, 7, 4, TRUE),
('Taller de investigación II', 'IL705', 7, 7, 4, TRUE),
('Ingeniería económica', 'IL706', 7, 7, 5, TRUE),

-- 8vo Semestre
('Innovación', 'IL801', 7, 8, 4, TRUE),
('Comercio internacional', 'IL802', 7, 8, 5, TRUE),
('Formulación y evaluación de proyectos', 'IL803', 7, 8, 5, TRUE),
('Geografía para el transporte', 'IL804', 7, 8, 4, TRUE),

-- 9no Semestre
('Residencia profesional', 'IL901', 7, 9, 10, TRUE),
('Especialidad', 'IL902', 7, 9, 5, TRUE),
('Gestión de proyectos', 'IL903', 7, 9, 5, TRUE);

-- =====================================================
-- MATERIAS - INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIONES
-- =====================================================

INSERT IGNORE INTO materias (nombre, codigo, carrera_id, semestre, creditos, activa) VALUES
-- 1er Semestre
('Cálculo diferencial', 'ITIC101', 8, 1, 5, TRUE),
('Fundamentos de programación', 'ITIC102', 8, 1, 5, TRUE),
('Matemáticas discretas I', 'ITIC103', 8, 1, 5, TRUE),
('Fundamentos de redes', 'ITIC104', 8, 1, 5, TRUE),
('Telecomunicaciones', 'ITIC105', 8, 1, 5, TRUE),
('Introducción a las TICs', 'ITIC106', 8, 1, 4, TRUE),

-- 2do Semestre
('Cálculo integral', 'ITIC201', 8, 2, 5, TRUE),
('Programación orientada a objetos', 'ITIC202', 8, 2, 5, TRUE),
('Matemáticas discretas II', 'ITIC203', 8, 2, 5, TRUE),
('Redes de comunicación', 'ITIC204', 8, 2, 5, TRUE),
('Probabilidad y estadística', 'ITIC205', 8, 2, 5, TRUE),
('Arquitectura de computadoras', 'ITIC206', 8, 2, 5, TRUE),

-- 3er Semestre
('Matemáticas aplicadas a comunicaciones', 'ITIC301', 8, 3, 5, TRUE),
('Estructura y organización de datos', 'ITIC302', 8, 3, 5, TRUE),
('Sistemas operativos I', 'ITIC303', 8, 3, 4, TRUE),
('Fundamentos de bases de datos', 'ITIC304', 8, 3, 5, TRUE),
('Electricidad y magnetismo', 'ITIC305', 8, 3, 5, TRUE),
('Álgebra lineal', 'ITIC306', 8, 3, 5, TRUE),

-- 4to Semestre
('Análisis de señales y sistemas de comunicación', 'ITIC401', 8, 4, 5, TRUE),
('Programación II', 'ITIC402', 8, 4, 5, TRUE),
('Sistemas operativos II', 'ITIC403', 8, 4, 4, TRUE),
('Taller de bases de datos', 'ITIC404', 8, 4, 4, TRUE),
('Circuitos eléctricos y electrónicos', 'ITIC405', 8, 4, 5, TRUE),
('Ingeniería de software', 'ITIC406', 8, 4, 5, TRUE),

-- 5to Semestre
('Fundamentos de investigación', 'ITIC501', 8, 5, 4, TRUE),
('Redes emergentes', 'ITIC502', 8, 5, 5, TRUE),
('Contabilidad y costos', 'ITIC503', 8, 5, 4, TRUE),
('Bases de datos distribuidas', 'ITIC504', 8, 5, 5, TRUE),
('Taller de ingeniería de software', 'ITIC505', 8, 5, 4, TRUE),
('Ciberseguridad', 'ITIC506', 8, 5, 5, TRUE),

-- 6to Semestre
('Taller de investigación I', 'ITIC601', 8, 6, 4, TRUE),
('Programación web', 'ITIC602', 8, 6, 5, TRUE),
('Administración general', 'ITIC603', 8, 6, 4, TRUE),
('Administración y seguridad de redes', 'ITIC604', 8, 6, 5, TRUE),
('Desarrollo de aplicaciones para dispositivos móviles', 'ITIC605', 8, 6, 5, TRUE),
('Interacción humano computadora', 'ITIC606', 8, 6, 4, TRUE),

-- 7mo Semestre
('Taller de investigación II', 'ITIC701', 8, 7, 4, TRUE),
('Negocios electrónicos I', 'ITIC702', 8, 7, 4, TRUE),
('Matemáticas para la toma de decisiones', 'ITIC703', 8, 7, 5, TRUE),
('Tecnología inalámbrica', 'ITIC704', 8, 7, 5, TRUE),
('Desarrollo de aplicaciones de realidad aumentada', 'ITIC705', 8, 7, 5, TRUE),
('Internet de las cosas', 'ITIC706', 8, 7, 5, TRUE),

-- 8vo Semestre
('Administración de proyectos', 'ITIC801', 8, 8, 5, TRUE),
('Negocios electrónicos II', 'ITIC802', 8, 8, 4, TRUE),
('Desarrollo sustentable', 'ITIC803', 8, 8, 4, TRUE),
('Auditoría en tecnologías de la información', 'ITIC804', 8, 8, 5, TRUE),
('Ingeniería del conocimiento', 'ITIC805', 8, 8, 5, TRUE),
('Herramientas para el análisis de datos masivos (BIG DATA)', 'ITIC806', 8, 8, 5, TRUE),

-- 9no Semestre
('Taller de ética', 'ITIC901', 8, 9, 3, TRUE),
('Residencia profesional', 'ITIC902', 8, 9, 10, TRUE);

-- =====================================================
-- VERIFICACIÓN FINAL
-- =====================================================

-- Mostrar resumen de inserción
SELECT 
    c.nombre as carrera,
    COUNT(m.id) as total_materias
FROM carreras c
LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
WHERE c.activa = TRUE
GROUP BY c.id, c.nombre
ORDER BY c.nombre;

-- Mostrar total general
SELECT 
    COUNT(DISTINCT c.id) as total_carreras,
    COUNT(m.id) as total_materias
FROM carreras c
LEFT JOIN materias m ON c.id = m.carrera_id AND m.activa = TRUE
WHERE c.activa = TRUE;
