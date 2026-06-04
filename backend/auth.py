"""Utilidades de autenticacion y autorizacion (base de HU-000).

Aqui viven los helpers reutilizables: hashing de contrasenas, emision y
verificacion de JWT, obtencion del usuario actual y control por rol.
Los endpoints de login/registro se construyen sobre esto en HU-001.
"""
from datetime import datetime, timedelta
from typing import Optional
import os

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import models
from database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """Valida el JWT del header Authorization y devuelve el usuario."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


def require_permissions(*allowed_permissions: str):
    """Factory de dependency: restringe una ruta a los permisos indicados (HU-002)."""
    def _checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        user_permissions = current_user.role.permissions if current_user.role else []
        if not any(p in user_permissions for p in allowed_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta accion",
            )
        return current_user
    return _checker
