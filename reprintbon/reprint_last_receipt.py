import requests
from datetime import datetime
import argparse
import os
from dotenv import load_dotenv

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

# Get the server IP from the environment variable or use the default value
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)

# Get the number of prints from the environment variable or use the default value
NUM_PRINTS = int(os.getenv("NUM_PRINTS", DEFAULT_NUM_PRINTS))


def get_last_receipt():
    get_last_receipt_url = f"http://{SERVER_IP}:8001/getLastReceipt"

    # url = os.getenv("LAST_RECEIPT_URL")
    try:
        response = requests.get(get_last_receipt_url)
        if response.status_code == 200:
            receipt_data = response.json()
            receipt_number = receipt_data["receiptItems"][0]["receiptNumber"]
            return receipt_number  # Return the receipt number
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def reprint_last_receipt(num_prints):
    receipt_number = get_last_receipt()
    reprint_receipt_url = f"http://{SERVER_IP}:8001/ReprintLastReceipt/"
    # reprint_receipt_url = os.getenv("REPRINT_LAST_RECEIPT_URL")
    try:
        with open("printing_reports.txt", "a") as file:
            response_text = ""
            for i in range(num_prints):
                response = requests.get(reprint_receipt_url)
                if response.status_code == 200:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    success_message = f"Successful printed Receipt #{receipt_number} at: ({timestamp})"
                    response_text += success_message + "\n"
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    failure_message = f"Print #{i+1}: Failed ({timestamp})"
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

# Add the positional argument for the number of prints
parser.add_argument(
    "num_prints",
    type=int,
    nargs="?",
    default=NUM_PRINTS,
    help="Number of times to reprint the last receipt (default: value from .env)",
)

# Parse the command-line arguments
args = parser.parse_args()

# Get the number of prints from the parsed arguments
num_prints = args.num_prints

# Call the reprint_last_receipt function with the provided number of prints
reprint_last_receipt(num_prints)
