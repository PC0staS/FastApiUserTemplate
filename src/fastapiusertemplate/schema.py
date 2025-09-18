"""
Esquemas de Pydantic para FastAPI User Template.

Este módulo contiene las definiciones de los esquemas de validación y serialización
utilizados por la API para validar datos de entrada y formatear respuestas.

Classes:
    User: Esquema de respuesta para datos de usuario
    CreateUser: Esquema para creación de nuevos usuarios
    Login: Esquema para datos de autenticación
    Token: Esquema para tokens JWT
    LoginResponse: Esquema de respuesta para login exitoso
    RefreshRequest: Esquema para solicitud de refresh de tokens
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    """
    Esquema de respuesta para datos de usuario.

    Utilizado para devolver información del usuario en respuestas de la API,
    excluyendo datos sensibles como la contraseña.

    Attributes:
        id (UUID): Identificador único del usuario
        email (str): Email del usuario
        username (str): Nombre de usuario
    """

    id: UUID
    email: str
    username: str

    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    """
    Esquema para la creación de nuevos usuarios.

    Contiene los datos necesarios para registrar un nuevo usuario
    en el sistema.

    Attributes:
        email (str): Email único del nuevo usuario
        username (str): Nombre de usuario único
        password (str): Contraseña en texto plano (será hasheada)
    """

    email: str
    username: str
    password: str


class Login(BaseModel):
    """
    Esquema para datos de autenticación.

    Utilizado en el endpoint de login para validar las credenciales
    del usuario.

    Attributes:
        username (str): Nombre de usuario o email
        password (str): Contraseña en texto plano
    """

    username: str
    password: str


class Token(BaseModel):
    """
    Esquema para tokens JWT.

    Estructura de respuesta que contiene los tokens de acceso y refresh.
    Nota: En la implementación actual usamos cookies HTTP-only.

    Attributes:
        access_token (str): Token de acceso JWT
        refresh_token (str): Token de refresh JWT
        token_type (str): Tipo de token (por defecto "bearer")
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """
    Esquema de respuesta para login exitoso.

    Contiene el mensaje de confirmación y los datos del usuario.
    Los tokens se envían como cookies HTTP-only.

    Attributes:
        message (str): Mensaje de confirmación
        user (User): Datos del usuario autenticado
    """

    message: str
    user: User


class RefreshRequest(BaseModel):
    """
    Esquema para solicitud de refresh de tokens.

    Aunque incluye el campo refresh_token, en la implementación actual
    el token se lee desde las cookies HTTP-only.

    Attributes:
        refresh_token (Optional[str]): Token de refresh (opcional)
    """

    refresh_token: Optional[str] = None  # Opcional porque lo leeremos de cookie
