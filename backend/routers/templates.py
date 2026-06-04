from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models

router = APIRouter(prefix="/templates", tags=["Templates"])


# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/")
def create_template(data: dict, db: Session = Depends(get_db)):
    template = models.TournamentTemplate(**data)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


# GET ALL
@router.get("/")
def get_templates(db: Session = Depends(get_db)):
    return db.query(models.TournamentTemplate).all()


# GET ONE
@router.get("/{template_id}")
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(models.TournamentTemplate).filter(
        models.TournamentTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return template


# UPDATE
@router.put("/{template_id}")
def update_template(template_id: int, data: dict, db: Session = Depends(get_db)):
    template = db.query(models.TournamentTemplate).filter(
        models.TournamentTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    for key, value in data.items():
        setattr(template, key, value)

    db.commit()
    db.refresh(template)
    return template


# DELETE
@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(models.TournamentTemplate).filter(
        models.TournamentTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(template)
    db.commit()

    return {"message": "Deleted successfully"}