from ftplib import FTP_TLS
import ssl
import json
import os
from dotenv import load_dotenv
import pdb

load_dotenv("settings.env")

ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")


def preparing_to_upload_ftp(file_path, ftp_host, ftp_user, ftp_password):
    try:
        # Connect to the FTP server with SSL/TLS
        ftp = FTP_TLS(ftp_host, context=ssl._create_unverified_context())
        ftp.login(user=ftp_user, passwd=ftp_password)

        # Enable SSL/TLS for the data channel
        ftp.prot_p()

        # Set the target directory on the FTP server
        target_directory = "public_html/blitzkasse.de/download/ftpupload"

        # Extract the file name from the file path
        filename = os.path.basename(file_path)

        # Open the local file in binary mode for reading
        with open(file_path, 'rb') as file:
            # Upload the file to the FTP server in the target directory
            ftp.storbinary(f'STOR {target_directory}/{filename}', file)

        print(f"File '{filename}' uploaded successfully.")

        ftp.quit()  # Send the QUIT command to the server and close the connection
    except Exception as e:
        filename = os.path.basename(file_path)  # Assign a default value to filename
        print(f"Error uploading file '{filename}': {str(e)}")


def get_missing_files(upload_report):
    missing_files = []
    for receipt_number, status in upload_report.items():
        if status == "Not Uploaded":
            file_name = f"{receipt_number}.pdf"
            file_path = os.path.join("data", "pdf_rechnungs", file_name)
            missing_files.append(file_path)
    return missing_files


def upload_missing_files():
    # Load the upload report from the file
    with open("upload_report.txt", "r") as report_file:
        upload_report = json.load(report_file)

    # Get the list of missing files
    missing_files = get_missing_files(upload_report)

    # Upload the missing files
    for file_path in missing_files:
        filename = os.path.basename(file_path)
        print(f"Uploading missing file '{filename}'")
        preparing_to_upload_ftp(file_path, ftp_host, ftp_user, ftp_password)


upload_missing_files()