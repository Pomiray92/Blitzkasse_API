import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests


DEFAULT_SERVER_IP = "localhost"
LAST_RECEIPT_URL = "http://{SERVER_IP}:8001/getLastReceipt"
CLIENT_INFO_URL = "http://{SERVER_IP}:8001/ConfigComplete"


def get_receipt_info(server_ip: str) -> Optional[Dict]:
    url = LAST_RECEIPT_URL.format(SERVER_IP=server_ip)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            receipt_data = response.json()
            return receipt_data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None


def get_client_info(server_ip: str) -> Optional[Dict]:
    url = CLIENT_INFO_URL.format(SERVER_IP=server_ip)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            client_info = response.json()
            return client_info
        else:
            print(
                "Error: Failed to retrieve receipt information. Status code:",
                response.status_code,
            )
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", e)
    return None


def format_price(price: float) -> str:
    return "{:,.2f}".format(price)


def consolidate_items(receipt_items: List[Dict]) -> Dict[str, Dict]:
    consolidated_items = {}
    for item in receipt_items:
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
    return consolidated_items


def calculate_total_price(items: Dict[str, Dict]) -> float:
    return sum(item_data["price"] for item_data in items.values())


def prepare_data_dict(receipt_data: Dict, client_data: Dict, timestamp: str) -> Dict:
    receipt_items = receipt_data.get("receiptItems", [])
    taxProducts = receipt_data.get("taxProducts")

    secure_element_start_time = receipt_data.get("secureElementStartTime", "0")
    secure_element_end_time = receipt_data.get("secureElementEndTime", "0")

    start_timestamp = datetime.strptime(timestamp, "%d.%m.%Y %H:%M:%S")
    secure_element_start_time = (
        datetime.now()
        if secure_element_start_time in ["0", 0]
        else datetime.strptime(secure_element_start_time, "%d.%m.%Y %H:%M:%S")
    )
    secure_element_end_time = (
        start_timestamp + timedelta(seconds=2)
        if secure_element_end_time in ["0", 0]
        else datetime.strptime(secure_element_end_time, "%d.%m.%Y %H:%M:%S")
    )

    consolidated_items = consolidate_items(receipt_items)
    total_price = calculate_total_price(consolidated_items)

    formatted_total_price = format_price(total_price)
    formatted_summ = format_price(receipt_data.get("summ", 0))

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
        "DATE": timestamp,
        "formattedTotalPrice": formatted_total_price,
        "TOTALSUMM": formatted_summ,
        "consolidated_items": consolidated_items,
    }

    return data_dict



def get_data_dict(server_ip: str, timestamp: str) -> Dict:
    receipt_data = get_receipt_info(server_ip)
    client_data = get_client_info(server_ip)

    if receipt_data and client_data:
        return prepare_data_dict(receipt_data, client_data, timestamp)
    return {}

server_ip = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
data_dict = get_data_dict(server_ip, timestamp)