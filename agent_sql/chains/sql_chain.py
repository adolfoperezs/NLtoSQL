from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # Importar ChatOpenAI
import re

class SQLAgentChain:
    def __init__(self, llm=None):
        # Usar ChatOpenAI en lugar de OpenAI
        self.llm = llm or ChatOpenAI(model="o4-mini", temperature=1)
        
        prompt = PromptTemplate(
            input_variables=["user_query", "schema"],
            template=(
                "Eres un asistente que convierte consultas en lenguaje natural "
                "a SQL para una base de datos PostgreSQL con este esquema:\n"
                "{schema}\n\n"
                "Reglas:\n"
                "- Solo SELECT. No permitas DROP, DELETE, UPDATE ni INSERT.\n"
                "- La consulta SQL debe ser una sola línea, sin saltos de línea.\n"

                "Consulta: {user_query}\n"
                "SQL:"
            )
        )
        self.chain = LLMChain(llm=self.llm, prompt=prompt)

    def generate_sql(self, user_query: str, schema: str) -> str:
        # LLMChain.invoke devuelve un diccionario, extraemos la clave 'text'
        response = self.chain.invoke({"user_query": user_query, "schema": schema})
        raw_sql = response.get('text', '')
        return self._validate_sql(raw_sql)

    def _validate_sql(self, sql: str) -> str:
        # Usar regex para eliminar los delimitadores de markdown y saltos de línea
        sql = re.sub(r"```sql\s*", "", sql).strip()
        sql = re.sub(r"```", "", sql).strip()

        # Si hay un punto y coma al final, lo eliminamos
        if sql.endswith(";"):
            sql = sql[:-1]

        # 1. Primero, verificar que no haya múltiples consultas
        if re.search(r";", sql):
            raise ValueError("Múltiples consultas o inyección de SQL detectada.")

        # 2. Segundo, verificar palabras prohibidas
        forbidden = ["DROP ", "DELETE ", "UPDATE ", "INSERT "]
        if any(word in sql.upper() for word in forbidden):
            raise ValueError("Consulta no permitida. Usa solo SELECT.")
            
        return sql 