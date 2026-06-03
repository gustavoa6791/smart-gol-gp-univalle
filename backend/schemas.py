from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from models import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.viewer


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Respuesta de login. El endpoint que lo emite se implementa en HU-001."""
    access_token: str
    token_type: str = "bearer"
