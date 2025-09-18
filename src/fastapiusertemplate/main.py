from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status, Response, Request
from . import auth
from . import models
from . import crud 
from . import schema
from .database import SessionLocal, engine, get_db
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

# Metadata para la documentación de la API
app = FastAPI(
    title="FastAPI User Template",
    description="""
    ## 🚀 FastAPI User Authentication Template

    Una API completa y segura para autenticación de usuarios con **FastAPI** y **PostgreSQL**.

    ### 🔐 Características principales:
    
    * **Autenticación JWT**: Sistema seguro con tokens JWT
    * **Cookies HTTP-only**: Tokens almacenados de forma segura
    * **PostgreSQL**: Base de datos robusta con UUID
    * **Bcrypt**: Hash seguro de contraseñas
    * **Refresh Tokens**: Renovación automática de sesiones
    * **Documentación automática**: Swagger/OpenAPI integrado

    ### 🔄 Flujo de autenticación:

    1. **Registro**: Crea una cuenta con email y contraseña
    2. **Login**: Autentica y recibe cookies seguras
    3. **Acceso**: Usa rutas protegidas automáticamente
    4. **Refresh**: Renueva tokens cuando sea necesario
    5. **Logout**: Limpia las cookies de sesión

    ### 🛡️ Seguridad:

    - Cookies HTTP-only (no accesibles desde JavaScript)
    - Tokens JWT con expiración automática
    - Passwords hasheados con bcrypt + salt
    - Validación estricta con Pydantic
    - CORS configurado apropiadamente

    ### 👨‍💻 Desarrollado por:

    **Pablo Costas**  
    🌐 [GitHub](https://github.com/PC0staS)  
    📧 Contacto: [Crear issue en GitHub](https://github.com/PC0staS/FastApiUserTemplate)

    ---
    
    *¿Encontraste un bug? ¿Tienes una sugerencia? ¡Contribuye al proyecto!*
    """,
    version="1.0.0",
    terms_of_service="https://github.com/PC0staS/FastApiUserTemplate/blob/master/LICENSE",
    contact={
        "name": "Pablo Costas",
        "url": "https://github.com/PC0staS",
        "email": "https://github.com/PC0staS/FastApiUserTemplate/issues",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/PC0staS/FastApiUserTemplate/blob/master/LICENSE",
    },
    openapi_tags=[
        {
            "name": "authentication",
            "description": "Operaciones de autenticación: registro, login, logout y refresh de tokens",
        },
        {
            "name": "users",
            "description": "Gestión de usuarios y perfil de usuario",
        },
        {
            "name": "health",
            "description": "Endpoints de estado y verificación del servicio",
        }
    ]
)

@app.get("/users/{user_id}", response_model=schema.User, tags=["users"])
async def read_user(user_id: UUID, db: Session = Depends(get_db), current_user: schema.User = Depends(auth.get_current_user)):
    """Obtener información de un usuario específico por ID"""
    user = crud.get_user(db, user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/users", response_model=list[schema.User], tags=["users"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los usuarios (paginado)"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/me", response_model=schema.User, tags=["users"])
async def read_users_me(current_user: schema.User = Depends(auth.get_current_user)):
    """Obtener perfil del usuario autenticado"""
    return current_user

@app.post("/register", response_model=schema.User, tags=["authentication"])
async def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario
    
    - **email**: Email único del usuario
    - **username**: Nombre de usuario único
    - **password**: Contraseña (será hasheada automáticamente)
    """
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

@app.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un usuario por ID"""
    result = crud.delete_user(db, user_id)
    return result

@app.post("/login", response_model=schema.LoginResponse, tags=["authentication"])
async def login(form_data: schema.Login, response: Response, db: Session = Depends(get_db)):
    """
    Iniciar sesión con credenciales
    
    - **username**: Nombre de usuario o email
    - **password**: Contraseña del usuario
    
    Retorna cookies HTTP-only con tokens de acceso y refresh.
    """
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

@app.post("/refresh", tags=["authentication"])
async def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Renovar token de acceso usando refresh token
    
    Utiliza el refresh token almacenado en cookies para generar un nuevo access token.
    """
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

@app.post("/logout", tags=["authentication"])
async def logout(response: Response):
    """
    Cerrar sesión del usuario
    
    Elimina las cookies de autenticación (access_token y refresh_token).
    """
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}


# Endpoints de salud y testing
@app.get("/", tags=["health"])
async def root():
    """
    Health check del servicio
    
    Endpoint básico para verificar que la API esté funcionando correctamente.
    """
    return {
        "message": "🚀 FastAPI User Template API",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "github": "https://github.com/PC0staS/FastApiUserTemplate"
    }


@app.get("/protected", tags=["health"])
async def protected_route(current_user: schema.User = Depends(auth.get_current_user)):
    """
    Endpoint protegido de ejemplo
    
    Demuestra cómo funcionan las rutas que requieren autenticación.
    Solo usuarios autenticados pueden acceder a este endpoint.
    """
    return {
        "message": "🔐 Esta es una ruta protegida!",
        "user_id": current_user.id,
        "username": current_user.username,
        "access_granted": True
    }