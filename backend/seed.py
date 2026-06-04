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
        roles_to_seed = [
            ("admin", ["manage_roles", "manage_users", "view_admin_panel"]),
            ("organizer", ["manage_tournaments", "view_admin_panel"]),
            ("viewer", ["view_tournaments"]),
        ]
        
        roles_dict = {}
        for role_name, permissions in roles_to_seed:
            role = db.query(models.Role).filter(models.Role.name == role_name).first()
            if not role:
                role = models.Role(name=role_name, permissions=permissions)
                db.add(role)
                db.commit()
                db.refresh(role)
            else:
                role.permissions = permissions
                db.commit()
            roles_dict[role_name] = role

        users_to_seed = [
            ("Admin Smart Gol", "admin@smartgol.com", "admin123", "admin"),
            ("Organizador Demo", "organizer@smartgol.com", "organizer123", "organizer"),
            ("Viewer Demo", "viewer@smartgol.com", "viewer123", "viewer"),
        ]

        for name, email, password, role_name in users_to_seed:
            user = db.query(models.User).filter(models.User.email == email).first()
            if user is None:
                db.add(models.User(
                    name=name,
                    email=email,
                    hashed_password=hash_password(password),
                    role_id=roles_dict[role_name].id,
                ))
                print(f"Usuario creado: {email} / {password} ({role_name})")
            else:
                user.role_id = roles_dict[role_name].id
                print(f"Usuario ya existe: {email} ({role_name})")

        db.commit()
        print("Seed completado.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
