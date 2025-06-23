// Variables globales
let usuarioEncontrado = false
let datosUsuario = null
let currentUID = localStorage.getItem("uid") || null
let socket = null
const io = window.io // Declare the io variable

// Elementos del DOM
const uidDisplay = document.getElementById("uid-display")
const uidValue = document.getElementById("uid-value")
const rolSelect = document.getElementById("rol")
const roleIndicator = document.getElementById("role-indicator")
const roleAvatar = document.getElementById("role-avatar")
const roleTitle = document.getElementById("role-title")
const roleDescription = document.getElementById("role-description")
const searchSection = document.getElementById("search-section")
const searchLabel = document.getElementById("search-label")
const identificadorInput = document.getElementById("identificador")
const buscarBtn = document.getElementById("buscar-btn")
const loadingStatus = document.getElementById("loading-status")
const userFound = document.getElementById("user-found")
const userInfo = document.getElementById("user-info")
const passwordSection = document.getElementById("password-section")
const contraseñaInput = document.getElementById("contraseña")
const confirmarInput = document.getElementById("confirmar")
const passwordStrengthBar = document.getElementById("password-strength-bar")
const passwordFeedback = document.getElementById("password-feedback")
const submitBtn = document.getElementById("submit-btn")
const submitText = document.getElementById("submit-text")
const messageContainer = document.getElementById("message-container")
const messageElement = document.getElementById("message")

// Configuración por rol
const roleConfig = {
  alumno: {
    title: "Registro de Alumno",
    description: "Complete la información para registrar un nuevo alumno",
    icon: "fas fa-graduation-cap",
    avatar: "avatar-alumno",
    indicator: "role-alumno",
    searchLabel: "Matrícula del Alumno",
    placeholder: "Ingrese la matrícula",
    endpoint: "http://localhost:8000/usuarios/consultar_alumno/",
  },
  docente: {
    title: "Registro de Docente",
    description: "Complete la información para registrar un nuevo docente",
    icon: "fas fa-chalkboard-teacher",
    avatar: "avatar-docente",
    indicator: "role-docente",
    searchLabel: "Clave del Docente",
    placeholder: "Ingrese la clave de docente",
    endpoint: "http://localhost:8000/usuarios/consultar_docente/",
  },
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo = "error") {
  messageElement.textContent = mensaje
  messageElement.className = `status-card ${
    tipo === "error" ? "status-error" : tipo === "success" ? "status-success" : "status-loading"
  }`
  messageElement.classList.remove("hidden")

  // Auto-hide después de 5 segundos para mensajes de éxito
  if (tipo === "success") {
    setTimeout(() => {
      messageElement.classList.add("hidden")
    }, 5000)
  }
}

// Función para actualizar UID
function actualizarUID(nuevoUID) {
  if (nuevoUID && nuevoUID !== currentUID) {
    console.log(`🔄 Actualizando UID: ${currentUID} → ${nuevoUID}`)
    currentUID = nuevoUID
    localStorage.setItem("uid", nuevoUID)

    document.getElementById("uid").value = nuevoUID
    uidValue.textContent = nuevoUID
    uidDisplay.className = "uid-display animate-pulse"

    setTimeout(() => {
      uidDisplay.className = "uid-display"
    }, 2000)

    mostrarMensaje("Nueva tarjeta detectada para registro.", "success")

    if (usuarioEncontrado) {
      resetearFormulario()
      mostrarMensaje("Nueva tarjeta detectada. Complete el registro nuevamente.", "info")
    }
  }
}

// Conectar Socket.IO
function conectarSocket() {
  try {
    socket = io("http://localhost:8000", {
      transports: ["polling", "websocket"],
      timeout: 10000,
    })

    socket.on("connect", () => {
      console.log("✅ Socket conectado en registro")
    })

    socket.on("respuesta_uid", (data) => {
      const nuevoUID = data.uid || data
      if (nuevoUID) {
        console.log("📥 Nuevo UID recibido:", nuevoUID)
        actualizarUID(nuevoUID)
      }
    })

    socket.on("disconnect", () => {
      console.log("🔌 Socket desconectado")
    })
  } catch (error) {
    console.error("❌ Error conectando socket:", error)
  }
}

// Cambiar interfaz según rol
function cambiarInterfazSegunRol() {
  const rol = rolSelect.value
  const config = roleConfig[rol]

  if (!config) return

  // Actualizar indicador visual
  roleIndicator.className = `role-indicator ${config.indicator} rounded-xl p-4 mb-6`
  roleAvatar.className = `user-avatar ${config.avatar} mr-4`
  roleAvatar.innerHTML = `<i class="${config.icon}"></i>`
  roleTitle.textContent = config.title
  roleDescription.textContent = config.description

  // Actualizar campos de búsqueda
  searchLabel.textContent = config.searchLabel
  identificadorInput.placeholder = config.placeholder

  // Resetear formulario
  resetearFormulario()
}

// Validar contraseña
function validarContraseña(password) {
  const validaciones = {
    longitud: password.length === 8,
    tieneNumero: /\d/.test(password),
    tieneLetra: /[a-zA-Z]/.test(password),
    noEspacios: !/\s/.test(password),
  }

  return validaciones
}

// Mostrar fortaleza de contraseña
function mostrarFortalezaContraseña(password) {
  if (!password) {
    passwordStrengthBar.className = "password-strength"
    passwordFeedback.textContent = ""
    return false
  }

  const validaciones = validarContraseña(password)
  const validCount = Object.values(validaciones).filter((v) => v).length

  // Actualizar barra visual
  const strengthClasses = ["strength-weak", "strength-fair", "strength-good", "strength-strong"]
  passwordStrengthBar.className = `password-strength ${strengthClasses[validCount - 1] || ""}`

  // Mostrar feedback
  const mensajes = []
  if (!validaciones.longitud) mensajes.push("8 caracteres")
  if (!validaciones.tieneNumero) mensajes.push("números")
  if (!validaciones.tieneLetra) mensajes.push("letras")
  if (!validaciones.noEspacios) mensajes.push("sin espacios")

  const todasValidas = Object.values(validaciones).every((v) => v)

  if (todasValidas) {
    passwordFeedback.innerHTML =
      '<i class="fas fa-check text-green-600 mr-1"></i><span class="text-green-600">Contraseña válida</span>'
  } else {
    passwordFeedback.innerHTML = `<i class="fas fa-exclamation-triangle text-orange-500 mr-1"></i><span class="text-orange-600">Falta: ${mensajes.join(", ")}</span>`
  }

  return todasValidas
}

// Verificar coincidencia de contraseñas
function verificarCoincidenciaContraseñas() {
  const password = contraseñaInput.value
  const confirm = confirmarInput.value

  if (confirm.length === 0) return false

  const coinciden = password === confirm
  return coinciden
}

// Actualizar estado del botón
function actualizarBotonEnvio() {
  const passwordValida = mostrarFortalezaContraseña(contraseñaInput.value)
  const passwordsCoinciden = verificarCoincidenciaContraseñas()

  const puedeEnviar = usuarioEncontrado && passwordValida && passwordsCoinciden

  submitBtn.disabled = !puedeEnviar

  if (puedeEnviar) {
    submitBtn.className = "btn-primary w-full mt-6"
    submitText.textContent = "Registrar Usuario"
  } else {
    submitBtn.className = "btn-primary w-full mt-6 opacity-50 cursor-not-allowed"
    submitText.textContent = "Complete todos los campos"
  }
}

// Event listeners
rolSelect.addEventListener("change", cambiarInterfazSegunRol)
contraseñaInput.addEventListener("input", actualizarBotonEnvio)
confirmarInput.addEventListener("input", actualizarBotonEnvio)

// Toggle password visibility
document.getElementById("toggle-password").addEventListener("click", () => {
  const input = contraseñaInput
  const icon = document.querySelector("#toggle-password i")

  if (input.type === "password") {
    input.type = "text"
    icon.className = "fas fa-eye-slash"
  } else {
    input.type = "password"
    icon.className = "fas fa-eye"
  }
})

document.getElementById("toggle-confirm").addEventListener("click", () => {
  const input = confirmarInput
  const icon = document.querySelector("#toggle-confirm i")

  if (input.type === "password") {
    input.type = "text"
    icon.className = "fas fa-eye-slash"
  } else {
    input.type = "password"
    icon.className = "fas fa-eye"
  }
})

// Buscar usuario
buscarBtn.addEventListener("click", async () => {
  const rol = rolSelect.value
  const identificador = identificadorInput.value.trim()
  const config = roleConfig[rol]

  if (!identificador) {
    mostrarMensaje("Por favor ingrese un identificador", "error")
    return
  }

  // Mostrar loading
  loadingStatus.classList.remove("hidden")
  userFound.classList.add("hidden")
  passwordSection.classList.add("hidden")
  buscarBtn.disabled = true
  buscarBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Buscando...'

  usuarioEncontrado = false
  mostrarMensaje("", "")

  try {
    console.log("Buscando en:", config.endpoint + encodeURIComponent(identificador))
    const response = await fetch(config.endpoint + encodeURIComponent(identificador))

    if (response.ok) {
      const data = await response.json()
      console.log("Datos recibidos:", data)

      datosUsuario = { ...data, rol, identificador }
      mostrarDatosUsuario(datosUsuario)
      usuarioEncontrado = true
      mostrarCamposContraseña()
      mostrarMensaje("Usuario encontrado correctamente", "success")
    } else {
      const errorData = await response.json()
      mostrarMensaje(`${errorData.detail || "Usuario no encontrado"}`, "error")
    }
  } catch (error) {
    console.error("Error al buscar:", error)
    mostrarMensaje("Error de conexión. Verifique que el servidor esté funcionando.", "error")
  } finally {
    loadingStatus.classList.add("hidden")
    buscarBtn.disabled = false
    buscarBtn.innerHTML = '<i class="fas fa-search mr-2"></i>Buscar'
  }
})

// Mostrar datos del usuario
function mostrarDatosUsuario(datos) {
  console.log("Mostrando datos:", datos)

  let infoHTML = `
    <div class="flex items-center">
      <i class="fas fa-user text-green-600 mr-2"></i>
      <span class="font-medium">Nombre:</span>
    </div>
    <div class="text-gray-700">${datos.nombre || "N/A"}</div>
  `

  if (datos.rol === "alumno") {
    infoHTML += `
      <div class="flex items-center">
        <i class="fas fa-id-card text-green-600 mr-2"></i>
        <span class="font-medium">Matrícula:</span>
      </div>
      <div class="text-gray-700">${datos.matricula || datos.identificador || "N/A"}</div>
      
      <div class="flex items-center">
        <i class="fas fa-graduation-cap text-green-600 mr-2"></i>
        <span class="font-medium">Carrera:</span>
      </div>
      <div class="text-gray-700">${datos.carrera || "N/A"}</div>
      
      <div class="flex items-center">
        <i class="fas fa-layer-group text-green-600 mr-2"></i>
        <span class="font-medium">Semestre:</span>
      </div>
      <div class="text-gray-700">${datos.semestre || "N/A"}°</div>
      
      <div class="flex items-center">
        <i class="fas fa-users text-green-600 mr-2"></i>
        <span class="font-medium">Grupo:</span>
      </div>
      <div class="text-gray-700">${datos.grupo || "N/A"}</div>
    `
  } else if (datos.rol === "docente") {
    infoHTML += `
      <div class="flex items-center">
        <i class="fas fa-key text-green-600 mr-2"></i>
        <span class="font-medium">Clave:</span>
      </div>
      <div class="text-gray-700">${datos.clave || datos.identificador || "N/A"}</div>
      
      <div class="flex items-center">
        <i class="fas fa-chalkboard text-green-600 mr-2"></i>
        <span class="font-medium">Especialidad:</span>
      </div>
      <div class="text-gray-700">${datos.especialidad || "N/A"}</div>
    `
  }

  userInfo.innerHTML = infoHTML
  userFound.classList.remove("hidden")
}

// Mostrar campos de contraseña
function mostrarCamposContraseña() {
  passwordSection.classList.remove("hidden")
  contraseñaInput.value = ""
  confirmarInput.value = ""
  passwordStrengthBar.className = "password-strength"
  passwordFeedback.textContent = ""

  setTimeout(() => {
    contraseñaInput.focus()
  }, 100)

  actualizarBotonEnvio()
}

// Resetear formulario
function resetearFormulario() {
  userFound.classList.add("hidden")
  passwordSection.classList.add("hidden")
  loadingStatus.classList.add("hidden")
  usuarioEncontrado = false
  datosUsuario = null
  identificadorInput.value = ""
  contraseñaInput.value = ""
  confirmarInput.value = ""
  messageElement.classList.add("hidden")
  actualizarBotonEnvio()
}

// Envío del formulario
document.getElementById("registro-form").addEventListener("submit", async (e) => {
  e.preventDefault()

  if (!usuarioEncontrado) {
    mostrarMensaje("Debe buscar y encontrar un usuario válido antes de registrar", "error")
    return
  }

  const uid = currentUID
  const contraseña = contraseñaInput.value
  const confirmar = confirmarInput.value

  // Validaciones finales
  if (!uid) {
    mostrarMensaje("UID no encontrado. Vuelva a pasar la tarjeta.", "error")
    return
  }

  if (contraseña.length !== 8) {
    mostrarMensaje("La contraseña debe tener exactamente 8 caracteres.", "error")
    return
  }

  if (contraseña !== confirmar) {
    mostrarMensaje("Las contraseñas no coinciden.", "error")
    return
  }

  // Deshabilitar botón
  submitBtn.disabled = true
  submitText.textContent = "Registrando..."
  submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Registrando...'

  try {
    const payload = {
      uid: uid,
      rol: datosUsuario.rol,
      identificador: datosUsuario.identificador,
      contraseña: contraseña,
      confirmar_contraseña: confirmar,
      datos_usuario: datosUsuario,
    }

    console.log("🚀 Enviando datos:", payload)

    const response = await fetch("http://localhost:8000/usuarios/registrar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })

    const data = await response.json()
    console.log("📥 Respuesta:", data)

    if (response.ok && data.mensaje === "Usuario registrado correctamente") {
      mostrarMensaje("✅ Usuario registrado correctamente. Redirigiendo al login...", "success")

      // Deshabilitar formulario
      document.getElementById("registro-form").style.pointerEvents = "none"
      document.getElementById("registro-form").style.opacity = "0.7"

      setTimeout(() => {
        window.location.href = "login.html"
      }, 2000)
    } else {
      mostrarMensaje(`❌ ${data.detail || "Error al registrar"}`, "error")
    }
  } catch (error) {
    console.error("Error al registrar:", error)
    mostrarMensaje("Error de conexión. Verifique que el servidor esté funcionando.", "error")
  } finally {
    if (!document.getElementById("message").textContent.includes("correctamente")) {
      submitBtn.disabled = false
      submitText.textContent = "Registrar Usuario"
      submitBtn.innerHTML = '<i class="fas fa-user-plus mr-2"></i>Registrar Usuario'
      actualizarBotonEnvio()
    }
  }
})

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
  // Mostrar UID actual
  if (currentUID) {
    uidValue.textContent = currentUID
  }

  // Configurar interfaz inicial
  cambiarInterfazSegunRol()

  // Conectar socket
  conectarSocket()

  console.log("📋 Registro inicializado con UID:", currentUID)
})

// Limpiar socket al salir
window.addEventListener("beforeunload", () => {
  if (socket) {
    socket.disconnect()
  }
})
