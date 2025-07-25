import pytest
from unittest.mock import patch, MagicMock
from agent_sql.db import execute_query


def test_execute_query_simple():
    """Test básico de execute_query usando mock para simular la base de datos"""
    
    # Mock del resultado de la consulta
    mock_result = MagicMock()
    mock_result.fetchall.return_value = [(1,)]
    mock_result.keys.return_value = ['num']
    
    # Mock de la conexión
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result
    
    # Mock del engine
    with patch('agent_sql.db.engine') as mock_engine:
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Ejecutar la función
        result = execute_query("SELECT 1 AS num;")
        
        # Verificar el resultado
        assert isinstance(result, list)
        assert result == [{"num": 1}]
        
        # Verificar que se llamó a execute con la consulta correcta
        mock_conn.execute.assert_called_once()


def test_execute_query_multiple_rows():
    """Test de execute_query con múltiples filas"""
    
    # Mock del resultado con múltiples filas
    mock_result = MagicMock()
    mock_result.fetchall.return_value = [(1, 'Alice'), (2, 'Bob')]
    mock_result.keys.return_value = ['id', 'name']
    
    # Mock de la conexión
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result
    
    # Mock del engine
    with patch('agent_sql.db.engine') as mock_engine:
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Ejecutar la función
        result = execute_query("SELECT id, name FROM users;")
        
        # Verificar el resultado
        expected = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        assert result == expected


def test_execute_query_empty_result():
    """Test de execute_query sin resultados"""
    
    # Mock del resultado vacío
    mock_result = MagicMock()
    mock_result.fetchall.return_value = []
    mock_result.keys.return_value = ['id', 'name']
    
    # Mock de la conexión
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result
    
    # Mock del engine
    with patch('agent_sql.db.engine') as mock_engine:
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Ejecutar la función
        result = execute_query("SELECT * FROM empty_table;")
        
        # Verificar el resultado vacío
        assert isinstance(result, list)
        assert result == [] 