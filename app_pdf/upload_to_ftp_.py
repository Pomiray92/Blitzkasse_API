from ftplib import FTP_TLS
import ssl
import json
import os
from dotenv import load_dotenv
from get_api import data_dict

load_dotenv("settings.env")

ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")
receipt_number = data_dict["BONNUMBER"]

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

        #print(f"File '{filename}' uploaded successfully.")
        def upload_report():
            log_data = {
                f"Receipt_N{receipt_number}": 'successful uploaded',
            }

            upload_log_file_path = os.path.join(os.getcwd(), "logs/upload_log.json")

            # Check if the log file exists
            if os.path.exists(upload_log_file_path):
                with open(upload_log_file_path, "r") as log_file:
                    existing_data = json.load(log_file)

                # Update the existing data with the new entry
                existing_data.update(log_data)
                with open(upload_log_file_path, "w") as log_file:
                    json.dump(existing_data, log_file, indent=4)
            else:
                with open(upload_log_file_path, "w") as log_file:
                    json.dump(log_data, log_file, indent=4)
        upload_report()

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
    with open("logs/pdf_creation_log.json", "r") as json_file:
        file_paths = json.load(json_file)

    # Get the last file path
    last_file_path = list(file_paths.values())[-1]

    # Upload the last file
    filename = os.path.basename(last_file_path)
    print(f"Uploading file '{filename}'")
    preparing_to_upload_ftp(last_file_path, ftp_host, ftp_user, ftp_password)

