import requests
import pdb


def get_last_receipt():
    last_receipt_url = "http://localhost:8001/getLastReceipt"

    try:
        response = requests.get(last_receipt_url)
        if response.status_code == 200:
            receipt_data = response.json()

            # Store the receipt data as per your requirements
            # Example: save it to a file, database, or variable
            # ...
            # print(receipt_data)
            receipt_number = receipt_data["receiptItems"][0]["receiptNumber"]
            paymentOrderNumber = receipt_data["receiptItems"][0]["paymentOrderNumber"]
            userName = receipt_data["receiptItems"][0]["userName"]
            country = receipt_data["taxProducts"][0]["country"]
            print("country:", country)
            print("User Name:", userName)
            print("Payment Order Number:", paymentOrderNumber)
            print("Receipt Number:", receipt_number)
            print("-----------------------------\n")
            print("Last receipt data:", receipt_data)
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


get_last_receipt()
