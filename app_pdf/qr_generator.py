import qrcode
import os
import requests
from urllib.parse import urlencode

DEFAULT_SERVER_IP = "localhost"
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
SERVER_URL = f"http://{SERVER_IP}:8080/getPDF"

def put_pdf_to_server():
    try:
        with open("receipt.pdf", "rb") as file:
            files = {"file": file}
            response = requests.put(SERVER_URL, files=files)

            if response.status_code == 200:
                print("PDF file successfully posted to the server.")
            else:
                print(f"Error: {response.status_code} - {response.reason}")
    except IOError as e:
        print(f"Error: Failed to open the PDF file - {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to the server - {e}")

put_pdf_to_server()

# Create the download URL
download_url = SERVER_URL

# Create the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(download_url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")

# Save or display the QR code image
qr_img.save("qr_code.png")
qr_img.show()