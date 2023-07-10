import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pdb

load_dotenv("settings.env")

# CONSTANT VARIABLES
DEFAULT_SERVER_IP = "localhost"
SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
ZABSCHLAG_URL = f"http://{SERVER_IP}:8001/GetAllZAbschlag"
TIMESTAMP = datetime.now().strftime("%d.%m.%Y %H:%M:%S")



def get_zabschlag():
    try:
        response = requests.get(ZABSCHLAG_URL)
        if response.status_code == 200:
            receipt_data = response.json()
            #breakpoint()
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


receipt_data = get_zabschlag()
entries = receipt_data[0]["entries"]
userEntries = receipt_data[0]["userEntries"]
categoryEntries = receipt_data[0]["categoryEntries"]
pulls = receipt_data[0]["pulls"]



data_dict = {
    "companyName" : receipt_data[0]["companyName"],
    "companyAdress" : receipt_data[0]["companyAdress"],
    "companyZip" : receipt_data[0]["companyZip"],
    "companyCity" : receipt_data[0]["companyCity"],
    "companyPhone" : receipt_data[0]["companyPhone"],
    "companyOwner" : receipt_data[0]["companyOwner"],
    "companyEmail" : receipt_data[0]["companyEmail"],
    "companyTurnTaxId" : receipt_data[0]["companyTurnTaxId"],
    "startDate" : receipt_data[0]["startDate"],
    "endDate" : receipt_data[0]["endDate"],
    "returnIndex" : receipt_data[0]["returnIndex"],

    "taxValue_7": entries[0]["taxValue"],
    "taxTotal_7" : entries[0]["taxTotal"],
    "withTaxSum_7": entries[0]["withTaxSum"],
    "withoutTax_7" : entries[0]["withoutTax"],
    "taxValue_19": entries[1]["taxValue"],
    "taxTotal_19" : entries[1]["taxTotal"],
    "withTaxSum_19": entries[1]["withTaxSum"],
    "withoutTax_19" : entries[1]["withoutTax"],
    "categoryName_tageskarte": categoryEntries[0]["categoryName"],
    "categorySum_tageskarte" : categoryEntries[0]["categorySum"],
    "categoryName_A-frei": categoryEntries[1]["categoryName"],
    "categorySum_A-frei" : categoryEntries[1]["categorySum"],

}

#breakpoint()
