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
            #print(receipt_data)
            receipt_number = receipt_data['receiptItems'][0]['receiptNumber']
            receipt_number
            #print("Receipt Number:", receipt_number)
            #print("-----------------------------\n")
            #print("Last receipt data:", receipt_data)
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


