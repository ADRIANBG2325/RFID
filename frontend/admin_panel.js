// Variables globales
let adminData = null
let usuariosData = []
let docentesData = []
let alumnosData = []
let carrerasData = []
let asistenciasDocentesData = []
let materiasData = []
let alumnosSeleccionados = []
const graficos = {}

// Configuración de API
const API_BASE = "http://localhost:8000"

// MAPEO CORRECTO DE CARRERAS
const CARRERAS_MAP = {
  1: "Ingeniería Industrial",
  2: "Ingeniería en Tecnologías de la Información y Comunicaciones",
  3: "Ingeniería en Sistemas Computacionales",
  4: "Ingeniería Mecatrónica",
  5: "Ingeniería Civil",
  6: "Licenciatura en Administración",
  7: "Ingeniería Química",
  8: "Ingeniería en Logística",
}

// DÍAS DE LA SEMANA
const DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

// MATERIAS POR CARRERA Y SEMESTRE - CORREGIDO SEGÚN SEMESTRE ACTUAL
const MATERIAS_POR_CARRERA = {
  1: {
    // Ingeniería Industrial - SEMESTRES PARES para 2025-1
    2: [
      { id: 4, nombre: "Cálculo Integral" },
      { id: 5, nombre: "Física I" },
      { id: 6, nombre: "Probabilidad y Estadística" },
    ],
    4: [
      { id: 10, nombre: "Ecuaciones Diferenciales" },
      { id: 11, nombre: "Mecánica de Fluidos" },
      { id: 12, nombre: "Investigación de Operaciones I" },
    ],
    6: [
      { id: 16, nombre: "Control Estadístico" },
      { id: 17, nombre: "Simulación" },
      { id: 18, nombre: "Ergonomía" },
    ],
    8: [
      { id: 22, nombre: "Proyecto Integrador" },
      { id: 23, nombre: "Administración de Proyectos" },
      { id: 24, nombre: "Ética Profesional" },
    ],
  },
  2: {
    // Ingeniería en TIC - SEMESTRES PARES para 2025-1
    2: [
      { id: 28, nombre: "Matemáticas Discretas Avanzadas" },
      { id: 29, nombre: "Programación Estructurada" },
      { id: 30, nombre: "Fundamentos de Hardware" },
    ],
    4: [
      { id: 31, nombre: "Estructuras de Datos Avanzadas" },
      { id: 32, nombre: "Arquitectura de Computadoras" },
      { id: 33, nombre: "Análisis de Algoritmos" },
    ],
    6: [
      { id: 34, nombre: "Redes de Computadoras" },
      { id: 35, nombre: "Ingeniería de Software" },
      { id: 36, nombre: "Base de Datos Avanzadas" },
    ],
    8: [
      { id: 37, nombre: "Sistemas Operativos" },
      { id: 38, nombre: "Seguridad Informática" },
      { id: 39, nombre: "Proyecto de TIC" },
    ],
  },
  3: {
    // Ingeniería en Sistemas Computacionales - SEMESTRES PARES para 2025-1
    2: [
      { id: 43, nombre: "Matemáticas para Computación II" },
      { id: 44, nombre: "Programación Orientada a Objetos" },
      { id: 45, nombre: "Fundamentos de Sistemas II" },
    ],
    4: [
      { id: 46, nombre: "Algoritmos y Estructuras II" },
      { id: 47, nombre: "Sistemas Digitales Avanzados" },
      { id: 48, nombre: "Métodos Numéricos" },
    ],
    6: [
      { id: 49, nombre: "Arquitectura de Computadoras II" },
      { id: 50, nombre: "Compiladores" },
      { id: 51, nombre: "Sistemas Distribuidos" },
    ],
    8: [
      { id: 52, nombre: "Inteligencia Artificial Aplicada" },
      { id: 53, nombre: "Graficación por Computadora" },
      { id: 54, nombre: "Proyecto de Sistemas" },
    ],
  },
  4: {
    // Ingeniería Mecatrónica - SEMESTRES PARES para 2025-1
    2: [
      { id: 56, nombre: "Mecánica Clásica" },
      { id: 57, nombre: "Circuitos Eléctricos" },
      { id: 58, nombre: "Materiales" },
    ],
    4: [
      { id: 59, nombre: "Control Automático" },
      { id: 60, nombre: "Electrónica Analógica" },
      { id: 61, nombre: "Mecánica de Materiales" },
    ],
    6: [
      { id: 62, nombre: "Robótica" },
      { id: 63, nombre: "Sistemas Embebidos" },
      { id: 64, nombre: "Automatización" },
    ],
    8: [
      { id: 65, nombre: "Proyecto Mecatrónico" },
      { id: 66, nombre: "Manufactura Asistida" },
      { id: 67, nombre: "Instrumentación" },
    ],
  },
  5: {
    // Ingeniería Civil - SEMESTRES PARES para 2025-1
    2: [
      { id: 68, nombre: "Estática" },
      { id: 69, nombre: "Topografía" },
      { id: 70, nombre: "Materiales de Construcción" },
    ],
    4: [
      { id: 71, nombre: "Mecánica de Suelos" },
      { id: 72, nombre: "Hidráulica" },
      { id: 73, nombre: "Estructuras de Concreto" },
    ],
    6: [
      { id: 74, nombre: "Diseño Estructural" },
      { id: 75, nombre: "Vías Terrestres" },
      { id: 76, nombre: "Construcción" },
    ],
    8: [
      { id: 77, nombre: "Proyecto Civil" },
      { id: 78, nombre: "Administración de Obras" },
      { id: 79, nombre: "Impacto Ambiental" },
    ],
  },
  6: {
    // Licenciatura en Administración - SEMESTRES PARES para 2025-1
    2: [
      { id: 81, nombre: "Contabilidad Intermedia" },
      { id: 82, nombre: "Matemáticas Financieras" },
      { id: 83, nombre: "Teoría Administrativa" },
    ],
    4: [
      { id: 84, nombre: "Mercadotecnia Estratégica" },
      { id: 85, nombre: "Finanzas Corporativas" },
      { id: 86, nombre: "Comportamiento Organizacional" },
    ],
    6: [
      { id: 87, nombre: "Investigación de Mercados" },
      { id: 88, nombre: "Derecho Empresarial" },
      { id: 89, nombre: "Planeación Estratégica" },
    ],
    8: [
      { id: 90, nombre: "Emprendimiento" },
      { id: 91, nombre: "Ética Empresarial" },
      { id: 92, nombre: "Proyecto Empresarial" },
    ],
  },
  7: {
    // Ingeniería Química - SEMESTRES PARES para 2025-1
    2: [
      { id: 95, nombre: "Cálculo Integral" },
      { id: 96, nombre: "Química Orgánica I" },
      { id: 97, nombre: "Balance de Materia y Energía" },
    ],
    4: [
      { id: 98, nombre: "Termodinámica Química" },
      { id: 99, nombre: "Fenómenos de Transporte" },
      { id: 100, nombre: "Química Analítica" },
    ],
    6: [
      { id: 101, nombre: "Operaciones Unitarias" },
      { id: 102, nombre: "Control de Procesos" },
      { id: 103, nombre: "Cinética Química" },
    ],
    8: [
      { id: 104, nombre: "Ingeniería Ambiental" },
      { id: 105, nombre: "Biotecnología" },
      { id: 106, nombre: "Proyecto Químico" },
    ],
  },
  8: {
    // Ingeniería en Logística - SEMESTRES PARES para 2025-1
    2: [
      { id: 109, nombre: "Matemáticas Aplicadas II" },
      { id: 110, nombre: "Administración de Operaciones" },
      { id: 111, nombre: "Fundamentos de Logística II" },
    ],
    4: [
      { id: 112, nombre: "Transporte y Distribución" },
      { id: 113, nombre: "Gestión de Almacenes" },
      { id: 114, nombre: "Cadena de Suministro II" },
    ],
    6: [
      { id: 115, nombre: "Sistemas de Información Logística" },
      { id: 116, nombre: "Calidad en Logística" },
      { id: 117, nombre: "Logística Internacional" },
    ],
    8: [
      { id: 118, nombre: "Comercio Exterior" },
      { id: 119, nombre: "Proyecto Logístico" },
      { id: 120, nombre: "Optimización Logística" },
    ],
  },
}

// ==================== GESTIÓN DE SEMESTRES ====================

function obtenerSemestreActual() {
  const ahora = new Date()
  const año = ahora.getFullYear()
  const mes = ahora.getMonth() + 1
  const dia = ahora.getDate()

  if ((mes === 2 && dia >= 1) || (mes >= 3 && mes <= 7)) {
    return {
      numero: 1,
      codigo: `${año}-1`,
      nombre: `${año}-1`,
      fechas: `Febrero - Julio ${año}`,
      inicio: new Date(año, 1, 1),
      fin: new Date(año, 6, 31),
      semestresPermitidos: [2, 4, 6, 8], // SEMESTRES PARES
    }
  } else if (mes >= 8 || mes <= 1) {
    const añoSemestre = mes >= 8 ? año : año - 1
    return {
      numero: 2,
      codigo: `${añoSemestre}-2`,
      nombre: `${añoSemestre}-2`,
      fechas: `Agosto ${añoSemestre} - Febrero ${añoSemestre + 1}`,
      inicio: new Date(añoSemestre, 7, 1),
      fin: new Date(añoSemestre + 1, 1, 28),
      semestresPermitidos: [1, 3, 5, 7, 9], // SEMESTRES IMPARES
    }
  }

  return {
    numero: 0,
    codigo: "Transición",
    nombre: "Período de Transición",
    fechas: "Entre semestres",
    inicio: null,
    fin: null,
    semestresPermitidos: [],
  }
}

// ==================== VALIDACIÓN DE CÓDIGOS DE GRUPO ====================

function validarCodigoGrupo(codigo, carrera, semestre) {
  if (!/^\d{4}$/.test(codigo)) {
    return { valido: false, error: "El código debe tener exactamente 4 dígitos" }
  }

  const carreraCode = Number.parseInt(codigo[0])
  const semestreCode = Number.parseInt(codigo[1])
  const tercerDigito = Number.parseInt(codigo[2])
  const grupoCode = Number.parseInt(codigo[3])

  if (carreraCode !== carrera) {
    return { valido: false, error: `El primer dígito debe ser ${carrera} (carrera seleccionada)` }
  }

  if (semestreCode !== semestre) {
    return { valido: false, error: `El segundo dígito debe ser ${semestre} (semestre seleccionado)` }
  }

  if (tercerDigito !== 0) {
    return { valido: false, error: "El tercer dígito debe ser 0" }
  }

  if (grupoCode < 1 || grupoCode > 4) {
    return { valido: false, error: "El último dígito debe ser entre 1 y 4 (número de grupo)" }
  }

  return { valido: true }
}

// ==================== FUNCIONES DE UTILIDAD ====================

function mostrarMensaje(mensaje, tipo = "info") {
  console.log(`[${tipo.toUpperCase()}] ${mensaje}`)

  let mensajeElement = document.getElementById("mensaje-global")
  if (!mensajeElement) {
    mensajeElement = document.createElement("div")
    mensajeElement.id = "mensaje-global"
    mensajeElement.className = "fixed top-4 right-4 z-50 max-w-md"
    document.body.appendChild(mensajeElement)
  }

  const colores = {
    error: "bg-red-100 text-red-700 border-red-300",
    success: "bg-green-100 text-green-700 border-green-300",
    warning: "bg-yellow-100 text-yellow-700 border-yellow-300",
    info: "bg-blue-100 text-blue-700 border-blue-300",
  }

  mensajeElement.innerHTML = `
    <div class="p-4 rounded-lg border ${colores[tipo]} shadow-lg">
      <div class="flex justify-between items-center">
        <span>${mensaje}</span>
        <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-lg font-bold">&times;</button>
      </div>
    </div>
  `

  setTimeout(() => {
    if (mensajeElement && mensajeElement.parentNode) {
      mensajeElement.remove()
    }
  }, 5000)
}

function verificarAutenticacion() {
  console.log("🔐 Verificando autenticación...")

  const uid = localStorage.getItem("uid")
  const userData = localStorage.getItem("userData")
  const usuarioRol = localStorage.getItem("usuario_rol")

  if (!uid) {
    console.error("❌ No hay UID en localStorage")
    alert("Sesión no encontrada. Redirigiendo al login...")
    window.location.href = "admin_login.html"
    return false
  }

  if (usuarioRol !== "admin") {
    console.error("❌ Usuario no es administrador:", usuarioRol)
    alert("Acceso denegado: Se requieren permisos de administrador")
    window.location.href = "index.html"
    return false
  }

  if (userData) {
    try {
      adminData = JSON.parse(userData)
      if (adminData.rol !== "admin") {
        console.error("❌ Usuario no es administrador en userData:", adminData.rol)
        alert("Acceso denegado: Se requieren permisos de administrador")
        window.location.href = "index.html"
        return false
      }

      const adminNameElement = document.getElementById("admin-name")
      if (adminNameElement) {
        adminNameElement.textContent = adminData.nombre || "Administrador"
      }

      return true
    } catch (error) {
      console.error("❌ Error parseando userData:", error)
      alert("Error en los datos de sesión. Redirigiendo al login...")
      window.location.href = "admin_login.html"
      return false
    }
  } else {
    const nombreUsuario = localStorage.getItem("usuario_nombre") || "Administrador"
    adminData = {
      uid: uid,
      nombre: nombreUsuario,
      rol: "admin",
    }

    const adminNameElement = document.getElementById("admin-name")
    if (adminNameElement) {
      adminNameElement.textContent = nombreUsuario
    }

    return true
  }
}

// ==================== SEGURIDAD: CERRAR SESIÓN AL ACTUALIZAR PÁGINA ====================

function configurarSeguridadSesion() {
  // Detectar actualización de página y cerrar sesión por seguridad
  window.addEventListener("beforeunload", (e) => {
    console.log("🔒 Página actualizándose - Cerrando sesión por seguridad...")

    // Limpiar localStorage
    localStorage.removeItem("uid")
    localStorage.removeItem("userData")
    localStorage.removeItem("usuario_rol")
    localStorage.removeItem("usuario_nombre")

    // No mostrar mensaje de confirmación, solo limpiar
    return undefined
  })

  // También detectar si se intenta navegar fuera de la página
  window.addEventListener("pagehide", (e) => {
    console.log("🔒 Saliendo de la página - Limpiando sesión...")
    localStorage.removeItem("uid")
    localStorage.removeItem("userData")
    localStorage.removeItem("usuario_rol")
    localStorage.removeItem("usuario_nombre")
  })
}

// ==================== INICIALIZACIÓN ====================

function inicializarPanel() {
  console.log("🎯 Inicializando panel...")
  configurarSeguridadSesion() // NUEVA: Configurar seguridad de sesión
  cargarSemestreActual()
  cargarEstadisticas()
  cargarUsuarios()
  cargarDocentes()
  cargarAlumnos()
  cargarCarreras()
  cargarAsistenciasDocentes()
  cargarMaterias()
  configurarEventos()
}

function configurarEventos() {
  console.log("⚙️ Configurando eventos...")

  const botonesSidebar = document.querySelectorAll(".sidebar-button")
  botonesSidebar.forEach((boton) => {
    boton.addEventListener("click", function (e) {
      e.preventDefault()
      const tabName = this.getAttribute("data-tab")
      if (tabName) {
        mostrarTab(tabName)
      }
    })
  })

  const botonCerrarSesion = document.getElementById("cerrar-sesion")
  if (botonCerrarSesion) {
    botonCerrarSesion.addEventListener("click", cerrarSesion)
  }

  console.log("✅ Eventos configurados")
}

// ==================== PETICIONES A LA API ====================

async function peticionAutenticada(endpoint, options = {}) {
  const uid = localStorage.getItem("uid")

  if (!uid) {
    console.error("❌ No hay UID para peticiones autenticadas")
    window.location.href = "admin_login.html"
    return null
  }

  const separator = endpoint.includes("?") ? "&" : "?"
  const url = `${API_BASE}${endpoint}${separator}uid=${encodeURIComponent(uid)}`

  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  }

  console.log(`🌐 Petición autenticada a: ${url}`)

  try {
    const response = await fetch(url, { ...defaultOptions, ...options })
    return response
  } catch (error) {
    console.error("❌ Error en petición:", error)
    mostrarMensaje("Error de conexión con el servidor", "error")
    return null
  }
}

// ==================== CARGA DE DATOS ====================

async function cargarSemestreActual() {
  try {
    console.log("📅 Cargando semestre actual...")

    const response = await peticionAutenticada("/admin/semestre_actual")

    if (response && response.ok) {
      const semestre = await response.json()
      console.log("📅 Semestre actual:", semestre)

      actualizarElementoTexto("semestre-actual", semestre.nombre)
      actualizarElementoTexto("fechas-semestre", semestre.fechas)
      actualizarElementoTexto("semestre-sidebar", semestre.codigo)

      console.log("✅ Semestre actual cargado")
    } else {
      throw new Error("Error en la respuesta de la API")
    }
  } catch (error) {
    console.error("❌ Error cargando semestre actual:", error)
    mostrarMensaje(`Error cargando semestre actual: ${error.message}`, "error")

    const semestreLocal = obtenerSemestreActual()
    actualizarElementoTexto("semestre-actual", semestreLocal.nombre)
    actualizarElementoTexto("fechas-semestre", semestreLocal.fechas)
    actualizarElementoTexto("semestre-sidebar", semestreLocal.codigo)
  }
}

async function cargarEstadisticas() {
  try {
    console.log("📊 Cargando estadísticas del dashboard...")

    const uid = localStorage.getItem("uid")
    const [usuariosResponse, asistenciasHoyResponse] = await Promise.all([
      fetch(`${API_BASE}/usuarios/listar_usuarios/?admin_uid=${uid}`),
      peticionAutenticada("/admin/estadisticas/asistencias_hoy"),
    ])

    let totalUsuarios = 0
    let totalAlumnos = 0
    let totalDocentes = 0
    let asistenciasHoy = 0

    if (usuariosResponse && usuariosResponse.ok) {
      const usuarios = await usuariosResponse.json()
      totalUsuarios = usuarios.length
      totalAlumnos = usuarios.filter((u) => u.rol === "alumno").length
      totalDocentes = usuarios.filter((u) => u.rol === "docente").length
    }

    if (asistenciasHoyResponse && asistenciasHoyResponse.ok) {
      const dataHoy = await asistenciasHoyResponse.json()
      asistenciasHoy = dataHoy.total || 0
    }

    actualizarElementoTexto("total-usuarios", totalUsuarios)
    actualizarElementoTexto("total-alumnos", totalAlumnos)
    actualizarElementoTexto("total-docentes", totalDocentes)
    actualizarElementoTexto("asistencias-hoy", asistenciasHoy)

    actualizarActividadReciente(totalUsuarios, totalAlumnos, totalDocentes, asistenciasHoy)

    console.log("✅ Estadísticas actualizadas")
  } catch (error) {
    console.error("❌ Error cargando estadísticas:", error)
    mostrarMensaje(`Error cargando estadísticas: ${error.message}`, "error")

    actualizarElementoTexto("total-usuarios", "0")
    actualizarElementoTexto("total-alumnos", "0")
    actualizarElementoTexto("total-docentes", "0")
    actualizarElementoTexto("asistencias-hoy", "0")
  }
}

async function cargarUsuarios() {
  try {
    console.log("👥 Cargando usuarios...")

    const uid = localStorage.getItem("uid")
    const response = await fetch(`${API_BASE}/usuarios/listar_usuarios/?admin_uid=${uid}`)

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    usuariosData = await response.json()
    console.log("👥 Usuarios recibidos:", usuariosData)
    mostrarUsuarios(usuariosData)

    actualizarElementoTexto("usuarios-sidebar", usuariosData.length)

    console.log(`✅ ${usuariosData.length} usuarios cargados`)
  } catch (error) {
    console.error("❌ Error cargando usuarios:", error)
    mostrarMensaje(`Error cargando usuarios: ${error.message}`, "error")

    const tbody = document.getElementById("tabla-usuarios")
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="5" class="px-4 py-8 text-center text-red-500">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            Error cargando usuarios: ${error.message}
          </td>
        </tr>
      `
    }
  }
}

async function cargarDocentes() {
  try {
    console.log("👨‍🏫 Cargando docentes...")

    const response = await peticionAutenticada("/admin/docentes_base/")

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    docentesData = await response.json()
    console.log("👨‍🏫 Docentes recibidos:", docentesData)
    mostrarDocentes(docentesData)

    console.log(`✅ ${docentesData.length} docentes cargados`)
  } catch (error) {
    console.error("❌ Error cargando docentes:", error)
    mostrarMensaje(`Error cargando docentes: ${error.message}`, "error")

    const tbody = document.getElementById("tabla-docentes")
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="5" class="px-4 py-8 text-center text-red-500">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            Error cargando docentes: ${error.message}
          </td>
        </tr>
      `
    }
  }
}

async function cargarAlumnos() {
  try {
    console.log("🎓 Cargando alumnos...")

    const response = await peticionAutenticada("/admin/alumnos_base/")

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    alumnosData = await response.json()
    console.log("🎓 Alumnos recibidos:", alumnosData)
    mostrarAlumnos(alumnosData)

    console.log(`✅ ${alumnosData.length} alumnos cargados`)
  } catch (error) {
    console.error("❌ Error cargando alumnos:", error)
    mostrarMensaje(`Error cargando alumnos: ${error.message}`, "error")

    const tbody = document.getElementById("tabla-alumnos")
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="px-4 py-8 text-center text-red-500">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            Error cargando alumnos: ${error.message}
          </td>
        </tr>
      `
    }
  }
}

async function cargarCarreras() {
  try {
    console.log("📚 Cargando carreras...")

    const response = await peticionAutenticada("/admin/carreras/")

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    carrerasData = await response.json()
    console.log("📚 Carreras recibidas:", carrerasData)
    mostrarCarreras(carrerasData)

    console.log(`✅ ${carrerasData.length} carreras cargadas`)
  } catch (error) {
    console.error("❌ Error cargando carreras:", error)
    mostrarMensaje(`Error cargando carreras: ${error.message}`, "error")
  }
}

async function cargarAsistenciasDocentes() {
  try {
    console.log("📊 Cargando asistencias de docentes...")

    const response = await peticionAutenticada("/admin/asistencias_docentes/")

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    asistenciasDocentesData = await response.json()
    console.log("📊 Asistencias de docentes:", asistenciasDocentesData)

    mostrarAsistenciasDocentes(asistenciasDocentesData || [])

    console.log("✅ Asistencias de docentes cargadas")
  } catch (error) {
    console.error("❌ Error cargando asistencias de docentes:", error)
    mostrarMensaje(`Error cargando asistencias de docentes: ${error.message}`, "error")
  }
}

async function cargarMaterias() {
  try {
    console.log("📖 Cargando materias asignadas...")

    const response = await peticionAutenticada("/admin/materias_asignadas/")

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    materiasData = await response.json()
    console.log("📖 Materias recibidas:", materiasData)
    mostrarMaterias(materiasData)

    console.log(`✅ ${materiasData.length} materias cargadas`)
  } catch (error) {
    console.error("❌ Error cargando materias:", error)
    mostrarMensaje(`Error cargando materias: ${error.message}`, "error")

    const container = document.getElementById("lista-materias")
    if (container) {
      container.innerHTML = `
            <div class="text-center py-8 text-red-500">
                <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                <p>Error cargando materias: ${error.message}</p>
            </div>
        `
    }
  }
}

// ==================== FUNCIONES PARA ASIGNACIÓN DE MATERIAS ====================

function cargarSemestresDisponibles() {
  const carreraSelect = document.getElementById("materia-carrera")
  const semestreSelect = document.getElementById("materia-semestre")

  if (!carreraSelect || !semestreSelect) {
    console.error("❌ Elementos del modal no encontrados")
    return
  }

  const carreraId = Number.parseInt(carreraSelect.value)

  if (!carreraId) {
    semestreSelect.innerHTML = '<option value="">Primero selecciona una carrera...</option>'
    semestreSelect.disabled = true
    return
  }

  const semestreActual = obtenerSemestreActual()
  const semestresPermitidos = semestreActual.semestresPermitidos || []

  const semestresCarrera = Object.keys(MATERIAS_POR_CARRERA[carreraId] || {}).map((s) => Number.parseInt(s))
  const semestresValidos = semestresCarrera.filter((s) => semestresPermitidos.includes(s))

  semestreSelect.innerHTML = '<option value="">Seleccionar semestre...</option>'

  if (semestresValidos.length === 0) {
    semestreSelect.innerHTML += '<option value="" disabled>No hay semestres disponibles en este período</option>'
    semestreSelect.disabled = true
    mostrarMensaje(`No hay semestres disponibles para esta carrera en el período ${semestreActual.nombre}`, "warning")
  } else {
    semestresValidos.forEach((semestre) => {
      semestreSelect.innerHTML += `<option value="${semestre}">${semestre}°</option>`
    })
    semestreSelect.disabled = false
  }

  const materiasContainer = document.getElementById("materias-container")
  if (materiasContainer) {
    materiasContainer.innerHTML = '<p class="text-gray-500 text-sm">Selecciona un semestre...</p>'
  }

  const horariosContainer = document.getElementById("horarios-container")
  if (horariosContainer) {
    horariosContainer.style.display = "none"
  }
}

let materiasSeleccionadas = []

function cargarMateriasPorCarrera() {
  const carreraSelect = document.getElementById("materia-carrera")
  const semestreSelect = document.getElementById("materia-semestre")
  const materiasContainer = document.getElementById("materias-container")

  if (!carreraSelect || !semestreSelect || !materiasContainer) {
    console.error("❌ Elementos del modal no encontrados")
    return
  }

  const carreraId = Number.parseInt(carreraSelect.value)
  const semestre = Number.parseInt(semestreSelect.value)

  if (!carreraId || !semestre) {
    materiasContainer.innerHTML = '<p class="text-gray-500 text-sm">Selecciona carrera y semestre...</p>'
    return
  }

  const materias = MATERIAS_POR_CARRERA[carreraId]?.[semestre] || []

  if (materias.length === 0) {
    materiasContainer.innerHTML = '<p class="text-gray-500 text-sm">No hay materias para esta combinación</p>'
    return
  }

  materiasContainer.innerHTML = materias
    .map(
      (materia) => `
        <div class="flex items-center mb-2">
            <input type="checkbox" id="materia-${materia.id}" value="${materia.id}" 
                   class="materia-checkbox mr-2 rounded" onchange="actualizarMateriasSeleccionadas()">
            <label for="materia-${materia.id}" class="text-sm cursor-pointer">${materia.nombre}</label>
        </div>
    `,
    )
    .join("")
}

function actualizarMateriasSeleccionadas() {
  const checkboxes = document.querySelectorAll(".materia-checkbox:checked")
  materiasSeleccionadas = Array.from(checkboxes).map((cb) => ({
    id: Number.parseInt(cb.value),
    nombre: cb.nextElementSibling.textContent,
  }))

  if (materiasSeleccionadas.length > 0) {
    mostrarConfiguracionHorarios()
  } else {
    document.getElementById("horarios-container").style.display = "none"
  }
}

function generarCodigosGrupoValidos(carreraId, semestre) {
  const grupos = []
  for (let i = 1; i <= 4; i++) {
    const codigo = `${carreraId}${semestre}0${i}`
    grupos.push({
      codigo: codigo,
      nombre: `Grupo ${codigo}`,
    })
  }
  return grupos
}

function mostrarConfiguracionHorarios() {
  const carreraId = Number.parseInt(document.getElementById("materia-carrera").value)
  const semestre = Number.parseInt(document.getElementById("materia-semestre").value)
  const gruposValidos = generarCodigosGrupoValidos(carreraId, semestre)

  const horariosContainer = document.getElementById("horarios-materias")

  horariosContainer.innerHTML = materiasSeleccionadas
    .map(
      (materia) => `
        <div class="border border-gray-200 rounded-lg p-4 mb-4">
            <h4 class="font-semibold text-gray-800 mb-3">${materia.nombre}</h4>
            
            <div class="grid grid-cols-2 gap-4 mb-3">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Grupo</label>
                    <select id="grupo-${materia.id}" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="">Seleccionar grupo...</option>
                        ${gruposValidos
                          .map((grupo) => `<option value="${grupo.codigo}">${grupo.nombre}</option>`)
                          .join("")}
                    </select>
                    <p class="text-xs text-gray-500 mt-1">Formato: ${carreraId}${semestre}0X (X = 1-4)</p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Aula</label>
                    <input type="text" id="aula-${materia.id}" placeholder="ej: A-101" 
                           class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
            </div>
            
            <div class="mb-3">
                <label class="block text-sm font-medium text-gray-700 mb-2">Días de la semana</label>
                <div class="grid grid-cols-3 gap-2">
                    ${DIAS_SEMANA.map(
                      (dia) => `
                        <label class="flex items-center">
                            <input type="checkbox" class="dia-checkbox-${materia.id} mr-1 rounded" value="${dia}" onchange="actualizarHorariosPorDia(${materia.id})">
                            <span class="text-sm">${dia}</span>
                        </label>
                    `,
                    ).join("")}
                </div>
            </div>
            
            <div id="horarios-dias-${materia.id}">
                <!-- Se llenarán dinámicamente según días seleccionados -->
            </div>
        </div>
    `,
    )
    .join("")

  document.getElementById("horarios-container").style.display = "block"
}

function actualizarHorariosPorDia(materiaId) {
  const diasSeleccionados = Array.from(document.querySelectorAll(`.dia-checkbox-${materiaId}:checked`)).map(
    (cb) => cb.value,
  )

  const horariosContainer = document.getElementById(`horarios-dias-${materiaId}`)

  if (diasSeleccionados.length === 0) {
    horariosContainer.innerHTML = ""
    return
  }

  horariosContainer.innerHTML = diasSeleccionados
    .map(
      (dia) => `
        <div class="bg-gray-50 rounded-lg p-3 mb-2">
            <h5 class="font-medium text-gray-700 mb-2">${dia}</h5>
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Hora Inicio</label>
                    <select id="inicio-${materiaId}-${dia}" required class="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" onchange="validarHorarios(${materiaId}, '${dia}')">
                        <option value="">Seleccionar...</option>
                        ${Array.from({ length: 14 }, (_, i) => i + 7)
                          .map(
                            (hora) =>
                              `<option value="${hora.toString().padStart(2, "0")}:00">${hora.toString().padStart(2, "0")}:00</option>`,
                          )
                          .join("")}
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Hora Fin</label>
                    <select id="fin-${materiaId}-${dia}" required class="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" onchange="validarHorarios(${materiaId}, '${dia}')">
                        <option value="">Seleccionar...</option>
                        ${Array.from({ length: 15 }, (_, i) => i + 8)
                          .map(
                            (hora) =>
                              `<option value="${hora.toString().padStart(2, "0")}:00">${hora.toString().padStart(2, "0")}:00</option>`,
                          )
                          .join("")}
                    </select>
                </div>
            </div>
            <div id="error-horario-${materiaId}-${dia}" class="text-red-500 text-xs mt-1 hidden"></div>
        </div>
    `,
    )
    .join("")
}

function validarHorarios(materiaId, dia) {
  const inicioSelect = document.getElementById(`inicio-${materiaId}-${dia}`)
  const finSelect = document.getElementById(`fin-${materiaId}-${dia}`)
  const errorDiv = document.getElementById(`error-horario-${materiaId}-${dia}`)

  const horaInicio = inicioSelect.value
  const horaFin = finSelect.value

  if (horaInicio && horaFin) {
    if (horaInicio >= horaFin) {
      errorDiv.textContent = "La hora de fin debe ser posterior a la hora de inicio"
      errorDiv.classList.remove("hidden")
      finSelect.classList.add("border-red-300")
      return false
    } else {
      errorDiv.classList.add("hidden")
      finSelect.classList.remove("border-red-300")
      return true
    }
  }

  return true
}

// ==================== FUNCIONES PARA CREAR ALUMNO ====================

function actualizarSemestresPermitidos() {
  const carreraSelect = document.getElementById("alumno-carrera")
  const semestreSelect = document.getElementById("alumno-semestre")
  const semestreInfo = document.getElementById("semestre-info")

  if (!carreraSelect.value) {
    semestreSelect.innerHTML = '<option value="">Seleccionar...</option>'
    semestreInfo.textContent = "Primero selecciona una carrera"
    return
  }

  const semestreActual = obtenerSemestreActual()
  const semestresPermitidos = semestreActual.semestresPermitidos || []

  semestreSelect.innerHTML = '<option value="">Seleccionar...</option>'

  if (semestresPermitidos.length > 0) {
    semestresPermitidos.forEach((semestre) => {
      semestreSelect.innerHTML += `<option value="${semestre}">${semestre}°</option>`
    })

    const tipoSemestres = semestreActual.numero === 1 ? "pares" : "impares"
    semestreInfo.textContent = `${semestreActual.nombre}: Solo semestres ${tipoSemestres} (${semestresPermitidos.join(", ")})`
  } else {
    semestreInfo.textContent = "Período de transición - Contactar administración"
  }

  document.getElementById("alumno-grupo").value = ""
}

function generarCodigoGrupo() {
  const carreraSelect = document.getElementById("alumno-carrera")
  const semestreSelect = document.getElementById("alumno-semestre")
  const numeroGrupoSelect = document.getElementById("alumno-numero-grupo")
  const grupoInput = document.getElementById("alumno-grupo")

  const carreraId = carreraSelect.value
  const semestre = semestreSelect.value
  const numeroGrupo = numeroGrupoSelect.value

  if (carreraId && semestre && numeroGrupo) {
    const codigoGrupo = `${carreraId}${semestre}0${numeroGrupo}`
    grupoInput.value = codigoGrupo

    const validacion = validarCodigoGrupo(codigoGrupo, Number.parseInt(carreraId), Number.parseInt(semestre))
    if (validacion.valido) {
      grupoInput.className = grupoInput.className.replace("border-red-300", "border-gray-300")
    } else {
      grupoInput.className = grupoInput.className.replace("border-gray-300", "border-red-300")
    }
  } else {
    grupoInput.value = ""
  }
}

// ==================== FUNCIONES DE ASIGNACIÓN Y CREACIÓN ====================

async function asignarMaterias(event) {
  event.preventDefault()

  if (!docenteSeleccionadoId) {
    mostrarMensaje("Error: No hay docente seleccionado", "error")
    return
  }

  if (materiasSeleccionadas.length === 0) {
    mostrarMensaje("Debe seleccionar al menos una materia", "error")
    return
  }

  try {
    mostrarMensaje("Validando asignaciones...", "info")

    const asignaciones = []
    const carreraId = Number.parseInt(document.getElementById("materia-carrera").value)
    const semestre = Number.parseInt(document.getElementById("materia-semestre").value)

    for (const materia of materiasSeleccionadas) {
      const grupoSelect = document.getElementById(`grupo-${materia.id}`)
      const grupo = grupoSelect.value
      const aula = document.getElementById(`aula-${materia.id}`).value

      if (!grupo) {
        throw new Error(`Debe seleccionar un grupo para ${materia.nombre}`)
      }

      const validacion = validarCodigoGrupo(grupo, carreraId, semestre)
      if (!validacion.valido) {
        throw new Error(`${materia.nombre}: ${validacion.error}`)
      }

      const diasSeleccionados = Array.from(document.querySelectorAll(`.dia-checkbox-${materia.id}:checked`)).map(
        (cb) => cb.value,
      )

      if (diasSeleccionados.length === 0) {
        throw new Error(`Debe seleccionar al menos un día para ${materia.nombre}`)
      }

      for (const dia of diasSeleccionados) {
        const horaInicio = document.getElementById(`inicio-${materia.id}-${dia}`).value
        const horaFin = document.getElementById(`fin-${materia.id}-${dia}`).value

        if (!horaInicio || !horaFin) {
          throw new Error(`Debe completar horarios para ${materia.nombre} - ${dia}`)
        }

        if (horaInicio >= horaFin) {
          throw new Error(`${materia.nombre} - ${dia}: La hora de fin debe ser posterior a la hora de inicio`)
        }

        asignaciones.push({
          docente_id: docenteSeleccionadoId,
          materia_id: materia.id,
          carrera_id: carreraId,
          semestre: semestre,
          grupo: grupo,
          dia_semana: dia,
          hora_inicio: horaInicio,
          hora_fin: horaFin,
          aula: aula,
        })
      }
    }

    mostrarMensaje(`Enviando ${asignaciones.length} asignaciones...`, "info")

    for (const asignacion of asignaciones) {
      const response = await peticionAutenticada("/admin/asignar_materia/", {
        method: "POST",
        body: JSON.stringify(asignacion),
      })

      if (!response || !response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP ${response?.status}`)
      }
    }

    mostrarMensaje(`${asignaciones.length} asignaciones creadas correctamente`, "success")
    cerrarModalAsignarMaterias()
    cargarMaterias()
  } catch (error) {
    console.error("❌ Error asignando materias:", error)
    mostrarMensaje(`Error asignando materias: ${error.message}`, "error")
  }
}

async function crearAlumno(event) {
  event.preventDefault()

  try {
    const nombre = document.getElementById("alumno-nombre").value
    const matricula = document.getElementById("alumno-matricula").value
    const carreraId = document.getElementById("alumno-carrera").value
    const carreraNombre = document.getElementById("alumno-carrera").selectedOptions[0].text
    const semestre = Number.parseInt(document.getElementById("alumno-semestre").value)
    const grupo = document.getElementById("alumno-grupo").value

    if (!grupo) {
      mostrarMensaje("El código de grupo no se ha generado correctamente", "error")
      return
    }

    const validacion = validarCodigoGrupo(grupo, Number.parseInt(carreraId), semestre)
    if (!validacion.valido) {
      mostrarMensaje(validacion.error, "error")
      return
    }

    const semestreActual = obtenerSemestreActual()
    if (semestreActual.numero !== 0 && !semestreActual.semestresPermitidos.includes(semestre)) {
      const permitidos = semestreActual.semestresPermitidos.join(", ")
      mostrarMensaje(`En el ${semestreActual.nombre} solo se permiten semestres: ${permitidos}`, "error")
      return
    }

    const alumnoData = {
      nombre: nombre,
      matricula: matricula,
      carrera: carreraNombre,
      semestre: semestre,
      grupo: grupo,
    }

    if (alumnoEditandoId) {
      mostrarMensaje("Actualizando alumno...", "info")

      const response = await peticionAutenticada(`/admin/alumnos_base/${alumnoEditandoId}`, {
        method: "PUT",
        body: JSON.stringify(alumnoData),
      })

      if (!response || !response.ok) {
        throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
      }

      mostrarMensaje(`Alumno "${nombre}" actualizado correctamente`, "success")
    } else {
      mostrarMensaje("Creando alumno...", "info")

      const response = await peticionAutenticada("/admin/alumnos_base/", {
        method: "POST",
        body: JSON.stringify(alumnoData),
      })

      if (!response || !response.ok) {
        throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
      }

      mostrarMensaje(`Alumno "${nombre}" creado correctamente con código de grupo ${grupo}`, "success")
    }

    cerrarModalCrearAlumno()
    cargarAlumnos()
    cargarEstadisticas()
  } catch (error) {
    console.error("❌ Error con alumno:", error)
    mostrarMensaje(`Error: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE ELIMINACIÓN ====================

async function eliminarAlumnoPermanente(alumnoId) {
  try {
    const alumno = alumnosData.find((a) => a.id === alumnoId)
    if (!alumno) {
      mostrarMensaje("Alumno no encontrado", "error")
      return
    }

    if (
      !confirm(
        `¿Estás seguro de que deseas ELIMINAR PERMANENTEMENTE al alumno "${alumno.nombre}"?\n\nEsta acción NO se puede deshacer.`,
      )
    ) {
      return
    }

    mostrarMensaje("Eliminando alumno permanentemente...", "info")

    const response = await peticionAutenticada(`/admin/alumnos_base/${alumnoId}`, {
      method: "DELETE",
    })

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    mostrarMensaje(`Alumno "${alumno.nombre}" eliminado permanentemente`, "success")
    cargarAlumnos()
    cargarEstadisticas()
  } catch (error) {
    console.error("❌ Error eliminando alumno:", error)
    mostrarMensaje(`Error eliminando alumno: ${error.message}`, "error")
  }
}

async function eliminarDocentePermanente(docenteId) {
  try {
    const docente = docentesData.find((d) => d.id === docenteId)
    if (!docente) {
      mostrarMensaje("Docente no encontrado", "error")
      return
    }

    if (
      !confirm(
        `¿Estás seguro de que deseas ELIMINAR PERMANENTEMENTE al docente "${docente.nombre}"?\n\nEsta acción eliminará también todas sus asignaciones de materias y NO se puede deshacer.`,
      )
    ) {
      return
    }

    mostrarMensaje("Eliminando docente permanentemente...", "info")

    const response = await peticionAutenticada(`/admin/docentes_base/${docenteId}`, {
      method: "DELETE",
    })

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    mostrarMensaje(`Docente "${docente.nombre}" eliminado permanentemente`, "success")
    cargarDocentes()
    cargarMaterias()
    cargarEstadisticas()
  } catch (error) {
    console.error("❌ Error eliminando docente:", error)
    mostrarMensaje(`Error eliminando docente: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE EDICIÓN ====================

let alumnoEditandoId = null
let docenteEditandoId = null

async function editarAlumno(alumnoId) {
  try {
    const alumno = alumnosData.find((a) => a.id === alumnoId)
    if (!alumno) {
      mostrarMensaje("Alumno no encontrado", "error")
      return
    }

    alumnoEditandoId = alumnoId

    document.getElementById("alumno-nombre").value = alumno.nombre
    document.getElementById("alumno-matricula").value = alumno.matricula

    const carreraSelect = document.getElementById("alumno-carrera")
    carreraSelect.innerHTML = '<option value="">Seleccionar carrera...</option>'
    Object.entries(CARRERAS_MAP).forEach(([id, nombre]) => {
      const selected = nombre === alumno.carrera ? "selected" : ""
      carreraSelect.innerHTML += `<option value="${id}" ${selected}>${nombre}</option>`
    })

    actualizarSemestresPermitidos()

    setTimeout(() => {
      document.getElementById("alumno-semestre").value = alumno.semestre
      document.getElementById("alumno-grupo").value = alumno.grupo
    }, 100)

    document.querySelector("#modal-crear-alumno h3").textContent = "Editar Alumno"
    document.querySelector("#modal-crear-alumno button[type='submit']").textContent = "Actualizar Alumno"

    document.getElementById("modal-crear-alumno").classList.remove("hidden")
  } catch (error) {
    console.error("❌ Error preparando edición de alumno:", error)
    mostrarMensaje(`Error preparando edición: ${error.message}`, "error")
  }
}

async function editarDocente(docenteId) {
  try {
    const docente = docentesData.find((d) => d.id === docenteId)
    if (!docente) {
      mostrarMensaje("Docente no encontrado", "error")
      return
    }

    docenteEditandoId = docenteId

    document.getElementById("docente-nombre").value = docente.nombre
    document.getElementById("docente-clave").value = docente.clave
    document.getElementById("docente-especialidad").value = docente.especialidad || ""

    document.querySelector("#modal-crear-docente h3").textContent = "Editar Docente"
    document.querySelector("#modal-crear-docente button[type='submit']").textContent = "Actualizar Docente"

    document.getElementById("modal-crear-docente").classList.remove("hidden")
  } catch (error) {
    console.error("❌ Error preparando edición de docente:", error)
    mostrarMensaje(`Error preparando edición: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE ACTUALIZACIÓN DE UI ====================

function actualizarElementoTexto(id, texto) {
  const elemento = document.getElementById(id)
  if (elemento) {
    elemento.textContent = texto
  }
}

function actualizarActividadReciente(totalUsuarios, totalAlumnos, totalDocentes, asistenciasHoy) {
  const actividadElement = document.getElementById("actividad-reciente")
  const semestreActual = obtenerSemestreActual()

  if (actividadElement) {
    actividadElement.innerHTML = `
      <div class="space-y-4">
        <div class="flex items-center p-4 bg-blue-50 rounded-xl border border-blue-200">
          <div class="p-2 bg-blue-100 rounded-lg mr-4">
            <i class="fas fa-calendar-check text-blue-600"></i>
          </div>
          <div>
            <p class="font-medium text-blue-800">Sistema Activo</p>
            <p class="text-sm text-blue-600">Semestre ${semestreActual.nombre} en curso</p>
          </div>
        </div>
        <div class="flex items-center p-4 bg-green-50 rounded-xl border border-green-200">
          <div class="p-2 bg-green-100 rounded-lg mr-4">
            <i class="fas fa-users text-green-600"></i>
          </div>
          <div>
            <p class="font-medium text-green-800">${totalUsuarios} usuarios registrados</p>
            <p class="text-sm text-green-600">${totalAlumnos} alumnos y ${totalDocentes} docentes activos</p>
          </div>
        </div>
        <div class="flex items-center p-4 bg-purple-50 rounded-xl border border-purple-200">
          <div class="p-2 bg-purple-100 rounded-lg mr-4">
            <i class="fas fa-chart-line text-purple-600"></i>
          </div>
          <div>
            <p class="font-medium text-purple-800">${asistenciasHoy} asistencias registradas hoy</p>
            <p class="text-sm text-purple-600">Sistema funcionando correctamente</p>
          </div>
        </div>
      </div>
    `
  }
}

// ==================== NAVEGACIÓN ====================

function mostrarTab(tabName) {
  console.log("📋 Cambiando a tab:", tabName)

  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active")
    tab.style.display = "none"
  })

  document.querySelectorAll(".sidebar-button").forEach((btn) => {
    btn.classList.remove("active")
  })

  const targetTab = document.getElementById(tabName)
  if (targetTab) {
    targetTab.classList.add("active")
    targetTab.style.display = "block"
  }

  const activeButton = document.querySelector(`[data-tab="${tabName}"]`)
  if (activeButton) {
    activeButton.classList.add("active")
  }

  switch (tabName) {
    case "dashboard":
      cargarEstadisticas()
      break
    case "usuarios":
      cargarUsuarios()
      break
    case "docentes":
      cargarDocentes()
      break
    case "alumnos":
      cargarAlumnos()
      break
    case "asistencias-docentes":
      cargarAsistenciasDocentes()
      break
    case "carreras":
      cargarCarreras()
      break
    case "materias":
      cargarMaterias()
      break
  }
}

// ==================== MOSTRAR DATOS ====================

function mostrarUsuarios(usuarios) {
  const tbody = document.getElementById("tabla-usuarios")

  if (!tbody) {
    console.error("❌ Elemento tabla-usuarios no encontrado")
    return
  }

  if (usuarios.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="px-6 py-8 text-center text-gray-500">
          <i class="fas fa-users mr-2"></i>
          No hay usuarios registrados
        </td>
      </tr>
    `
    return
  }

  tbody.innerHTML = usuarios
    .map(
      (usuario) => `
        <tr class="hover:bg-gray-50 transition-colors duration-200">
            <td class="px-6 py-4 text-sm font-mono text-gray-900">${usuario.uid}</td>
            <td class="px-6 py-4 text-sm font-medium text-gray-900">${usuario.nombre}</td>
            <td class="px-6 py-4 text-sm">
                <span class="px-3 py-1 text-xs font-semibold rounded-full ${getRolColor(usuario.rol)}">
                    ${usuario.rol.toUpperCase()}
                </span>
            </td>
            <td class="px-6 py-4 text-sm">
                <span class="px-3 py-1 text-xs font-semibold rounded-full ${usuario.activo ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}">
                    ${usuario.activo ? "ACTIVO" : "INACTIVO"}
                </span>
            </td>
            <td class="px-6 py-4 text-sm">
                <div class="flex space-x-2">
                    <button onclick="verDetalleUsuario('${usuario.uid}')" class="text-blue-600 hover:text-blue-800 p-2 rounded-lg hover:bg-blue-50 transition-colors" title="Ver Detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="toggleUsuario(${usuario.id}, ${!usuario.activo})" class="text-${usuario.activo ? "orange" : "green"}-600 hover:text-${usuario.activo ? "orange" : "green"}-800 p-2 rounded-lg hover:bg-${usuario.activo ? "orange" : "green"}-50 transition-colors" title="${usuario.activo ? "Desactivar" : "Activar"}">
                        <i class="fas fa-${usuario.activo ? "ban" : "check"}"></i>
                    </button>
                </div>
            </td>
        </tr>
    `,
    )
    .join("")
}

function mostrarDocentes(docentes) {
  const tbody = document.getElementById("tabla-docentes")

  if (!tbody) {
    console.error("❌ Elemento tabla-docentes no encontrado")
    return
  }

  if (docentes.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="px-6 py-8 text-center text-gray-500">
          <i class="fas fa-chalkboard-teacher mr-2"></i>
          No hay docentes registrados
        </td>
      </tr>
    `
    return
  }

  tbody.innerHTML = docentes
    .map(
      (docente) => `
        <tr class="hover:bg-gray-50 transition-colors duration-200">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">${docente.nombre}</td>
            <td class="px-6 py-4 text-sm font-mono text-gray-600">${docente.clave}</td>
            <td class="px-6 py-4 text-sm text-gray-600">${docente.especialidad || "No especificada"}</td>
            <td class="px-6 py-4 text-sm">
                <span class="px-3 py-1 text-xs font-semibold rounded-full ${docente.activo ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}">
                    ${docente.activo ? "ACTIVO" : "INACTIVO"}
                </span>
            </td>
            <td class="px-6 py-4 text-sm">
                <div class="flex space-x-2">
                    <button onclick="verDetalleDocente(${docente.id})" class="text-blue-600 hover:text-blue-800 p-2 rounded-lg hover:bg-blue-50 transition-colors" title="Ver Detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="mostrarModalAsignarMaterias(${docente.id}, '${docente.nombre}')" class="text-green-600 hover:text-green-800 p-2 rounded-lg hover:bg-green-50 transition-colors" title="Asignar Materias">
                        <i class="fas fa-plus-circle"></i>
                    </button>
                    <button onclick="editarDocente(${docente.id})" class="text-yellow-600 hover:text-yellow-800 p-2 rounded-lg hover:bg-yellow-50 transition-colors" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="exportarAsistenciasDocente(${docente.id}, '${docente.nombre}')" class="text-purple-600 hover:text-purple-800 p-2 rounded-lg hover:bg-purple-50 transition-colors" title="Exportar Asistencias">
                        <i class="fas fa-download"></i>
                    </button>
                    <button onclick="eliminarDocentePermanente(${docente.id})" class="text-red-600 hover:text-red-800 p-2 rounded-lg hover:bg-red-50 transition-colors" title="Eliminar Permanentemente">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `,
    )
    .join("")
}

function mostrarAlumnos(alumnos) {
  const tbody = document.getElementById("tabla-alumnos")

  if (!tbody) {
    console.error("❌ Elemento tabla-alumnos no encontrado")
    return
  }

  if (alumnos.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="px-6 py-8 text-center text-gray-500">
          <i class="fas fa-graduation-cap mr-2"></i>
          No hay alumnos registrados
        </td>
      </tr>
    `
    return
  }

  tbody.innerHTML = alumnos
    .map(
      (alumno) => `
        <tr class="hover:bg-gray-50 transition-colors duration-200">
            <td class="px-6 py-4 text-sm">
                <input type="checkbox" class="alumno-checkbox rounded" value="${alumno.id}" onchange="actualizarSeleccionados()">
            </td>
            <td class="px-6 py-4 text-sm font-medium text-gray-900">${alumno.nombre}</td>
            <td class="px-6 py-4 text-sm font-mono text-gray-600">${alumno.matricula}</td>
            <td class="px-6 py-4 text-sm text-gray-600">${alumno.carrera}</td>
            <td class="px-6 py-4 text-sm text-gray-600">${alumno.semestre}°</td>
            <td class="px-6 py-4 text-sm text-gray-600">${alumno.grupo || "N/A"}</td>
            <td class="px-6 py-4 text-sm">
                <span class="px-3 py-1 text-xs font-semibold rounded-full ${alumno.activo ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}">
                    ${alumno.activo ? "ACTIVO" : "INACTIVO"}
                </span>
            </td>
            <td class="px-6 py-4 text-sm">
                <div class="flex space-x-2">
                    <button onclick="verDetalleAlumno(${alumno.id})" class="text-blue-600 hover:text-blue-800 p-2 rounded-lg hover:bg-blue-50 transition-colors" title="Ver Detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="editarAlumno(${alumno.id})" class="text-green-600 hover:text-green-800 p-2 rounded-lg hover:bg-green-50 transition-colors" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="exportarAsistenciasAlumno('${alumno.matricula}', '${alumno.nombre}')" class="text-purple-600 hover:text-purple-800 p-2 rounded-lg hover:bg-purple-50 transition-colors" title="Exportar Asistencias">
                        <i class="fas fa-download"></i>
                    </button>
                    <button onclick="eliminarAlumnoPermanente(${alumno.id})" class="text-red-600 hover:text-red-800 p-2 rounded-lg hover:bg-red-50 transition-colors" title="Eliminar Permanentemente">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `,
    )
    .join("")
}

function mostrarCarreras(carreras) {
  const container = document.getElementById("lista-carreras")

  if (!container) {
    console.error("❌ Elemento lista-carreras no encontrado")
    return
  }

  if (carreras.length === 0) {
    container.innerHTML = `
      <div class="col-span-full text-center py-8 text-gray-500">
        <i class="fas fa-book text-4xl mb-4"></i>
        <p>No hay carreras registradas</p>
      </div>
    `
    return
  }

  container.innerHTML = carreras
    .map(
      (carrera) => `
        <div class="content-card rounded-2xl shadow-lg p-6 card-hover transition-all duration-300">
            <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                    <h3 class="text-lg font-bold text-gray-800 mb-2">${carrera.nombre}</h3>
                    <p class="text-sm text-gray-600 mb-3">Código: ${carrera.codigo || carrera.id}</p>
                    
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span class="text-gray-500">ID:</span>
                            <span class="font-medium ml-2">${carrera.id}</span>
                        </div>
                        <div>
                            <span class="text-gray-500">Estado:</span>
                            <span class="font-medium ml-2">${carrera.activa ? "Activa" : "Inactiva"}</span>
                        </div>
                    </div>
                </div>
                
                <div class="flex flex-col space-y-2 ml-4">
                    <button onclick="verDetalleCarrera(${carrera.id})" class="text-blue-600 hover:text-blue-800 p-2 rounded-lg hover:bg-blue-50 transition-colors" title="Ver Detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>
            
            <div class="border-t pt-4">
                <div class="flex items-center justify-between text-sm text-gray-600">
                    <span>Carrera ${carrera.activa ? "activa" : "inactiva"}</span>
                    <span class="px-2 py-1 rounded-full text-xs ${carrera.activa ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}">
                        ${carrera.activa ? "ACTIVA" : "INACTIVA"}
                    </span>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

function mostrarAsistenciasDocentes(asistencias) {
  const container = document.getElementById("lista-asistencias-docentes")

  if (!container) {
    console.error("❌ Elemento lista-asistencias-docentes no encontrado")
    return
  }

  if (asistencias.length === 0) {
    container.innerHTML = `
      <div class="col-span-full text-center py-8 text-gray-500">
        <i class="fas fa-chart-line text-4xl mb-4"></i>
        <p>No hay datos de asistencias de docentes</p>
      </div>
    `
    return
  }

  const docentesActivos = asistencias.filter((d) => d.total_clases > 0).length
  const promedioAsistencia =
    asistencias.length > 0 ? asistencias.reduce((sum, d) => sum + d.porcentaje_asistencia, 0) / asistencias.length : 0
  const clasesHoy = asistencias.reduce((sum, d) => sum + (d.clases_asistidas || 0), 0)
  const materiasAsignadas = asistencias.reduce((sum, d) => sum + (d.materias_asignadas || 0), 0)

  actualizarElementoTexto("docentes-activos", docentesActivos)
  actualizarElementoTexto("promedio-asistencia", `${promedioAsistencia.toFixed(1)}%`)
  actualizarElementoTexto("clases-hoy", clasesHoy)
  actualizarElementoTexto("materias-asignadas", materiasAsignadas)

  container.innerHTML = asistencias
    .map(
      (docente) => `
        <div class="content-card rounded-2xl shadow-lg p-6 card-hover transition-all duration-300">
            <div class="flex items-start justify-between mb-4">
                <div class="flex items-center">
                    <div class="w-12 h-12 rounded-full flex items-center justify-center mr-4 ${docente.porcentaje_asistencia >= 80 ? "bg-green-100" : docente.porcentaje_asistencia >= 60 ? "bg-yellow-100" : "bg-red-100"}">
                        <i class="fas fa-chalkboard-teacher ${docente.porcentaje_asistencia >= 80 ? "text-green-600" : docente.porcentaje_asistencia >= 60 ? "text-yellow-600" : "text-red-600"}"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-gray-800">${docente.nombre}</h3>
                        <p class="text-sm text-gray-600">UID: ${docente.uid}</p>
                    </div>
                </div>
                
                <div class="text-right">
                    <div class="text-2xl font-bold ${docente.porcentaje_asistencia >= 80 ? "text-green-600" : docente.porcentaje_asistencia >= 60 ? "text-yellow-600" : "text-red-600"}">
                        ${docente.porcentaje_asistencia.toFixed(1)}%
                    </div>
                    <div class="text-sm text-gray-500">Asistencia</div>
                </div>
            </div>
            
            <div class="grid grid-cols-4 gap-4 mb-4">
                <div class="text-center">
                    <div class="text-xl font-bold text-blue-600">${docente.total_clases || 0}</div>
                    <div class="text-xs text-gray-500">Total Clases</div>
                </div>
                <div class="text-center">
                    <div class="text-xl font-bold text-green-600">${docente.clases_asistidas || 0}</div>
                    <div class="text-xs text-gray-500">Asistencias</div>
                </div>
                <div class="text-center">
                    <div class="text-xl font-bold text-red-600">${docente.clases_faltadas || 0}</div>
                    <div class="text-xs text-gray-500">Inasistencias</div>
                </div>
                <div class="text-center">
                    <div class="text-xl font-bold text-purple-600">${docente.materias_asignadas || 0}</div>
                    <div class="text-xs text-gray-500">Materias</div>
                </div>
            </div>
            
            <div class="border-t pt-4">
                <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
                    <span>Carreras: ${(docente.carreras || ["Ingeniería"]).join(", ")}</span>
                </div>
                
                <div class="flex space-x-2">
                    <button onclick="verDetalleDocenteAsistencias('${docente.uid}')" class="flex-1 bg-blue-50 text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-100 transition-colors text-sm">
                        <i class="fas fa-eye mr-1"></i>
                        Ver Detalles
                    </button>
                    <button onclick="exportarAsistenciasDocente('${docente.uid}', '${docente.nombre}')" class="bg-green-50 text-green-600 px-3 py-2 rounded-lg hover:bg-green-100 transition-colors text-sm">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

function mostrarMaterias(materias) {
  const container = document.getElementById("lista-materias")

  if (!container) {
    console.error("❌ Elemento lista-materias no encontrado")
    return
  }

  if (materias.length === 0) {
    container.innerHTML = `
      <div class="text-center py-8 text-gray-500">
        <i class="fas fa-book-open text-4xl mb-4"></i>
        <p>No hay materias asignadas</p>
        <button onclick="mostrarModalAsignarMaterias()" class="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          <i class="fas fa-plus mr-2"></i>
          Asignar Primera Materia
        </button>
      </div>
    `
    return
  }

  container.innerHTML = materias
    .map(
      (materia) => `
        <div class="content-card rounded-2xl shadow-lg p-6 card-hover transition-all duration-300">
            <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                    <h3 class="text-lg font-bold text-gray-800 mb-2">${materia.nombre}</h3>
                    <p class="text-sm text-gray-600 mb-3">Docente: ${materia.docente_nombre}</p>
                    
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span class="text-gray-500">Carrera:</span>
                            <span class="font-medium ml-2">${CARRERAS_MAP[materia.carrera_id] || `Carrera ${materia.carrera_id}`}</span>
                        </div>
                        <div>
                            <span class="text-gray-500">Semestre:</span>
                            <span class="font-medium ml-2">${materia.semestre}°</span>
                        </div>
                        <div>
                            <span class="text-gray-500">Grupo:</span>
                            <span class="font-medium ml-2">${materia.grupo}</span>
                        </div>
                        <div>
                            <span class="text-gray-500">Aula:</span>
                            <span class="font-medium ml-2">${materia.aula || "Sin asignar"}</span>
                        </div>
                    </div>
                </div>
                
                <div class="flex flex-col space-y-2 ml-4">
                    <button onclick="eliminarAsignacionMateria(${materia.id})" class="text-red-600 hover:text-red-800 p-2 rounded-lg hover:bg-red-50 transition-colors" title="Eliminar Asignación">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            
            <div class="border-t pt-4">
                <div class="flex items-center justify-between text-sm text-gray-600">
                    <span>${materia.dia_semana}: ${materia.hora_inicio} - ${materia.hora_fin}</span>
                    <span class="px-2 py-1 rounded-full text-xs ${materia.activa ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}">
                        ${materia.activa ? "ACTIVA" : "INACTIVA"}
                    </span>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

// ==================== FUNCIONES DE UTILIDAD PARA UI ====================

function getRolColor(rol) {
  switch (rol) {
    case "admin":
      return "bg-red-100 text-red-800"
    case "docente":
      return "bg-blue-100 text-blue-800"
    case "alumno":
      return "bg-green-100 text-green-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

function actualizarSeleccionados() {
  const checkboxes = document.querySelectorAll(".alumno-checkbox:checked")
  alumnosSeleccionados = Array.from(checkboxes).map((cb) => Number.parseInt(cb.value))

  const botonEliminar = document.getElementById("eliminar-seleccionados")
  if (botonEliminar) {
    if (alumnosSeleccionados.length > 0) {
      botonEliminar.style.display = "inline-flex"
      botonEliminar.textContent = `Eliminar ${alumnosSeleccionados.length} seleccionado${alumnosSeleccionados.length > 1 ? "s" : ""}`
    } else {
      botonEliminar.style.display = "none"
    }
  }
}

// ==================== FUNCIONES DE MODALES - CORREGIDAS ====================

let docenteSeleccionadoId = null

function mostrarModalAsignarMaterias(docenteId = null, docenteNombre = "") {
  console.log("🎯 Abriendo modal asignar materias:", { docenteId, docenteNombre })

  // CORREGIDO: Si se proporciona docenteId, mostrar directamente el docente seleccionado
  if (docenteId && docenteNombre) {
    docenteSeleccionadoId = docenteId
    document.getElementById("docente-seleccionado-nombre").textContent = docenteNombre

    // Ocultar selector y mostrar docente seleccionado
    document.getElementById("selector-docente").style.display = "none"
    document.getElementById("docente-seleccionado").style.display = "block"

    console.log("✅ Docente preseleccionado:", docenteNombre)
  } else {
    // Si no hay docente preseleccionado, mostrar selector
    const select = document.getElementById("docente-select")
    select.innerHTML = '<option value="">Seleccionar docente...</option>'
    docentesData.forEach((docente) => {
      select.innerHTML += `<option value="${docente.id}">${docente.nombre} (${docente.clave})</option>`
    })
    document.getElementById("selector-docente").style.display = "block"
    document.getElementById("docente-seleccionado").style.display = "none"
    docenteSeleccionadoId = null
  }

  // Configurar carreras
  const carreraSelect = document.getElementById("materia-carrera")
  carreraSelect.innerHTML = '<option value="">Seleccionar carrera...</option>'
  Object.entries(CARRERAS_MAP).forEach(([id, nombre]) => {
    carreraSelect.innerHTML += `<option value="${id}">${nombre}</option>`
  })

  // Limpiar selecciones previas
  materiasSeleccionadas = []
  document.getElementById("materia-semestre").innerHTML = '<option value="">Seleccionar...</option>'
  document.getElementById("materias-container").innerHTML =
    '<p class="text-gray-500 text-sm">Selecciona carrera y semestre...</p>'
  document.getElementById("horarios-container").style.display = "none"

  // Mostrar modal
  document.getElementById("modal-asignar-materias").classList.remove("hidden")
}

function seleccionarDocente() {
  const select = document.getElementById("docente-select")
  const docenteId = select.value

  if (!docenteId) {
    mostrarMensaje("Debe seleccionar un docente", "error")
    return
  }

  const docente = docentesData.find((d) => d.id === Number.parseInt(docenteId))
  if (!docente) {
    mostrarMensaje("Docente no encontrado", "error")
    return
  }

  docenteSeleccionadoId = Number.parseInt(docenteId)
  document.getElementById("docente-seleccionado-nombre").textContent = docente.nombre

  document.getElementById("selector-docente").style.display = "none"
  document.getElementById("docente-seleccionado").style.display = "block"
}

function cerrarModalAsignarMaterias() {
  document.getElementById("modal-asignar-materias").classList.add("hidden")
  docenteSeleccionadoId = null
  materiasSeleccionadas = []

  // Resetear estado del modal
  document.getElementById("selector-docente").style.display = "block"
  document.getElementById("docente-seleccionado").style.display = "none"
  document.getElementById("horarios-container").style.display = "none"

  // Limpiar formularios
  document.getElementById("materia-carrera").value = ""
  document.getElementById("materia-semestre").innerHTML = '<option value="">Seleccionar...</option>'
  document.getElementById("materias-container").innerHTML =
    '<p class="text-gray-500 text-sm">Selecciona carrera y semestre...</p>'
}

function mostrarModalCrearAlumno() {
  alumnoEditandoId = null

  document.getElementById("alumno-nombre").value = ""
  document.getElementById("alumno-matricula").value = ""
  document.getElementById("alumno-grupo").value = ""

  const carreraSelect = document.getElementById("alumno-carrera")
  carreraSelect.innerHTML = '<option value="">Seleccionar carrera...</option>'
  Object.entries(CARRERAS_MAP).forEach(([id, nombre]) => {
    carreraSelect.innerHTML += `<option value="${id}">${nombre}</option>`
  })

  const numeroGrupoSelect = document.getElementById("alumno-numero-grupo")
  numeroGrupoSelect.innerHTML = '<option value="">Seleccionar...</option>'
  for (let i = 1; i <= 4; i++) {
    numeroGrupoSelect.innerHTML += `<option value="${i}">Grupo ${i}</option>`
  }

  actualizarSemestresPermitidos()

  document.querySelector("#modal-crear-alumno h3").textContent = "Crear Nuevo Alumno"
  document.querySelector("#modal-crear-alumno button[type='submit']").textContent = "Crear Alumno"

  document.getElementById("modal-crear-alumno").classList.remove("hidden")
}

function cerrarModalCrearAlumno() {
  document.getElementById("modal-crear-alumno").classList.add("hidden")
  alumnoEditandoId = null
}

function mostrarModalCrearDocente() {
  docenteEditandoId = null

  document.getElementById("docente-nombre").value = ""
  document.getElementById("docente-clave").value = ""
  document.getElementById("docente-especialidad").value = ""

  document.querySelector("#modal-crear-docente h3").textContent = "Crear Nuevo Docente"
  document.querySelector("#modal-crear-docente button[type='submit']").textContent = "Crear Docente"

  document.getElementById("modal-crear-docente").classList.remove("hidden")
}

function cerrarModalCrearDocente() {
  document.getElementById("modal-crear-docente").classList.add("hidden")
  docenteEditandoId = null
}

// ==================== FUNCIONES DE CREACIÓN ====================

async function crearDocente(event) {
  event.preventDefault()

  try {
    const nombre = document.getElementById("docente-nombre").value
    const clave = document.getElementById("docente-clave").value
    const especialidad = document.getElementById("docente-especialidad").value

    const docenteData = {
      nombre: nombre,
      clave: clave,
      especialidad: especialidad,
    }

    if (docenteEditandoId) {
      mostrarMensaje("Actualizando docente...", "info")

      const response = await peticionAutenticada(`/admin/docentes_base/${docenteEditandoId}`, {
        method: "PUT",
        body: JSON.stringify(docenteData),
      })

      if (!response || !response.ok) {
        throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
      }

      mostrarMensaje(`Docente "${nombre}" actualizado correctamente`, "success")
    } else {
      mostrarMensaje("Creando docente...", "info")

      const response = await peticionAutenticada("/admin/docentes_base/", {
        method: "POST",
        body: JSON.stringify(docenteData),
      })

      if (!response || !response.ok) {
        throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
      }

      mostrarMensaje(`Docente "${nombre}" creado correctamente`, "success")
    }

    cerrarModalCrearDocente()
    cargarDocentes()
    cargarEstadisticas()
  } catch (error) {
    console.error("❌ Error con docente:", error)
    mostrarMensaje(`Error: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE ELIMINACIÓN MASIVA ====================

async function eliminarAlumnosSeleccionados() {
  if (alumnosSeleccionados.length === 0) {
    mostrarMensaje("No hay alumnos seleccionados", "error")
    return
  }

  const nombresSeleccionados = alumnosSeleccionados
    .map((id) => {
      const alumno = alumnosData.find((a) => a.id === id)
      return alumno ? alumno.nombre : `ID ${id}`
    })
    .join(", ")

  if (
    !confirm(
      `¿Estás seguro de que deseas ELIMINAR PERMANENTEMENTE a ${alumnosSeleccionados.length} alumno${alumnosSeleccionados.length > 1 ? "s" : ""}?\n\nAlumnos: ${nombresSeleccionados}\n\nEsta acción NO se puede deshacer.`,
    )
  ) {
    return
  }

  try {
    mostrarMensaje(`Eliminando ${alumnosSeleccionados.length} alumnos permanentemente...`, "info")

    const response = await peticionAutenticada("/admin/eliminar_alumnos_masivo/", {
      method: "DELETE",
      body: JSON.stringify({
        alumno_ids: alumnosSeleccionados,
      }),
    })

    if (!response || !response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response?.status}`)
    }

    const resultado = await response.json()

    mostrarMensaje(`${resultado.eliminados} alumnos eliminados permanentemente`, "success")

    alumnosSeleccionados = []
    document.getElementById("eliminar-seleccionados").style.display = "none"

    document.querySelectorAll(".alumno-checkbox").forEach((cb) => {
      cb.checked = false
    })

    cargarAlumnos()
    cargarEstadisticas()
  } catch (error) {
    console.error("❌ Error eliminando alumnos:", error)
    mostrarMensaje(`Error eliminando alumnos: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE ELIMINACIÓN DE ASIGNACIONES ====================

async function eliminarAsignacionMateria(asignacionId) {
  try {
    const asignacion = materiasData.find((m) => m.id === asignacionId)
    if (!asignacion) {
      mostrarMensaje("Asignación no encontrada", "error")
      return
    }

    if (
      !confirm(
        `¿Estás seguro de que deseas eliminar la asignación de "${asignacion.nombre}" del docente "${asignacion.docente_nombre}"?`,
      )
    ) {
      return
    }

    mostrarMensaje("Eliminando asignación...", "info")

    const response = await peticionAutenticada(`/admin/materias_asignadas/${asignacionId}`, {
      method: "DELETE",
    })

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    mostrarMensaje("Asignación eliminada correctamente", "success")
    cargarMaterias()
  } catch (error) {
    console.error("❌ Error eliminando asignación:", error)
    mostrarMensaje(`Error eliminando asignación: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE DETALLES - MEJORADAS ====================

async function verDetalleAlumno(alumnoId) {
  try {
    mostrarMensaje("Cargando detalle del alumno...", "info")

    const response = await peticionAutenticada(`/admin/alumno/${alumnoId}/detalle`)

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    const detalle = await response.json()

    const modal = document.createElement("div")
    modal.className = "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    modal.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-bold text-gray-800">Detalle del Alumno</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                </div>
            </div>
            
            <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-blue-50 rounded-xl p-4">
                        <h3 class="font-semibold text-blue-800 mb-3">Información Personal</h3>
                        <div class="space-y-2 text-sm">
                            <div><span class="text-gray-600">Nombre:</span> <span class="font-medium">${detalle.alumno.nombre}</span></div>
                            <div><span class="text-gray-600">Matrícula:</span> <span class="font-medium">${detalle.alumno.matricula}</span></div>
                            <div><span class="text-gray-600">Carrera:</span> <span class="font-medium">${detalle.alumno.carrera}</span></div>
                            <div><span class="text-gray-600">Semestre:</span> <span class="font-medium">${detalle.alumno.semestre}°</span></div>
                            <div><span class="text-gray-600">Grupo:</span> <span class="font-medium">${detalle.alumno.grupo}</span></div>
                        </div>
                    </div>
                    
                    <div class="bg-green-50 rounded-xl p-4">
                        <h3 class="font-semibold text-green-800 mb-3">Resumen Académico</h3>
                        <div class="space-y-2 text-sm">
                            <div><span class="text-gray-600">Total Materias:</span> <span class="font-medium">${detalle.resumen.total_materias}</span></div>
                            <div><span class="text-gray-600">Promedio Asistencia:</span> <span class="font-medium">${detalle.resumen.promedio_asistencia}%</span></div>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Materias y Asistencias</h3>
                    ${
                      detalle.materias.length > 0
                        ? `
                        <div class="grid gap-4">
                            ${detalle.materias
                              .map(
                                (materia) => `
                                <div class="border border-gray-200 rounded-xl p-4">
                                    <div class="flex justify-between items-start mb-3">
                                        <div>
                                            <h4 class="font-semibold text-gray-800">${materia.materia_nombre}</h4>
                                            <p class="text-sm text-gray-600">Docente: ${materia.docente_nombre}</p>
                                        </div>
                                        <div class="text-right">
                                            <div class="text-lg font-bold ${materia.porcentaje_asistencia >= 80 ? "text-green-600" : materia.porcentaje_asistencia >= 60 ? "text-yellow-600" : "text-red-600"}">
                                                ${materia.porcentaje_asistencia}%
                                            </div>
                                            <div class="text-xs text-gray-500">Asistencia</div>
                                        </div>
                                    </div>
                                    
                                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                        <div>
                                            <span class="text-gray-500">Horario:</span>
                                            <div class="font-medium">${materia.dia_semana}</div>
                                            <div class="text-xs text-gray-600">${materia.hora_inicio} - ${materia.hora_fin}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Aula:</span>
                                            <div class="font-medium">${materia.aula}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Asistencias:</span>
                                            <div class="font-medium text-green-600">${materia.asistencias_presente}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Total Clases:</span>
                                            <div class="font-medium">${materia.total_asistencias}</div>
                                        </div>
                                    </div>
                                </div>
                            `,
                              )
                              .join("")}
                        </div>
                    `
                        : `
                        <div class="text-center py-8 text-gray-500">
                            <i class="fas fa-book-open text-4xl mb-4"></i>
                            <p>No hay materias asignadas para este alumno</p>
                        </div>
                    `
                    }
                </div>
            </div>
        </div>
    `

    document.body.appendChild(modal)
  } catch (error) {
    console.error("❌ Error obteniendo detalle del alumno:", error)
    mostrarMensaje(`Error obteniendo detalle: ${error.message}`, "error")
  }
}

// ==================== FUNCIÓN DE DETALLE DE DOCENTE MEJORADA CON ELIMINACIÓN ====================

async function verDetalleDocenteAsistencias(docenteClave) {
  try {
    mostrarMensaje("Cargando detalle del docente...", "info")

    const response = await peticionAutenticada(`/admin/docente/${docenteClave}/detalle`)

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    const detalle = await response.json()

    const modal = document.createElement("div")
    modal.className = "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    modal.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-bold text-gray-800">Detalle del Docente</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                </div>
            </div>
            
            <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-blue-50 rounded-xl p-4">
                        <h3 class="font-semibold text-blue-800 mb-3">Información Personal</h3>
                        <div class="space-y-2 text-sm">
                            <div><span class="text-gray-600">Nombre:</span> <span class="font-medium">${detalle.docente.nombre}</span></div>
                            <div><span class="text-gray-600">Clave:</span> <span class="font-medium">${detalle.docente.clave}</span></div>
                            <div><span class="text-gray-600">Especialidad:</span> <span class="font-medium">${detalle.docente.especialidad || "No especificada"}</span></div>
                        </div>
                    </div>
                    
                    <div class="bg-green-50 rounded-xl p-4">
                        <h3 class="font-semibold text-green-800 mb-3">Estadísticas de Asistencia</h3>
                        <div class="space-y-2 text-sm">
                            <div><span class="text-gray-600">Total Materias:</span> <span class="font-medium">${detalle.estadisticas.total_materias}</span></div>
                            <div><span class="text-gray-600">Clases Estimadas:</span> <span class="font-medium">${detalle.estadisticas.total_clases_estimadas}</span></div>
                            <div><span class="text-gray-600">Asistencias Registradas:</span> <span class="font-medium">${detalle.estadisticas.total_asistencias_registradas}</span></div>
                            <div><span class="text-gray-600">Porcentaje Asistencia:</span> <span class="font-medium">${detalle.estadisticas.porcentaje_asistencia}%</span></div>
                            <div><span class="text-gray-600">Carreras:</span> <span class="font-medium">${detalle.estadisticas.carreras_atendidas.join(", ")}</span></div>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Materias Asignadas</h3>
                    ${
                      detalle.materias.length > 0
                        ? `
                        <div class="grid gap-4">
                            ${detalle.materias
                              .map(
                                (materia) => `
                                <div class="border border-gray-200 rounded-xl p-4">
                                    <div class="flex justify-between items-start mb-3">
                                        <div class="flex-1">
                                            <h4 class="font-semibold text-gray-800">${materia.materia_nombre}</h4>
                                            <p class="text-sm text-gray-600">${materia.carrera_nombre} - ${materia.semestre}° Semestre</p>
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <div class="text-right">
                                                <div class="text-sm text-gray-600">Grupo ${materia.grupo}</div>
                                                <div class="text-xs text-gray-500">${materia.total_alumnos} alumnos</div>
                                            </div>
                                            <button onclick="eliminarAsignacionDocenteDetalle(${materia.asignacion_id}, '${materia.materia_nombre}', this)" 
                                                    class="text-red-600 hover:text-red-800 p-2 rounded-lg hover:bg-red-50 transition-colors" 
                                                    title="Eliminar Asignación">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                        <div>
                                            <span class="text-gray-500">Horario:</span>
                                            <div class="font-medium">${materia.dia_semana}</div>
                                            <div class="text-xs text-gray-600">${materia.hora_inicio} - ${materia.hora_fin}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Aula:</span>
                                            <div class="font-medium">${materia.aula}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Clases Estimadas:</span>
                                            <div class="font-medium">${materia.clases_estimadas}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Asistencias:</span>
                                            <div class="font-medium text-green-600">${materia.asistencias_registradas}</div>
                                        </div>
                                    </div>
                                </div>
                            `,
                              )
                              .join("")}
                        </div>
                    `
                        : `
                        <div class="text-center py-8 text-gray-500">
                            <i class="fas fa-chalkboard-teacher text-4xl mb-4"></i>
                            <p>No hay materias asignadas para este docente</p>
                        </div>
                    `
                    }
                </div>
            </div>
        </div>
    `

    document.body.appendChild(modal)
  } catch (error) {
    console.error("❌ Error obteniendo detalle del docente:", error)
    mostrarMensaje(`Error obteniendo detalle: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES PARA ELIMINAR ASIGNACIÓN DESDE DETALLE ====================

async function eliminarAsignacionDocenteDetalle(asignacionId, nombreMateria, botonElement) {
  try {
    if (!confirm(`¿Estás seguro de que deseas eliminar la asignación de "${nombreMateria}"?`)) {
      return
    }

    mostrarMensaje("Eliminando asignación...", "info")

    const response = await peticionAutenticada(`/admin/materias_asignadas/${asignacionId}`, {
      method: "DELETE",
    })

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    mostrarMensaje("Asignación eliminada correctamente", "success")

    // Remover la tarjeta de materia del DOM
    const materiaCard = botonElement.closest(".border.border-gray-200.rounded-xl")
    if (materiaCard) {
      materiaCard.remove()
    }

    // Recargar datos en el panel principal
    cargarMaterias()
    cargarAsistenciasDocentes()
  } catch (error) {
    console.error("❌ Error eliminando asignación:", error)
    mostrarMensaje(`Error eliminando asignación: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES DE EXPORTACIÓN ====================

function exportarAsistenciasAlumno(matricula, nombre) {
  mostrarMensaje(`Exportando asistencias de ${nombre}...`, "info")

  const csvContent = `Alumno,Matrícula,Fecha,Estado\n${nombre},${matricula},${new Date().toLocaleDateString()},Ejemplo`

  const blob = new Blob([csvContent], { type: "text/csv" })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `asistencias_${matricula}_${nombre.replace(/\s+/g, "_")}.csv`
  a.click()
  window.URL.revokeObjectURL(url)

  mostrarMensaje("Asistencias exportadas correctamente", "success")
}

function exportarAsistenciasDocente(docenteId, nombre) {
  mostrarMensaje(`Exportando asistencias de ${nombre}...`, "info")

  const csvContent = `Docente,ID,Fecha,Estado\n${nombre},${docenteId},${new Date().toLocaleDateString()},Ejemplo`

  const blob = new Blob([csvContent], { type: "text/csv" })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `asistencias_docente_${docenteId}_${nombre.replace(/\s+/g, "_")}.csv`
  a.click()
  window.URL.revokeObjectURL(url)

  mostrarMensaje("Asistencias exportadas correctamente", "success")
}

// ==================== FUNCIONES DE SESIÓN ====================

function cerrarSesion() {
  if (confirm("¿Estás seguro de que deseas cerrar sesión?")) {
    console.log("🚪 Cerrando sesión...")

    localStorage.removeItem("uid")
    localStorage.removeItem("userData")
    localStorage.removeItem("usuario_rol")
    localStorage.removeItem("usuario_nombre")

    mostrarMensaje("Sesión cerrada correctamente", "success")

    setTimeout(() => {
      window.location.href = "admin_login.html"
    }, 1000)
  }
}

// ==================== FUNCIONES PARA USUARIOS ====================

async function verDetalleUsuario(uid) {
  try {
    const usuario = usuariosData.find((u) => u.uid === uid)
    if (!usuario) {
      mostrarMensaje("Usuario no encontrado", "error")
      return
    }

    const modal = document.createElement("div")
    modal.className = "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    modal.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-bold text-gray-800">Detalle del Usuario</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                </div>
            </div>
            
            <div class="p-6">
                <div class="grid grid-cols-1 gap-6">
                    <div class="bg-blue-50 rounded-xl p-4">
                        <h3 class="font-semibold text-blue-800 mb-3">Información General</h3>
                        <div class="space-y-3 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-600">UID:</span> 
                                <span class="font-medium font-mono">${usuario.uid}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Nombre:</span> 
                                <span class="font-medium">${usuario.nombre}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Rol:</span> 
                                <span class="px-3 py-1 text-xs font-semibold rounded-full ${getRolColor(usuario.rol)}">
                                    ${usuario.rol.toUpperCase()}
                                </span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Estado:</span> 
                                <span class="px-3 py-1 text-xs font-semibold rounded-full ${usuario.activo ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}">
                                    ${usuario.activo ? "ACTIVO" : "INACTIVO"}
                                </span>
                            </div>
                            ${
                              usuario.fecha_registro
                                ? `
                            <div class="flex justify-between">
                                <span class="text-gray-600">Fecha Registro:</span> 
                                <span class="font-medium">${new Date(usuario.fecha_registro).toLocaleDateString()}</span>
                            </div>
                            `
                                : ""
                            }
                        </div>
                    </div>
                    
                    ${
                      usuario.rol === "alumno"
                        ? `
                    <div class="bg-green-50 rounded-xl p-4">
                        <h3 class="font-semibold text-green-800 mb-3">Información Académica</h3>
                        <div class="space-y-3 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-600">Matrícula:</span> 
                                <span class="font-medium font-mono">${usuario.matricula || "N/A"}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Carrera:</span> 
                                <span class="font-medium">${usuario.carrera || "N/A"}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Semestre:</span> 
                                <span class="font-medium">${usuario.semestre ? usuario.semestre + "°" : "N/A"}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Grupo:</span> 
                                <span class="font-medium">${usuario.grupo || "N/A"}</span>
                            </div>
                        </div>
                    </div>
                    `
                        : ""
                    }
                    
                    ${
                      usuario.rol === "docente"
                        ? `
                    <div class="bg-purple-50 rounded-xl p-4">
                        <h3 class="font-semibold text-purple-800 mb-3">Información Docente</h3>
                        <div class="space-y-3 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-600">Clave Docente:</span> 
                                <span class="font-medium font-mono">${usuario.clave_docente || "N/A"}</span>
                            </div>
                        </div>
                    </div>
                    `
                        : ""
                    }
                </div>
            </div>
        </div>
    `

    document.body.appendChild(modal)
  } catch (error) {
    console.error("❌ Error obteniendo detalle del usuario:", error)
    mostrarMensaje(`Error obteniendo detalle: ${error.message}`, "error")
  }
}

async function toggleUsuario(usuarioId, nuevoEstado) {
  try {
    const usuario = usuariosData.find((u) => u.id === usuarioId)
    if (!usuario) {
      mostrarMensaje("Usuario no encontrado", "error")
      return
    }

    const accion = nuevoEstado ? "activar" : "desactivar"

    if (!confirm(`¿Estás seguro de que deseas ${accion} al usuario "${usuario.nombre}"?`)) {
      return
    }

    mostrarMensaje(`${accion === "activar" ? "Activando" : "Desactivando"} usuario...`, "info")

    const response = await peticionAutenticada(`/admin/usuarios/${usuarioId}/toggle`, {
      method: "PATCH",
      body: JSON.stringify({ activo: nuevoEstado }),
    })

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    const resultado = await response.json()
    mostrarMensaje(resultado.message, "success")

    // Actualizar datos locales
    usuario.activo = nuevoEstado
    mostrarUsuarios(usuariosData)
    cargarEstadisticas()
  } catch (error) {
    console.error("❌ Error cambiando estado del usuario:", error)
    mostrarMensaje(`Error cambiando estado: ${error.message}`, "error")
  }
}

// ==================== FUNCIONES PARA DOCENTES ====================

async function verDetalleDocente(docenteId) {
  try {
    const docente = docentesData.find((d) => d.id === docenteId)
    if (!docente) {
      mostrarMensaje("Docente no encontrado", "error")
      return
    }

    mostrarMensaje("Cargando detalle del docente...", "info")

    const response = await peticionAutenticada(`/admin/docente/${docente.clave}/detalle`)

    if (!response || !response.ok) {
      throw new Error(`HTTP ${response?.status}: ${response?.statusText}`)
    }

    const detalle = await response.json()

    const modal = document.createElement("div")
    modal.className = "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    modal.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-bold text-gray-800">Detalle del Docente</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                </div>
            </div>
            
            <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-blue-50 rounded-xl p-4">
                        <h3 class="font-semibold text-blue-800 mb-3">Información Personal</h3>
                        <div class="space-y-2 text-sm">
                            <div><span class="text-gray-600">Nombre:</span> <span class="font-medium">${detalle.docente.nombre}</span></div>
                            <div><span class="text-gray-600">Clave:</span> <span class="font-medium">${detalle.docente.clave}</span></div>
                            <div><span class="text-gray-600">Especialidad:</span> <span class="font-medium">${detalle.docente.especialidad || "No especificada"}</span></div>
                        </div>
                    </div>
                    
                    <div class="bg-green-50 rounded-xl p-4">
                        <h3 class="font-semibold text-green-800 mb-3">Estadísticas de Asistencia</h3>
                        <div class="space-y-2 text-sm">
                            <div><span class="text-gray-600">Total Materias:</span> <span class="font-medium">${detalle.estadisticas.total_materias}</span></div>
                            <div><span class="text-gray-600">Clases Estimadas:</span> <span class="font-medium">${detalle.estadisticas.total_clases_estimadas}</span></div>
                            <div><span class="text-gray-600">Asistencias Registradas:</span> <span class="font-medium">${detalle.estadisticas.total_asistencias_registradas}</span></div>
                            <div><span class="text-gray-600">Porcentaje Asistencia:</span> <span class="font-medium">${detalle.estadisticas.porcentaje_asistencia}%</span></div>
                            <div><span class="text-gray-600">Carreras:</span> <span class="font-medium">${detalle.estadisticas.carreras_atendidas.join(", ")}</span></div>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Materias Asignadas</h3>
                    ${
                      detalle.materias.length > 0
                        ? `
                        <div class="grid gap-4">
                            ${detalle.materias
                              .map(
                                (materia) => `
                                <div class="border border-gray-200 rounded-xl p-4">
                                    <div class="flex justify-between items-start mb-3">
                                        <div class="flex-1">
                                            <h4 class="font-semibold text-gray-800">${materia.materia_nombre}</h4>
                                            <p class="text-sm text-gray-600">${materia.carrera_nombre} - ${materia.semestre}° Semestre</p>
                                        </div>
                                        <div class="text-right">
                                            <div class="text-sm text-gray-600">Grupo ${materia.grupo}</div>
                                            <div class="text-xs text-gray-500">${materia.total_alumnos} alumnos</div>
                                        </div>
                                    </div>
                                    
                                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                        <div>
                                            <span class="text-gray-500">Horario:</span>
                                            <div class="font-medium">${materia.dia_semana}</div>
                                            <div class="text-xs text-gray-600">${materia.hora_inicio} - ${materia.hora_fin}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Aula:</span>
                                            <div class="font-medium">${materia.aula}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Clases Estimadas:</span>
                                            <div class="font-medium">${materia.clases_estimadas}</div>
                                        </div>
                                        <div>
                                            <span class="text-gray-500">Asistencias:</span>
                                            <div class="font-medium text-green-600">${materia.asistencias_registradas}</div>
                                        </div>
                                    </div>
                                </div>
                            `,
                              )
                              .join("")}
                        </div>
                    `
                        : `
                        <div class="text-center py-8 text-gray-500">
                            <i class="fas fa-chalkboard-teacher text-4xl mb-4"></i>
                            <p>No hay materias asignadas para este docente</p>
                        </div>
                    `
                    }
                </div>
            </div>
        </div>
    `

    document.body.appendChild(modal)
  } catch (error) {
    console.error("❌ Error obteniendo detalle del docente:", error)
    mostrarMensaje(`Error obteniendo detalle: ${error.message}`, "error")
  }
}

// ==================== INICIALIZACIÓN PRINCIPAL ====================

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Iniciando panel de administración...")

  if (!verificarAutenticacion()) {
    return
  }

  inicializarPanel()

  console.log("✅ Panel de administración iniciado correctamente")
})

// ==================== FUNCIONES GLOBALES PARA HTML ====================

window.mostrarTab = mostrarTab
window.cerrarSesion = cerrarSesion
window.mostrarModalCrearAlumno = mostrarModalCrearAlumno
window.cerrarModalCrearAlumno = cerrarModalCrearAlumno
window.mostrarModalCrearDocente = mostrarModalCrearDocente
window.cerrarModalCrearDocente = cerrarModalCrearDocente
window.mostrarModalAsignarMaterias = mostrarModalAsignarMaterias
window.cerrarModalAsignarMaterias = cerrarModalAsignarMaterias
window.seleccionarDocente = seleccionarDocente
window.cargarSemestresDisponibles = cargarSemestresDisponibles
window.cargarMateriasPorCarrera = cargarMateriasPorCarrera
window.actualizarMateriasSeleccionadas = actualizarMateriasSeleccionadas
window.actualizarHorariosPorDia = actualizarHorariosPorDia
window.validarHorarios = validarHorarios
window.actualizarSemestresPermitidos = actualizarSemestresPermitidos
window.generarCodigoGrupo = generarCodigoGrupo
window.crearAlumno = crearAlumno
window.crearDocente = crearDocente
window.asignarMaterias = asignarMaterias
window.editarAlumno = editarAlumno
window.editarDocente = editarDocente
window.eliminarAlumnoPermanente = eliminarAlumnoPermanente
window.eliminarDocentePermanente = eliminarDocentePermanente
window.eliminarAsignacionMateria = eliminarAsignacionMateria
window.eliminarAsignacionDocenteDetalle = eliminarAsignacionDocenteDetalle
window.eliminarAlumnosSeleccionados = eliminarAlumnosSeleccionados
window.actualizarSeleccionados = actualizarSeleccionados
window.verDetalleAlumno = verDetalleAlumno
window.verDetalleDocenteAsistencias = verDetalleDocenteAsistencias
window.exportarAsistenciasAlumno = exportarAsistenciasAlumno
window.exportarAsistenciasDocente = exportarAsistenciasDocente
window.verDetalleUsuario = verDetalleUsuario
window.toggleUsuario = toggleUsuario
window.verDetalleDocente = verDetalleDocente
