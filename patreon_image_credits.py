''

''

import requests
import os
from dotenv import load_dotenv
import pandas as pd
import json

# Load environment variables from .env file
load_dotenv()

# Access environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CAMPAIGN_ID = '3725823'

def get_all_patrons():
    url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{CAMPAIGN_ID}/members"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    all_patrons = []
    next_page = url

    while next_page:
        response = requests.get(next_page, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_patrons.extend(data.get('data', []))
            next_page = data.get('links', {}).get('next')
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return []

    return all_patrons

def create_csv_from_patrons(patrons):
    # Extract necessary attributes for DataFrame
    patron_data = [{'full_name': patron.get('attributes', {}).get('full_name', ''),
                    'patron_status': patron.get('attributes', {}).get('patron_status', '')}
                   for patron in patrons]
    
    # Create DataFrame
    df = pd.DataFrame(patron_data)
    
    # Save DataFrame to CSV
    df.to_csv('patrons_data.csv', index=False)
    print("CSV file created successfully.")



if __name__ == "__main__":
    patrons = get_all_patrons()
    create_csv_from_patrons(patrons)

# campaign_id = get_campaign_id()
# if campaign_id:
#     print(f"Your campaign ID is: {campaign_id}")