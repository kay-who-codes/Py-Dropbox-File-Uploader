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
SCRIPT_NAME = "Dropbox File Uploader.py"

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

def upload_directory(local_directory, dropbox_directory, dbx):
    """Uploads all files in a directory, including files in subdirectories."""
    # Traverse the local directory, including subfolders
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            local_path = os.path.join(root, file_name)

            # Skip the script itself
            if file_name != SCRIPT_NAME:
                # Construct Dropbox path with sub-folder structure
                relative_path = os.path.relpath(local_path, local_directory)
                dropbox_path = os.path.join(dropbox_directory, relative_path).replace("\\", "/")  # Ensure forward slashes for Dropbox paths

                # Ensure the folder exists in Dropbox
                folder_path = os.path.dirname(dropbox_path)
                ensure_dropbox_folder_exists(folder_path, dbx)

                # Upload the file
                upload_file_to_dropbox(local_path, dropbox_path, dbx)

def main():
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    # Ensure the target Dropbox folder exists
    ensure_dropbox_folder_exists(DROPBOX_FOLDER, dbx)

    # Upload all files in the local folder (including subfolders)
    upload_directory(LOCAL_FOLDER, DROPBOX_FOLDER, dbx)

if __name__ == "__main__":
    main()
