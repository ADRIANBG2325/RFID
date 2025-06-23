// Variables globales
let currentUID = null
let socket = null
let tipoLogin = "tarjeta" // "tarjeta" o "username"
const io = window.io // Declare the io variable

// Elementos del DOM
const uidDisplay = document.getElementById("uid-display")
const usernameInput = document.getElementById("username-input")
const contraseñaInput = document.getElementById("contraseña")
const submitBtn = document.getElementById("submit-btn")
const mensajeElement = document.getElementById("mensaje")

// Secciones
const seccionTarjeta = document.getElementById("seccion-tarjeta")
const seccionUsername = document.getElementById("seccion-username")

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo = "error") {
  if (mensajeElement) {
    mensajeElement.textContent = mensaje
    mensajeElement.className = `font-medium mb-4 p-3 rounded ${
      tipo === "error"
        ? "text-red-700 bg-red-50 border border-red-200"
        : tipo === "success"
          ? "text-green-700 bg-green-50 border border-green-200"
          : tipo === "warning"
            ? "text-yellow-700 bg-yellow-50 border border-yellow-200"
            : "text-blue-700 bg-blue-50 border border-blue-200"
    }`
  }
}

// Función para cambiar tipo de login
function cambiarTipoLogin(nuevoTipo) {
  tipoLogin = nuevoTipo
  console.log(`🔄 Cambiando tipo de login a: ${tipoLogin}`)

  if (tipoLogin === "tarjeta") {
    // Mostrar sección de tarjeta
    seccionTarjeta.classList.remove("hidden")
    seccionUsername.classList.add("hidden")

    // Conectar socket si no está conectado
    if (!socket) {
      conectarSocket()
    }
  } else {
    // Mostrar sección de username
    seccionTarjeta.classList.add("hidden")
    seccionUsername.classList.remove("hidden")

    // Desconectar socket si está conectado
    if (socket) {
      socket.disconnect()
      socket = null
    }

    // Enfocar campo de username
    usernameInput.focus()
  }

  // Limpiar estado
  currentUID = null
  mostrarMensaje("", "info")
  actualizarBotonEnvio()
}

// Event listeners para radio buttons
document.querySelectorAll('input[name="tipo-login"]').forEach((radio) => {
  radio.addEventListener("change", (e) => {
    cambiarTipoLogin(e.target.value)
  })
})

// Función para actualizar UID automáticamente (solo para tarjeta)
function actualizarUID(nuevoUID) {
  if (tipoLogin !== "tarjeta") return

  if (nuevoUID && nuevoUID !== currentUID) {
    console.log(`🔄 Actualizando UID admin login: ${currentUID} → ${nuevoUID}`)
    currentUID = nuevoUID

    if (uidDisplay) {
      uidDisplay.textContent = nuevoUID
      uidDisplay.className =
        "font-mono text-lg font-bold text-red-600 bg-red-50 px-3 py-1 rounded border-2 border-red-200 animate-pulse"

      // Quitar animación después de 2 segundos
      setTimeout(() => {
        uidDisplay.className =
          "font-mono text-lg font-bold text-red-600 bg-red-50 px-3 py-1 rounded border-2 border-red-200"
      }, 2000)
    }

    mostrarMensaje("Tarjeta detectada para login de administrador.", "info")
    verificarAdminUID(nuevoUID)
  }
}

// Verificar si el UID pertenece a un administrador
async function verificarAdminUID(uid) {
  try {
    const response = await fetch("http://localhost:8000/usuarios/verificar_uid_admin/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ uid: uid }),
    })

    const data = await response.json()
    console.log("📋 Verificación UID admin login:", data)

    if (data.existe) {
      mostrarMensaje(`Administrador encontrado: ${data.admin.nombre}`, "success")
      actualizarBotonEnvio()
    } else if (data.error) {
      mostrarMensaje(data.error, "error")
    } else {
      // Verificar si es otro tipo de usuario
      await verificarOtroTipoUsuario(uid)
    }
  } catch (error) {
    console.error("❌ Error verificando UID admin:", error)
    mostrarMensaje("Error verificando UID", "error")
  }
}

// Verificar si el UID pertenece a otro tipo de usuario
async function verificarOtroTipoUsuario(uid) {
  try {
    const response = await fetch("http://localhost:8000/usuarios/verificar_uid/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ uid: uid }),
    })

    const data = await response.json()
    console.log("📋 Verificación otro usuario:", data)

    if (data.existe && data.usuario) {
      const rol = data.usuario.rol
      const nombre = data.usuario.nombre

      mostrarMensaje(`Esta tarjeta pertenece a ${nombre} (${rol}). Redirigiendo...`, "warning")

      setTimeout(() => {
        if (rol === "alumno") {
          window.location.href = "alumno_panel.html"
        } else if (rol === "docente") {
          window.location.href = "docente_panel.html"
        } else {
          window.location.href = "login.html"
        }
      }, 2000)
    } else {
      mostrarMensaje("Esta tarjeta no está registrada en el sistema.", "error")
    }
  } catch (error) {
    console.error("❌ Error verificando otro usuario:", error)
    mostrarMensaje("Esta tarjeta no pertenece a un administrador.", "error")
  }
}

// Conectar a Socket.IO para recibir UIDs en tiempo real (solo para tarjeta)
function conectarSocket() {
  if (tipoLogin !== "tarjeta") return

  try {
    socket = io("http://localhost:8000", {
      transports: ["polling", "websocket"],
      timeout: 10000,
    })

    socket.on("connect", () => {
      console.log("✅ Socket conectado en admin login")
    })

    socket.on("respuesta_uid", (data) => {
      const nuevoUID = data.uid || data
      if (nuevoUID) {
        console.log("📥 Nuevo UID recibido en admin login:", nuevoUID)
        actualizarUID(nuevoUID)
      }
    })

    socket.on("disconnect", () => {
      console.log("🔌 Socket desconectado en admin login")
    })
  } catch (error) {
    console.error("❌ Error conectando socket:", error)
  }
}

// Función para actualizar estado del botón de envío
function actualizarBotonEnvio() {
  let tieneIdentificador = false

  if (tipoLogin === "tarjeta") {
    tieneIdentificador = currentUID !== null
  } else {
    tieneIdentificador = usernameInput.value.trim().length >= 3
  }

  const tieneContraseña = contraseñaInput.value.length > 0

  const puedeEnviar = tieneIdentificador && tieneContraseña

  submitBtn.disabled = !puedeEnviar

  if (puedeEnviar) {
    submitBtn.className =
      "w-full bg-red-600 hover:bg-red-700 text-white px-4 py-3 rounded font-medium transition-colors cursor-pointer"
  } else {
    submitBtn.className = "w-full bg-gray-400 text-gray-700 px-4 py-3 rounded font-medium cursor-not-allowed"
  }
}

// Event listeners para validación en tiempo real
usernameInput.addEventListener("input", actualizarBotonEnvio)
contraseñaInput.addEventListener("input", actualizarBotonEnvio)

// Manejar envío del formulario - CORREGIDO
document.getElementById("admin-login-form").addEventListener("submit", async (e) => {
  e.preventDefault()

  let identificador = ""

  if (tipoLogin === "tarjeta") {
    identificador = currentUID
  } else {
    identificador = usernameInput.value.trim()
  }

  const contraseña = contraseñaInput.value

  // Validaciones finales
  if (!identificador) {
    mostrarMensaje(
      tipoLogin === "tarjeta" ? "Debe acercar una tarjeta RFID." : "Debe ingresar un nombre de usuario.",
      "error",
    )
    return
  }

  if (!contraseña) {
    mostrarMensaje("Debe ingresar su contraseña.", "error")
    return
  }

  // Deshabilitar botón durante el envío
  submitBtn.disabled = true
  submitBtn.textContent = "Iniciando sesión..."
  submitBtn.className = "w-full bg-gray-400 text-gray-700 px-4 py-3 rounded font-medium cursor-not-allowed"

  try {
    const payload = {
      uid: identificador,
      password: contraseña, // CORREGIDO: usar 'password' en lugar de 'contraseña'
    }

    console.log("🚀 Enviando login de administrador:", payload)

    const response = await fetch("http://localhost:8000/usuarios/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    })

    console.log(`📡 Respuesta del servidor: ${response.status}`)

    if (!response.ok) {
      const errorData = await response.json()
      console.error("❌ Error del servidor:", errorData)
      mostrarMensaje(`Error: ${errorData.detail || "Error en el login"}`, "error")
      return
    }

    const data = await response.json()
    console.log("📥 Respuesta exitosa:", data)

    if (data.rol === "admin") {
      mostrarMensaje("✅ Login exitoso. Redirigiendo al panel de administración...", "success")

      // Guardar datos del administrador
      localStorage.clear()
      localStorage.setItem("uid", data.uid)
      localStorage.setItem("userData", JSON.stringify(data))
      localStorage.setItem("usuario_rol", data.rol)
      localStorage.setItem("usuario_nombre", data.nombre)

      console.log("💾 Datos de admin guardados en localStorage")

      setTimeout(() => {
        window.location.href = "admin_panel.html"
      }, 1500)
    } else {
      // Usuario no es admin, redirigir según su rol
      mostrarMensaje(`Usted es ${data.rol}. Redirigiendo a su panel...`, "warning")

      localStorage.setItem("uid", data.uid)
      localStorage.setItem("userData", JSON.stringify(data))
      localStorage.setItem("usuario_rol", data.rol)
      localStorage.setItem("usuario_nombre", data.nombre)

      setTimeout(() => {
        if (data.rol === "alumno") {
          window.location.href = "alumno_panel.html"
        } else if (data.rol === "docente") {
          window.location.href = "docente_panel.html"
        } else {
          window.location.href = "index.html"
        }
      }, 2000)
    }
  } catch (error) {
    console.error("❌ Error en login admin:", error)
    mostrarMensaje("Error de conexión. Verifique que el servidor esté funcionando.", "error")
  } finally {
    if (!document.getElementById("mensaje").textContent.includes("exitoso")) {
      submitBtn.disabled = false
      submitBtn.textContent = "Iniciar Sesión"
      actualizarBotonEnvio()
    }
  }
})

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
  // Limpiar localStorage al cargar la página de login
  localStorage.clear()

  // Inicializar con tarjeta por defecto
  cambiarTipoLogin("tarjeta")

  // Enfocar campo de contraseña
  contraseñaInput.focus()

  console.log("🔐 Login de administrador inicializado")
})

// Limpiar socket al salir
window.addEventListener("beforeunload", () => {
  if (socket) {
    socket.disconnect()
  }
})
