FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

FROM base AS dev
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS prod
CMD [
  "gunicorn",
  "app.main:app",
  "-k", "uvicorn.workers.UvicornWorker",
  "--workers", "4",
  "--bind", "0.0.0.0:8000"
]
