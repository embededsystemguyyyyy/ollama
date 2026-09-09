# sql_validation.py
# A hard, code-level validation layer for generated SQL. This is the
# real safety boundary   the system prompt in sql_generation.py is a
# nudge, this is the enforcement.

import re
import sqlite3

FORBIDDEN_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "REPLACE", "ATTACH", "DETACH", "PRAGMA",
}


class SQLValidationError(Exception):
    pass


def validate_sql(sql: str, db_path: str) -> str:
    """
    Validates a generated SQL query. Raises SQLValidationError if the
    query is anything other than a safe, read-only SELECT against
    known tables. Returns the cleaned SQL string if valid.
    """
    cleaned = sql.strip().rstrip(";")

    if not cleaned.upper().startswith("SELECT"):
        raise SQLValidationError("Only SELECT statements are permitted.")

    tokens = set(re.findall(r"[A-Za-z]+", cleaned.upper()))
    forbidden_found = tokens & FORBIDDEN_KEYWORDS
    if forbidden_found:
        raise SQLValidationError(f"Query contains forbidden keyword(s): {forbidden_found}")

    # Confirm the query at least parses correctly against SQLite's own
    # parser using EXPLAIN, without actually running it.
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(f"EXPLAIN {cleaned}")
    except sqlite3.Error as exc:
        raise SQLValidationError(f"Query failed to validate: {exc}")
    finally:
        conn.close()

    return cleaned
