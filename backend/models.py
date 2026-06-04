import enum as py_enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from database import Base
from sqlalchemy import JSON


class UserRole(str, py_enum.Enum):
    """Roles del sistema. La autenticacion por rol se implementa en HU-001."""
    admin = "admin"
    organizer = "organizer"
    viewer = "viewer"


class User(Base):
    """Usuario del sistema. Modelo base de HU-000; el resto de modelos de
    dominio (Player, Team, Tournament, ...) los agregan las HU siguientes."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.viewer,
        server_default=UserRole.viewer.value,
    )



class TournamentTemplate(Base):
    __tablename__ = "tournament_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    config = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
