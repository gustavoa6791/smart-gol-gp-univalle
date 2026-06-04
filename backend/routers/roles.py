from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import require_permissions

router = APIRouter(prefix="/api/roles", tags=["roles"])

@router.get("", response_model=List[schemas.RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    _ = Depends(require_permissions("manage_roles"))
):
    return db.query(models.Role).all()

@router.post("", response_model=schemas.RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: schemas.RoleCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_permissions("manage_roles"))
):
    role = db.query(models.Role).filter(models.Role.name == role_in.name).first()
    if role:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    
    new_role = models.Role(name=role_in.name, permissions=role_in.permissions)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.put("/{role_id}", response_model=schemas.RoleOut)
def update_role(
    role_id: int,
    role_in: schemas.RoleCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_permissions("manage_roles"))
):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
        
    role.name = role_in.name
    role.permissions = role_in.permissions
    db.commit()
    db.refresh(role)
    return role
