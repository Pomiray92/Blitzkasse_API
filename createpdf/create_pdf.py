from fpdf import FPDF
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from create_functions import *
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", DEFAULT_SERVER_IP)
LAST_RECEIPT_URL = f"http://{SERVER_IP}:8001/getLastReceipt"

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
    transaction_data = receipt_data.get("transactionData")
    get_taxProducts = receipt_data["taxProducts"]
    secure_element_serial = receipt_data.get("secureElementSerial")
    secure_element_start_time = receipt_data.get("secureElementStartTime")
    secure_element_end_time = receipt_data.get("secureElementEndTime")
    cecure_element_client = receipt_data.get("secureElementClient")
    secure_element_log_time = receipt_data.get("secureElementLogTime")
    secure_element_public_key = receipt_data.get("secureElementPublicKey")
    secure_element_algorithm = receipt_data.get("secureElementAlgorithm")


    tax_data = {}
    if isinstance(get_taxProducts, list):
        for tax_product in get_taxProducts:
            total_brutto = tax_product["totalBrutto"]
            if total_brutto != 0:
                total_netto = tax_product["totalNetto"]
                total_absolute_tax = tax_product["totalAbsoluteTax"]
                name = tax_product["name"]
                tax_value = tax_product["taxValue"]
                name_and_tax = f"{name}= {tax_value}%"

                tax_data[name] = {
                    "MwSt.": name_and_tax,
                    "Brutto": total_brutto,
                    "Netto": total_netto,
                    "Steuer": total_absolute_tax
                }
    else:
        print("Error: get_taxProducts is not a list")
    print(tax_data)

    if receipt_data is not None and client_data is not None:
        # Create a new PDF instance with custom header and footer
        class MyPDF(FPDF):
            def __init__(
                    self, company_name, company_address, company_city, company_taxId, company_email,
                    company_phone, id_receipt, get_table, receipt_items, summ, paymentMode, moneyGiven,
                    returnMoney, personnelId, personnelName, taxProducts,
                    transaction_data, secure_element_serial, secure_element_start_time, secure_element_end_time,
                    cecure_element_client, secure_element_log_time, secure_element_public_key, secure_element_algorithm
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
                self.transaction_data = transaction_data
                self.secure_element_serial = secure_element_serial
                self.secure_element_start_time = secure_element_start_time
                self.secure_element_end_time = secure_element_end_time
                self.cecure_element_client = cecure_element_client
                self.secure_element_log_time = secure_element_log_time
                self.secure_element_public_key = secure_element_public_key
                self.secure_element_algorithm = secure_element_algorithm

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

                
                # Set the column widths
                col_widths = [20, 20, 20, 20]

                # Set the data for the table
                header_row = ["MwSt.", "Brutto", "Netto", "Steuer"]
                data_rows = []

                # Iterate over the tax_data dictionary
                for tax_name, tax_info in tax_data.items():
                    name_and_tax = tax_info["MwSt."]
                    total_brutto = tax_info["Brutto"]
                    total_netto = tax_info["Netto"]
                    total_absolute_tax = tax_info["Steuer"]
                    data_row = [name_and_tax, "{:.2f}".format(total_brutto), "{:.2f}".format(total_netto), "{:.2f}".format(total_absolute_tax)]
                    data_rows.append(data_row)

                # Set the alignment for each column
                alignments = ["C", "C", "C", "C"]
                offset = 50    

                # Calculate the x-coordinate to move the items to the right
                x = self.get_x() + offset

                # Draw the header row
                self.set_x(x)
                for i, header_cell in enumerate(header_row):
                    self.cell(col_widths[i], 10, header_cell, 0, 0, "C")

                self.ln(10)  # Move to the next line

                # Draw the data rows
                self.set_x(x)
                for data_row in data_rows:
                    for i, data_cell in enumerate(data_row):
                        self.cell(col_widths[i], 10, str(data_cell), 0, 0, alignments[i])

                    self.ln(10)  # Move to the next line
                    

                self.cell(0, 5, "______________________________________", 0, 1, "C")
                self.set_font("Arial", "B", 10)
                self.cell(0, 5, f"GESAMT: {str(self.summ)}", 0, 1, "C")
                self.set_font("Arial", "", 12)
                self.cell(0, 5, "====================================", 0, 1, "C")
                
                
                # Set the left and right margins as percentages of the page width
                l_margin_percent = 10  # Adjust the left margin percentage as needed
                r_margin_percent = 90  # Adjust the right margin percentage as needed
                page_width = self.w - self.l_margin - self.r_margin
                l_margin = (page_width * l_margin_percent) / 100
                r_margin = (page_width * r_margin_percent) / 100

                # Define the labels and data as lists
                labels = ["Zahlart:", "Gezahlt:", "Rückgabe:", "Datum:", "Kasse:", "Es bedient Sie:"]
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
                    returnMoney, personnelId, personnelName, taxProducts,
                    transaction_data, secure_element_serial, secure_element_start_time, secure_element_end_time,
                    cecure_element_client, secure_element_log_time, secure_element_public_key, secure_element_algorithm
                )
        pdf.add_page()
    

        start_time = datetime.now()
        stop_time = start_time + timedelta(seconds=2)

        # Set the font and add a header to the PDF
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Vielen Dank", ln=True, align="C")
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, f"TSE Signature: {receiptsSignature}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Transaktion: {transaction_data}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Start: {start_time.strftime('%d.%m.%Y-%H:%M:%S')}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Stop:  {stop_time.strftime('%d.%m.%Y-%H:%M:%S')}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Serialnummer: {secure_element_serial}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Sigantureaccount: {cecure_element_client}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Zeitformat: {secure_element_log_time}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE Publickey: {secure_element_public_key}", 0, 1, "C")
        pdf.cell(0, 5, f"TSE HashAlgorithm: {secure_element_algorithm}", 0, 1, "C")
        # Add spacing after the header
        pdf.ln(10)

        # Set the font and size for the content
        pdf.set_font("Arial", size=12)

        # Set the directory path to store the PDF
        directory_path = os.path.join(os.getcwd(), "data/pdf_rechnungs", str(YEAR), str(MONTH), str(DAY))

        # Create the directory if it does not exist
        os.makedirs(directory_path, exist_ok=True)

        # Save the PDF file with the current datetime in the filename and store it in the year folder
        file_path = os.path.join(directory_path, f"receipt{datetime.now().strftime('%d.%m.%Y-%H_%M_%S')}.pdf")

        # Output the PDF
        pdf.output(file_path)
        print("PDF created successfully.")
    else:
        print("Error: Failed to retrieve receipt information.")

create_pdf()
create_default_readme_file()