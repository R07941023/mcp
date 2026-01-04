FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY rag-service/pyproject.toml rag-service/uv.lock* ./
RUN uv sync --no-dev --frozen

COPY rag-service/ ./

EXPOSE 8000

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]