from fpdf import FPDF
import requests
from datetime import datetime

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
    current_datetime = datetime.now().strftime(f"{'%Y'}-{'%m'}-{'%d'}_{'%H'}-{'%M'}-{'%S'}")
    receipt_data = get_last_receipt()
    if receipt_data is not None:
        pdf = FPDF()
        pdf.add_page()

        # Assuming receipt_data is a dictionary with relevant information
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Receipt Information", ln=True, align="C")

        for key, value in receipt_data.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)

        pdf.output(f"receipt{current_datetime}.pdf")
        print("PDF created successfully.")
    else:
        print("Error: Failed to retrieve receipt information.")

create_pdf()