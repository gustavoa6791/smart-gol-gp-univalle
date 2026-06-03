"""Router de salud. Sirve como ejemplo del patron de routers del proyecto:
cada HU agrega su propio archivo en routers/ y lo registra en main.py.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    """Verifica que la API y la base de datos respondan."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "down"
    return {"status": "ok", "database": db_status}
