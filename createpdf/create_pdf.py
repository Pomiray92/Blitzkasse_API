from fpdf import FPDF
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# CONSTANT VARIABLES
TIMESTAMP = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
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
    # Call the get_last_receipt() and get_client_info functions to retrieve receipt data
    receipt_data = get_receipt_info()
    client_data = get_client_info()
    company_name = client_data.get('companyName')
    company_address = client_data.get('companyAdress')
    company_city = client_data.get('companyCity')
    company_taxId = client_data.get('companyTaxId')
    company_email = client_data.get('companyEmail')
    company_phone = client_data.get('companyPhone')
    get_table = receipt_data.get("levelDetailText")
    id_receipt = receipt_data.get("receiptNumber")
    receipt_items = receipt_data.get("receiptItems", [])
    summ = receipt_data.get("summ")
    paymentMode = receipt_data.get("paymentMode")
    moneyGiven = receipt_data.get("moneyGiven")
    returnMoney = receipt_data.get("returnMoney")
    personnelId = receipt_data.get("personnelId")
    personnelName = receipt_data.get("personnelName")
    receiptsSignature = receipt_data.get("receiptsSignature")
    taxProducts = receipt_data.get("taxProducts")

    get_taxProducts = receipt_data["taxProducts"]

    tax_name_a = []
    tax_name_b = []
    tax_name_c = []

    for tax_product in get_taxProducts:
        if tax_product["totalBrutto"] != 0:
            # Store the information in separate lists based on taxValue
            tax_value = tax_product["taxValue"]
            total_brutto = tax_product["totalBrutto"]
            total_netto = tax_product["totalNetto"]
            total_absolute_tax = tax_product["totalAbsoluteTax"]
            name = tax_product["name"]
            name_and_tax = f"{name}= {tax_value}%"

            if tax_value == 19:
                tax_name_a.append({
                    " ": name_and_tax,
                    "Brutto": total_brutto,
                    "Netto": total_netto,
                    "Steuer": total_absolute_tax
                })
            elif tax_value == 7:
                tax_name_b.append({
                    " ": name_and_tax,
                    "Brutto": total_brutto,
                    "Netto": total_netto,
                    "Steuer": total_absolute_tax
                })
            elif tax_value == 0:
                tax_name_c.append({
                    " ": name_and_tax,
                    "Brutto": total_brutto,
                    "Netto": total_netto,
                    "Steuer": total_absolute_tax
                })
        else:
            # Skip to the next item
            continue
    
    

    if receipt_data is not None and client_data is not None:
        # Create a new PDF instance with custom header and footer
        class MyPDF(FPDF):
            def __init__(
                    self, company_name, company_address, company_city, company_taxId, company_email,
                    company_phone, id_receipt, get_table, receipt_items, summ, paymentMode, moneyGiven,
                    returnMoney, personnelId, personnelName, taxProducts, tax_name_a, tax_name_b, tax_name_c,
                ):

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
                self.summ = summ
                self.paymentMode = paymentMode
                self.moneyGiven = moneyGiven
                self.returnMoney = returnMoney
                self.personnelId = personnelId
                self.personnelIdName = personnelName
                self.taxProducts = taxProducts
                self.tax_name_a = tax_name_a
                self.tax_name_b = tax_name_b
                self.tax_name_c = tax_name_c

            def header(self):
                # Add a custom header to each page
                self.set_font("Arial", "B", 12)
                self.cell(0, 5, self.company_name, 0, 1, "C")
                self.cell(0, 5, self.company_address, 0, 1, "C")
                self.cell(0, 5, self.company_city, 0, 1, "C")
                self.cell(0, 5, self.company_taxId, 0, 1, "C")
                self.cell(0, 5, self.company_email, 0, 1, "C")
                self.cell(0, 5, self.company_phone, 0, 1, "C")
                self.cell(0, 5, f"Rechnung: {self.id_receipt}", 0, 1, "C")
                self.cell(0, 5, f"Tish: {self.get_table}", 0, 1, "C")
                
                self.set_font("Arial", "", 12)
                self.cell(0, 5, "______________________________________", 0, 1, "C")

                for item in self.receipt_items:
                    # Get the count, name, and price of the item
                    item_count = str(item['count'])
                    item_name = item['name']
                    item_price = "{:.2f}".format(item['price'])

                    # Calculate the height of the cell based on the content
                    cell_height = max(self.font_size, 2) * 1.25

                    # Calculate the width of each column
                    count_width = 15
                    name_width = 50
                    price_width = 15

                    # Calculate the remaining width for the item name column
                    name_remaining_width = self.w - (count_width + name_width + price_width)

                    # Calculate the number of lines needed to display the item name
                    name_lines = len(item_name.split("\n"))

                    # Calculate the height of the cell based on the number of lines
                    cell_height = max(cell_height, self.font_size * name_lines)

                   # Calculate the available width for the columns
                    available_width = self.w - self.l_margin - self.r_margin

                    # Set the position for the count column (10% of available width)
                    count_x = self.l_margin + (available_width * 0.25)
                    self.set_x(count_x)
                    self.cell(count_width, cell_height, item_count, ln=0, align="C")

                    # Set the position for the item name column (40% of available width)
                    name_x = count_x + (available_width * 0.05)
                    self.set_x(name_x)
                    self.cell(name_width, cell_height, item_name, ln=0, align="L")

                    # Set the position for the price column (50% of available width)
                    price_x = name_x + (available_width * 0.3)
                    self.set_x(price_x)
                    self.cell(price_width, cell_height, item_price, ln=1, align="R")
                
                self.cell(0, 5, "______________________________________", 0, 1, "C")
                
                self.cell(0, 5, "====================================", 0, 1, "C")

                
                if len(self.tax_name_a) != 0:
                    self.cell(150, 5, f"{tax_name_a}", 0, 1, "C")
                    if len(self.tax_name_b)!= 0:
                        self.cell(150, 5, f"{tax_name_b}", 0, 1, "C")
                    if len(self.tax_name_c)!= 0:
                        self.cell(150, 5, f"{tax_name_c}", 0, 1, "C")
                    

                self.cell(0, 5, "______________________________________", 0, 1, "C")
                self.cell(0, 5, str(self.summ), 0, 1, "C")
                self.cell(0, 5, "====================================", 0, 1, "C")
                
                
                # Set the left and right margins as percentages of the page width
                l_margin_percent = 10  # Adjust the left margin percentage as needed
                r_margin_percent = 90  # Adjust the right margin percentage as needed
                page_width = self.w - self.l_margin - self.r_margin
                l_margin = (page_width * l_margin_percent) / 100
                r_margin = (page_width * r_margin_percent) / 100

                # Define the labels and data as lists
                labels = ["Zahlart:", "Gezahlt:", "Rest:", "Datum:", "Kasse:", "Es bedient Sie:"]
                data = [self.paymentMode, self.moneyGiven, self.returnMoney, TIMESTAMP, self.personnelId, self.personnelIdName]

                # Set the position for the labels and data columns
                self.set_font('Arial', 'B', 10)  # Adjust the font and size as needed
                column_width = page_width * 0.43
                label_x = l_margin
                data_x = l_margin + column_width + 5  # Adjust the spacing between columns as needed

                for i in range(len(labels)):
                    self.set_x(label_x)
                    self.cell(column_width, 5, labels[i], 0, 0, "R")
                    
                    self.set_x(data_x)
                    self.cell(column_width, 5, str(data[i]), 0, 1, "L")
                            
            def footer(self):
                # Add a custom footer to each page
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

        pdf = MyPDF(
                    company_name, company_address, company_city, company_taxId, company_email,
                    company_phone, id_receipt, get_table, receipt_items, summ, paymentMode, moneyGiven,
                    returnMoney, personnelId, personnelName, taxProducts, tax_name_a, tax_name_b, tax_name_c
                )
        pdf.add_page()

        # Set the font and add a header to the PDF
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Vielen Dank", ln=True, align="C")
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, f"TSE Signature: {receiptsSignature}", 0, 1, "C")

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

create_pdf()