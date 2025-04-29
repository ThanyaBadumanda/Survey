FROM python:3.13.2

# Set working directory
WORKDIR /app

# Copy code and requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Run migrations + start server using Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn survey_project.wsgi:application --bind 0.0.0.0:8000"]
