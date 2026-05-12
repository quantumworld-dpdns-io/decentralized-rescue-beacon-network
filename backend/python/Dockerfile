FROM python:3.12-slim

WORKDIR /app

COPY backend/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY backend/python/app/ ./app/

ENV PYTHONPATH=/app/src
ENV PYTHON_SERVICE_PORT=5000

EXPOSE 5000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
