// Variables globales
let currentUID = null
let socket = null
let tipoRegistro = "tarjeta" // "tarjeta" o "username"
const io = window.io // Declare the io variable

// Elementos del DOM
const uidDisplay = document.getElementById("uid-display")
const usernameInput = document.getElementById("username-input")
const nombreCompletoInput = document.getElementById("nombre-completo")
const claveSecretaInput = document.getElementById("clave-secreta")
const contraseñaInput = document.getElementById("contraseña")
const confirmarInput = document.getElementById("confirmar")
const passwordStrength = document.getElementById("password-strength")
const passwordMatch = document.getElementById("password-match")
const submitBtn = document.getElementById("submit-btn")
const mensajeElement = document.getElementById("mensaje")

// Secciones
const seccionTarjeta = document.getElementById("seccion-tarjeta")
const seccionUsername = document.getElementById("seccion-username")
const seccionNombre = document.getElementById("seccion-nombre")

// Función para mostrar mensajes - MEJORADA
function mostrarMensaje(mensaje, tipo = "error") {
  console.log(`[${tipo.toUpperCase()}] ${mensaje}`)

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

// Función para cambiar tipo de registro
function cambiarTipoRegistro(nuevoTipo) {
  tipoRegistro = nuevoTipo
  console.log(`🔄 Configurando registro de administrador: ${tipoRegistro}`)

  if (tipoRegistro === "tarjeta") {
    // Mostrar sección de tarjeta y conectar socket
    seccionTarjeta.classList.remove("hidden")
    seccionUsername.classList.remove("hidden")
    seccionNombre.classList.remove("hidden")

    // Conectar socket para tarjeta
    conectarSocket()

    // Actualizar labels
    document.querySelector('label[for="username-input"]').textContent = "Nombre de usuario del administrador:"
    usernameInput.placeholder = "Ingrese nombre de usuario único"

    mostrarMensaje("Registro con tarjeta: Acerque su tarjeta RFID Y complete los datos.", "info")
  } else {
    // Modo solo username (sin tarjeta física)
    seccionTarjeta.classList.add("hidden")
    seccionUsername.classList.remove("hidden")
    seccionNombre.classList.remove("hidden")

    // Desconectar socket
    if (socket) {
      socket.disconnect()
      socket = null
    }

    // Actualizar labels
    document.querySelector('label[for="username-input"]').textContent = "Nombre de usuario (será su UID):"
    usernameInput.placeholder = "Este será su identificador único"

    mostrarMensaje("Registro sin tarjeta: Complete todos los campos.", "info")
  }

  // Limpiar estado
  currentUID = null
  if (uidDisplay) {
    uidDisplay.textContent = "Esperando tarjeta..."
    uidDisplay.className =
      "font-mono text-lg font-bold text-gray-500 bg-gray-50 px-3 py-1 rounded border-2 border-gray-200"
  }
  actualizarBotonEnvio()
}

// Event listeners para radio buttons
document.querySelectorAll('input[name="tipo-registro"]').forEach((radio) => {
  radio.addEventListener("change", (e) => {
    cambiarTipoRegistro(e.target.value)
  })
})

// Función para actualizar UID automáticamente (CORREGIDA)
function actualizarUID(nuevoUID) {
  if (tipoRegistro !== "tarjeta") return

  if (nuevoUID && nuevoUID !== currentUID) {
    console.log(`🔄 UID RECIBIDO para admin: ${currentUID} → ${nuevoUID}`)
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

    mostrarMensaje(`Tarjeta detectada: ${nuevoUID}. Complete los demás campos.`, "success")
    verificarUIDAdmin(nuevoUID)
    actualizarBotonEnvio()
  }
}

// Verificar si el UID puede ser usado para admin
async function verificarUIDAdmin(uid) {
  try {
    console.log(`🔍 Verificando UID admin: ${uid}`)
    const response = await fetch("http://localhost:8000/usuarios/verificar_uid_admin/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ uid: uid }),
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()
    console.log("📋 Verificación UID admin:", data)

    if (data.existe) {
      mostrarMensaje("Este UID ya está registrado como administrador.", "error")
      submitBtn.disabled = true
    } else if (data.error) {
      mostrarMensaje(data.error, "error")
      submitBtn.disabled = true
    } else if (data.disponible) {
      mostrarMensaje(`UID ${uid} disponible para registro de administrador.`, "success")
      actualizarBotonEnvio()
    }
  } catch (error) {
    console.error("❌ Error verificando UID admin:", error)
    mostrarMensaje("Error verificando UID", "error")
  }
}

// Verificar si el nombre de usuario está disponible
async function verificarUsername(username) {
  if (!username || username.length < 3) return

  try {
    const response = await fetch("http://localhost:8000/usuarios/verificar_username_admin/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ username: username }),
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()
    console.log("📋 Verificación username admin:", data)

    if (data.existe) {
      mostrarMensaje(data.error || "Nombre de usuario no disponible", "error")
      return false
    } else if (data.disponible) {
      mostrarMensaje("Nombre de usuario disponible.", "success")
      return true
    }
  } catch (error) {
    console.error("❌ Error verificando username:", error)
    mostrarMensaje("Error verificando nombre de usuario", "error")
    return false
  }
}

// Event listener para verificar username en tiempo real
usernameInput.addEventListener("blur", async () => {
  const username = usernameInput.value.trim()
  if (username) {
    await verificarUsername(username)
    actualizarBotonEnvio()
  }
})

usernameInput.addEventListener("input", () => {
  // Limpiar mensaje cuando el usuario está escribiendo
  if (mensajeElement.textContent.includes("usuario")) {
    mostrarMensaje("", "info")
  }
  actualizarBotonEnvio()
})

// Conectar a Socket.IO para recibir UIDs en tiempo real (CORREGIDO)
function conectarSocket() {
  if (tipoRegistro !== "tarjeta") return

  try {
    console.log("🔌 Conectando socket para admin registro...")
    socket = io("http://localhost:8000", {
      transports: ["polling", "websocket"],
      timeout: 10000,
    })

    socket.on("connect", () => {
      console.log("✅ Socket conectado en admin registro")
      mostrarMensaje("Conexión establecida. Acerque su tarjeta RFID.", "info")
    })

    socket.on("respuesta_uid", (data) => {
      console.log("📥 Datos recibidos del socket:", data)
      const nuevoUID = data.uid || data
      if (nuevoUID) {
        console.log("📥 Nuevo UID recibido en admin registro:", nuevoUID)
        actualizarUID(nuevoUID)
      }
    })

    socket.on("disconnect", () => {
      console.log("🔌 Socket desconectado en admin registro")
      mostrarMensaje("Conexión perdida. Reintentando...", "warning")
    })

    socket.on("connect_error", (error) => {
      console.error("❌ Error de conexión socket:", error)
      mostrarMensaje("Error de conexión. Verifique que el servidor esté funcionando.", "error")
    })
  } catch (error) {
    console.error("❌ Error conectando socket:", error)
    mostrarMensaje("Error conectando con el servidor.", "error")
  }
}

// Función para validar contraseña
function validarContraseña(password) {
  const validaciones = {
    longitud: password.length === 8,
    tieneNumero: /\d/.test(password),
    tieneLetra: /[a-zA-Z]/.test(password),
    noEspacios: !/\s/.test(password),
  }

  return validaciones
}

// Función para mostrar fortaleza de contraseña
function mostrarFortalezaContraseña(password) {
  if (!password) {
    passwordStrength.innerHTML = "Ingrese una contraseña de 8 caracteres"
    passwordStrength.className = "mb-4 text-sm p-2 bg-gray-50 rounded text-gray-500"
    return false
  }

  const validaciones = validarContraseña(password)
  const mensajes = []

  if (!validaciones.longitud) {
    mensajes.push(`❌ Debe tener exactamente 8 caracteres (actual: ${password.length})`)
  } else {
    mensajes.push("✅ Longitud correcta (8 caracteres)")
  }

  if (!validaciones.tieneNumero) {
    mensajes.push("❌ Debe contener al menos un número")
  } else {
    mensajes.push("✅ Contiene números")
  }

  if (!validaciones.tieneLetra) {
    mensajes.push("❌ Debe contener al menos una letra")
  } else {
    mensajes.push("✅ Contiene letras")
  }

  if (!validaciones.noEspacios) {
    mensajes.push("❌ No debe contener espacios")
  } else {
    mensajes.push("✅ Sin espacios")
  }

  const todasValidas = Object.values(validaciones).every((v) => v)
  passwordStrength.innerHTML = mensajes.join("<br>")
  passwordStrength.className = `mb-4 text-sm p-2 rounded ${
    todasValidas ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"
  }`

  return todasValidas
}

// Función para verificar coincidencia de contraseñas
function verificarCoincidenciaContraseñas() {
  const password = contraseñaInput.value
  const confirm = confirmarInput.value

  if (confirm.length === 0) {
    passwordMatch.textContent = ""
    return false
  }

  const coinciden = password === confirm
  passwordMatch.textContent = coinciden ? "✅ Las contraseñas coinciden" : "❌ Las contraseñas no coinciden"
  passwordMatch.className = `text-sm font-medium ${coinciden ? "text-green-600" : "text-red-600"}`

  return coinciden
}

// Función para actualizar estado del botón de envío (CORREGIDA)
function actualizarBotonEnvio() {
  let tieneIdentificador = false
  let tieneUsername = false

  if (tipoRegistro === "tarjeta") {
    // Requiere TANTO tarjeta como username
    tieneIdentificador = currentUID !== null && currentUID !== ""
    tieneUsername = usernameInput.value.trim().length >= 3
  } else {
    // Solo requiere username (que será el UID)
    tieneIdentificador = usernameInput.value.trim().length >= 3
    tieneUsername = true // Ya validado arriba
  }

  const tieneNombreCompleto = nombreCompletoInput.value.trim().length >= 3
  const tieneClaveSecreta = claveSecretaInput.value.trim().length > 0
  const passwordValida = mostrarFortalezaContraseña(contraseñaInput.value)
  const passwordsCoinciden = verificarCoincidenciaContraseñas()

  const puedeEnviar =
    tieneIdentificador &&
    tieneUsername &&
    tieneNombreCompleto &&
    tieneClaveSecreta &&
    passwordValida &&
    passwordsCoinciden

  submitBtn.disabled = !puedeEnviar

  if (puedeEnviar) {
    submitBtn.className =
      "w-full bg-red-600 hover:bg-red-700 text-white px-4 py-3 rounded font-medium transition-colors cursor-pointer"
  } else {
    submitBtn.className = "w-full bg-gray-400 text-gray-700 px-4 py-3 rounded font-medium cursor-not-allowed"
  }

  // Debug: mostrar qué falta
  if (!puedeEnviar) {
    const faltantes = []
    if (!tieneIdentificador) faltantes.push(tipoRegistro === "tarjeta" ? "tarjeta RFID" : "nombre de usuario")
    if (!tieneUsername && tipoRegistro === "tarjeta") faltantes.push("nombre de usuario")
    if (!tieneNombreCompleto) faltantes.push("nombre completo")
    if (!tieneClaveSecreta) faltantes.push("clave secreta")
    if (!passwordValida) faltantes.push("contraseña válida")
    if (!passwordsCoinciden) faltantes.push("confirmación de contraseña")

    console.log("Faltan:", faltantes.join(", "))
  }
}

// Event listeners para validación en tiempo real
claveSecretaInput.addEventListener("input", actualizarBotonEnvio)
contraseñaInput.addEventListener("input", actualizarBotonEnvio)
confirmarInput.addEventListener("input", actualizarBotonEnvio)
nombreCompletoInput.addEventListener("input", actualizarBotonEnvio)

// Manejar envío del formulario - CORREGIDO
document.getElementById("admin-form").addEventListener("submit", async (e) => {
  e.preventDefault()

  console.log("🚀 === INICIO ENVÍO FORMULARIO ADMIN ===")

  let identificadorUID = ""
  let nombreUsuario = ""
  const nombreCompleto = nombreCompletoInput.value.trim()
  const claveSecreta = claveSecretaInput.value.trim()
  const contraseña = contraseñaInput.value
  const confirmar = confirmarInput.value

  if (tipoRegistro === "tarjeta") {
    // Modo tarjeta: usar UID de tarjeta + nombre de usuario separado
    identificadorUID = currentUID
    nombreUsuario = usernameInput.value.trim()

    if (!identificadorUID) {
      mostrarMensaje("Debe acercar una tarjeta RFID.", "error")
      return
    }
  } else {
    // Modo username: el nombre de usuario ES el UID
    identificadorUID = usernameInput.value.trim()
    nombreUsuario = identificadorUID
  }

  console.log("📋 Datos del formulario:")
  console.log(`- Tipo registro: ${tipoRegistro}`)
  console.log(`- UID/Username: ${identificadorUID}`)
  console.log(`- Nombre usuario: ${nombreUsuario}`)
  console.log(`- Nombre completo: ${nombreCompleto}`)
  console.log(`- Clave secreta: ${claveSecreta}`)

  // Validaciones finales
  if (!identificadorUID) {
    mostrarMensaje(
      tipoRegistro === "tarjeta" ? "Debe acercar una tarjeta RFID." : "Debe ingresar un nombre de usuario.",
      "error",
    )
    return
  }

  if (tipoRegistro === "tarjeta" && !nombreUsuario) {
    mostrarMensaje("Debe ingresar un nombre de usuario.", "error")
    return
  }

  if (!nombreCompleto) {
    mostrarMensaje("Debe ingresar el nombre completo.", "error")
    return
  }

  if (!claveSecreta) {
    mostrarMensaje("Debe ingresar la clave secreta.", "error")
    return
  }

  console.log(`🔑 Clave secreta ingresada: '${claveSecreta}'`)

  if (contraseña.length !== 8) {
    mostrarMensaje("La contraseña debe tener exactamente 8 caracteres.", "error")
    return
  }

  if (contraseña !== confirmar) {
    mostrarMensaje("Las contraseñas no coinciden.", "error")
    return
  }

  // Deshabilitar botón durante el envío
  submitBtn.disabled = true
  submitBtn.textContent = "Registrando..."
  submitBtn.className = "w-full bg-gray-400 text-gray-700 px-4 py-3 rounded font-medium cursor-not-allowed"

  try {
    const payload = {
      uid_o_username: identificadorUID,
      nombre_usuario: nombreUsuario,
      nombre_completo: nombreCompleto,
      clave_secreta: claveSecreta,
      contraseña: contraseña,
      confirmar_contraseña: confirmar,
      tipo_registro: tipoRegistro,
    }

    console.log("🚀 Enviando payload:", payload)

    const response = await fetch("http://localhost:8000/usuarios/registrar_admin/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    })

    console.log(`📡 Respuesta del servidor: ${response.status} ${response.statusText}`)

    // Leer respuesta como texto primero para debug
    const responseText = await response.text()
    console.log("📥 Respuesta cruda:", responseText)

    let data
    try {
      data = JSON.parse(responseText)
    } catch (parseError) {
      console.error("❌ Error parseando JSON:", parseError)
      mostrarMensaje("Error: Respuesta inválida del servidor", "error")
      return
    }

    console.log("📥 Datos parseados:", data)

    if (response.ok) {
      if (data.mensaje && data.mensaje.includes("exitosamente")) {
        mostrarMensaje("✅ Administrador registrado correctamente. Redirigiendo al login de admin...", "success")

        // Deshabilitar todo el formulario
        document.getElementById("admin-form").style.pointerEvents = "none"
        document.getElementById("admin-form").style.opacity = "0.7"

        // Redirigir al login de admin después de 2 segundos
        setTimeout(() => {
          window.location.href = "admin_login.html"
        }, 2000)
      } else {
        mostrarMensaje(`❌ ${data.detail || data.mensaje || "Error desconocido"}`, "error")
      }
    } else {
      mostrarMensaje(`❌ ${data.detail || data.mensaje || "Error del servidor"}`, "error")
    }
  } catch (error) {
    console.error("❌ Error en la petición:", error)
    mostrarMensaje("Error de conexión. Verifique que el servidor esté funcionando.", "error")
  } finally {
    if (!document.getElementById("mensaje").textContent.includes("correctamente")) {
      submitBtn.disabled = false
      submitBtn.textContent = "Registrar Administrador"
      actualizarBotonEnvio()
    }
  }
})

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
  console.log("🔐 Inicializando registro de administrador...")

  // Verificar que todos los elementos existen
  const elementos = {
    uidDisplay,
    usernameInput,
    nombreCompletoInput,
    claveSecretaInput,
    contraseñaInput,
    confirmarInput,
    passwordStrength,
    passwordMatch,
    submitBtn,
    mensajeElement,
  }

  for (const [nombre, elemento] of Object.entries(elementos)) {
    if (!elemento) {
      console.error(`❌ Elemento no encontrado: ${nombre}`)
    } else {
      console.log(`✅ Elemento encontrado: ${nombre}`)
    }
  }

  // Inicializar con tarjeta por defecto
  cambiarTipoRegistro("tarjeta")

  // Enfocar campo de clave secreta
  if (claveSecretaInput) {
    claveSecretaInput.focus()
  }

  console.log("✅ Registro de administrador inicializado")
})

// Limpiar socket al salir
window.addEventListener("beforeunload", () => {
  if (socket) {
    socket.disconnect()
  }
})
