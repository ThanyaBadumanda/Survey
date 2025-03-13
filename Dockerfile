FROM python:3.12.4
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
# Run the Django application
CMD sh -c "python manage.py migrate && echo 'Server running at: http://localhost:8000/' && python manage.py runserver 0.0.0.0:8000"