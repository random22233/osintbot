import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_endato_email_data(email):
    GALAXY_AP_NAME = os.getenv("GALAXY_AP_NAME")
    GALAXY_AP_PASSWORD = os.getenv("GALAXY_AP_PASSWORD")
    
    url = "https://devapi.endato.com/Email/Enrich"

    payload = { "Email": email }
    headers = {
        "accept": "application/json",
        "galaxy-ap-name": GALAXY_AP_NAME,
        "galaxy-ap-password": GALAXY_AP_PASSWORD,
        "galaxy-search-type": "DevAPIEmailID",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    # Checking if the request was successful
    if response.status_code == 200:
        # If successful, print the JSON response
        data = response.json()
        return data
    else:
        # If not successful, print the error
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
        return response.text