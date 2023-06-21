import requests
from get_api import *
from settings import *
from datetime import datetime, timedelta

# CONSTANT VARIABLES
DEFAULT_SERVER_IP = "localhost"
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
LAST_RECEIPT_URL = f"http://{SERVER_IP}:8001/getLastReceipt"
TIMESTAMP = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
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
secure_element_start_time = receipt_data.get("secureElementStartTime")  # Convert to string
secure_element_end_time = receipt_data.get("secureElementEndTime")
start_timestamp = datetime.strptime(TIMESTAMP, "%d.%m.%Y %H:%M:%S")

if secure_element_start_time in ["0", 0]:
    secure_element_start_time = datetime.now()
else:
    secure_element_start_time = datetime.strptime(secure_element_start_time, "%d.%m.%Y %H:%M:%S")

if secure_element_end_time in ["0", 0]:
    secure_element_end_time = start_timestamp + timedelta(seconds=2)
else:
    secure_element_end_time = datetime.strptime(secure_element_end_time, "%d.%m.%Y %H:%M:%S")


data_dict = {
    'secureElementStartTime': secure_element_start_time,
    'secureElementEndTime': secure_element_end_time,
    'CUSTOMERNAME': client_data.get('companyName'),
    'CUSTOMERSTREET': client_data.get('companyAdress'),
    'CUSTOMERCITY': client_data.get('companyCity'),
    'companyTaxId': client_data.get('companyTaxId'),
    'CUSTOMEREMAIL': client_data.get('companyEmail'),
    'CUSTOMERNUMBER': client_data.get('companyPhone'),
    'TABLENUMBER': receipt_data.get("levelDetailText"),
    'BONNUMBER': receipt_data.get("receiptNumber"),
    'receiptItems': receipt_items,
    'summ': receipt_data.get('summ'),
    'PAYMENTTYPE': receipt_data.get("paymentMode"),
    'GIVEMONEY': receipt_data.get("moneyGiven"),
    'BACKMONEY': receipt_data.get("returnMoney"),
    'DEVICEID': receipt_data.get("personnelId"),
    'USERNAME': receipt_data.get("personnelName"),
    'taxProducts': taxProducts,
    'receiptsSignature': receipt_data.get("receiptsSignature"),    
    'transactionData': receipt_data.get("transactionData"),
    'secureElementSerial': receipt_data.get("secureElementSerial"),
    'secureElementClient': receipt_data.get("secureElementClient"),
    'secureElementLogTime': receipt_data.get("secureElementLogTime"),
    'secureElementPublicKey': receipt_data.get("secureElementPublicKey"),
    'secureElementAlgorithm': receipt_data.get("secureElementAlgorithm"),
    'DATE': TIMESTAMP
}

consolidated_items = {}
    
    # Calculate the quantities and prices for the consolidated items
for item in data_dict['receiptItems']:
    item_name = item['name']
    item_price = item['price']
    item_count = item['count']
    item_total_price = item_price * item_count

    if item_name in consolidated_items:
        consolidated_items[item_name]['count'] += item_count
        consolidated_items[item_name]['price'] += item_total_price
    else:
        consolidated_items[item_name] = {'count': item_count, 'price': item_total_price}

# Update the data_dict with consolidated items
data_dict['consolidatedItems'] = consolidated_items

# Format the prices with commas and two decimal places for each item
for item_data in consolidated_items.values():
    item_data['formatted_price'] = '{:,.2f}'.format(item_data['price'] / item_data['count'])
    item_data['formatted_last_price'] = '{:,.2f}'.format(item_data['price'])

# Calculate the sum of prices for all items
total_price = sum(item_data['price'] for item_data in consolidated_items.values())

# Format the total price with commas and two decimal places
formatted_total_price = '{:,.2f}'.format(total_price)


# Add the total price and formated_summ to the data_dict
data_dict['formattedTotalPrice'] = formatted_total_price
data_dict["TOTALSUMM"] = '{:,.2f}'.format(data_dict['summ'])

print(data_dict)
