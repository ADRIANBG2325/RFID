// Variables globales
let currentUID = localStorage.getItem("uid") || null
let socket = null
let currentUserData = null
const io = window.io // Declare the io variable

// Elementos del DOM
const uidDisplay = document.getElementById("uid-display")
const contraseñaInput = document.getElementById("contraseña")
const loginBtn = document.getElementById("login-btn")
const loginBtnText = document.getElementById("login-btn-text")
const mensajeElement = document.getElementById("mensaje")
const cardStatus = document.getElementById("card-status")
const userInfo = document.getElementById("user-info")
const userName = document.getElementById("user-name")
const userRole = document.getElementById("user-role")
const userAvatar = document.getElementById("user-avatar")
const roleIndicator = document.getElementById("role-indicator")
const togglePassword = document.getElementById("toggle-password")

// ==================== FUNCIONES DE UTILIDAD ====================

function obtenerPrimerNombre(nombreCompleto) {
  if (!nombreCompleto) return "Usuario"
  return nombreCompleto.split(" ")[0]
}

function mostrarMensaje(mensaje, tipo = "error") {
  mensajeElement.textContent = mensaje
  mensajeElement.className = `text-center text-sm font-medium ${
    tipo === "error"
      ? "text-red-500"
      : tipo === "success"
        ? "text-green-500"
        : tipo === "warning"
          ? "text-yellow-500"
          : "text-blue-500"
  }`
}

function actualizarEstadoTarjeta(estado, mensaje) {
  const iconos = {
    waiting: "fas fa-credit-card",
    detected: "fas fa-check-circle",
    error: "fas fa-exclamation-triangle",
  }

  const colores = {
    waiting: "bg-gray-100 text-gray-600",
    detected: "bg-green-100 text-green-600",
    error: "bg-red-100 text-red-600",
  }

  cardStatus.innerHTML = `
    <i class="${iconos[estado]} mr-2"></i>
    <span>${mensaje}</span>
  `
  cardStatus.className = `inline-flex items-center px-4 py-2 rounded-full ${colores[estado]}`
}

function actualizarIndicadorRol(rol) {
  const clases = {
    admin: "role-admin",
    docente: "role-docente",
    alumno: "role-alumno",
  }

  roleIndicator.className = `h-2 transition-all duration-500 ${clases[rol] || "bg-gray-300"}`
}

function actualizarAvatarUsuario(rol, nombre) {
  const iconos = {
    admin: "fas fa-user-shield",
    docente: "fas fa-chalkboard-teacher",
    alumno: "fas fa-user-graduate",
  }

  const colores = {
    admin: "bg-purple-500",
    docente: "bg-blue-500",
    alumno: "bg-green-500",
  }

  userAvatar.innerHTML = `<i class="${iconos[rol] || "fas fa-user"}"></i>`
  userAvatar.className = `w-12 h-12 rounded-full ${colores[rol] || "bg-gray-500"} flex items-center justify-center text-white font-bold mr-4`
}

// ==================== GESTIÓN DE UID Y TARJETAS ====================

function actualizarUID(nuevoUID) {
  if (nuevoUID && nuevoUID !== currentUID) {
    console.log(`🔄 Actualizando UID: ${currentUID} → ${nuevoUID}`)
    currentUID = nuevoUID
    localStorage.setItem("uid", nuevoUID)

    if (uidDisplay) {
      uidDisplay.value = nuevoUID
      uidDisplay.className =
        "w-full px-4 py-3 border-2 border-green-500 rounded-lg bg-green-50 font-mono text-center text-lg focus:ring-2 focus:ring-green-500 pulse-animation"

      setTimeout(() => {
        uidDisplay.className =
          "w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 font-mono text-center text-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
      }, 2000)
    }

    actualizarEstadoTarjeta("detected", "Tarjeta detectada")
    mostrarInfoUsuarioTarjeta(nuevoUID)
    contraseñaInput.value = ""
    actualizarBotonLogin()
  }
}

async function mostrarInfoUsuarioTarjeta(uid) {
  try {
    console.log(`🔍 Consultando información para UID: ${uid}`)

    const response = await fetch(`http://localhost:8000/usuarios/info_tarjeta/${uid}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })

    if (response.ok) {
      const userData = await response.json()
      currentUserData = userData

      const primerNombre = obtenerPrimerNombre(userData.nombre)
      const rolCapitalizado = userData.rol.charAt(0).toUpperCase() + userData.rol.slice(1)

      // Actualizar UI con información del usuario
      userName.textContent = primerNombre
      userRole.textContent = rolCapitalizado
      actualizarAvatarUsuario(userData.rol, userData.nombre)
      actualizarIndicadorRol(userData.rol)

      userInfo.classList.remove("hidden")
      mostrarMensaje(`👋 Hola ${primerNombre}, ingresa tu contraseña`, "info")

      console.log(`✅ Usuario detectado: ${primerNombre} - ${rolCapitalizado}`)
    } else {
      userInfo.classList.add("hidden")
      actualizarIndicadorRol(null)
      mostrarMensaje("Tarjeta detectada. Ingresa tu contraseña.", "info")
      console.log(`⚠️ UID ${uid} no encontrado en la base de datos`)
    }
  } catch (error) {
    console.error("❌ Error consultando información de usuario:", error)
    userInfo.classList.add("hidden")
    mostrarMensaje("Nueva tarjeta detectada.", "info")
  }
}

// ==================== CONEXIÓN SOCKET ====================

function conectarSocket() {
  try {
    socket = io("http://localhost:8000", {
      transports: ["polling", "websocket"],
      timeout: 10000,
    })

    socket.on("connect", () => {
      console.log("✅ Socket conectado")
      actualizarEstadoTarjeta("waiting", "Esperando tarjeta...")
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
      actualizarEstadoTarjeta("error", "Conexión perdida")
    })
  } catch (error) {
    console.error("❌ Error conectando socket:", error)
    actualizarEstadoTarjeta("error", "Error de conexión")
  }
}

// ==================== GESTIÓN DE BOTÓN LOGIN ====================

function actualizarBotonLogin() {
  const tieneUID = currentUID && currentUID.length > 0
  const tieneContraseña = contraseñaInput.value.length > 0
  const puedeLogin = tieneUID && tieneContraseña

  loginBtn.disabled = !puedeLogin

  if (puedeLogin) {
    loginBtn.className =
      "w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 bg-indigo-600 hover:bg-indigo-700 text-white transform hover:scale-105"
  } else {
    loginBtn.className =
      "w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed"
  }
}

// ==================== REDIRECCIÓN MEJORADA ====================

function redirigirSegunRol(datosUsuario) {
  console.log(`🔄 Redirigiendo usuario con rol: ${datosUsuario.rol}`)

  // Guardar datos del usuario en localStorage
  localStorage.setItem("usuario", JSON.stringify(datosUsuario))
  localStorage.setItem("uid", datosUsuario.uid)
  localStorage.setItem("usuario_rol", datosUsuario.rol)
  localStorage.setItem("usuario_nombre", datosUsuario.nombre)

  // URLs de redirección CORREGIDAS
  const redirectUrls = {
    admin: "admin_panel.html",
    docente: "docente_panel.html",
    alumno: "alumno_panel.html",
  }

  const redirectUrl = redirectUrls[datosUsuario.rol] || "index.html"
  console.log(`➡️ Redirigiendo a: ${redirectUrl}`)

  // Mostrar mensaje de bienvenida
  const primerNombre = obtenerPrimerNombre(datosUsuario.nombre)
  mostrarMensaje(`✅ Bienvenido ${primerNombre}`, "success")

  // Actualizar botón con estado de carga
  loginBtn.disabled = true
  loginBtnText.innerHTML = `<i class="fas fa-spinner fa-spin mr-2"></i>Redirigiendo...`

  // Redireccionar después de un breve delay
  setTimeout(() => {
    window.location.href = redirectUrl
  }, 1500)
}

// ==================== MANEJO DE LOGIN ====================

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault()

  const uid = currentUID
  const contraseña = contraseñaInput.value

  if (!uid) {
    mostrarMensaje("UID no encontrado. Vuelva a pasar la tarjeta.", "error")
    return
  }

  if (!contraseña) {
    mostrarMensaje("Por favor ingrese su contraseña.", "error")
    return
  }

  login(uid, contraseña)
})

async function login(uid, contraseña) {
  try {
    console.log(`🔐 Intentando login con UID: ${uid}`)

    // Actualizar UI durante el login
    loginBtn.disabled = true
    loginBtnText.innerHTML = `<i class="fas fa-spinner fa-spin mr-2"></i>Verificando...`

    const response = await fetch("http://localhost:8000/usuarios/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        uid: uid,
        contraseña: contraseña,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      console.log("✅ Login exitoso:", data)
      redirigirSegunRol(data)
    } else {
      console.error("❌ Error en login:", data)
      mostrarMensaje(data.detail || "Error en el login", "error")

      // Restablecer botón
      loginBtn.disabled = false
      loginBtnText.innerHTML = `<i class="fas fa-sign-in-alt mr-2"></i>Iniciar Sesión`
    }
  } catch (error) {
    console.error("❌ Error de conexión:", error)
    mostrarMensaje("Error de conexión. Verifique que el servidor esté funcionando.", "error")

    // Restablecer botón
    loginBtn.disabled = false
    loginBtnText.innerHTML = `<i class="fas fa-sign-in-alt mr-2"></i>Iniciar Sesión`
  }
}

// ==================== EVENT LISTENERS ====================

// Actualizar botón cuando se escribe la contraseña
contraseñaInput.addEventListener("input", actualizarBotonLogin)

// Toggle para mostrar/ocultar contraseña
togglePassword.addEventListener("click", () => {
  const tipo = contraseñaInput.type === "password" ? "text" : "password"
  contraseñaInput.type = tipo

  const icono = tipo === "password" ? "fas fa-eye" : "fas fa-eye-slash"
  togglePassword.innerHTML = `<i class="${icono}"></i>`
})

// ==================== INICIALIZACIÓN ====================

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Inicializando página de login...")

  // Verificar si ya hay un UID guardado
  if (currentUID) {
    console.log(`🔄 UID encontrado en localStorage: ${currentUID}`)
    if (uidDisplay) {
      uidDisplay.value = currentUID
      mostrarInfoUsuarioTarjeta(currentUID)
    }
  }

  // Conectar socket para recibir UIDs
  conectarSocket()

  // Actualizar estado inicial del botón
  actualizarBotonLogin()

  console.log("✅ Login inicializado correctamente")
})

// Limpiar conexiones al salir de la página
window.addEventListener("beforeunload", () => {
  if (socket) {
    socket.disconnect()
  }
})
