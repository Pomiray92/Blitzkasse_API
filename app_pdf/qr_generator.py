import qrcode
from PIL import Image
import json
import pdb
import os
from dotenv import load_dotenv
load_dotenv("ftp_server_settings")

download_url = os.getenv("DOWNLOAD_URL", "https://blitzkasse.de/")
target_directory = os.getenv("TARGET_DIRECTORY", "download/ftpupload")
#breakpoint()
def qr_generator():
    # Load the file paths from the JSON file
    with open("log.json", "r") as json_file:
        file_paths = json.load(json_file)

    # Get the latest receipt number
    latest_receipt_number = max(file_paths.keys())

    # Get the file path for the latest receipt number
    file_path = file_paths[latest_receipt_number]

    # Complete file name and path
    file_name = f"{latest_receipt_number}.pdf"
    
    file_path = target_directory + '/' + os.path.basename(file_paths[latest_receipt_number])

    # Download URL
    download_path = download_url + file_path
    
    # Generate the QR code
    qr = qrcode.QRCode()
    qr.add_data(download_path)
    qr.make()

    # Create an image from the QR code
    qr_image = qr.make_image()

    # Save the QR code image
    if not os.path.exists("png_receipts"):
        os.makedirs("png_receipts")
    qr_image.save(f"png_receipts/{file_name}.png")

    # Open the QR code image
    img = Image.open(f"png_receipts/{file_name}.png")
    img.show()

