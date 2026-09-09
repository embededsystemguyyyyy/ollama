# sql_assistant.py
# The full natural-language SQL assistant: generate, validate, execute
# read-only, and explain results in plain language.

import sqlite3
from sql_generation import generate_sql
from sql_validation import validate_sql, SQLValidationError
from ollama_client import chat_once

SQL_MODEL = "qwen2.5-coder:7b"
EXPLAIN_MODEL = "llama3.2:3b"


def execute_readonly(sql: str, db_path: str) -> list[tuple]:
    # SQLite supports a genuine read-only connection mode via URI syntax  
    # this is a real database-level guarantee, not just an application check.
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return columns, rows


def explain_results(question: str, sql: str, columns: list[str], rows: list[tuple]) -> str:
    formatted_rows = "\n".join(str(dict(zip(columns, row))) for row in rows[:20])

    messages = [
        {"role": "system", "content": (
            "You answer questions using SQL query results. Give a clear, "
            "concise natural-language answer based only on the data shown. "
            "Do not make up numbers not present in the results."
        )},
        {"role": "user", "content": (
            f"Question: {question}\nSQL used: {sql}\nResults:\n{formatted_rows}"
        )},
    ]
    return chat_once(EXPLAIN_MODEL, messages, temperature=0.2)


def ask_database(question: str, db_path: str = "sample.db") -> str:
    sql = generate_sql(question, db_path)
    print(f"  Generated SQL: {sql}")

    try:
        validated_sql = validate_sql(sql, db_path)
    except SQLValidationError as exc:
        return f"I couldn't safely answer that question: {exc}"

    try:
        columns, rows = execute_readonly(validated_sql, db_path)
    except sqlite3.Error as exc:
        return f"The query failed to execute: {exc}"

    if not rows:
        return "That query returned no results."

    return explain_results(question, validated_sql, columns, rows)


def main():
    print("Natural-language database assistant. Type 'exit' to quit.\n")
    while True:
        question = input("Ask about your data: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        answer = ask_database(question)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    main()
