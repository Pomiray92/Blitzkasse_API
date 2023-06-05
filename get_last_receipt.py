import requests

def get_last_receipt():
    url = "http://localhost:8001/getLastReceipt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            receipt_data = response.json()
            # Store the receipt data as per your requirements
            # Example: save it to a file, database, or variable
            # ...
            print("Last receipt data:", receipt_data)
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Call the function to retrieve and store the last receipt
get_last_receipt()

