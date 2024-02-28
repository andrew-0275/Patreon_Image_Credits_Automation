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
    
    # Assuming EMAIL_RECIPIENT now contains multiple email addresses separated by a comma
    email_recipients = os.getenv('EMAIL_RECIPIENTS').split(',')
    
    # Connect to the server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_sender, email_password)
        
        for email_recipient in email_recipients:
            # Create message for each recipient
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = email_recipient  # Single recipient for this email
            
            # Format the current month and year for the subject line
            current_month_year = datetime.datetime.now().strftime("%B %Y")  # "%B" gives the full month name, "%Y" gives the four-digit year
            msg['Subject'] = f"Patron Credits Image {current_month_year}"
            
            # Email body
            body = "Attached is the latest patron credits image for this month."
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
            
            # Send the email to the current recipient
            server.sendmail(email_sender, email_recipient, msg.as_string())
            print(f"Email sent successfully to {email_recipient}.")

def main():
    send_image_via_email()

if __name__ == "__main__":
    main()

