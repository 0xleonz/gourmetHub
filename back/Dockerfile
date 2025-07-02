# back/Dockerfile
FROM python:3.11-slim

# 1) Instala la CLI de uv (el gestor de Astral)
RUN pip install uv

WORKDIR /app

# 2) Copia solo definición de deps (pyproject + lock)
COPY pyproject.toml uv.lock /app/

# 3) Instala dependencias con uv
RUN uv sync --no-dev

# 4) Copia el código de la app
COPY app /app/app

EXPOSE 8000

# 5) Comando de arranque con reload
CMD ["uv", "run", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

