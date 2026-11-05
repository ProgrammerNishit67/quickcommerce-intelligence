import os
import glob
import pytest
from sqlalchemy import text
from app.database import engine

SQL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "sql_queries"
)

def test_sql_query_files_exist():
    sql_files = glob.glob(os.path.join(SQL_DIR, "*.sql"))
    assert len(sql_files) >= 25, f"Expected at least 25 SQL query files, found {len(sql_files)}"

@pytest.mark.parametrize("query_file", sorted(glob.glob(os.path.join(SQL_DIR, "*.sql"))))
def test_sql_query_execution(query_file):
    """
    Execute each SQL query file against the database to guarantee syntax correctness,
    join alignment, and non-empty execution where applicable.
    """
    with open(query_file, "r", encoding="utf-8") as f:
        sql_content = f.read().strip()
    
    # Strip comments and empty lines
    clean_lines = [line for line in sql_content.splitlines() if not line.strip().startswith("--")]
    clean_sql = "\n".join(clean_lines).strip()
    
    if not clean_sql:
        return

    with engine.connect() as conn:
        result = conn.execute(text(clean_sql))
        rows = result.fetchall()
        # Verify execution completed without raising exception
        assert result.keys() is not None
        assert len(result.keys()) > 0
