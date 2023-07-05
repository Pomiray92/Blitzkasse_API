from ftplib import FTP_TLS
from dotenv import load_dotenv
import os
import pdb
load_dotenv("ftp_server_settings.env")

filename = os.getenv("FILENAME")
ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")

breakpoint()
def upload_file_to_ftp(filename, ftp_host, ftp_user, ftp_password):
    try:
        # Connect to the FTP server with SSL/TLS
        ftp = FTP_TLS(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)

        # Enable SSL/TLS for the data channel
        ftp.prot_p()

        # Set the target directory on the FTP server
        target_directory = "ftpupload"

        # Open the local file in binary mode for reading
        with open(filename, 'rb') as file:
            # Upload the file to the FTP server in the target directory
            ftp.storbinary(f'STOR {target_directory}/{filename}', file)

        # Close the FTP connection
        ftp.quit()
        print("File uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

upload_file_to_ftp(filename, ftp_host, ftp_user, ftp_password)