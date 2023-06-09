from fpdf import FPDF
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# CONSTANT VARIABLES
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CURRENT_DATETIME = datetime.now()
YEAR = CURRENT_DATETIME.year
MONTH = CURRENT_DATETIME.strftime("%B")
DAY = CURRENT_DATETIME.day
DEFAULT_SERVER_IP = "localhost"

# Create a default settings.env file
if not os.path.isfile("settings.env"):
    with open("settings.env", "w") as env_file:
        env_file.write(f"SERVER_IP={DEFAULT_SERVER_IP}\n")

SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
LAST_RECEIPT_URL = f"http://{SERVER_IP}:8001/getLastReceipt"
CLIENT_INFO_URL = f"http://{SERVER_IP}:8001/ConfigComplete"

# Create a default README.txt file
if not os.path.isfile("README.txt"):
    with open("README.txt", "w") as file:
        file.write("---------------------------------------\n")
        file.write("APP for creating pdf from retrieve receipt Information:\n")
        file.write("\n")
        file.write("This app allows you to create a PDF from retrieve receipt data, store it or send via email.\n")
        file.write(".\n")
        file.write("\n")

# Validate the server IP
try:
    requests.get(f"http://{SERVER_IP}:8001")
    if DEFAULT_SERVER_IP == True:
        print(f"Using default server IP: {SERVER_IP}")
except requests.exceptions.RequestException:
    print(f"Error: Invalid value for 'SERVER_IP' in the .env file. Please provide a correct SERVER_IP address. ({TIMESTAMP})")
    exit(1)

def get_receipt_info():
    try:
        response = requests.get(LAST_RECEIPT_URL)
        if response.status_code == 200:
            receipt_data = response.json()
            category_names = []
            for item in receipt_data.get("receiptItems", []):
                item_name = f"{item['name']} {item['count']}x {item['price']:.2f}"
                if item_name not in category_names:
                    category_names.append(item_name)
                else:
                    # Update the cost and quantity for existing item
                    existing_item_index = category_names.index(item_name)
                    existing_item = category_names[existing_item_index]
                    quantity = int(existing_item.split(" ")[-2][:-1]) + item["count"]
                    cost = float(existing_item.split(" ")[-1].replace(",", ".")) + (item["count"] * item["price"])
                    category_names[existing_item_index] = f"{item['name']} {quantity}x {cost:.2f}"
            
            #print(category_names)
            
            # receipt_number = receipt_data.get('receiptItems', [{}])[0].get('receiptNumber')
            # paymentOrderNumber = receipt_data.get('receiptItems', [{}])[0].get('paymentOrderNumber')
            # userName = receipt_data.get('receiptItems', [{}])[0].get('userName')

            # print("User Name:", userName)
            # print("Payment Order Number:", paymentOrderNumber)
            # print("Receipt Number:", receipt_number)
            # print("-----------------------------\n")
            #print("Last receipt data:", receipt_data)
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def get_client_info():
    try:
        response_client_info = requests.get(CLIENT_INFO_URL)
        if response_client_info.status_code == 200:
            # Assuming the response is in JSON format
            client_info = response_client_info.json()
            return client_info
        else:
            print("Error: Failed to retrieve receipt information. Status code:", response_client_info.status_code)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", e)

    return response_client_info

def create_pdf():
    # Call the get_last_receipt() function to retrieve receipt data
    receipt_data = get_receipt_info()
    client_data = get_client_info()
    company_name = client_data.get('companyName')
    company_address = client_data.get('companyAdress')
    company_city = client_data.get('companyCity')
    company_taxId = client_data.get('companyTaxId')
    company_email = client_data.get('companyEmail')
    company_phone = client_data.get('companyPhone')

    if receipt_data is not None and client_data is not None:
        # Create a new PDF instance with custom header and footer
        class MyPDF(FPDF):
            def __init__(self, category_names):
                super().__init__()
                self.category_names = category_names

            def header(self):
                # Add a custom header to each page
                self.set_font("Arial", "B", 8)
                self.cell(0, 5, company_name, 0, 1, "C")
                self.cell(0, 5, company_address, 0, 1, "C")
                self.cell(0, 5, company_city, 0, 1, "C")
                self.cell(0, 5, company_taxId, 0, 1, "C")
                self.cell(0, 5, company_email, 0, 1, "C")
                self.cell(0, 5, company_phone, 0, 1, "C")
                self.cell(0, 5, "------------------------------", 0, 1, "C")
                for category_name in self.category_names:
                    self.cell(0, 5, category_name, 0, 1, "C")

            def footer(self):
                # Add a custom footer to each page
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
                self.cell(0, 10, f"Page dsfsdfds", 0, 0, "C")
        
        # Retrieve category names from receipt data
        category_names = []
        for item in receipt_data["receiptItems"]:
            item_name = f"{item['name']} {item['count']}x {item['price']:.2f}"
            if item_name not in category_names:
                category_names.append(item_name)
            else:
                # Update the cost and quantity for existing item
                existing_item_index = category_names.index(item_name)
                existing_item = category_names[existing_item_index]
                quantity = int(existing_item.split(" ")[-2][:-1]) + item["count"]
                cost = float(existing_item.split(" ")[-1].replace(",", ".")) + (item["count"] * item["price"])
                category_names[existing_item_index] = f"{item['name']} {quantity}x {cost:.2f}"
        
        pdf = MyPDF(category_names)
        pdf.add_page()

        # Set the font and add a header to the PDF
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Receipt Information", ln=True, align="C")

        # Add spacing after the header
        pdf.ln(10)

        # Set the font and size for the content
        pdf.set_font("Arial", size=12)

        # Set the directory path to store the PDF
        directory_path = os.path.join(os.getcwd(), "data/pdf_rechnungs", str(YEAR), str(MONTH), str(DAY))

        # Create the directory if it does not exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Save the PDF file with the current datetime in the filename and store it in the year folder
        file_path = os.path.join(directory_path, f"receipt{TIMESTAMP}.pdf")
        pdf.output(file_path)
        print("PDF created successfully.")
    else:
        print("Error: Failed to retrieve receipt information.")

# Call the create_pdf() function to generate the PDF
create_pdf()
