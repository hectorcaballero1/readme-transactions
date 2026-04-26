FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8006"]
