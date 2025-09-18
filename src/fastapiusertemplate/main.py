from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status, Response, Request
from . import auth
from . import models
from . import crud 
from . import schema
from .database import SessionLocal, engine, get_db
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users/{user_id}", response_model=schema.User)
async def read_user(user_id: UUID, db: Session = Depends(get_db), current_user: schema.User = Depends(auth.get_current_user)):
    user = crud.get_user(db, user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/users", response_model=list[schema.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/me", response_model=schema.User)
async def read_users_me(current_user: schema.User = Depends(auth.get_current_user)):
    """Obtener perfil del usuario autenticado"""
    return current_user

@app.post("/register", response_model=schema.User)
async def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Verificar si el username ya existe
    existing_username = crud.get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )
    
    db_user = crud.create_user(db, user)
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    result = crud.delete_user(db, user_id)
    return result

@app.post("/login", response_model=schema.LoginResponse)
async def login(form_data: schema.Login, response: Response, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)})
    
    # Establecer cookies HTTP-only para mayor seguridad
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # No accesible desde JavaScript
        secure=False,   # True en producción con HTTPS
        samesite="lax", # Protección CSRF
        max_age=15 * 60  # 15 minutos
    )
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token,
        httponly=True,
        secure=False,   # True en producción con HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 días
    )
    
    # Solo devolver información del usuario, NO los tokens
    return {"message": "Login successful", "user": user}

@app.post("/refresh")
async def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    # Leer refresh token desde cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found in cookies"
        )
    
    user_id = auth.verify_token(refresh_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Crear nuevos tokens
    new_access_token = auth.create_access_token(data={"sub": str(user.id)})
    new_refresh_token = auth.create_refresh_token(data={"sub": str(user.id)})
    
    # Actualizar cookies
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,   # True en producción
        samesite="lax",
        max_age=15 * 60  # 15 minutos
    )
    response.set_cookie(
        key="refresh_token", 
        value=new_refresh_token,
        httponly=True,
        secure=False,   # True en producción
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 días
    )
    
    return {"message": "Tokens refreshed successfully"}

@app.post("/logout")
async def logout(response: Response):
    """Logout del usuario - limpia las cookies"""
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}