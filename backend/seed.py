"""Datos iniciales. Crea un usuario por rol para poder probar HU-001 en adelante.

Uso (con Docker corriendo):
    docker exec smart_gol_backend python seed.py
"""
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

import models
from auth import hash_password
from database import SessionLocal


def seed_data():
    db = SessionLocal()
    try:
        users_to_seed = [
            ("Admin Smart Gol", "admin@smartgol.com", "admin123", models.UserRole.admin),
            ("Organizador Demo", "organizer@smartgol.com", "organizer123", models.UserRole.organizer),
            ("Viewer Demo", "viewer@smartgol.com", "viewer123", models.UserRole.viewer),
        ]

        for name, email, password, role in users_to_seed:
            user = db.query(models.User).filter(models.User.email == email).first()
            if user is None:
                db.add(models.User(
                    name=name,
                    email=email,
                    hashed_password=hash_password(password),
                    role=role,
                ))
                print(f"Usuario creado: {email} / {password} ({role.value})")
            else:
                print(f"Usuario ya existe: {email} ({role.value})")

        db.commit()
        print("Seed completado.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
