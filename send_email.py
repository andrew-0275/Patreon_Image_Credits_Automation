import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

def send_image_via_email():
    # Load environment variables
    load_dotenv()
    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_recipient = os.getenv('EMAIL_RECIPIENT')

    # Create message
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = "Patron Credits Image"
    
    # Email body
    body = "Attached is the latest Patron Credits image."
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the image
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"patrons_credits_{current_date}.png"
    filepath = os.path.join(os.getcwd(), filename)  # Assumes file is in the current working directory
    with open(filepath, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)
    
    # Connect to the server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_recipient, msg.as_string())

def main():
    send_image_via_email()
    print("Email sent successfully.")

if __name__ == "__main__":
    main()

