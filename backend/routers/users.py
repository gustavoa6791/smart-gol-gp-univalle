from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
import schemas
from database import get_db
from auth import require_permissions

router = APIRouter(prefix="/api/users", tags=["users"])

class UserRoleUpdate(BaseModel):
    role_id: int

@router.get("", response_model=List[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    _ = Depends(require_permissions("manage_users"))
):
    return db.query(models.User).all()

@router.put("/{user_id}/role", response_model=schemas.UserOut)
def update_user_role(
    user_id: int,
    role_in: UserRoleUpdate,
    db: Session = Depends(get_db),
    _ = Depends(require_permissions("manage_users"))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    role = db.query(models.Role).filter(models.Role.id == role_in.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Rol invalido")
        
    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user
