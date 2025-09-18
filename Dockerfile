# Usar imagen oficial de Python
FROM python:3.13-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Configurar Poetry para no crear entorno virtual (ya estamos en Docker)
RUN poetry config virtualenvs.create false

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock ./

# Instalar solo dependencias (sin el proyecto actual)
RUN poetry install --no-root

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "src.fastapiusertemplate.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]