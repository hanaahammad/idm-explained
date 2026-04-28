import duckdb

DB_PATH = "demo_dbt/demo_dbt.duckdb"

def run_query(query):
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            return conn.execute(query).df()
    except Exception as e:
        return None

def safe_col(df, candidates):
    if df is None:
        return None
    for c in candidates:
        if c in df.columns:
            return c
    return None