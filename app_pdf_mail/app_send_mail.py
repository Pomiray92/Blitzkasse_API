import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from app_get_zabschlag import data_dict
from dotenv import load_dotenv
load_dotenv("settings.env")
import pdb

DEFAULT_SENDER_EMAIL = data_dict["companyEmail"]

DEFAULT_SUBJECT = "Z-Abschlag N"

SENDER_EMAIL = os.getenv("SENDER_EMAIL", DEFAULT_SENDER_EMAIL)
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SUBJECT = os.getenv("SUBJECT", DEFAULT_SUBJECT)
#breakpoint()


def send_mail(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, SUBJECT, message,  attachment_path):
    # Create a multipart message object
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = SUBJECT

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, "plain"))

    # Open and attach the PDF file
    with open(attachment_path, "rb") as attachment:
        pdf_part = MIMEApplication(attachment.read(), "pdf")
        pdf_part.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment_path))
        msg.attach(pdf_part)

    # Create a secure SSL/TLS connection to the SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login to the email account
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    # Send the email
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    # Close the connection
    server.quit()

# Example usage
message = "Nu Privet"
attachment_path = "data/receipt_N61_07.07.2023_19-39-37.pdf"

send_mail(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, SUBJECT, message, attachment_path)