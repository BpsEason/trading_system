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
COPY backend/django_order_app /app/django_order_app
COPY backend/django_order_app/tests /app/django_order_app/tests # 修正複製測試文件路徑

# Expose port
EXPOSE 8000

# Run Django migrations and start the server
CMD ["python", "django_order_app/manage.py", "runserver", "0.0.0.0:8000"]
