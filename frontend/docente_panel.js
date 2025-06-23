let datosDocente = null
let asistenciasCompletas = []
let asistenciasFiltradas = []
let materiasDocente = []
let claseActiva = null
let asistenciaEditando = null

// Verificar autenticación
function verificarAutenticacion() {
  const uid = localStorage.getItem("uid")
  const rol = localStorage.getItem("usuario_rol")

  if (!uid || rol !== "docente") {
    window.location.href = "index.html"
    return false
  }
  return true
}

// Cargar datos del docente
async function cargarDatosDocente() {
  try {
    const uid = localStorage.getItem("uid")
    const response = await fetch(`http://localhost:8000/usuarios/perfil/${uid}`)

    if (response.ok) {
      datosDocente = await response.json()
      mostrarDatosDocente()
    } else {
      throw new Error("Error al cargar datos del docente")
    }
  } catch (error) {
    console.error("Error:", error)
    mostrarError("Error al cargar los datos del docente")
  }
}

// Mostrar datos del docente
function mostrarDatosDocente() {
  if (!datosDocente) return

  document.getElementById("nombre-docente").textContent = datosDocente.nombre
  document.getElementById("info-docente").textContent = `Clave: ${datosDocente.clave_docente}`
}

// Cargar materias del docente
async function cargarMateriasDocente() {
  try {
    const response = await fetch(`http://localhost:8000/materias/por_docente/?docente_id=${datosDocente.id}`)

    if (response.ok) {
      materiasDocente = await response.json()
      llenarFiltroMaterias()
      verificarClaseActiva()
    } else {
      throw new Error("Error al cargar materias")
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

// Verificar si hay clase activa
function verificarClaseActiva() {
  const ahora = new Date()
  const horaActual = ahora.getHours() * 60 + ahora.getMinutes()
  const diaActual = ahora.toLocaleDateString("es-ES", { weekday: "long" })

  claseActiva = materiasDocente.find((materia) => {
    if (materia.dia.toLowerCase() !== diaActual.toLowerCase()) return false

    const [horaInicio] = materia.hora_inicio.split(":").map(Number)
    const [horaFin] = materia.hora_fin.split(":").map(Number)
    const inicioMinutos =
      horaInicio * 60 + (materia.hora_inicio.split(":")[1] ? Number.parseInt(materia.hora_inicio.split(":")[1]) : 0)
    const finMinutos =
      horaFin * 60 + (materia.hora_fin.split(":")[1] ? Number.parseInt(materia.hora_fin.split(":")[1]) : 0)

    return horaActual >= inicioMinutos && horaActual <= finMinutos
  })

  if (claseActiva) {
    mostrarClaseActiva()
  }
}

// Mostrar alerta de clase activa
function mostrarClaseActiva() {
  const alert = document.getElementById("clase-activa-alert")
  const info = document.getElementById("clase-activa-info")

  info.textContent = `${claseActiva.materia} - Grupo ${claseActiva.grupo} (${claseActiva.hora_inicio} - ${claseActiva.hora_fin})`
  alert.classList.remove("hidden")

  document.getElementById("estado-clase").textContent = "🟢 En clase"
}

// Cargar asistencias
async function cargarAsistencias() {
  try {
    const uid = localStorage.getItem("uid")
    const response = await fetch(`http://localhost:8000/asistencias/ver/${uid}`)

    if (response.ok) {
      asistenciasCompletas = await response.json()
      asistenciasFiltradas = [...asistenciasCompletas]

      actualizarEstadisticas()
      llenarFiltroGrupos()
      mostrarAsistencias()
    } else {
      throw new Error("Error al cargar asistencias")
    }
  } catch (error) {
    console.error("Error:", error)
    mostrarError("Error al cargar las asistencias")
  } finally {
    document.getElementById("loading-asistencias").style.display = "none"
  }
}

// Actualizar estadísticas
function actualizarEstadisticas() {
  const hoy = new Date().toISOString().split("T")[0]
  const asistenciasHoy = asistenciasCompletas.filter((a) => a.fecha === hoy)
  const grupos = [...new Set(asistenciasCompletas.map((a) => a.grupo))]

  document.getElementById("total-materias").textContent = materiasDocente.length
  document.getElementById("total-alumnos").textContent = [
    ...new Set(asistenciasCompletas.map((a) => a.alumno_id)),
  ].length
  document.getElementById("asistencias-hoy").textContent = asistenciasHoy.filter((a) => a.estado === "Presente").length
  document.getElementById("clases-hoy").textContent = materiasDocente.filter((m) => {
    const hoy = new Date().toLocaleDateString("es-ES", { weekday: "long" })
    return m.dia.toLowerCase() === hoy.toLowerCase()
  }).length
}

// Llenar filtros
function llenarFiltroMaterias() {
  const select = document.getElementById("filtro-materia")
  select.innerHTML = '<option value="">Seleccionar materia</option>'

  materiasDocente.forEach((materia) => {
    const option = document.createElement("option")
    option.value = materia.materia
    option.textContent = materia.materia
    select.appendChild(option)
  })
}

function llenarFiltroGrupos() {
  const grupos = [...new Set(asistenciasCompletas.map((a) => a.grupo))]
  const select = document.getElementById("filtro-grupo")

  select.innerHTML = '<option value="">Todos los grupos</option>'

  grupos.forEach((grupo) => {
    const option = document.createElement("option")
    option.value = grupo
    option.textContent = `Grupo ${grupo}`
    select.appendChild(option)
  })
}

// Mostrar asistencias
function mostrarAsistencias() {
  const tbody = document.getElementById("tabla-asistencias")
  const noAsistencias = document.getElementById("no-asistencias")

  if (asistenciasFiltradas.length === 0) {
    tbody.innerHTML = ""
    noAsistencias.classList.remove("hidden")
    return
  }

  noAsistencias.classList.add("hidden")

  tbody.innerHTML = asistenciasFiltradas
    .map((asistencia) => {
      const estadoClass = getEstadoClass(asistencia.estado)
      const puedeModificar = claseActiva && esHoy(asistencia.fecha)

      return `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
          ${asistencia.alumno_nombre || "N/A"}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${asistencia.matricula || "N/A"}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${asistencia.grupo || "N/A"}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${formatearFecha(asistencia.fecha)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${formatearHora(asistencia.hora)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${estadoClass}">
            ${asistencia.estado}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
          ${
            puedeModificar
              ? `
            <button onclick="abrirModalModificar(${asistencia.id})" 
                    class="text-green-600 hover:text-green-900 mr-2">
              <i data-lucide="edit" class="h-4 w-4 inline"></i>
              Modificar
            </button>
          `
              : `
            <span class="text-gray-400">Solo lectura</span>
          `
          }
        </td>
      </tr>
    `
    })
    .join("")

  if (typeof lucide !== "undefined") {
    lucide.createIcons()
  }
}

// Funciones auxiliares
function getEstadoClass(estado) {
  switch (estado) {
    case "Presente":
      return "bg-green-100 text-green-800"
    case "Ausente":
      return "bg-red-100 text-red-800"
    case "Tardanza":
      return "bg-yellow-100 text-yellow-800"
    case "Justificado":
      return "bg-blue-100 text-blue-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

function esHoy(fecha) {
  const hoy = new Date().toISOString().split("T")[0]
  return fecha === hoy
}

function formatearFecha(fecha) {
  if (!fecha) return "N/A"
  const date = new Date(fecha)
  return date.toLocaleDateString("es-ES")
}

function formatearHora(hora) {
  if (!hora) return "N/A"
  return hora.substring(0, 5)
}

// Aplicar filtros
function aplicarFiltros() {
  const materiaFiltro = document.getElementById("filtro-materia").value
  const grupoFiltro = document.getElementById("filtro-grupo").value
  const fechaFiltro = document.getElementById("filtro-fecha").value

  asistenciasFiltradas = asistenciasCompletas.filter((asistencia) => {
    if (materiaFiltro && asistencia.materia !== materiaFiltro) return false
    if (grupoFiltro && asistencia.grupo !== grupoFiltro) return false
    if (fechaFiltro && asistencia.fecha !== fechaFiltro) return false
    return true
  })

  mostrarAsistencias()
}

// Limpiar filtros
function limpiarFiltros() {
  document.getElementById("filtro-materia").value = ""
  document.getElementById("filtro-grupo").value = ""
  document.getElementById("filtro-fecha").value = ""

  asistenciasFiltradas = [...asistenciasCompletas]
  mostrarAsistencias()
}

// Modal para modificar asistencia
function abrirModalModificar(asistenciaId) {
  asistenciaEditando = asistenciasCompletas.find((a) => a.id === asistenciaId)
  if (!asistenciaEditando) return

  document.getElementById("modal-alumno").textContent = asistenciaEditando.alumno_nombre
  document.getElementById("modal-fecha").textContent = formatearFecha(asistenciaEditando.fecha)
  document.getElementById("modal-estado").value = asistenciaEditando.estado

  document.getElementById("modal-modificar").classList.remove("hidden")
  document.getElementById("modal-modificar").classList.add("flex")
}

function cerrarModal() {
  document.getElementById("modal-modificar").classList.add("hidden")
  document.getElementById("modal-modificar").classList.remove("flex")
  asistenciaEditando = null
}

// Guardar cambio de asistencia
async function guardarCambioAsistencia() {
  if (!asistenciaEditando) return

  const nuevoEstado = document.getElementById("modal-estado").value
  const uid = localStorage.getItem("uid")

  try {
    const response = await fetch("http://localhost:8000/asistencias/modificar/", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        asistencia_id: asistenciaEditando.id,
        nuevo_estado: nuevoEstado,
        uid: uid,
      }),
    })

    if (response.ok) {
      // Actualizar localmente
      asistenciaEditando.estado = nuevoEstado
      const index = asistenciasCompletas.findIndex((a) => a.id === asistenciaEditando.id)
      if (index !== -1) {
        asistenciasCompletas[index].estado = nuevoEstado
      }

      mostrarAsistencias()
      cerrarModal()
      mostrarNotificacion("Asistencia modificada correctamente", "success")
    } else {
      throw new Error("Error al modificar asistencia")
    }
  } catch (error) {
    console.error("Error:", error)
    mostrarNotificacion("Error al modificar asistencia", "error")
  }
}

// Marcar todos como presentes
function marcarTodosPresentes() {
  if (!claseActiva) {
    mostrarNotificacion("No hay clase activa", "warning")
    return
  }

  if (confirm("¿Marcar todos los alumnos como presentes para la clase actual?")) {
    // Implementar lógica para marcar todos como presentes
    mostrarNotificacion("Funcionalidad en desarrollo", "info")
  }
}

// Exportar asistencias
function exportarAsistencias() {
  // Implementar exportación a CSV/Excel
  mostrarNotificacion("Funcionalidad de exportación en desarrollo", "info")
}

// Mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = "info") {
  // Crear elemento de notificación
  const notificacion = document.createElement("div")
  notificacion.className = `fixed top-4 right-4 p-4 rounded-md shadow-lg z-50 ${
    tipo === "success"
      ? "bg-green-500 text-white"
      : tipo === "error"
        ? "bg-red-500 text-white"
        : tipo === "warning"
          ? "bg-yellow-500 text-white"
          : "bg-blue-500 text-white"
  }`
  notificacion.textContent = mensaje

  document.body.appendChild(notificacion)

  // Remover después de 3 segundos
  setTimeout(() => {
    notificacion.remove()
  }, 3000)
}

// Mostrar error
function mostrarError(mensaje) {
  const tbody = document.getElementById("tabla-asistencias")
  tbody.innerHTML = `
    <tr>
      <td colspan="7" class="px-6 py-4 text-center text-red-600">
        <i data-lucide="alert-circle" class="h-5 w-5 inline mr-2"></i>
        ${mensaje}
      </td>
    </tr>
  `

  if (typeof lucide !== "undefined") {
    lucide.createIcons()
  }
}

// Cerrar sesión
function cerrarSesion() {
  localStorage.removeItem("uid")
  localStorage.removeItem("usuario_rol")
  localStorage.removeItem("usuario_nombre")
  window.location.href = "index.html"
}

// Inicializar
document.addEventListener("DOMContentLoaded", async () => {
  if (!verificarAutenticacion()) return

  await cargarDatosDocente()
  await cargarMateriasDocente()
  await cargarAsistencias()

  // Establecer fecha de hoy por defecto
  document.getElementById("filtro-fecha").value = new Date().toISOString().split("T")[0]
})
