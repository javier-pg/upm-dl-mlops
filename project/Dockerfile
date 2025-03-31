# Usa una imagen base oficial de Python (por ejemplo, Python 3.9 slim)
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias sin cache para reducir el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación al contenedor
COPY . .

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "project/src/inference_api.py"]
