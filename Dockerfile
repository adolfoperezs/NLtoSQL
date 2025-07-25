# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto si es necesario (para futuras APIs)
# EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["python", "-m", "agent_sql.main"] 