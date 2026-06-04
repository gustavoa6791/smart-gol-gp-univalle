import enum as py_enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Role(Base):
    """Modelo de Rol gestionable por UI (HU-002)"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    # Permisos estaticos asociados a este rol, ej: ["create_users", "edit_roles"]
    permissions = Column(JSON, default=list, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    """Usuario del sistema. Modelo base de HU-000"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    role = relationship("Role", back_populates="users")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TournamentTemplate(Base):
    __tablename__ = "tournament_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    config = Column(JSON, nullable=False)