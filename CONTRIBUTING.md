# Contributing to FastAPI User Template

¡Gracias por tu interés en contribuir a este proyecto! Este documento proporciona pautas y información sobre cómo contribuir de manera efectiva.

## Configuración del Entorno de Desarrollo

### Prerrequisitos

- Python 3.11+
- Poetry
- Docker y Docker Compose
- Git

### Configuración Inicial

1. **Fork y clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/FastApiUserTemplate.git
   cd FastApiUserTemplate
   ```

2. **Instala las dependencias:**

   ```bash
   poetry install
   poetry shell
   ```

3. **Configura la base de datos para desarrollo:**

   ```bash
   docker-compose up -d db
   ```

4. **Ejecuta los tests:**
   ```bash
   poetry run pytest
   ```

## Tests

### Ejecutar Tests

```bash
# Todos los tests
poetry run pytest

# Tests con coverage
poetry run pytest --cov=src/

# Tests específicos
poetry run pytest tests/test_auth_flow.py
```

## Proceso de Contribución

### 1. Issues

- Revisa los issues existentes antes de crear uno nuevo
- Usa las plantillas de issue cuando estén disponibles
- Proporciona información detallada y pasos para reproducir bugs

### 2. Pull Requests

1. **Crea una rama para tu feature:**

   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

2. **Haz commits atómicos y descriptivos:**

   ```bash
   git commit -m "feat: añade autenticación con cookies HTTP-only"
   ```

3. **Sigue el formato de commits convencionales:**

   - `feat:` nueva funcionalidad
   - `fix:` corrección de bug
   - `docs:` cambios en documentación (Crear)
   - `style:` cambios de formato (no afectan la lógica)
   - `refactor:` refactorización de código
   - `test:` añadir o modificar tests
   - `chore:` cambios en herramientas, configuración, etc.

4. **Ejecuta todos los tests antes de hacer push:**

   ```bash
   poetry run pytest
   ```

5. **Abre un Pull Request con:**
   - Título descriptivo
   - Descripción detallada de los cambios
   - Referencias a issues relacionados
   - Screenshots si aplica

### 3. Review Process

- Todos los PRs necesitan al menos una revisión
- Responde a los comentarios de review de manera constructiva
- Haz los cambios solicitados en commits adicionales

## Arquitectura del Proyecto

### Estructura de Código

```
src/
└── fastapiusertemplate/
    ├── __init__.py
    ├── main.py          # Aplicación FastAPI principal
    ├── models.py        # Modelos SQLAlchemy
    ├── schema.py        # Esquemas Pydantic
    ├── crud.py          # Operaciones de base de datos
    ├── auth.py          # Sistema de autenticación
    └── database.py      # Configuración de base de datos
```

### Principios de Diseño

- **Separación de responsabilidades:** cada módulo tiene una responsabilidad específica
- **Dependency Injection:** usa FastAPI dependencies para inyección de dependencias
- **Error Handling:** maneja errores de manera consistente con HTTPException

## Seguridad

### Autenticación

- Usa cookies HTTP-only para tokens JWT
- Implementa refresh tokens para sesiones seguras
- Hash passwords con bcrypt
- Valida todas las entradas del usuario

### Consideraciones

- No commites secretos o claves API
- Usa variables de entorno para configuración sensible
- Revisa dependencies por vulnerabilidades conocidas

## Base de Datos

### Modelos

- Usa UUID como primary keys

### README

- Mantén el README actualizado con cambios significativos
- Incluye ejemplos de uso
- Documenta cambios en la API

## Deployment

### Docker

- El proyecto usa Docker para desarrollo y producción
- Usa multi-stage builds para optimizar tamaño de imagen
- Configura health checks apropiados

### Variables de Entorno

```bash
# Desarrollo
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_template_user
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Producción
# Usa valores seguros y únicos
```

## Preguntas y Soporte

- Crea un issue para preguntas técnicas
- Revisa la documentación existente
- Participa en discusiones constructivas

## Reconocimientos

Reconocemos y agradecemos todas las contribuciones, desde código hasta documentación y reportes de bugs.

¡Gracias por contribuir! 🚀
