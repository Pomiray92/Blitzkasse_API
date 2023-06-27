import pdfkit
from datetime import datetime
from get_api import data_dict
import os

current_datetime = datetime.now()
year = current_datetime.year
month = current_datetime.strftime("%B")
day = current_datetime.day
timestamp = datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
receipt_number = data_dict["BONNUMBER"]


def convert_to_pdf():
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    html_file = r"templates\rendered_template.html"
    directory_path = os.path.join(
        os.getcwd(), "data/pdf_rechnungs", str(year), str(month), str(day)
    )
    # Create the directory if it does not exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Save the PDF file with the current datetime in the filename and store it in the year folder
    file_path = os.path.join(
        directory_path, f"receipt{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    )

    pdfkit.from_file(html_file, file_path, configuration=config)
