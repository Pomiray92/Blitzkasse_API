import requests
from fpdf import FPDF
import requests
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv

load_dotenv()

# CONSTANT VARIABLES
DEFAULT_SERVER_IP = "localhost"
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
LAST_RECEIPT_URL = f"http://{SERVER_IP}:8001/getLastReceipt"


TIMESTAMP = datetime.now().strftime("%d.%m.%Y-%H:%M")
CURRENT_DATETIME = datetime.now()
YEAR = CURRENT_DATETIME.year
MONTH = CURRENT_DATETIME.strftime("%B")
DAY = CURRENT_DATETIME.day
CLIENT_INFO_URL = f"http://{SERVER_IP}:8001/ConfigComplete"



def create_settings_env_file():
    DEFAULT_SERVER_IP = "127.0.0.1"

    if not os.path.isfile("settings.env"):
        with open("settings.env", "w") as env_file:
            env_file.write(f"SERVER_IP={DEFAULT_SERVER_IP}\n")


def create_default_readme_file():
    if not os.path.isfile("README.txt"):
        with open("README.txt", "w") as file:
            file.write("---------------------------------------\n")
            file.write("APP for creating pdf from retrieve receipt Information:\n")
            file.write("\n")
            file.write("This app allows you to create a PDF from retrieve receipt data, store it or send via email.\n")
            file.write(".\n")
            file.write("\n")


def validate_server_ip(server_ip):
    try:
        requests.get(f"http://{server_ip}:8001")
        if server_ip == DEFAULT_SERVER_IP:
            print(f"Using default server IP: {server_ip}")
    except requests.exceptions.RequestException:
        print(f"Error: Invalid value for 'SERVER_IP' in the .env file. Please provide a correct SERVER_IP address.")
        exit(1)


def get_receipt_info():

    try:
        response = requests.get(LAST_RECEIPT_URL)
        if response.status_code == 200:
            receipt_data = response.json()
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_client_info():
    try:
        response_client_info = requests.get(CLIENT_INFO_URL)
        if response_client_info.status_code == 200:
            # Assuming the response is in JSON format
            client_info = response_client_info.json()
            return client_info
        else:
            print("Error: Failed to retrieve receipt information. Status code:", response_client_info.status_code)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", e)

    return response_client_info