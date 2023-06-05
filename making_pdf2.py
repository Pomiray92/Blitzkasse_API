import requests

# Function to retrieve the last receipt data
def get_last_receipt():
    response = requests.get("http://localhost:8001/getLastReceipt")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to send a POST request to print the last receipt
def print_last_receipt():
    response = requests.post("http://localhost:8001/PrintLastReceipt")
    if response.status_code == 200:
        print("Print request sent successfully.")
    else:
        print("Failed to send print request.")

# Function to create the PDF
def create_pdf(receipt_data):
    # Your PDF creation code here
    # Replace the sample_receipt_data with receipt_data in the function

# Get the last receipt data
receipt_data = get_last_receipt()

if receipt_data is not None:
    # Create the PDF using the receipt data
    create_pdf(receipt_data)

    # Optionally, send a print request
    print_last_receipt()
else:
    print("Failed to retrieve last receipt data.")