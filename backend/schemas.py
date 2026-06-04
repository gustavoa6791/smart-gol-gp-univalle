from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleBase(BaseModel):
    name: str
    permissions: List[str] = []


class RoleCreate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserRegister(BaseModel):
    """Registro publico. El rol siempre se fuerza a viewer en el backend."""
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
<<<<<<< HEAD
    role: Optional[RoleOut] = None
=======
    role: UserRole
>>>>>>> origin/main
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
