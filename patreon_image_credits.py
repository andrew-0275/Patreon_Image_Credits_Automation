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