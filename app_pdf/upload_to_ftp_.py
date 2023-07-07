from ftplib import FTP_TLS
import ssl
import json
import os
from dotenv import load_dotenv

load_dotenv("ftp_server_settings.env")

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


def get_uploaded_file_list(ftp, target_directory):
    # Get the list of files in the target directory
    ftp.cwd(target_directory)
    file_list = ftp.nlst()
    ftp.cwd('/')  # Return to the root directory
    return file_list


def mark_file_as_uploaded(ftp, target_directory, filename):
    # Create a marker file in the target directory to indicate that the file has been uploaded
    marker_filename = f"{filename}.uploaded"
    ftp.storbinary(f'STOR {target_directory}/{marker_filename}', open(os.devnull, 'rb'))


def read_from_json_and_upload():
    # Load the file paths from the JSON file
    with open("log.json", "r") as json_file:
        file_paths = json.load(json_file)

    # Get the last file path
    last_file_path = list(file_paths.values())[-1]

    # Upload the last file
    filename = os.path.basename(last_file_path)
    print(f"Uploading file '{filename}'")
    preparing_to_upload_ftp(last_file_path, ftp_host, ftp_user, ftp_password)

