# Blitzkasse_API

* Overall, the app retrieves the last receipt information from a specific endpoint, generates a PDF receipt using the retrieved data, and saves the PDF in a directory structure based on the year, month, and day.

* The app performs the following tasks:

    -  Imports necessary modules such as FPDF for PDF generation, requests for making HTTP requests, and datetime for handling date and time.

    -  Defines a function named get_last_receipt that sends an HTTP GET request to localhost:8001/getLastReceipt to retrieve the last receipt information. It handles potential errors and returns the receipt information in JSON format.

    -  Defines a function named create_pdf that generates a PDF receipt using the receipt information obtained from get_last_receipt.

    - Within create_pdf, it gets the current date and time using datetime.now() and extracts the year, month, and day.
    - It creates a new FPDF instance and adds a page to it.
    - It sets the font and adds a header to the PDF.
    - It iterates over the receipt data, adding key-value pairs to the PDF.
    - It defines a directory path for storing the PDF based on the current working directory, including a "data" folder and subfolders for year, month, and day.
    - It checks if the directory path exists and creates it if it doesn't.
    - It saves the PDF file with a filename based on the current datetime and stores it in the appropriate directory.
    - It prints a success message if the PDF is created successfully, or an error message if there was a problem retrieving the receipt information.
    - Calls the create_pdf function to generate the PDF receipt.