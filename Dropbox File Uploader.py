# Dropbox Access Token: PLACE_YOUR_ACCESS_TOKEN_HERE_FOR_EASY_ACCESS

import os
import dropbox

# Replace with your Dropbox access token
ACCESS_TOKEN = "ACCESS_TOKEN_GOES_HERE"

# The Dropbox folder path to upload files (e.g., /New Files)
DROPBOX_FOLDER = "DROPBOX_FOLDER_GOES_HERE"

# The local folder containing files to upload
LOCAL_FOLDER = os.path.dirname(os.path.abspath(__file__))  # Directory where the script is located

# Script name to exclude from upload
SCRIPT_NAME = "Book Uploader.py"

def upload_file_to_dropbox(local_path, dropbox_path, dbx):
    """Uploads a file to Dropbox."""
    with open(local_path, "rb") as f:
        try:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
            print(f"Uploaded: {local_path} to {dropbox_path}")
        except dropbox.exceptions.ApiError as e:
            print(f"Failed to upload {local_path}: {e}")

def ensure_dropbox_folder_exists(folder_path, dbx):
    """Ensures the specified folder exists in Dropbox."""
    try:
        dbx.files_get_metadata(folder_path)
        print(f"Folder '{folder_path}' already exists.")
    except dropbox.exceptions.ApiError:
        try:
            dbx.files_create_folder_v2(folder_path)
            print(f"Created folder: {folder_path}")
        except dropbox.exceptions.ApiError as e:
            print(f"Failed to create folder '{folder_path}': {e}")

def main():
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    # Ensure the target Dropbox folder exists
    ensure_dropbox_folder_exists(DROPBOX_FOLDER, dbx)

    # Upload all files in the local folder
    for file_name in os.listdir(LOCAL_FOLDER):
        local_path = os.path.join(LOCAL_FOLDER, file_name)

        # Skip directories and exclude the script itself
        if os.path.isfile(local_path) and file_name != SCRIPT_NAME:
            dropbox_path = f"{DROPBOX_FOLDER}/{file_name}"
            upload_file_to_dropbox(local_path, dropbox_path, dbx)

if __name__ == "__main__":
    main()
