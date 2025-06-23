let currentUID = null
let socket = null
let connectionAttempts = 0
const MAX_RECONNECT_ATTEMPTS = 5
const RECONNECT_DELAY = 3000 // 3 segundos

// Elementos del DOM
const mensajeElement = document.getElementById("mensaje")
const respuestaElement = document.getElementById("respuesta")

// Variable para controlar cambio automático de UID
let lastUIDTime = 0
const UID_CHANGE_COOLDOWN = 1000 // 1 segundo entre cambios

// Al inicio del archivo, después de las variables existentes
// Usar configuración dinámica de URLs
const API_BASE_URL = window.APP_CONFIG?.API_URL || "http://localhost:8000"
const SOCKET_URL = window.APP_CONFIG?.SOCKET_URL || "http://localhost:8000"

// Obtener la IP del servidor dinámicamente
async function obtenerIPServidor() {
  try {
    // En producción, usar la URL configurada
    if (window.APP_CONFIG?.API_URL) {
      const url = new URL(window.APP_CONFIG.API_URL)
      return url.hostname
    }

    // Código existente para desarrollo local...
    const response = await fetch(`${API_BASE_URL}/network-info`)
    const data = await response.json()
    return data.server_ip
  } catch (error) {
    console.log("No se pudo obtener IP del servidor, usando configuración por defecto")
    return window.APP_CONFIG?.API_URL ? new URL(window.APP_CONFIG.API_URL).hostname : "localhost"
  }
}

// Función para actualizar el estado en la UI
function updateStatus(message, type = "info") {
  if (mensajeElement) {
    mensajeElement.textContent = message
    mensajeElement.className = `mb-2 text-lg ${
      type === "error" ? "text-red-600" : type === "success" ? "text-green-600" : "text-blue-600"
    }`
  }
  console.log(`[${type.toUpperCase()}] ${message}`)
}

// Función para actualizar indicador de conexión
function updateConnectionIndicator(connected) {
  const indicator = document.getElementById("connection-indicator")
  const text = document.getElementById("connection-text")

  if (indicator && text) {
    if (connected) {
      indicator.className = "w-3 h-3 bg-green-500 rounded-full animate-pulse"
      text.textContent = "Conectado"
      text.className = "text-sm text-green-600"
    } else {
      indicator.className = "w-3 h-3 bg-red-500 rounded-full"
      text.textContent = "Desconectado"
      text.className = "text-sm text-red-600"
    }
  }
}

// Función para conectar al backend
async function connectToBackend() {
  try {
    updateStatus("Conectando al servidor...", "info")
    updateConnectionIndicator(false)

    const socketURL = SOCKET_URL
    console.log(`🌐 Conectando a: ${socketURL}`)

    socket = io(socketURL, {
      transports: ["polling", "websocket"],
      timeout: 10000,
      forceNew: true,
    })

    // Evento: Conexión exitosa
    socket.on("connect", () => {
      console.log(`✅ Conectado al backend vía Socket.IO en ${socketURL}`)
      updateStatus("Conectado al servidor. Esperando tarjeta RFID...", "success")
      updateConnectionIndicator(true)
      connectionAttempts = 0

      // Enviar ping para verificar conexión
      socket.emit("ping", { message: "Frontend conectado" })
    })

    // Evento: Error de conexión
    socket.on("connect_error", (error) => {
      console.error("❌ Error de conexión:", error)
      updateStatus(`Error de conexión al servidor (${API_BASE_URL}:8000)`, "error")
      updateConnectionIndicator(false)
      attemptReconnect()
    })

    // Evento: Desconexión
    socket.on("disconnect", (reason) => {
      console.warn("🔌 Desconectado del backend:", reason)
      updateStatus("Desconectado del servidor", "error")
      updateConnectionIndicator(false)

      if (reason === "io server disconnect") {
        // Reconexión manual si el servidor desconectó
        attemptReconnect()
      }
    })

    // Evento: Estado de conexión
    socket.on("connection_status", (data) => {
      console.log("📡 Estado de conexión:", data)
      updateStatus(data.message, "success")
    })

    // Evento: UID recibido desde el backend
    socket.on("respuesta_uid", (data) => {
      console.log("📥 UID recibido del backend:", data)
      handleReceivedUID(data)
    })

    // Evento: Pong (respuesta al ping)
    socket.on("pong", (data) => {
      console.log("🏓 Pong recibido:", data)
    })
  } catch (error) {
    console.error("❌ Error inicializando Socket.IO:", error)
    updateStatus("Error inicializando conexión", "error")
    updateConnectionIndicator(false)
  }
}

// Función para manejar reconexión
function attemptReconnect() {
  if (connectionAttempts < MAX_RECONNECT_ATTEMPTS) {
    connectionAttempts++
    updateStatus(`Reintentando conexión... (${connectionAttempts}/${MAX_RECONNECT_ATTEMPTS})`, "info")

    setTimeout(() => {
      connectToBackend()
    }, RECONNECT_DELAY)
  } else {
    updateStatus("No se pudo conectar al servidor. Verifique que esté funcionando.", "error")
    updateConnectionIndicator(false)
    if (respuestaElement) {
      respuestaElement.innerHTML = `
        <div class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          <strong>Error de conexión:</strong><br>
          • Verifique que el servidor backend esté ejecutándose<br>
          • Verifique la conexión de red<br>
          • Recargue la página para reintentar
        </div>
      `
    }
  }
}

// Función para manejar UID recibido con cambio automático
function handleReceivedUID(data) {
  const uid = data.uid || data

  if (!uid) {
    console.warn("❌ UID inválido recibido:", data)
    updateStatus("UID inválido recibido", "error")
    return
  }

  const now = Date.now()

  // Verificar si es un UID diferente
  if (currentUID && currentUID !== uid && now - lastUIDTime > UID_CHANGE_COOLDOWN) {
    console.log(`🔄 Nueva tarjeta detectada: ${currentUID} → ${uid}`)
    updateStatus(`Nueva tarjeta detectada: ${uid}`, "info")

    // Limpiar estado anterior
    if (respuestaElement) {
      respuestaElement.innerHTML = ""
    }

    // Actualizar localStorage inmediatamente
    localStorage.setItem("uid", uid)

    // Mostrar notificación de cambio
    if (respuestaElement) {
      respuestaElement.innerHTML = `
        <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded animate-pulse">
          <strong>🔄 Nueva tarjeta detectada</strong><br>
          <strong>UID:</strong> ${uid}<br>
          <small class="text-gray-600">Procesando...</small>
        </div>
      `
    }
  }

  currentUID = uid
  lastUIDTime = now

  console.log("🎫 UID procesado:", currentUID)
  updateStatus(`UID detectado: ${currentUID}`, "success")

  // Verificar el estado del UID
  verificarEstadoUID(currentUID)
}

// Función principal para verificar el estado del UID
async function verificarEstadoUID(uid) {
  try {
    updateStatus("Verificando UID...", "info")

    // Obtener IP del servidor para las peticiones HTTP
    const serverIP = await obtenerIPServidor()
    const apiURL = `http://${serverIP}:8000`

    // PRIMERO: Verificar si es administrador
    console.log("🔍 Verificando si es administrador...")
    const responseAdmin = await fetch(`${apiURL}/usuarios/verificar_uid_admin/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ uid: uid }),
    })

    if (responseAdmin.ok) {
      const dataAdmin = await responseAdmin.json()
      console.log("📋 Respuesta verificación admin:", dataAdmin)

      if (dataAdmin.existe) {
        // Es administrador - redirigir al portal de admin
        console.log("🔐 UID de administrador detectado. Redirigiendo...")
        updateStatus("Administrador detectado. Redirigiendo al portal...", "success")

        if (respuestaElement) {
          respuestaElement.innerHTML = `
            <div class="mt-4 p-4 bg-red-50 border border-red-200 rounded">
              <strong>🔐 Administrador detectado</strong><br>
              <strong>Nombre:</strong> ${dataAdmin.admin.nombre}<br>
              <strong>UID:</strong> ${uid}<br>
              <p class="mt-2">Redirigiendo al portal de administrador...</p>
            </div>
          `
        }

        // Guardar UID y redirigir
        localStorage.setItem("uid", uid)
        setTimeout(() => {
          window.location.href = "admin_login.html"
        }, 2000)
        return
      }
    }

    // SEGUNDO: Verificar usuario normal (alumno/docente)
    console.log("🔍 Verificando usuario normal...")
    const response = await fetch(`${apiURL}/usuarios/verificar_uid/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ uid: uid }),
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    console.log("📋 Respuesta de verificación normal:", data)

    // Guardar UID en localStorage
    localStorage.setItem("uid", uid)

    if (data.nuevo || !data.existe) {
      // Usuario nuevo - ir a registro
      console.log("🔐 UID no registrado. Redirigiendo a registro...")
      updateStatus("UID no registrado. Redirigiendo a registro...", "info")

      if (respuestaElement) {
        respuestaElement.innerHTML = `
          <div class="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
            <strong>👤 Usuario nuevo detectado</strong><br>
            <strong>UID:</strong> ${uid}<br>
            <p class="mt-2">Redirigiendo al formulario de registro...</p>
          </div>
        `
      }

      setTimeout(() => {
        window.location.href = "registro.html"
      }, 2000)
    } else {
      // Usuario registrado - ir a login
      console.log("✅ UID encontrado. Redirigiendo a login...")
      updateStatus("UID encontrado. Redirigiendo a login...", "success")

      if (respuestaElement) {
        respuestaElement.innerHTML = `
          <div class="mt-4 p-4 bg-green-50 border border-green-200 rounded">
            <strong>✅ Usuario registrado encontrado</strong><br>
            <strong>Nombre:</strong> ${data.usuario?.nombre || "N/A"}<br>
            <strong>Rol:</strong> ${data.usuario?.rol || "N/A"}<br>
            <p class="mt-2">Redirigiendo al login...</p>
          </div>
        `
      }

      setTimeout(() => {
        window.location.href = "login.html"
      }, 2000)
    }
  } catch (error) {
    console.error("❌ Error verificando UID:", error)
    updateStatus("Error verificando UID", "error")

    if (respuestaElement) {
      respuestaElement.innerHTML = `
        <div class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          <strong>❌ Error:</strong> ${error.message}<br>
          <small>UID: ${uid}</small>
        </div>
      `
    }
  }
}

// Función para simular UID (solo para testing)
function simulateUID() {
  const testUID = "TEST" + Math.random().toString(36).substr(2, 8).toUpperCase()
  console.log("🧪 Simulando UID:", testUID)
  handleReceivedUID({ uid: testUID, timestamp: new Date().toISOString() })
}

// Inicializar cuando se carga la página
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Iniciando aplicación frontend...")
  updateStatus("Iniciando aplicación...", "info")

  // Conectar al backend
  connectToBackend()

  // Solo agregar botón de prueba en desarrollo
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    const testButton = document.createElement("button")
    testButton.textContent = "🧪 Simular Tarjeta"
    testButton.className = "mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors"
    testButton.onclick = simulateUID
    document.body.appendChild(testButton)
  }
})

// Limpiar al salir
window.addEventListener("beforeunload", () => {
  if (socket) {
    socket.disconnect()
  }
})
