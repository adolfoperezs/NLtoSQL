from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

from agent_sql.db import execute_query
from agent_sql.chains.sql_chain import SQLAgentChain

# Carga variables de entorno
load_dotenv()

# Inicializa FastAPI
app = FastAPI(
    title="SQLAgent API",
    description="API para ejecutar consultas SQL generadas a partir de lenguaje natural",
    version="0.1.0"
)

# Endpoint raíz para verificar que la API está activa
@app.get("/")
def read_root():
    return {"message": "SQLAgent API está en funcionamiento. Usa el endpoint /query para enviar consultas."}

# Inicializa el agente de SQL
agent = SQLAgentChain()

# Modelos de Pydantic para request/response
class QueryRequest(BaseModel):
    """
    query: Consulta en lenguaje natural
    schema: Descripción del esquema de la base de datos
    """
    query: str
    db_schema: str = Field(alias="schema")

class QueryResponse(BaseModel):
    """
    sql: Consulta SQL generada
    results: Resultados de la ejecución (lista de diccionarios)
    """
    sql: str
    results: list[dict]

@app.post("/query", response_model=QueryResponse)
def run_query(request: QueryRequest):
    """
    Endpoint para recibir una consulta en NL, generar SQL y retornar resultados.
    """
    try:
        # Genera y valida SQL
        sql = agent.generate_sql(request.query, request.db_schema)
        
        # Ejecuta la consulta
        results = execute_query(sql)
        
        return QueryResponse(sql=sql, results=results)
        
    except ValueError as ve:
        # Errores de validación de SQL
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Errores inesperados
        # Es bueno loggear el error real para depuración
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    import uvicorn
    # Ejecutar con: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 