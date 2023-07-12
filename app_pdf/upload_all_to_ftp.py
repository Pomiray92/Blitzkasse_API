from ftplib import FTP_TLS
import ssl
import json
import os
from dotenv import load_dotenv

load_dotenv("settings.env")

ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")

#breakpoint()
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

        # Check if the marker file already exists on the FTP server
        marker_filename = f"{filename}.uploaded"
        if marker_filename in ftp.nlst(target_directory):
            print(f"File '{filename}' is already uploaded.")
            return

        # Open the local file in binary mode for reading
        with open(file_path, 'rb') as file:

            # Upload the file to the FTP server in the target directory
            ftp.storbinary(f'STOR {target_directory}/{filename}', file)

        ftp.quit()  # Send the QUIT command to the server and close the connection
    except Exception as e:
        filename = os.path.basename(file_path)  # Assign a default value to filename
        print(f"Error uploading file '{filename}': {str(e)}")


def get_uploaded_file_list(ftp, target_directory):
    # Get the list of files in the target directory
    ftp.cwd(target_directory)
    file_list = ftp.nlst()
    ftp.cwd('/')  # Return to the root directory
    #breakpoint()
    return file_list


def mark_file_as_uploaded(ftp, target_directory, filename):
    # Create a marker file in the target directory to indicate that the file has been uploaded
    marker_filename = f"{filename}.uploaded"
    ftp.storbinary(f'STOR {target_directory}/{marker_filename}', open(os.devnull, 'rb'))


def check_all_uploaded():
    # Load the log files
    with open('logs/pdf_creation_log.json') as creation_file, open('logs/upload_log.json') as upload_file:
        creation_log = json.load(creation_file)
        upload_log = json.load(upload_file)

    # Connect to the FTP server with SSL/TLS
    ftp = FTP_TLS(ftp_host, context=ssl._create_unverified_context())
    ftp.login(user=ftp_user, passwd=ftp_password)

    # Enable SSL/TLS for the data channel
    ftp.prot_p()

    # Set the target directory on the FTP server
    target_directory = "public_html/blitzkasse.de/download/ftpupload"

    # Get the list of files already uploaded on the FTP server
    uploaded_files = get_uploaded_file_list(ftp, target_directory)

    # Check if all items in the creation log are uploaded
    for key in creation_log:
        if key in upload_log or key in uploaded_files:
            continue  # Skip the file if it's already uploaded

        file_path = creation_log[key]
        preparing_to_upload_ftp(file_path, ftp_host, ftp_user, ftp_password)
        #mark_file_as_uploaded(ftp, target_directory, os.path.basename(file_path))
        upload_log[key] = "successful uploaded"

    ftp.quit()  # Send the QUIT command to the server and close the connection

    # Update the upload log file
    with open('logs/upload_log.json', 'w') as upload_file:
        json.dump(upload_log, upload_file)

    return True

check_all_uploaded()