import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_userbox_data(phone):

    # URL and Bearer token
    url = "https://api.usersbox.ru/v1/search?"
    USERBOX_TOKEN = os.getenv("USERBOX_TOKEN")

    # Headers including the Authorization with Bearer token
    headers = {
        "Authorization": f"Bearer {USERBOX_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    # Optional query parameter (e.g., q=your_query)
    params = {
        "q": phone # Replace with your search query
    }

    # Sending the GET request
    response = requests.get(url, headers=headers, params=params)

    # Checking if the request was successful
    if response.status_code == 200:
        hits = []
        # If successful, print the JSON response
        data = response.json()
        data = data["data"]["items"]
        for row in data:
            hits_items = row["hits"]["items"]
            for hit in hits_items:
                hits.append(hit)
        return hits
    else:
        # If not successful, print the error
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
        return response.text