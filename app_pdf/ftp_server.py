from ftplib import FTP_TLS
import ssl
import json
import os
from dotenv import load_dotenv
import pdb
load_dotenv("ftp_server_settings.env")

ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")


def upload_file_to_ftp(file_path, ftp_host, ftp_user, ftp_password):
    try:
        # Connect to the FTP server with SSL/TLS
        ftp = FTP_TLS(ftp_host, context=ssl._create_unverified_context())
        ftp.login(user=ftp_user, passwd=ftp_password)

        # Enable SSL/TLS for the data channel
        ftp.prot_p()

        # Set the target directory on the FTP server
        target_directory = "ftpupload"

        # Open the local file in binary mode for reading
        with open(file_path, 'rb') as file:
            # Extract the file name from the file path
            filename = os.path.basename(file_path)

            # Upload the file to the FTP server in the target directory
            ftp.storbinary(f'STOR {target_directory}/{filename}', file)

        ftp.quit()  # Send the QUIT command to the server and close the connection
        print(f"File '{filename}' uploaded successfully.")
    except Exception as e:
        filename = os.path.basename(file_path)  # Assign a default value to filename
        print(f"Error uploading file '{filename}': {str(e)}")
        

# Load the file paths from the JSON file
with open("log.json", "r") as json_file:
    file_paths = json.load(json_file)

# FTP server credentials
ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")


# Upload each file to the FTP server
for receipt_number, file_path in file_paths.items():
    print(f"Uploading file '{receipt_number}'")
    upload_file_to_ftp(file_path, ftp_host, ftp_user, ftp_password)
