# readme-transactions

Microservicio de transacciones y reseñas.

## 1. Configuración

```bash
cp .env.example .env
# Rellenar los valores en .env
```

## 2. Desarrollo local

```bash
# Levantar base de datos
docker compose up -d db

# Correr el microservicio
uv run uvicorn app.main:app --reload --port 8006
```

## 3. Docker

```bash
docker build -t readme-transactions .
docker run --env-file .env -p 8006:8006 readme-transactions
```
