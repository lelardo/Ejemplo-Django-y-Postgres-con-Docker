# Usa la imagen oficial de Python
FROM python:3.13.3

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto para correr Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
