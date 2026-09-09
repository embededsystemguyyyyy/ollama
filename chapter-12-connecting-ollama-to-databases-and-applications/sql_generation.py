# sql_generation.py
# Generates a SQL query from a natural-language question, using the
# discovered schema as context.

from ollama_client import chat_once
from schema_discovery import discover_schema

SQL_MODEL = "qwen2.5-coder:7b"


def generate_sql(question: str, db_path: str) -> str:
    schema = discover_schema(db_path)

    messages = [
        {"role": "system", "content": (
            "You are a SQL generator. Given a database schema and a question, "
            "write a single valid SQLite SELECT query that answers it. "
            "Only use tables and columns from the schema provided. "
            "Never write INSERT, UPDATE, DELETE, DROP, or ALTER statements   "
            "only SELECT. Respond with ONLY the SQL query, no explanation, "
            "no markdown formatting."
        )},
        {"role": "user", "content": f"Schema:\n{schema}\n\nQuestion: {question}"},
    ]

    response = chat_once(SQL_MODEL, messages, temperature=0.1)
    # Strip common markdown code fence artifacts, just in case.
    return response.strip().strip("`").replace("sql\n", "", 1).strip()
