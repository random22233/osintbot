import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_leak_osint_data(phone):
    LEAK_OSINT_API = os.getenv("LEAK_OSINT_API")

    data =  {"token":LEAK_OSINT_API, "request":phone, "limit": 100, "lang":"ru"}
    url = 'https://server.leakosint.com/'
    response = requests.post(url, json=data)
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