from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class User(BaseModel):
    id: UUID
    email: str
    username: str

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    email: str
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    message: str
    user: User

class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = None  # Opcional porque lo leeremos de cookie