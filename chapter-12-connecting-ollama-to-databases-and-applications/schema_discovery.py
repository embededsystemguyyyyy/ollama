# schema_discovery.py
# Introspects a SQLite database and produces a schema description
# suitable for use as model context.

import sqlite3


def discover_schema(db_path: str) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

    schema_lines = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        column_desc = ", ".join(f"{col[1]} ({col[2]})" for col in columns)
        schema_lines.append(f"Table {table}: {column_desc}")

    conn.close()
    return "\n".join(schema_lines)


if __name__ == "__main__":
    print(discover_schema("sample.db"))
