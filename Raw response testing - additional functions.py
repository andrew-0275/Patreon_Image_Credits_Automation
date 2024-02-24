''

''

import requests
import os
from dotenv import load_dotenv
import pandas as pd
import datetime

# Load environment variables from .env file
load_dotenv()

# Access environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CAMPAIGN_ID = '3725823'  # Example campaign ID

# Set the base URL for Patreon API
base_url = 'https://www.patreon.com/api/oauth2/v2'

# Specify the fields you want to include for each member
fields_members = 'full_name,patron_status,last_charge_date,last_charge_status,lifetime_support_cents,currently_entitled_amount_cents,pledge_relationship_start,is_follower,email'

# Specify the endpoint for fetching campaign members, including desired fields
endpoint = f'/campaigns/{CAMPAIGN_ID}/members?fields[member]={fields_members}'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
}

# Initialize a list to hold patron data
patrons_data = []

# Function to make the API request and process the response
def fetch_patrons(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for member in data.get('data', []):
            # Collect required information for each member
            member_info = {
                'Full Name': member['attributes'].get('full_name'),
                'Patron Status': member['attributes'].get('patron_status'),
                'Last Charge Date': member['attributes'].get('last_charge_date'),
                'Last Charge Status': member['attributes'].get('last_charge_status'),
                'Lifetime Support Cents': member['attributes'].get('lifetime_support_cents'),
                'Currently Entitled Amount Cents': member['attributes'].get('currently_entitled_amount_cents'),
                'Pledge Relationship Start': member['attributes'].get('pledge_relationship_start'),
                'Is Follower': member['attributes'].get('is_follower'),
                'Email': member['attributes'].get('email')  # Ensure you have the correct permissions to access this
            }
            patrons_data.append(member_info)
        
        # Check for pagination and fetch next page if exists
        next_page = data['meta']['pagination'].get('cursors', {}).get('next')
        if next_page:
            next_page_url = f'{base_url}{endpoint}&page[cursor]={next_page}'
            fetch_patrons(next_page_url)
    else:
        print(f'Failed to fetch patrons: {response.status_code}')

# Define the base URL for Patreon API
base_url = 'https://www.patreon.com/api/oauth2/v2'

# Start fetching patrons
fetch_patrons(f'{base_url}{endpoint}')

# Convert the list of dictionaries into a DataFrame
patrons_df = pd.DataFrame(patrons_data)

# Save the DataFrame to a CSV file
patrons_df.to_csv('patrons_members.csv', index=False)



# Current date in YYYY-MM-DD format
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Filter the DataFrame to include only active patrons
active_patrons_df = patrons_df[patrons_df['Patron Status'] == 'active_patron']

# Filename with current date
filename = f'active_patron_members_{current_date}.csv'

# Save the filtered DataFrame to a new CSV file
active_patrons_df.to_csv(filename, index=False)

print(f'Active patron members saved to {filename}')






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


