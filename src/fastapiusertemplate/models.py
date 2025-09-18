"""
Modelos de base de datos para FastAPI User Template.

Este módulo contiene las definiciones de las tablas y modelos de SQLAlchemy
utilizados por la aplicación para gestionar usuarios y autenticación.

Classes:
    User: Modelo principal de usuario con autenticación
"""

import uuid

from sqlalchemy import UUID, Column, String

from .database import Base


class User(Base):
    """
    Modelo de usuario para el sistema de autenticación.

    Esta clase define la estructura de la tabla 'users' en la base de datos
    y contiene toda la información necesaria para la autenticación y gestión
    de usuarios.

    Attributes:
        id (UUID): Identificador único del usuario (UUID v4)
        email (str): Email único del usuario, usado para login
        username (str): Nombre de usuario único, también usado para login
        hashed_password (str): Contraseña hasheada con bcrypt

    Note:
        - El email y username deben ser únicos en la base de datos
        - La contraseña se almacena hasheada por seguridad
        - Se usa UUID como primary key para mejor escalabilidad
    """

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
