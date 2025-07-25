import pytest
from unittest.mock import MagicMock
from langchain_core.runnables import Runnable
from agent_sql.chains.sql_chain import SQLAgentChain

class MockRunnable(Runnable):
    """
    Clase mock que simula ser un 'Runnable' de LangChain para los tests.
    Hereda de Runnable para ser compatible con la nueva arquitectura.
    """
    def __init__(self, output_text: str):
        self.output_text = output_text

    def invoke(self, inputs: dict, config=None, **kwargs) -> str: # Devolver str
        # Devolvemos el texto directamente
        return self.output_text

# --- Tests para la generación y validación de SQL ---

def test_generate_sql_simple_select():
    """Prueba que se genera una consulta SELECT simple correctamente."""
    mock_llm = MockRunnable(output_text="SELECT * FROM clientes;")
    agent = SQLAgentChain(llm=mock_llm)
    
    sql = agent.generate_sql("listar todos los clientes", "clientes(id, nombre)")
    
    assert sql == "SELECT * FROM clientes"
    assert "SELECT" in sql.upper()
    assert ";" not in sql

def test_validate_sql_rejects_drop():
    """Prueba que la validación rechaza sentencias DROP."""
    mock_llm = MockRunnable(output_text="DROP TABLE ventas;")
    agent = SQLAgentChain(llm=mock_llm)
    
    with pytest.raises(ValueError, match="Consulta no permitida. Usa solo SELECT."):
        agent.generate_sql("borrar la tabla de ventas", "ventas(id)")

def test_validate_sql_rejects_delete():
    """Prueba que la validación rechaza sentencias DELETE."""
    mock_llm = MockRunnable(output_text="DELETE FROM clientes WHERE id = 1;")
    agent = SQLAgentChain(llm=mock_llm)
    
    with pytest.raises(ValueError, match="Consulta no permitida. Usa solo SELECT."):
        agent.generate_sql("eliminar el cliente 1", "clientes(id)")

def test_validate_sql_rejects_multiple_statements():
    """Prueba que se rechazan múltiples sentencias para evitar inyección."""
    malicious_sql = "SELECT * FROM clientes; DROP DATABASE agent_db;"
    mock_llm = MockRunnable(output_text=malicious_sql)
    agent = SQLAgentChain(llm=mock_llm)
    
    with pytest.raises(ValueError, match="Múltiples consultas o inyección de SQL detectada."):
        agent.generate_sql("dame los clientes y borra la base de datos", "clientes(id)")

def test_removes_sql_markdown_delimiters():
    """Prueba que los delimitadores de markdown ```sql son eliminados."""
    sql_with_delimiters = "```sql\nSELECT nombre FROM clientes;\n```"
    mock_llm = MockRunnable(output_text=sql_with_delimiters)
    agent = SQLAgentChain(llm=mock_llm)
    
    sql = agent.generate_sql("dame los nombres de los clientes", "clientes(nombre)")
    
    assert sql == "SELECT nombre FROM clientes"
    assert "```" not in sql 