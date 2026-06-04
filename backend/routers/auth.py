"""Endpoints de autenticacion (HU-001: iniciar sesion segun rol).

Cubre registro publico, login (JWT + bcrypt) y usuario actual.
La administracion de roles/usuarios por admin es HU-002 y vive aparte.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth as auth_utils
import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(data: schemas.UserRegister, db: Session = Depends(get_db)):
    """Registro publico: el usuario se crea siempre con rol viewer."""
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya esta registrado",
        )
<<<<<<< HEAD
    
    # Buscar el rol viewer por defecto
    viewer_role = db.query(models.Role).filter(models.Role.name == "viewer").first()
    if not viewer_role:
        # Fallback de seguridad si no se ha ejecutado el seed
        viewer_role = models.Role(name="viewer", permissions=["view_tournaments"])
        db.add(viewer_role)
        db.commit()
        db.refresh(viewer_role)

=======
>>>>>>> origin/main
    user = models.User(
        name=data.name,
        email=data.email,
        hashed_password=auth_utils.hash_password(data.password),
<<<<<<< HEAD
        role_id=viewer_role.id,
=======
        role=models.UserRole.viewer,
>>>>>>> origin/main
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Valida credenciales y devuelve un JWT con el id del usuario."""
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth_utils.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contrasena incorrectos",
        )
    token = auth_utils.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    """Devuelve el usuario autenticado (incluye su rol)."""
    return current_user
