FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY web/pyproject.toml web/uv.lock* ./
RUN uv sync --no-dev --frozen

COPY web/ ./

EXPOSE 8000

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]