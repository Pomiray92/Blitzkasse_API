import requests

# Function to get the last receipt data
def get_last_receipt():
    last_receipt_url = "http://localhost:8001/getLastReceipt"
    response = requests.get(last_receipt_url)
    if response.status_code == 200:
        last_receipt_data = response.json()
        return last_receipt_data
    else:
        print("Failed to get the last receipt data.")
        return None

# Function to print the last receipt
def print_last_receipt():
    print_receipt_url = "http://localhost:8001/PrintLastReceipt"
    response = requests.post(print_receipt_url)
    if response.status_code == 200:
        print("Last receipt printed successfully!")
    else:
        print("Failed to print last receipt.")

# Manually call the functions
last_receipt_data = get_last_receipt()
if last_receipt_data is not None:
    print_last_receipt()