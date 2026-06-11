import sys
from scripts.extract_mysql import extract_from_mysql
from scripts.upload_gcs import upload_to_gcs
from scripts.load_snowflake import load_gcs_to_snowflake

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
        print(f"[FATAL] Pipeline stopped: Upload to GCS failed for file '{local_csv}'.")
        sys.exit(1)
        
    # --------------------------------------------------
    # STEP 3: LOAD (Google Cloud Storage -> Snowflake Warehouse)
    # --------------------------------------------------
    load_success = load_gcs_to_snowflake(table_name, gcs_blob_name)
    
    if not load_success:
        print(f"[FATAL] Pipeline stopped: Loading into Snowflake failed for table '{table_name}'.")
        sys.exit(1)

    print("==================================================")
    print(f"ETL PIPELINE COMPLETED SUCCESSFULLY FOR: {table_name.upper()}")
    print("==================================================\n")

if __name__ == "__main__":
    # Define the list of tables you want to sync from your e-commerce platform
    tables_to_sync = ["orders", "products", "customers"]
    
    for table in tables_to_sync:
        run_pipeline(table)
