import os
import duckdb

def load_csv_to_duckdb(table_name):
    print(f"[INFO] Starting DuckDB load for table: {table_name}...")
    local_csv_path = f"data/{table_name}.csv"
    
    if not os.path.exists(local_csv_path):
        print(f"[ERROR] Local CSV file not found: {local_csv_path}")
        return False

    try:
        # The database connection ONLY opens inside the function
        conn = duckdb.connect("ecommerce_warehouse.db")
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM '{local_csv_path}'")
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        print(f"[SUCCESS] Loaded rows into DuckDB table '{table_name}': {result}")
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to load data into DuckDB: {e}")
        return False

if __name__ == "__main__":
    load_csv_to_duckdb("orders")
