import requests
from get_api import *
from settings import *

# CONSTANT VARIABLES
DEFAULT_SERVER_IP = "localhost"
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
LAST_RECEIPT_URL = f"http://{SERVER_IP}:8001/getLastReceipt"
TIMESTAMP = datetime.now().strftime("%d.%m.%Y %H:%M")
CURRENT_DATETIME = datetime.now()
YEAR = CURRENT_DATETIME.year
MONTH = CURRENT_DATETIME.strftime("%B")
DAY = CURRENT_DATETIME.day
CLIENT_INFO_URL = f"http://{SERVER_IP}:8001/ConfigComplete"


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
        response = requests.get(CLIENT_INFO_URL)
        if response.status_code == 200:
            # Assuming the response is in JSON format
            client_info = response.json()
            return client_info
        else:
            print("Error: Failed to retrieve receipt information. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", e)

receipt_data = get_receipt_info()
client_data = get_client_info()

receipt_items = receipt_data.get("receiptItems", [])
taxProducts = receipt_data.get("taxProducts")

receipt_items = receipt_data.get("receiptItems", [])


data_dict = {
    'companyName': client_data.get('companyName'),
    'companyAddress': client_data.get('companyAdress'),
    'companyCity': client_data.get('companyCity'),
    'companyTaxId': client_data.get('companyTaxId'),
    'companyEmail': client_data.get('companyEmail'),
    'companyPhone': client_data.get('companyPhone'),
    'levelDetailText': receipt_data.get("levelDetailText"),
    'receiptNumber': receipt_data.get("receiptNumber"),
    'receiptItems': receipt_items,
    'summ': receipt_data.get("summ"),
    'paymentMode': receipt_data.get("paymentMode"),
    'moneyGiven': receipt_data.get("moneyGiven"),
    'returnMoney': receipt_data.get("returnMoney"),
    'personnelId': receipt_data.get("personnelId"),
    'personnelName': receipt_data.get("personnelName"),
    'taxProducts': taxProducts,
    'receiptsSignature': receipt_data.get("receiptsSignature"),    
    'transactionData': receipt_data.get("transactionData"),
    'secureElementSerial': receipt_data.get("secureElementSerial"),
    'secureElementStartTime': receipt_data.get("secureElementStartTime"),
    'secureElementEndTime': receipt_data.get("secureElementEndTime"),
    'secureElementClient': receipt_data.get("secureElementClient"),
    'secureElementLogTime': receipt_data.get("secureElementLogTime"),
    'secureElementPublicKey': receipt_data.get("secureElementPublicKey"),
    'secureElementAlgorithm': receipt_data.get("secureElementAlgorithm"),
    'timestamp': TIMESTAMP
}

#print(data_dict["companyCity"])