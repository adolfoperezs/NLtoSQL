import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Parámetros de conexión
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "agent_user"
DB_PASSWORD = "agent_pass"
DB_NAME = "agent_db"

def execute_query(sql: str):
    """
    FUNCIÓN TEMPORAL: Simula una respuesta de base de datos para pruebas.
    Una vez que confirmemos que el resto funciona, volveremos a la conexión real.
    """
    print(f"SQL generado: {sql}")
    
    # Simular resultados de base de datos
    mock_results = [
        {"id": 1, "nombre": "Juan Pérez", "email": "juan@ejemplo.com", "fecha_registro": "2024-01-15"},
        {"id": 2, "nombre": "María García", "email": "maria@ejemplo.com", "fecha_registro": "2024-01-20"},
        {"id": 3, "nombre": "Carlos López", "email": "carlos@ejemplo.com", "fecha_registro": "2024-01-25"}
    ]
    
    return mock_results

    # CÓDIGO ORIGINAL COMENTADO TEMPORALMENTE
    # conn_params = {
    #     "host": DB_HOST,
    #     "port": DB_PORT,
    #     "dbname": DB_NAME,
    #     "user": DB_USER,
    #     "password": DB_PASSWORD,
    # }
    # 
    # try:
    #     with psycopg2.connect(**conn_params) as conn:
    #         with conn.cursor(cursor_factory=DictCursor) as cur:
    #             cur.execute(sql)
    #             rows = cur.fetchall()
    # 
    #     # Decodificación manual y explícita para evitar errores
    #     results = []
    #     for row in rows:
    #         result_row = {}
    #         for key, value in row.items():
    #             if isinstance(value, bytes):
    #                 # Forzar la decodificación a latin1, que es la causa del problema
    #                 result_row[key] = value.decode('latin1')
    #             else:
    #                 result_row[key] = value
    #         results.append(result_row)
    #         
    #     return results
    # except Exception as e:
    #     print(f"Error executing query with manual decoding: {e}")
    #     raise
