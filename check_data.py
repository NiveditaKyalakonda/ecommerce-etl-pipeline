import duckdb

def check_my_warehouse():
    print("==================================================")
    print("CHECKING LOCAL DATA WAREHOUSE (DUCKDB)")
    print("==================================================")
    
    try:
        # 1. Connect to your database file
        conn = duckdb.connect('ecommerce_warehouse.db')
        
        # 2. Query and list all existing tables
        print("[INFO] Existing tables in warehouse:")
        tables = conn.execute("SHOW TABLES").fetchall()
        
        if not tables:
            print("[WARNING] No tables found! Run main.py first.")
            conn.close()
            return
            
        for t in tables:
            print(f" -> Table Name: {t[0]}")
            
        print("-" * 50)
        
        # 3. Print a quick preview of your data tables
        for t in tables:
            table_name = t[0]
            print(f"[INFO] Showing first 5 rows for table: {table_name}")
            
            # Use Pandas integration built straight into DuckDB for nice layout formatting
            df_preview = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").df()
            print(df_preview)
            print("-" * 50)
            
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] Failed to query database: {e}")

if __name__ == "__main__":
    check_my_warehouse()
