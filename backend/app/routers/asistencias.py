from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta, time
from app import models
from app.database import get_db

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

TOLERANCIA_MINUTOS = 15
TOLERANCIA_RETARDO = 15  # 15 minutos adicionales para retardo

@router.post("/registrar/")
def registrar_asistencia(data: dict = Body(...), db: Session = Depends(get_db)):
    uid = data.get("uid")
    if not uid:
        raise HTTPException(status_code=400, detail="UID no proporcionado")

    # Verificar usuario
    usuario = db.query(models.Usuario).filter(
        models.Usuario.uid == uid,
        models.Usuario.activo == True
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o inactivo")

    ahora = datetime.now()
    hora_actual = ahora.time()
    dia_actual = ahora.strftime("%A")
    
    # Mapear días al español
    dias_map = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    dia_espanol = dias_map.get(dia_actual, dia_actual)

    if usuario.rol == "alumno":
        return registrar_asistencia_alumno(usuario, ahora, hora_actual, dia_espanol, db)
    elif usuario.rol == "docente":
        return verificar_docente_en_clase(usuario, ahora, hora_actual, dia_espanol, db)
    else:
        raise HTTPException(status_code=403, detail="Rol no autorizado para registrar asistencia")

def registrar_asistencia_alumno(usuario, ahora, hora_actual, dia_espanol, db):
    try:
        print(f"👨‍🎓 Registrando asistencia para alumno: {usuario.nombre}")
        print(f"📅 Día: {dia_espanol}, Hora: {hora_actual}, Grupo: {usuario.grupo}")
        
        # Buscar asignaciones del grupo del alumno
        query = text("""
            SELECT am.id, am.hora_inicio, am.hora_fin, m.nombre as materia_nombre,
                   u.nombre as docente_nombre, am.grupo, am.aula
            FROM asignaciones_materias am
            JOIN materias m ON am.materia_id = m.id
            JOIN docentes d ON am.docente_id = d.id
            JOIN usuarios u ON d.usuario_id = u.id
            WHERE am.grupo = :grupo 
            AND am.dia_semana = :dia
            AND am.activa = TRUE
        """)
        
        result = db.execute(query, {
            "grupo": usuario.grupo,
            "dia": dia_espanol
        })
        
        asignaciones = result.fetchall()
        print(f"📚 Asignaciones encontradas: {len(asignaciones)}")
        
        for asignacion in asignaciones:
            asignacion_id, hora_inicio, hora_fin, materia_nombre, docente_nombre, grupo, aula = asignacion
            
            print(f"🔍 Verificando materia: {materia_nombre}")
            print(f"⏰ Horario: {hora_inicio} - {hora_fin}")
            
            # Verificar si está en el horario de clase (con tolerancia de 15 minutos + 15 de retardo)
            tolerancia_inicio = timedelta(minutes=TOLERANCIA_MINUTOS)
            tolerancia_retardo = timedelta(minutes=TOLERANCIA_MINUTOS + TOLERANCIA_RETARDO)

            inicio_con_tolerancia = (datetime.combine(ahora.date(), hora_inicio) - tolerancia_inicio).time()
            fin_con_retardo = (datetime.combine(ahora.date(), hora_inicio) + tolerancia_retardo).time()
            fin_clase = (datetime.combine(ahora.date(), hora_fin) + tolerancia_inicio).time()

            print(f"🕐 Ventana de asistencia: {inicio_con_tolerancia} - {fin_con_retardo}")
            print(f"🕐 Fin de clase: {fin_clase}")

            # Verificar si está en ventana de asistencia o retardo
            en_ventana_asistencia = inicio_con_tolerancia <= hora_actual <= fin_con_retardo
            en_horario_clase = hora_actual <= fin_clase

            if en_ventana_asistencia or en_horario_clase:
                print(f"✅ Alumno está en ventana válida para {materia_nombre}")
                
                # Verificar si ya registró asistencia hoy
                asistencia_query = text("""
                    SELECT id, hora_registro, estado FROM asistencias 
                    WHERE alumno_id = :alumno_id 
                    AND asignacion_id = :asignacion_id 
                    AND fecha = :fecha
                """)
                
                asistencia_result = db.execute(asistencia_query, {
                    "alumno_id": usuario.id,
                    "asignacion_id": asignacion_id,
                    "fecha": ahora.date()
                })
                
                asistencia_existente = asistencia_result.fetchone()
                
                if asistencia_existente:
                    print(f"⚠️ Ya tiene asistencia registrada")
                    return {
                        "mensaje": f"Ya registró asistencia para {materia_nombre}",
                        "ya_registrado": True,
                        "puede_iniciar_sesion": True,  # Puede iniciar sesión si ya tomó asistencia
                        "asistencia": {
                            "materia": materia_nombre,
                            "hora_registro": asistencia_existente[1].strftime("%H:%M") if asistencia_existente[1] else "N/A",
                            "estado": asistencia_existente[2] if asistencia_existente[2] else "Presente",
                            "docente": docente_nombre,
                            "aula": aula or "N/A"
                        }
                    }

                # Determinar estado según la hora
                estado = "Presente"
                if hora_actual > hora_inicio:
                    minutos_tarde = (datetime.combine(ahora.date(), hora_actual) - 
                                   datetime.combine(ahora.date(), hora_inicio)).total_seconds() / 60
                    if minutos_tarde > TOLERANCIA_MINUTOS:  # Más de 15 minutos tarde
                        estado = "Retardo"
                        print(f"⏰ Retardo detectado: {minutos_tarde:.1f} minutos")
                    elif minutos_tarde > 10:  # Entre 10 y 15 minutos
                        estado = "Tardanza"
                        print(f"⏰ Tardanza detectada: {minutos_tarde:.1f} minutos")

                # Registrar asistencia con manejo de concurrencia
                try:
                    # Usar transacción para evitar conflictos
                    db.begin()
                    
                    # Verificar nuevamente que no existe (por concurrencia)
                    verificacion_query = text("""
                        SELECT id FROM asistencias 
                        WHERE alumno_id = :alumno_id 
                        AND asignacion_id = :asignacion_id 
                        AND fecha = :fecha
                        FOR UPDATE
                    """)
                    
                    verificacion_result = db.execute(verificacion_query, {
                        "alumno_id": usuario.id,
                        "asignacion_id": asignacion_id,
                        "fecha": ahora.date()
                    })
                    
                    if verificacion_result.fetchone():
                        db.rollback()
                        return {
                            "mensaje": f"Asistencia ya registrada para {materia_nombre}",
                            "ya_registrado": True,
                            "puede_iniciar_sesion": True
                        }
                    
                    insert_query = text("""
                        INSERT INTO asistencias (alumno_id, asignacion_id, fecha, hora_registro, estado)
                        VALUES (:alumno_id, :asignacion_id, :fecha, :hora_registro, :estado)
                    """)
                    
                    db.execute(insert_query, {
                        "alumno_id": usuario.id,
                        "asignacion_id": asignacion_id,
                        "fecha": ahora.date(),
                        "hora_registro": hora_actual,
                        "estado": estado
                    })
                    
                    db.commit()
                    print(f"✅ Asistencia registrada exitosamente con estado: {estado}")

                    return {
                        "mensaje": f"Asistencia registrada para {materia_nombre}",
                        "exito": True,
                        "puede_iniciar_sesion": True,
                        "asistencia": {
                            "materia": materia_nombre,
                            "docente": docente_nombre,
                            "hora_registro": hora_actual.strftime("%H:%M"),
                            "estado": estado,
                            "grupo": grupo,
                            "aula": aula or "N/A"
                        }
                    }
                    
                except Exception as e:
                    db.rollback()
                    print(f"❌ Error en transacción: {e}")
                    raise e
            else:
                print(f"❌ Fuera de ventana de asistencia para {materia_nombre}")

        # Si llegamos aquí, no hay clases en este horario
        print(f"❌ No hay clases disponibles para asistencia")
        
        # Buscar próxima clase
        proxima_clase_query = text("""
            SELECT m.nombre, am.hora_inicio, am.dia_semana
            FROM asignaciones_materias am
            JOIN materias mat ON am.materia_id = mat.id
            JOIN materias m ON am.materia_id = m.id
            WHERE am.grupo = :grupo 
            AND am.activa = TRUE
            AND (
                (am.dia_semana = :dia AND am.hora_inicio > :hora_actual)
                OR am.dia_semana != :dia
            )
            ORDER BY 
                CASE am.dia_semana
                    WHEN 'Lunes' THEN 1 WHEN 'Martes' THEN 2 WHEN 'Miércoles' THEN 3
                    WHEN 'Jueves' THEN 4 WHEN 'Viernes' THEN 5 WHEN 'Sábado' THEN 6
                    WHEN 'Domingo' THEN 7
                END,
                am.hora_inicio
            LIMIT 1
        """)
        
        proxima_result = db.execute(proxima_clase_query, {
            "grupo": usuario.grupo,
            "dia": dia_espanol,
            "hora_actual": hora_actual
        })
        
        proxima_clase = proxima_result.fetchone()
        
        if proxima_clase:
            materia_proxima, hora_proxima, dia_proximo = proxima_clase
            mensaje = f"No tiene clases ahora. Próxima clase: {materia_proxima} el {dia_proximo} a las {hora_proxima.strftime('%H:%M')}"
        else:
            mensaje = "No tiene clases en este horario. Verifique su horario de clases."
        
        # Si no está en horario válido, no puede iniciar sesión
        raise HTTPException(
            status_code=403, 
            detail={
                "mensaje": mensaje,
                "puede_iniciar_sesion": False,
                "fuera_de_horario": True
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error registrando asistencia: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

def verificar_docente_en_clase(usuario, ahora, hora_actual, dia_espanol, db):
    try:
        print(f"👨‍🏫 Verificando docente: {usuario.nombre}")
        
        # Buscar clases del docente
        query = text("""
            SELECT am.id, am.hora_inicio, am.hora_fin, m.nombre as materia_nombre,
                   am.grupo, c.nombre as carrera_nombre, am.aula
            FROM asignaciones_materias am
            JOIN materias m ON am.materia_id = m.id
            JOIN carreras c ON m.carrera_id = c.id
            JOIN docentes d ON am.docente_id = d.id
            WHERE d.usuario_id = :usuario_id 
            AND am.dia_semana = :dia
            AND am.activa = TRUE
        """)
        
        result = db.execute(query, {
            "usuario_id": usuario.id,
            "dia": dia_espanol
        })
        
        asignaciones = result.fetchall()
        print(f"📚 Clases del docente hoy: {len(asignaciones)}")
        
        for asignacion in asignaciones:
            asignacion_id, hora_inicio, hora_fin, materia_nombre, grupo, carrera_nombre, aula = asignacion
            
            if hora_inicio <= hora_actual <= hora_fin:
                print(f"✅ Docente está en clase: {materia_nombre}")
                return {
                    "mensaje": f"Está en clase: {materia_nombre} - Grupo {grupo}",
                    "en_clase": True,
                    "puede_modificar": True,
                    "clase_info": {
                        "materia": materia_nombre,
                        "grupo": grupo,
                        "carrera": carrera_nombre,
                        "hora_inicio": hora_inicio.strftime("%H:%M"),
                        "hora_fin": hora_fin.strftime("%H:%M"),
                        "aula": aula or "N/A"
                    }
                }

        # Buscar próxima clase
        proxima_clase = None
        for asignacion in asignaciones:
            asignacion_id, hora_inicio, hora_fin, materia_nombre, grupo, carrera_nombre, aula = asignacion
            if hora_inicio > hora_actual:
                if not proxima_clase or hora_inicio < proxima_clase[1]:
                    proxima_clase = (materia_nombre, hora_inicio, grupo)
        
        if proxima_clase:
            return {
                "mensaje": f"No está en clase. Próxima clase: {proxima_clase[0]} a las {proxima_clase[1].strftime('%H:%M')}",
                "en_clase": False,
                "proxima_clase": {
                    "materia": proxima_clase[0],
                    "hora": proxima_clase[1].strftime("%H:%M"),
                    "grupo": proxima_clase[2]
                }
            }
        
        return {
            "mensaje": "No tiene clases asignadas para hoy",
            "en_clase": False,
            "sin_clases": True
        }
        
    except Exception as e:
        print(f"❌ Error verificando docente: {e}")
        return {
            "mensaje": "Error verificando horario de clases",
            "en_clase": False,
            "error": True
        }

@router.get("/ver/{uid}")
def ver_asistencias(uid: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.uid == uid,
        models.Usuario.activo == True
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.rol == "alumno":
        return obtener_asistencias_alumno(usuario, db)
    elif usuario.rol == "docente":
        return obtener_asistencias_docente(usuario, db)
    else:
        raise HTTPException(status_code=403, detail="Acceso denegado")

def obtener_asistencias_alumno(usuario, db):
    try:
        print(f"📊 Obteniendo asistencias para alumno: {usuario.nombre}")
        
        query = text("""
            SELECT a.id, a.fecha, a.hora_registro, a.estado, 
                   m.nombre as materia, u.nombre as docente, am.grupo, a.observaciones,
                   am.aula, am.hora_inicio, am.hora_fin
            FROM asistencias a
            JOIN asignaciones_materias am ON a.asignacion_id = am.id
            JOIN materias m ON am.materia_id = m.id
            JOIN docentes d ON am.docente_id = d.id
            JOIN usuarios u ON d.usuario_id = u.id
            WHERE a.alumno_id = :alumno_id
            ORDER BY a.fecha DESC, a.hora_registro DESC
        """)
        
        result = db.execute(query, {"alumno_id": usuario.id})
        asistencias = result.fetchall()
        
        resultado = []
        for asistencia in asistencias:
            resultado.append({
                "id": asistencia[0],
                "fecha": asistencia[1].isoformat() if asistencia[1] else None,
                "hora": asistencia[2].strftime("%H:%M") if asistencia[2] else "N/A",
                "estado": asistencia[3] or "Presente",
                "materia": asistencia[4] or "N/A",
                "docente": asistencia[5] or "N/A",
                "grupo": asistencia[6] or "N/A",
                "observaciones": asistencia[7] or "",
                "aula": asistencia[8] or "N/A",
                "hora_clase_inicio": asistencia[9].strftime("%H:%M") if asistencia[9] else "N/A",
                "hora_clase_fin": asistencia[10].strftime("%H:%M") if asistencia[10] else "N/A"
            })

        print(f"📋 Asistencias encontradas: {len(resultado)}")
        return resultado
        
    except Exception as e:
        print(f"❌ Error obteniendo asistencias alumno: {e}")
        return []

def obtener_asistencias_docente(usuario, db):
    try:
        print(f"📊 Obteniendo asistencias para docente: {usuario.nombre}")
        
        query = text("""
            SELECT a.id, a.fecha, a.hora_registro, a.estado,
                   u.nombre as alumno_nombre, u.matricula, m.nombre as materia, am.grupo, a.observaciones,
                   am.aula
            FROM asistencias a
            JOIN asignaciones_materias am ON a.asignacion_id = am.id
            JOIN materias m ON am.materia_id = m.id
            JOIN docentes d ON am.docente_id = d.id
            JOIN usuarios u ON a.alumno_id = u.id
            WHERE d.usuario_id = :usuario_id
            ORDER BY a.fecha DESC, a.hora_registro DESC
        """)
        
        result = db.execute(query, {"usuario_id": usuario.id})
        asistencias = result.fetchall()
        
        resultado = []
        for asistencia in asistencias:
            resultado.append({
                "id": asistencia[0],
                "fecha": asistencia[1].isoformat() if asistencia[1] else None,
                "hora": asistencia[2].strftime("%H:%M") if asistencia[2] else "N/A",
                "estado": asistencia[3] or "Presente",
                "alumno_nombre": asistencia[4] or "N/A",
                "matricula": asistencia[5] or "N/A",
                "materia": asistencia[6] or "N/A",
                "grupo": asistencia[7] or "N/A",
                "observaciones": asistencia[8] or "",
                "aula": asistencia[9] or "N/A"
            })

        print(f"📋 Asistencias encontradas: {len(resultado)}")
        return resultado
        
    except Exception as e:
        print(f"❌ Error obteniendo asistencias docente: {e}")
        return []

@router.put("/modificar/")
def modificar_asistencia(
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    asistencia_id = data.get("asistencia_id")
    nuevo_estado = data.get("nuevo_estado")
    uid = data.get("uid")
    
    if not all([asistencia_id, nuevo_estado, uid]):
        raise HTTPException(status_code=400, detail="Faltan parámetros requeridos")

    # Verificar que es docente
    usuario = db.query(models.Usuario).filter(
        models.Usuario.uid == uid,
        models.Usuario.rol == "docente",
        models.Usuario.activo == True
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=403, detail="Solo docentes pueden modificar asistencias")

    try:
        # Verificar que la asistencia existe y el docente puede modificarla
        query = text("""
            SELECT a.id FROM asistencias a
            JOIN asignaciones_materias am ON a.asignacion_id = am.id
            JOIN docentes d ON am.docente_id = d.id
            WHERE a.id = :asistencia_id AND d.usuario_id = :usuario_id
        """)
        
        result = db.execute(query, {
            "asistencia_id": asistencia_id,
            "usuario_id": usuario.id
        })
        
        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Asistencia no encontrada o sin permisos")

        # Modificar asistencia
        update_query = text("""
            UPDATE asistencias 
            SET estado = :nuevo_estado 
            WHERE id = :asistencia_id
        """)
        
        db.execute(update_query, {
            "nuevo_estado": nuevo_estado,
            "asistencia_id": asistencia_id
        })
        
        db.commit()

        return {"mensaje": "Asistencia modificada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error modificando asistencia: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/horario/{uid}")
def obtener_horario_alumno(uid: str, db: Session = Depends(get_db)):
    """Obtener horario de clases del alumno"""
    usuario = db.query(models.Usuario).filter(
        models.Usuario.uid == uid,
        models.Usuario.rol == "alumno",
        models.Usuario.activo == True
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    try:
        query = text("""
            SELECT am.dia_semana, am.hora_inicio, am.hora_fin, m.nombre as materia,
                   u.nombre as docente, am.aula, am.grupo
            FROM asignaciones_materias am
            JOIN materias m ON am.materia_id = m.id
            JOIN docentes d ON am.docente_id = d.id
            JOIN usuarios u ON d.usuario_id = u.id
            WHERE am.grupo = :grupo AND am.activa = TRUE
            ORDER BY 
                CASE am.dia_semana
                    WHEN 'Lunes' THEN 1 WHEN 'Martes' THEN 2 WHEN 'Miércoles' THEN 3
                    WHEN 'Jueves' THEN 4 WHEN 'Viernes' THEN 5 WHEN 'Sábado' THEN 6
                    WHEN 'Domingo' THEN 7
                END,
                am.hora_inicio
        """)
        
        result = db.execute(query, {"grupo": usuario.grupo})
        horarios = result.fetchall()
        
        resultado = []
        for horario in horarios:
            resultado.append({
                "dia": horario[0],
                "hora_inicio": horario[1].strftime("%H:%M"),
                "hora_fin": horario[2].strftime("%H:%M"),
                "materia": horario[3],
                "docente": horario[4],
                "aula": horario[5] or "N/A",
                "grupo": horario[6]
            })
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error obteniendo horario: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo horario: {str(e)}")
