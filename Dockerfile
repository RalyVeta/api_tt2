# Usa una imagen base de Python que incluya TensorFlow
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido actual del directorio al directorio /app en el contenedor
COPY . /app

# Copia el archivo requirements.txt al directorio de trabajo en el contenedor
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install -r requirements.txt

# Instala awsgi
RUN pip install awsgi

# Comando por defecto para ejecutar tu aplicación cuando el contenedor se inicie
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080", "--app=app.py"]