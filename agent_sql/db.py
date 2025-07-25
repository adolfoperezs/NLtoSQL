import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Parámetros de conexión separados para evitar problemas de codificación
DB_HOST = "host.docker.internal"
DB_PORT = "5432"
DB_USER = "agent_user"
DB_PASSWORD = "agent_pass"
DB_NAME = "agent_db"

# Crea el motor de SQLAlchemy con parámetros separados
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False,
    connect_args={
        "client_encoding": "utf8"
    }
)

def execute_query(sql: str):
    """
    Ejecuta la consulta SQL y devuelve resultados como lista de dicts.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

        # Mapea filas a dicts {columna: valor}
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
