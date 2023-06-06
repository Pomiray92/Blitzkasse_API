import requests

def reprint_last_receipt():
    reprint_receipt_url = "http://localhost:8001/ReprintLastReceipt/"
    try:
        response = requests.get(reprint_receipt_url)
        if response.status_code == 200:
            print("Last receipt printed successfully!")
        else:
            print("Failed to print last receipt. Status Code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Call the reprint_last_receipt() function
reprint_last_receipt()