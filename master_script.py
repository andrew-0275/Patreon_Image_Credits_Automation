import datetime
from fetch_patrons import fetch_patrons_10
from create_image import generate_patron_credits_image
from send_email import send_image_via_email

def main():
    
    # Fetch and save $10 and above patrons into a CSV
    fetch_patrons_10()
    
    # Create image from patron data
    generate_patron_credits_image()
    
    # Send the image via email
    send_image_via_email()

if __name__ == "__main__":
    main()
