import pdfkit
from datetime import datetime
from get_api import data_dict
import os
import json
import secrets
token = secrets.token_urlsafe(16)

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
    file_path = os.path.join(directory_path, f"receipt_N{receipt_number}_{timestamp}token{token}.pdf")

    pdfkit.from_file(html_file, file_path, configuration=config)

    # Get the relative path
    relative_path = os.path.relpath(file_path, start=os.getcwd())

    # Create a dictionary with the receipt number and relative file path
    log_data = {
        f"Receipt_N{receipt_number}": relative_path,
    }

    # Update the log file with the dictionary data
    log_file_path = os.path.join(os.getcwd(), "logs/pdf_creation_log.json")

    # Check if the log file exists
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            existing_data = json.load(log_file)

        # Update the existing data with the new entry
        existing_data.update(log_data)

        with open(log_file_path, "w") as log_file:
            json.dump(existing_data, log_file, indent=4)
    else:
        with open(log_file_path, "w") as log_file:
            json.dump(log_data, log_file, indent=4)


