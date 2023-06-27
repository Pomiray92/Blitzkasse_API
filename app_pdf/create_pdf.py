import pdfkit
from datetime import datetime
from get_api import data_dict

timestamp = datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
receipt_number = data_dict["BONNUMBER"]

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

html_file = r'C:\Users\POS\Desktop\somon\Blitzkasse_API\app_pdf\templates\rendered_template.html'
pdf_file = rf'C:\Users\POS\Desktop\somon\Blitzkasse_API\app_pdf\data_pdf\Rechnung_N_{receipt_number}_{timestamp}.pdf'

pdfkit.from_file(html_file, pdf_file, configuration=config)