# Utiliza una imagen base de Python
FROM python:3.9.19-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y el archivo de configuración de MongoDB
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto que Flask usará
EXPOSE 5000

# Define la variable de entorno para el Flask app
ENV FLASK_APP=app.py

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
