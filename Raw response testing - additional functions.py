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
CAMPAIGN_ID = '3725823'  # Example campaign ID

# Set the base URL for Patreon API
base_url = 'https://www.patreon.com/api/oauth2/v2'

# Specify the fields you want to include for each member
fields_members = 'full_name,patron_status,last_charge_status,currently_entitled_amount_cents'

# Specify the endpoint for fetching campaign members, including desired fields
endpoint = f'/campaigns/{CAMPAIGN_ID}/members?fields[member]={fields_members}'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
}

# Initialize a list to hold all patrons' full names
patrons_full_names = []

# Function to make the API request and process the response
def fetch_patrons(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for member in data.get('data', []):
            # Extract and print the full name of each member
            full_name = member['attributes'].get('full_name')
            patrons_full_names.append(full_name)
            #print(full_name)
        
        # Check for pagination and fetch next page if exists
        next_page = data['meta']['pagination'].get('cursors', {}).get('next')
        if next_page:
            next_page_url = f'{base_url}{endpoint}&page[cursor]={next_page}'
            fetch_patrons(next_page_url)
    else:
        print(f'Failed to fetch patrons: {response.status_code}')

# Start fetching patrons
fetch_patrons(f'{base_url}{endpoint}')

# Optionally, convert the list of full names into a DataFrame or save it as needed
patrons_df = pd.DataFrame(patrons_full_names, columns=['Full Name'])
patrons_df.to_csv('patrons_members.csv', index=False)



def get_campaign_id():
    url = 'https://www.patreon.com/api/oauth2/api/current_user/campaigns'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            # Assuming you have only one campaign, you can directly extract its ID
            campaign_id = data['data'][0]['id']
            return campaign_id
        else:
            print("No campaigns found for this user.")
            return None
    else:
        print(f"Failed to fetch campaign data: {response.status_code}")
        return None


