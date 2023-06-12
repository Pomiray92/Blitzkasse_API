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
    get_table = receipt_data["levelDetailText"]
    id_receipt = receipt_data["receiptNumber"]
    receipt_items = receipt_data.get("receiptItems", [])

    if receipt_data is not None and client_data is not None:
        # Create a new PDF instance with custom header and footer
        class MyPDF(FPDF):
            def __init__(self, company_name, company_address, company_city, company_taxId, company_email,
                         company_phone, id_receipt, get_table, receipt_items, ):
                super().__init__()
                self.company_name = company_name
                self.company_address = company_address
                self.company_city = company_city
                self.company_taxId = company_taxId
                self.company_email = company_email
                self.company_phone = company_phone
                self.id_receipt = id_receipt
                self.get_table = get_table
                self.receipt_items = receipt_items

            def header(self):
                # Add a custom header to each page
                self.set_font("Arial", "B", 8)
                self.cell(0, 5, self.company_name, 0, 1, "C")
                self.cell(0, 5, self.company_address, 0, 1, "C")
                self.cell(0, 5, self.company_city, 0, 1, "C")
                self.cell(0, 5, self.company_taxId, 0, 1, "C")
                self.cell(0, 5, self.company_email, 0, 1, "C")
                self.cell(0, 5, self.company_phone, 0, 1, "C")
                self.cell(0, 5, f"Rechnung: {self.id_receipt}", 0, 1, "C")
                self.cell(0, 5, f"Tish: {self.get_table}", 0, 1, "C")
                self.cell(0, 5, "------------------------------", 0, 1, "C")
                for item in self.receipt_items:
                    item_name = f"{item['name']} {item['count']}x {item['price']:.2f}"
                    self.cell(0, 5, item_name, 0, 1, "C")
                self.cell(0, 5, "______________________________", 0, 1, "C")

            def footer(self):
                # Add a custom footer to each page
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

        pdf = MyPDF(company_name, company_address, company_city, company_taxId, company_email, company_phone,
                    id_receipt, get_table, receipt_items)
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
        os.makedirs(directory_path, exist_ok=True)

        # Save the PDF file with the current datetime in the filename and store it in the year folder
        file_path = os.path.join(directory_path, f"receipt{TIMESTAMP}.pdf")

        # Output the PDF
        pdf.output(file_path)
        print("PDF created successfully.")
    else:
        print("Error: Failed to retrieve receipt information.")

# Call the create_pdf() function to generate the PDF
create_pdf()