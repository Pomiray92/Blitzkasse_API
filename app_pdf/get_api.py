import requests
from datetime import datetime, timedelta
import os

# CONSTANT VARIABLES
DEFAULT_SERVER_IP = "localhost"
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
LAST_RECEIPT_URL = f"http://{SERVER_IP}:8001/getLastReceipt"
TIMESTAMP = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
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
            print(
                "Error: Failed to retrieve receipt information. Status code:",
                response.status_code,
            )
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", e)


receipt_data = get_receipt_info()
client_data = get_client_info()

receipt_items = receipt_data.get("receiptItems", [])
taxProducts = receipt_data.get("taxProducts")

secure_element_start_time = receipt_data.get("secureElementStartTime", "0")
secure_element_end_time = receipt_data.get("secureElementEndTime", "0")

start_timestamp = datetime.strptime(TIMESTAMP, "%d.%m.%Y %H:%M:%S")
secure_element_start_time = (
    datetime.now() if secure_element_start_time in ["0", 0] else datetime.strptime(secure_element_start_time, "%d.%m.%Y %H:%M:%S")
)
secure_element_end_time = (
    start_timestamp + timedelta(seconds=2) if secure_element_end_time in ["0", 0] else datetime.strptime(secure_element_end_time, "%d.%m.%Y %H:%M:%S")
)

data_dict = {
    "secureElementStartTime": secure_element_start_time,
    "secureElementEndTime": secure_element_end_time,
    "CUSTOMERNAME": client_data.get("companyName"),
    "CUSTOMERSTREET": client_data.get("companyAddress"),
    "CUSTOMERCITY": client_data.get("companyCity"),
    "companyTaxId": client_data.get("companyTaxId"),
    "CUSTOMEREMAIL": client_data.get("companyEmail"),
    "CUSTOMERNUMBER": client_data.get("companyPhone"),
    "TABLENUMBER": receipt_data.get("levelDetailText"),
    "BONNUMBER": receipt_data.get("receiptNumber"),
    "receiptItems": receipt_items,
    "summ": receipt_data.get("summ"),
    "PAYMENTTYPE": receipt_data.get("paymentMode"),
    "GIVEMONEY": receipt_data.get("moneyGiven"),
    "BACKMONEY": receipt_data.get("returnMoney"),
    "DEVICEID": receipt_data.get("personnelId"),
    "USERNAME": receipt_data.get("personnelName"),
    "taxProducts": taxProducts,
    "receiptsSignature": receipt_data.get("receiptsSignature"),
    "transactionData": receipt_data.get("transactionData"),
    "secureElementSerial": receipt_data.get("secureElementSerial"),
    "secureElementClient": receipt_data.get("secureElementClient"),
    "secureElementLogTime": receipt_data.get("secureElementLogTime"),
    "secureElementPublicKey": receipt_data.get("secureElementPublicKey"),
    "secureElementAlgorithm": receipt_data.get("secureElementAlgorithm"),
    "DATE": TIMESTAMP,
}

consolidated_items = {}

for item in data_dict["receiptItems"]:
    item_id = item["productId"]
    item_name = item["name"]
    item_price = item["price"]
    item_count = item["count"]
    item_total_price = item_price * item_count

    if item_id in consolidated_items:
        consolidated_items[item_id]["count"] += item_count
        consolidated_items[item_id]["price"] += item_total_price
    else:
        consolidated_items[item_id] = {
            "count": item_count,
            "price": item_total_price,
            "name": item_name,
        }

# Format the prices with commas and two decimal places for each item
for item_data in consolidated_items.values():
    item_data["formatted_price"] = "{:,.2f}".format(
        item_data["price"] / item_data["count"]
    )
    item_data["formatted_last_price"] = "{:,.2f}".format(item_data["price"])

# Calculate the sum of prices for all items
total_price = sum(item_data["price"] for item_data in consolidated_items.values())

# Format the total price with commas and two decimal places
formatted_total_price = "{:,.2f}".format(total_price)

# Add the total price, formatted_summ and consolidated_items to the data_dict
data_dict["formattedTotalPrice"] = formatted_total_price
data_dict["TOTALSUMM"] = "{:,.2f}".format(data_dict["summ"])
data_dict["consolidated_items"] = consolidated_items