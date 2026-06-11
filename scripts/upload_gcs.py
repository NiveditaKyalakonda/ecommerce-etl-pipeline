import os
import sys
from google.cloud import storage

# Add the root directory to the python path so it can find the config folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def upload_to_gcs(local_file_path, destination_blob_name):
    """
    Uploads a local file to a specified Google Cloud Storage bucket.
    """
    print(f"[INFO] Starting upload for {local_file_path} to GCS...")
    
    # Verify local file exists before trying to upload
    if not os.path.exists(local_file_path):
        print(f"[ERROR] Local file not found: {local_file_path}")
        return False

    try:
        # 1. Point Google Cloud SDK to your JSON service account key file
        # This overrides defaults using the path from settings.py
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GCS_KEY_FILE
        
        # 2. Initialize the GCS Storage Client
        storage_client = storage.Client()
        
        # 3. Retrieve the target bucket
        bucket = storage_client.bucket(settings.GCS_BUCKET_NAME)
        
        # 4. Create a blob object representing the destination path inside the bucket
        blob = bucket.blob(destination_blob_name)
        
        # 5. Upload the file
        print(f"[INFO] Uploading to bucket '{settings.GCS_BUCKET_NAME}' as '{destination_blob_name}'...")
        blob.upload_from_filename(local_file_path)
        
        print(f"[SUCCESS] File successfully uploaded to GCS.")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to upload file to Google Cloud Storage: {e}")
        return False

if __name__ == "__main__":
    # Test the script with a dummy sample file path
    upload_to_gcs("data/orders.csv", "stage/orders.csv")

