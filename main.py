import sys
import os
from scripts.extract_mysql import extract_from_mysql
from scripts.upload_gcs import upload_to_gcs
from scripts.load_duckdb import load_csv_to_duckdb

def run_pipeline(table_name):
    print("==================================================")
    print(f"STARTING E-COMMERCE ETL PIPELINE FOR: {table_name.upper()}")
    print("==================================================")
    
    # --------------------------------------------------
    # STEP 1: EXTRACT (MySQL -> Local CSV)
    # --------------------------------------------------
    local_csv = extract_from_mysql(table_name)
    
    if not local_csv:
        print(f"[FATAL] Pipeline stopped: Extraction failed for table '{table_name}'.")
        sys.exit(1)
        
    # --------------------------------------------------
    # STEP 2: TRANSFORM/STAGE (Local CSV -> Google Cloud Storage)
    # --------------------------------------------------
    gcs_blob_name = f"stage/{table_name}.csv"
    upload_success = upload_to_gcs(local_csv, gcs_blob_name)
    
    if not upload_success:
        print(f"[WARNING] GCS Upload failed/skipped. Proceeding with local DuckDB load...")
        # Note: We use a warning instead of a fatal exit here so you can still 
        # completely test your pipeline locally even if your Google Cloud credentials aren't set up yet!
        
    # --------------------------------------------------
    # STEP 3: LOAD (Local CSV -> Local DuckDB Analytical Database)
    # --------------------------------------------------
    load_success = load_csv_to_duckdb(table_name)
    
    if not load_success:
        print(f"[FATAL] Pipeline stopped: Loading into DuckDB failed for table '{table_name}'.")
        sys.exit(1)

    print("==================================================")
    print(f"ETL PIPELINE COMPLETED SUCCESSFULLY FOR: {table_name.upper()}")
    print("==================================================\n")

if __name__ == "__main__":
    # Define the list of tables you want to sync from your e-commerce backend database
    tables_to_sync = ["orders", "products", "customers"]
    
    for table in tables_to_sync:
        run_pipeline(table)
