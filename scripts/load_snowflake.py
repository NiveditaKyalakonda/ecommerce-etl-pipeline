import os
import sys
import snowflake.connector

# Add the root directory to the python path so it can find the config folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def load_gcs_to_snowflake(table_name, gcs_file_path):
    """
    Triggers Snowflake to ingest a specific CSV file from Google Cloud Storage
    into a target Snowflake table using the COPY INTO command.
    """
    print(f"[INFO] Starting Snowflake load for table: {table_name}...")
    connection = None
    cursor = None

    try:
        # 1. Connect to Snowflake using configuration credentials
        connection = snowflake.connector.connect(
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            account=settings.SNOWFLAKE_ACCOUNT,
            warehouse=settings.SNOWFLAKE_WAREHOUSE,
            database=settings.SNOWFLAKE_DATABASE,
            schema=settings.SNOWFLAKE_SCHEMA
        )
        
        # 2. Create an execution cursor
        cursor = connection.cursor()
        
        # 3. Define the SQL statements
        # Statement A: Ensure target table exists (Basic structure example)
        # Note: In production, you generally pre-create tables with precise data types.
        # This is a fallback example assuming the table structure matches your incoming schema.
        
        # Statement B: Execute the bulk COPY INTO ingestion command from your GCS Integration Stage
        # Replace '@my_gcs_stage' with the name of your specific Snowflake External Stage object
        copy_query = f"""
        COPY INTO {settings.SNOWFLAKE_DATABASE}.{settings.SNOWFLAKE_SCHEMA}.{table_name}
        FROM @my_gcs_stage/{gcs_file_path}
        FILE_FORMAT = (
            TYPE = 'CSV'
            FIELD_DELIMITER = ','
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            EMPTY_FIELD_AS_NULL = TRUE
            ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
        )
        ON_ERROR = 'ABORT_STATEMENT';
        """
        
        # 4. Execute the load command
        print(f"[INFO] Executing COPY INTO command in Snowflake...")
        cursor.execute(copy_query)
        
        # 5. Fetch execution results to confirm performance status
        results = cursor.fetchall()
        for row in results:
            # Snowflake returns details like: file status, rows parsed, rows loaded, errors
            print(f"[SUCCESS] Snowflake Result -> File: {row[0]}, Status: {row[1]}, Rows Loaded: {row[2]}")
            
        return True

    except Exception as e:
        print(f"[ERROR] Failed to load data into Snowflake: {e}")
        return False
        
    finally:
        # 6. Safely close database connections
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("[INFO] Snowflake connection closed.")

if __name__ == "__main__":
    # Test execution assuming 'orders' file exists in your GCS stage directory path
    load_gcs_to_snowflake("orders", "stage/orders.csv")
