from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def create_pdf(receipt_data):
    # Create a new PDF file with current date and time in the name
    current_datetime = datetime.now().strftime(f"{'%Y'}-{'%m'}-{'%d'}_{'%H'}-{'%M'}-{'%S'}")
    pdf_file = f"receipt_{current_datetime}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)


    # Write the receipt details to the PDF
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "Receipt Details:")
    c.drawString(100, 680, f"Receipt Number: {receipt_data.get('receiptNumber', '')}")
    c.drawString(100, 660, f"Date: {receipt_data.get('stringDate', '')}")
    c.drawString(100, 640, f"Sum: {receipt_data.get('summ', '')}")
    c.drawString(100, 620, f"Paid: {receipt_data.get('paid', '')}")
    c.drawString(100, 600, f"Personnel ID: {receipt_data.get('personnelId', '')}")
    c.drawString(100, 580, f"Personnel Name: {receipt_data.get('personnelName', '')}")
    c.drawString(100, 560, f"Payment Orders Number: {receipt_data.get('paymentOrdersNumber', '')}")
    c.drawString(100, 540, f"Shipping Address: {receipt_data.get('shippingAdress', '')}")
    c.drawString(100, 520, f"Order Mode: {receipt_data.get('orderMode', '')}")
    c.drawString(100, 500, f"Return Money: {receipt_data.get('returnMoney', '')}")
    c.drawString(100, 480, f"Tipping Money: {receipt_data.get('tippingMoney', '')}")
    c.drawString(100, 460, f"Input Money: {receipt_data.get('inputMoney', '')}")
    c.drawString(100, 440, f"Output Money: {receipt_data.get('outputMoney', '')}")
    c.drawString(100, 420, f"Comment: {receipt_data.get('comment', '')}")
    c.drawString(100, 400, f"Device ID: {receipt_data.get('deviceId', '')}")
    c.drawString(100, 380, f"Receipts Signature: {receipt_data.get('receiptsSignature', '')}")

    # Write the receipt items to the PDF
    c.drawString(100, 340, "Receipt Items:")
    y = 320  # Initial y-coordinate for receipt items
    for item in receipt_data.get('receiptItems', []):
        item_name = item.get('name', '')
        item_count = item.get('count', '')
        item_price = item.get('price', '')
        c.drawString(120, y, f"{item_name} - {item_count}x")
        c.drawString(220, y, f"${item_price:.2f}")
        y -= 20

    # Write the tax products to the PDF
    if 'taxProducts' in receipt_data:
        c.drawString(100, 260, "Tax Products:")
        y = 240  # Initial y-coordinate for tax products
        for tax_product in receipt_data['taxProducts']:
            product_name = tax_product.get('name', '')
            total_brutto = tax_product.get('totalBrutto', '')
            total_netto = tax_product.get('totalNetto', '')
            total_tax = tax_product.get('totalAbsoluteTax', '')
            c.drawString(120, y, f"{product_name}")
            c.drawString(220, y, f"Total Brutto: {total_brutto:.2f}")
            c.drawString(220, y - 20, f"Total Netto: {total_netto:.2f}")
            c.drawString(220, y - 40, f"Total Tax: {total_tax:.2f}")
            y -= 60

    # Save and close the PDF
    c.save()
    print(f"Receipt PDF created: {pdf_file}")

# Sample receipt data
sample_receipt_data = {
    "receiptNumber": "123456",
    "stringDate": "2023-06-01",
    "summ": 200.0,
    "paid": 200.0,
    "receiptItems": [
        {
            "name": "Item 1",
            "count": 2,
            "price": 50.0
        },
        {
            "name": "Item 2",
            "count": 1,
            "price": 100.0
        }
    ]
}

# Generate PDF
create_pdf(sample_receipt_data)