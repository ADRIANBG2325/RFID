let datosAlumno = null
let asistenciasCompletas = []
let asistenciasFiltradas = []

// Verificar autenticación
function verificarAutenticacion() {
  const usuarioData = localStorage.getItem("usuario")
  const rol = localStorage.getItem("usuario_rol")

  console.log("🔍 Verificando autenticación de alumno...")
  console.log("Datos usuario:", usuarioData)
  console.log("Rol:", rol)

  if (!usuarioData || rol !== "alumno") {
    console.log("❌ No es alumno o no hay datos")
    window.location.href = "index.html"
    return false
  }

  try {
    const usuario = JSON.parse(usuarioData)
    if (usuario.rol !== "alumno") {
      console.log("❌ Rol incorrecto:", usuario.rol)
      window.location.href = "index.html"
      return false
    }
    console.log("✅ Autenticación de alumno correcta")
    return true
  } catch (error) {
    console.error("❌ Error parseando datos:", error)
    window.location.href = "index.html"
    return false
  }
}

// Cargar datos del alumno
async function cargarDatosAlumno() {
  try {
    const usuarioData = localStorage.getItem("usuario")
    const usuario = JSON.parse(usuarioData)

    console.log("📋 Cargando datos del alumno:", usuario)

    datosAlumno = {
      id: usuario.id,
      uid: usuario.uid,
      nombre: usuario.nombre,
      matricula: usuario.matricula,
      carrera: usuario.carrera,
      semestre: usuario.semestre,
      grupo: usuario.grupo,
    }

    mostrarDatosAlumno()
  } catch (error) {
    console.error("Error:", error)
    mostrarError("Error al cargar los datos del alumno")
  }
}

// Mostrar datos del alumno en la interfaz
function mostrarDatosAlumno() {
  if (!datosAlumno) return

  const nombreElement = document.getElementById("nombre-alumno")
  const infoElement = document.getElementById("info-alumno")

  if (nombreElement) {
    nombreElement.textContent = datosAlumno.nombre
  }

  if (infoElement) {
    infoElement.textContent = `${datosAlumno.carrera} - ${datosAlumno.semestre}° Semestre - Grupo ${datosAlumno.grupo}`
  }
}

// Cargar asistencias del alumno
async function cargarAsistencias() {
  try {
    const uid = localStorage.getItem("uid")
    console.log("📊 Cargando asistencias para UID:", uid)

    const response = await fetch(`http://localhost:8000/asistencias/ver/${uid}`)

    if (response.ok) {
      asistenciasCompletas = await response.json()
      asistenciasFiltradas = [...asistenciasCompletas]

      console.log("✅ Asistencias cargadas:", asistenciasCompletas.length)

      actualizarEstadisticas()
      llenarFiltroMaterias()
      mostrarAsistencias()
    } else {
      throw new Error("Error al cargar asistencias")
    }
  } catch (error) {
    console.error("Error:", error)
    mostrarError("Error al cargar las asistencias")
  } finally {
    const loadingElement = document.getElementById("loading-asistencias")
    if (loadingElement) {
      loadingElement.style.display = "none"
    }
  }
}

// Actualizar estadísticas
function actualizarEstadisticas() {
  const totalAsistencias = asistenciasCompletas.filter((a) => a.estado === "Presente").length
  const totalFaltas = asistenciasCompletas.filter((a) => a.estado === "Ausente").length
  const totalClases = asistenciasCompletas.length
  const materias = [...new Set(asistenciasCompletas.map((a) => a.materia))]
  const porcentaje = totalClases > 0 ? Math.round((totalAsistencias / totalClases) * 100) : 0

  const elementos = {
    totalAsistencias: document.getElementById("total-asistencias"),
    totalFaltas: document.getElementById("total-faltas"),
    totalMaterias: document.getElementById("total-materias"),
    porcentajeAsistencia: document.getElementById("porcentaje-asistencia"),
  }

  if (elementos.totalAsistencias) elementos.totalAsistencias.textContent = totalAsistencias
  if (elementos.totalFaltas) elementos.totalFaltas.textContent = totalFaltas
  if (elementos.totalMaterias) elementos.totalMaterias.textContent = materias.length
  if (elementos.porcentajeAsistencia) {
    elementos.porcentajeAsistencia.textContent = `${porcentaje}%`

    // Cambiar color del porcentaje según el valor
    if (porcentaje >= 80) {
      elementos.porcentajeAsistencia.className = "text-2xl font-bold text-green-600"
    } else if (porcentaje >= 60) {
      elementos.porcentajeAsistencia.className = "text-2xl font-bold text-yellow-600"
    } else {
      elementos.porcentajeAsistencia.className = "text-2xl font-bold text-red-600"
    }
  }
}

// Llenar filtro de materias
function llenarFiltroMaterias() {
  const materias = [...new Set(asistenciasCompletas.map((a) => a.materia))]
  const select = document.getElementById("filtro-materia")

  if (!select) return

  // Limpiar opciones existentes (excepto "Todas")
  select.innerHTML = '<option value="">Todas las materias</option>'

  materias.forEach((materia) => {
    const option = document.createElement("option")
    option.value = materia
    option.textContent = materia
    select.appendChild(option)
  })
}

// Mostrar asistencias en la tabla
function mostrarAsistencias() {
  const tbody = document.getElementById("tabla-asistencias")
  const noAsistencias = document.getElementById("no-asistencias")

  if (!tbody) return

  if (asistenciasFiltradas.length === 0) {
    tbody.innerHTML = ""
    if (noAsistencias) {
      noAsistencias.classList.remove("hidden")
    }
    return
  }

  if (noAsistencias) {
    noAsistencias.classList.add("hidden")
  }

  tbody.innerHTML = asistenciasFiltradas
    .map((asistencia) => {
      const estadoClass = asistencia.estado === "Presente" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
      const estadoIcon = asistencia.estado === "Presente" ? "✅" : "❌"

      return `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${formatearFecha(asistencia.fecha)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
          ${asistencia.materia || "N/A"}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${asistencia.docente || "N/A"}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${formatearHora(asistencia.hora)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${estadoClass}">
            ${estadoIcon} ${asistencia.estado}
          </span>
        </td>
      </tr>
    `
    })
    .join("")
}

// Aplicar filtros
function aplicarFiltros() {
  const materiaFiltro = document.getElementById("filtro-materia")?.value || ""
  const fechaDesde = document.getElementById("fecha-desde")?.value || ""
  const fechaHasta = document.getElementById("fecha-hasta")?.value || ""

  asistenciasFiltradas = asistenciasCompletas.filter((asistencia) => {
    // Filtro por materia
    if (materiaFiltro && asistencia.materia !== materiaFiltro) {
      return false
    }

    // Filtro por fecha
    if (fechaDesde && asistencia.fecha < fechaDesde) {
      return false
    }

    if (fechaHasta && asistencia.fecha > fechaHasta) {
      return false
    }

    return true
  })

  mostrarAsistencias()
  actualizarEstadisticasFiltradas()
}

// Actualizar estadísticas con datos filtrados
function actualizarEstadisticasFiltradas() {
  const totalAsistencias = asistenciasFiltradas.filter((a) => a.estado === "Presente").length
  const totalFaltas = asistenciasFiltradas.filter((a) => a.estado === "Ausente").length
  const totalClases = asistenciasFiltradas.length
  const porcentaje = totalClases > 0 ? Math.round((totalAsistencias / totalClases) * 100) : 0

  const elementos = {
    totalAsistencias: document.getElementById("total-asistencias"),
    totalFaltas: document.getElementById("total-faltas"),
    porcentajeAsistencia: document.getElementById("porcentaje-asistencia"),
  }

  if (elementos.totalAsistencias) elementos.totalAsistencias.textContent = totalAsistencias
  if (elementos.totalFaltas) elementos.totalFaltas.textContent = totalFaltas
  if (elementos.porcentajeAsistencia) elementos.porcentajeAsistencia.textContent = `${porcentaje}%`
}

// Limpiar filtros
function limpiarFiltros() {
  const filtroMateria = document.getElementById("filtro-materia")
  const fechaDesde = document.getElementById("fecha-desde")
  const fechaHasta = document.getElementById("fecha-hasta")

  if (filtroMateria) filtroMateria.value = ""
  if (fechaDesde) fechaDesde.value = ""
  if (fechaHasta) fechaHasta.value = ""

  asistenciasFiltradas = [...asistenciasCompletas]
  mostrarAsistencias()
  actualizarEstadisticas()
}

// Formatear fecha
function formatearFecha(fecha) {
  if (!fecha) return "N/A"
  const date = new Date(fecha)
  return date.toLocaleDateString("es-ES", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  })
}

// Formatear hora
function formatearHora(hora) {
  if (!hora) return "N/A"
  return hora.substring(0, 5) // HH:MM
}

// Mostrar error
function mostrarError(mensaje) {
  const tbody = document.getElementById("tabla-asistencias")
  if (tbody) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="px-6 py-4 text-center text-red-600">
          ⚠️ ${mensaje}
        </td>
      </tr>
    `
  }
}

// Cerrar sesión
function cerrarSesion() {
  localStorage.removeItem("uid")
  localStorage.removeItem("usuario_rol")
  localStorage.removeItem("usuario_nombre")
  localStorage.removeItem("usuario")
  window.location.href = "index.html"
}

// Configurar event listeners
function configurarEventListeners() {
  // Filtros
  const filtroMateria = document.getElementById("filtro-materia")
  const fechaDesde = document.getElementById("fecha-desde")
  const fechaHasta = document.getElementById("fecha-hasta")
  const btnLimpiar = document.getElementById("btn-limpiar-filtros")
  const btnCerrarSesion = document.getElementById("btn-cerrar-sesion")

  if (filtroMateria) filtroMateria.addEventListener("change", aplicarFiltros)
  if (fechaDesde) fechaDesde.addEventListener("change", aplicarFiltros)
  if (fechaHasta) fechaHasta.addEventListener("change", aplicarFiltros)
  if (btnLimpiar) btnLimpiar.addEventListener("click", limpiarFiltros)
  if (btnCerrarSesion) btnCerrarSesion.addEventListener("click", cerrarSesion)
}

// Inicializar cuando se carga la página
document.addEventListener("DOMContentLoaded", async () => {
  console.log("🎓 Iniciando panel de alumno...")

  if (!verificarAutenticacion()) return

  configurarEventListeners()
  await cargarDatosAlumno()
  await cargarAsistencias()

  console.log("✅ Panel de alumno inicializado")
})
