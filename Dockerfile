FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY app /app
COPY tests /tests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
