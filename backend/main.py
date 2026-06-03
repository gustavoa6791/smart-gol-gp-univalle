import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import engine
from routers import health

app = FastAPI(
    title="Smart Gol API",
    description="Sistema de gestion de torneos deportivos",
    version="0.1.0",
)

# CORS abierto: el frontend (Next.js) corre fuera del contenedor en dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers. Cada HU agrega los suyos aqui.
app.include_router(health.router)


@app.on_event("startup")
def startup():
    """Espera a que MySQL este disponible antes de aceptar trafico."""
    max_retries = 30
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Base de datos conectada")
            return
        except Exception as exc:
            print(f"DB no lista (intento {attempt}/{max_retries}): {exc}")
            if attempt == max_retries:
                raise
            time.sleep(3)


@app.get("/")
def root():
    return {"message": "Smart Gol API is running", "docs": "/docs"}
