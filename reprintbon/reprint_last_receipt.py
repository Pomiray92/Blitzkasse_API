import requests
from datetime import datetime
import argparse

def get_last_receipt():
    url = "http://localhost:8001/getLastReceipt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            receipt_data = response.json()
            receipt_number = receipt_data['receiptItems'][0]['receiptNumber']
            return receipt_number  # Return the receipt number
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def reprint_last_receipt(num_prints):
    receipt_number = get_last_receipt()
    # print(receipt_number)
    reprint_receipt_url = "http://localhost:8001/ReprintLastReceipt/"
    try:
        with open("printing_reports.txt", "a") as file:
            response_text = ""
            for i in range(num_prints):
                response = requests.get(reprint_receipt_url)
                if response.status_code == 200:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    response_text += f"Successful printed Receipt #{receipt_number} at:({timestamp})\n"
                    # print(f"Last receipt {receipt_number}: #{i+1} printed successfully!")
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    response_text += f"Print #{i+1}: Failed ({timestamp})\n"
                    # print(f"Failed to print last receipt #{i+1}. Status Code:", response.status_code)
            
            file.write(f"---------------------------------------\n")
            file.write(f"{num_prints} print(s): {'Successful' if response_text.count('Failed') == 0 else 'Failed'}\n")
            file.write(response_text)
            
            
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Create the argument parser
parser = argparse.ArgumentParser(description='Reprint Last Receipt')

# Add the positional argument for the number of prints
parser.add_argument('num_prints', type=int, nargs='?', default=1, help='Number of times to reprint the last receipt')

# Parse the command-line arguments
args = parser.parse_args()

# Get the number of prints from the parsed arguments
num_prints = args.num_prints

# Call the reprint_last_receipt function with the provided number of prints
reprint_last_receipt(num_prints)