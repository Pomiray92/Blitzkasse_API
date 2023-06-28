import qrcode
from datetime import datetime


data = "Hello, World!"  # The data to be encoded in the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=4)  # Create a QR code instance
qr.add_data(data)  # Add the data to the QR code
qr.make(fit=True)  # Make the QR code
qr_img = qr.make_image(fill_color="black", back_color="white")  # Create an image from the QR code


qr_img.save("qr_N.png")  # Save the QR code image to a file
qr_img.show()  # Display the QR code image