from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, database

router = APIRouter()
get_db = database.SessionLocal

@router.post("/crear_materia/")
def crear_materia(nombre: str, carrera: str, semestre: int, db: Session = Depends(get_db)):
    ya_existe = db.query(models.Materia).filter_by(nombre=nombre, carrera=carrera, semestre=semestre).first()
    if ya_existe:
        raise HTTPException(status_code=409, detail="Materia ya existe para esa carrera y semestre")

    materia = models.Materia(nombre=nombre, carrera=carrera, semestre=semestre)
    db.add(materia)
    db.commit()
    return {"mensaje": "Materia creada"}

@router.post("/asignar/")
def asignar_materia(docente_id: int, materia_id: int, grupo: str, dia: str, hora_inicio: str, hora_fin: str, db: Session = Depends(get_db)):
    # Evitar traslapes
    conflictos = db.query(models.MateriaAsignada).filter_by(
        docente_id=docente_id,
        dia=dia,
        grupo=grupo
    ).all()

    def hora_en_rango(h1_inicio, h1_fin, h2_inicio, h2_fin):
        return h1_inicio < h2_fin and h2_inicio < h1_fin

    for c in conflictos:
        if hora_en_rango(h1_inicio=hora_inicio, h1_fin=hora_fin, h2_inicio=c.hora_inicio, h2_fin=c.hora_fin):
            raise HTTPException(status_code=400, detail="Conflicto de horario con otra materia")

    materia = db.query(models.Materia).filter_by(id=materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    asignacion = models.MateriaAsignada(
        docente_id=docente_id,
        materia_id=materia_id,
        carrera=materia.carrera,
        semestre=materia.semestre,
        grupo=grupo,
        dia=dia,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin
    )
    db.add(asignacion)
    db.commit()
    return {"mensaje": "Materia asignada al docente"}

@router.get("/por_grupo/")
def materias_por_grupo(carrera: str, semestre: int, grupo: str, db: Session = Depends(get_db)):
    materias = db.query(models.MateriaAsignada).filter_by(carrera=carrera, semestre=semestre, grupo=grupo).all()
    return materias

@router.get("/por_docente/")
def materias_por_docente(docente_id: int, db: Session = Depends(get_db)):
    materias = db.query(models.MateriaAsignada).filter_by(docente_id=docente_id).all()
    return materias
