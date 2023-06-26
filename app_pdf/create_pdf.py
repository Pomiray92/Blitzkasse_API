import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

html_file = r'C:\Users\POS\Desktop\somon\Blitzkasse_API\app_pdf\templates\rendered_template.html'
pdf_file = r'C:\Users\POS\Desktop\somon\Blitzkasse_API\app_pdf\file.pdf'

pdfkit.from_file(html_file, pdf_file, configuration=config)