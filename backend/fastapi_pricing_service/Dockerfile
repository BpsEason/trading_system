# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project
COPY backend/fastapi_pricing_service /app/fastapi_pricing_service
COPY backend/tests /app/tests # 複製測試文件以便在容器內運行測試

# Expose port
EXPOSE 8001

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "fastapi_pricing_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
