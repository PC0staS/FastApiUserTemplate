# FastAPI User Template 🚀

Un template completo y seguro para autenticación de usuarios con FastAPI, PostgreSQL y autenticación basada en cookies.

## ✨ Características

- **🔐 Autenticación Segura**: Sistema completo con JWT tokens y cookies HTTP-only
- **🗄️ PostgreSQL**: Base de datos robusta con UUID como primary keys
- **🍪 Cookie-Based Auth**: Tokens seguros sin exposición en el frontend
- **🧪 Testing Completo**: Suite de tests con pytest y coverage
- **🐳 Docker Ready**: Containerización completa con Docker Compose
- **📚 Documentación**: API docs automática con Swagger/OpenAPI
- **🔄 Refresh Tokens**: Sistema de renovación automática de tokens
- **⚡ FastAPI**: Framework moderno y de alto rendimiento

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI 0.116.2+
- **Base de Datos**: PostgreSQL 13
- **ORM**: SQLAlchemy 2.0+
- **Autenticación**: JWT + bcrypt
- **Validación**: Pydantic v2
- **Testing**: pytest + FastAPI TestClient
- **Containerización**: Docker + Docker Compose
- **Gestión de Dependencias**: Poetry

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Python 3.11+ (opcional, para desarrollo local)
- Poetry (opcional, para desarrollo local)

### Opción 1: Con Docker (Recomendado)

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/FastApiUserTemplate.git
   cd FastApiUserTemplate
   ```

2. **Levanta los servicios:**

   ```bash
   docker-compose up -d
   ```

3. **¡Listo!** La API estará disponible en:
   - **API**: http://localhost:8000
   - **Documentación**: http://localhost:8000/docs
   - **pgAdmin** (opcional): http://localhost:5050

### Opción 2: Desarrollo Local

1. **Clona e instala dependencias:**

   ```bash
   git clone https://github.com/tu-usuario/FastApiUserTemplate.git
   cd FastApiUserTemplate
   poetry install
   poetry shell
   ```

2. **Levanta solo la base de datos:**

   ```bash
   docker-compose up -d db
   ```

3. **Ejecuta la aplicación:**
   ```bash
   uvicorn src.fastapiusertemplate.main:app --reload
   ```

## 📡 API Endpoints

### Autenticación

| Método | Endpoint    | Descripción             |
| ------ | ----------- | ----------------------- |
| `POST` | `/register` | Registrar nuevo usuario |
| `POST` | `/login`    | Iniciar sesión          |
| `POST` | `/logout`   | Cerrar sesión           |
| `POST` | `/refresh`  | Renovar token           |

### Usuario

| Método | Endpoint     | Descripción                       |
| ------ | ------------ | --------------------------------- |
| `GET`  | `/me`        | Obtener perfil del usuario actual |
| `GET`  | `/protected` | Endpoint protegido de ejemplo     |

### Utilidades

| Método | Endpoint | Descripción           |
| ------ | -------- | --------------------- |
| `GET`  | `/`      | Health check          |
| `GET`  | `/docs`  | Documentación Swagger |

## 🔒 Sistema de Autenticación

### Características de Seguridad

- **Cookies HTTP-only**: Los tokens JWT se almacenan en cookies seguras
- **Bcrypt Hashing**: Passwords hasheados con salt automático
- **Refresh Tokens**: Renovación segura de tokens expirados
- **CORS Configurado**: Policies de CORS apropiadas
- **Validación Estricta**: Validación de entrada con Pydantic

### Flujo de Autenticación

1. **Registro**: `POST /register`

   ```json
   {
     "email": "usuario@ejemplo.com",
     "password": "mi_password_seguro"
   }
   ```

2. **Login**: `POST /login`

   ```json
   {
     "email": "usuario@ejemplo.com",
     "password": "mi_password_seguro"
   }
   ```

   Respuesta: Cookie `access_token` configurada automáticamente

3. **Acceso a Rutas Protegidas**: Las cookies se envían automáticamente

4. **Refresh**: `POST /refresh` - Renueva el token automáticamente

5. **Logout**: `POST /logout` - Limpia las cookies

## 🧪 Testing

### Ejecutar Tests

```bash
# Con Docker
docker-compose exec web poetry run pytest

# Local
poetry run pytest

# Con coverage
poetry run pytest --cov=src/
```

### Tests Incluidos

- ✅ Flujo completo de autenticación
- ✅ Registro de usuarios
- ✅ Login y logout
- ✅ Refresh de tokens
- ✅ Rutas protegidas
- ✅ Validación de errores

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` o configura las siguientes variables:

```bash
# Base de Datos
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_template_user

# JWT
SECRET_KEY=tu-clave-super-secreta-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Entorno
ENVIRONMENT=development
DEBUG=true
```

### Configuración de Producción

Para producción, asegúrate de:

1. **Cambiar SECRET_KEY**: Usa una clave segura y única
2. **Configurar HTTPS**: Para cookies seguras
3. **Configurar CORS**: Solo dominios permitidos
4. **Base de Datos Segura**: Credentials seguras y conexión SSL
5. **Logs**: Configurar logging apropiado

## 🐳 Docker

### Servicios Disponibles

- **web**: Aplicación FastAPI
- **db**: PostgreSQL 13
- **pgadmin**: Administrador de BD (perfil admin)

### Comandos Útiles

```bash
# Levantar todos los servicios
docker-compose up -d

# Levantar con pgAdmin
docker-compose --profile admin up -d

# Ver logs
docker-compose logs -f web

# Acceder al contenedor
docker-compose exec web bash

# Rebuild
docker-compose build --no-cache
```

## 📁 Estructura del Proyecto

```
FastApiUserTemplate/
├── src/
│   └── fastapiusertemplate/
│       ├── __init__.py
│       ├── main.py          # Aplicación principal
│       ├── models.py        # Modelos SQLAlchemy
│       ├── schema.py        # Esquemas Pydantic
│       ├── crud.py          # Operaciones CRUD
│       ├── auth.py          # Sistema de autenticación
│       └── database.py      # Configuración de BD
├── tests/
│   ├── __init__.py
│   └── test_auth_flow.py    # Tests de autenticación
├── docker-compose.yml       # Orquestación de servicios
├── Dockerfile              # Imagen de la aplicación
├── pyproject.toml          # Configuración de Poetry
├── CONTRIBUTING.md         # Guía de contribución
├── LICENSE                 # Licencia MIT
└── README.md              # Este archivo
```

## 🔧 Desarrollo

### Configuración del Entorno

1. **Instala Poetry**: https://python-poetry.org/docs/#installation

2. **Configura el entorno:**

   ```bash
   poetry install
   poetry shell
   ```

3. **Pre-commit hooks** (opcional):
   ```bash
   poetry add --group dev pre-commit
   pre-commit install
   ```

### Comandos de Desarrollo

```bash
# Formateo de código
poetry run black src/ tests/

# Ordenar imports
poetry run isort src/ tests/

# Linting
poetry run flake8 src/ tests/

# Type checking
poetry run mypy src/
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para conocer el proceso.

### Pasos Rápidos

1. Fork del proyecto
2. Crea tu feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

- 📧 **Issues**: [GitHub Issues](https://github.com/tu-usuario/FastApiUserTemplate/issues)
- 📚 **Documentación**: [FastAPI Docs](https://fastapi.tiangolo.com/)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/tu-usuario/FastApiUserTemplate/discussions)

## 🎯 Roadmap

- [ ] Documentación adicional

## ⭐ Agradecimientos

- FastAPI por el framework increíble
- Pydantic por la validación robusta
- SQLAlchemy por el ORM potente
- La comunidad de Python por las herramientas

---

**¿Te gusta el proyecto?** ⭐ ¡Dale una estrella en GitHub!

**¿Encontraste un bug?** 🐛 [Reporta un issue](https://github.com/tu-usuario/FastApiUserTemplate/issues)

**¿Quieres contribuir?** 🚀 [Lee la guía de contribución](CONTRIBUTING.md)
