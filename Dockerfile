FROM python:3.10-slim
WORKDIR /app
COPY app/ app/
COPY static/ static/
COPY templates/ templates/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "app/main.py"]
