import os
from dotenv import load_dotenv
from agent_sql.chains.sql_chain import SQLAgentChain
# from agent_sql.db import execute_query

# Cargar variables de entorno
load_dotenv()

# Verificar que la clave de API de OpenAI esté configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")

# Esquema de ejemplo de la base de datos
SCHEMA = """
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    region TEXT,
    monto NUMERIC
);

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    email TEXT
);
"""

def main():
    """Función principal para probar el agente SQL."""
    
    # Crear instancia del agente
    agent = SQLAgentChain()
    
    # Consulta de ejemplo en lenguaje natural
    query_nl = "¿Cuántas ventas se realizaron en la región 'Norte' durante el mes de junio de 2025?"
    
    print(f"Consulta en lenguaje natural: {query_nl}")
    
    try:
        # Generar la consulta SQL
        sql_query = agent.generate_sql(query_nl, SCHEMA)
        print(f"Consulta SQL generada:\n{sql_query}")
        
        # # --- (Descomentar para ejecutar en la base de datos) ---
        # print("\nEjecutando consulta...")
        # resultados = execute_query(sql_query)
        # print("Resultados:")
        # print(resultados)
        
    except ValueError as e:
        print(f"Error de validación: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
