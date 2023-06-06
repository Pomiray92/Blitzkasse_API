from fpdf import FPDF
import requests
from datetime import datetime
import os

def get_last_receipt():
    url = "http://localhost:8001/getLastReceipt"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Assuming the response is in JSON format
            receipt_info = response.json()
            return receipt_info
        else:
            print("Error: Failed to retrieve receipt information. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", e)
    
    return None

def create_pdf():
    # Get the current datetime year month(str) and day
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.strftime("%B")
    day = current_datetime.day

    # Call the get_last_receipt() function to retrieve receipt data
    receipt_data = get_last_receipt()

    if receipt_data is not None:
        # Create a new PDF instance
        pdf = FPDF()
        pdf.add_page()

        # Set the font and add a header to the PDF
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Receipt Information", ln=True, align="C")

        # Iterate over the receipt_data dictionary and add key-value pairs to the PDF
        for key, value in receipt_data.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)

        # Set the directory path to store the PDF
        directory_path = os.path.join(os.getcwd(), "data/pdf_rechnungs", str(year), str(month), str(day))

        # Create the directory if it does not exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Save the PDF file with the current datetime in the filename and store it in the year folder
        file_path = os.path.join(directory_path, f"receipt{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.pdf")
        pdf.output(file_path)
        print("PDF created successfully.")
    else:
        print("Error: Failed to retrieve receipt information.")

# Call the create_pdf() function to generate the PDF
create_pdf()
