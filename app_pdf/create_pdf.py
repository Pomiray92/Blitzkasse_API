import pdfkit
from datetime import datetime
from get_api import data_dict
import os

def convert_to_pdf():
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.strftime("%B")
    day = current_datetime.day
    timestamp = current_datetime.strftime("%d.%m.%Y_%H-%M-%S")
    receipt_number = data_dict["BONNUMBER"]

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    html_file = r"templates\rendered_template.html"
    directory_path = os.path.join(os.getcwd(), "data", "pdf_rechnungs", str(year), str(month), str(day))

    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    # Save the PDF file with the current datetime in the filename and store it in the year folder
    file_path = os.path.join(directory_path, f"receipt_N{receipt_number}_{timestamp}.pdf")

    pdfkit.from_file(html_file, file_path, configuration=config)
