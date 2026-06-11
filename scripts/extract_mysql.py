import os
import sys
import mysql.connector
import pandas as pd

# Add the root directory to the python path so it can find the config folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def extract_from_mysql(table_name):
    """
    Connects to MySQL, extracts data from a specified table safely, 
    and saves it to a local CSV file.
    """
    print(f"[INFO] Starting extraction for table: {table_name}...")
    connection = None
    cursor = None
    
    try:
        # 1. Establish connection to MySQL
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE
        )
        
        # 2. Open a database cursor to safely fetch rows
        cursor = connection.cursor()
        
        # 3. Securely format the table name to prevent SQL injection issues
        # (Using basic backticks identifier cleaning)
        clean_table_name = f"`{table_name.replace('`', '')}`"
        query = f"SELECT * FROM {clean_table_name}"
        
        print(f"[INFO] Fetching data from MySQL...")
        cursor.execute(query)
        
        # 4. Fetch rows and column headers manually to feed Pandas without connection bugs
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # 5. Load the raw matrix cleanly into a Pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        # 6. Safely manage and auto-create the local output directory
        output_dir = "data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_file = os.path.join(output_dir, f"{table_name}.csv")
        
        # 7. Save the DataFrame to a CSV file (using UTF-8 encoding to support emojis/text symbols)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"[SUCCESS] Extracted {len(df)} rows. Saved to: {output_file}")
        
        return output_file

    except Exception as e:
        print(f"[ERROR] Failed to extract data from MySQL: {e}")
        return None
        
    finally:
        # 8. Clean up execution states and close connections safely
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("[INFO] MySQL connection closed.")

if __name__ == "__main__":
    # Test the script with an 'orders' table
    extract_from_mysql("orders")
