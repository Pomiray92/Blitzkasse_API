import requests
from datetime import datetime
import argparse
import os
from dotenv import load_dotenv
import pdb

DEFAULT_SERVER_IP = "localhost"
DEFAULT_NUM_PRINTS = 1

# Check if the .env file exists
if not os.path.isfile(".env"):
    # Create a default .env file
    with open(".env", "w") as env_file:
        env_file.write(f"SERVER_IP={DEFAULT_SERVER_IP}\n")
        env_file.write(f"NUM_PRINTS={DEFAULT_NUM_PRINTS}\n")

# Load the environment variables
load_dotenv()
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get the server IP from the environment variable or use the default value
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)

# Check if the README.txt file exists
if not os.path.isfile("README.md"):
    with open("README.md", "w") as file:
        file.write("---------------------------------------\n")
        file.write("APP for triggering printing process:\n")
        file.write("\n")
        file.write("This app allows you to trigger the printing process by reprinting the last receipt.\n")
        file.write("You can specify the number of times to reprint the receipt using command-line arguments or the .env file.\n")
        file.write("\n")

# Validate the server IP
try:
    requests.get(f"http://{SERVER_IP}:8001")
    if DEFAULT_SERVER_IP == True:
        print(f"Using default server IP: {SERVER_IP}")
except requests.exceptions.RequestException:
    print(f"Error: Invalid value for 'SERVER_IP' in the .env file. Please provide a correct SERVER_IP address. ({TIMESTAMP})")
    with open("printing_reports.txt", "a") as file:
        file.write("---------------------------------------\n")
        file.write("Print Error:\n")
        file.write(f"Error: Invalid value for 'SERVER_IP' in the .env file. Please provide a correct SERVER_IP address. ({TIMESTAMP})\n")
    exit(-1)

# Get the number of prints from the environment variable or use the default value
try:
    NUM_PRINTS = int(os.getenv("NUM_PRINTS", DEFAULT_NUM_PRINTS))
    if NUM_PRINTS < 1:
        print("Error: Invalid value for 'NUM_PRINTS' in the .env file. Please provide an integer.")
except ValueError:
    print("Error: Invalid value for 'NUM_PRINTS' in the .env file. Please provide an integer.")
    with open("printing_reports.txt", "a") as file:
        file.write("---------------------------------------\n")
        file.write("Print Error:\n")
        file.write(f"Invalid value for 'NUM_PRINTS' in the .env file. Please provide an integer. ({TIMESTAMP})\n")
    exit(-1)


def get_last_receipt_number():
    get_last_receipt_url = f"http://{SERVER_IP}:8001/getLastReceipt"

    try:
        response = requests.get(get_last_receipt_url)
        if response.status_code == 200:
            receipt_data = response.json()
            receipt_number = receipt_data["receiptItems"][0]["receiptNumber"]
            return receipt_number
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def reprint_last_receipt(num_prints, receipt_number=None):
    if receipt_number is None:
        receipt_number = get_last_receipt_number()

    reprint_receipt_url = f"http://{SERVER_IP}:8001/ReprintReceipt/"

    try:
        with open("printing_reports.txt", "a") as file:
            response_text = ""
            for i in range(num_prints):
                reprint_url = f"{reprint_receipt_url}{receipt_number}"
                response = requests.post(reprint_url)
                if response.status_code == 200:
                    success_message = f"Successful printed Receipt #{receipt_number} at: ({TIMESTAMP})"
                    response_text += success_message + "\n"
                else:
                    failure_message = f"Print #{i+1}: Failed ({TIMESTAMP})"
                    response_text += failure_message + "\n"

            file.write("---------------------------------------\n")
            file.write(
                f"{num_prints} print(s): {'Successful' if response_text.count('Failed') == 0 else 'Failed'}\n"
            )
            file.write(response_text)

    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Create the argument parser
parser = argparse.ArgumentParser(description="Reprint Last Receipt")

# Add the optional argument for the receipt number
parser.add_argument(
    "--receipt-number",
    type=int,
    dest="receipt_number",
    help="Receipt number to reprint (default: reprint last receipt)",
)

# Add the positional argument for the number of prints
parser.add_argument(
    "num_prints",
    type=int,
    default=NUM_PRINTS,
    help="Number of times to reprint the last receipt (default: value from .env)",
)

# Parse the command-line arguments
args = parser.parse_args()

# Get the number of prints from the parsed arguments or the .env file
num_prints = args.num_prints

# Get the receipt number from the parsed arguments or None
receipt_number_to_print = args.receipt_number

# Call the reprint_last_receipt function with the provided number of prints or the receipt number
try:
    if receipt_number_to_print is not None:
        print(f"Printing receipt number: {receipt_number_to_print}")
        reprint_last_receipt(num_prints, receipt_number_to_print)
    else:
        print("Printing the last receipt")
        reprint_last_receipt(num_prints)
except ValueError as e:
    with open("printing_reports.txt", "a") as file:
        file.write("---------------------------------------\n")
        file.write(f"Error: {e}\n")