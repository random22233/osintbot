import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_endato_person_data(phone):
    GALAXY_AP_NAME = os.getenv("GALAXY_AP_NAME")
    GALAXY_AP_PASSWORD = os.getenv("GALAXY_AP_PASSWORD")
    
    url = "https://devapi.endato.com/PersonSearch"

    payload = { "Phone": phone }
    headers = {
        "accept": "application/json",
        "galaxy-ap-name": GALAXY_AP_NAME,
        "galaxy-ap-password": GALAXY_AP_PASSWORD,
        "galaxy-search-type": "Person",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    # Checking if the request was successful
    if response.status_code == 200:
        # If successful, print the JSON response
        data = response.json()
        data = data["persons"]
        result = []
        coords = []
        for person in data:
            addresses = []
            phoneNumbers = []
            emailAddresses = []
            for address in person["addresses"]:
                addresses.append({"fullAddress": address["fullAddress"], "latitude": address["latitude"],
                                  "longitude": address["longitude"]})
                if len(address["latitude"]) > 0 and len(address["longitude"]) > 0:
                    coords.append((float(address["latitude"]), float(address["longitude"])))
            # for phone in person["phoneNumbers"]:
            #     phoneNumbers.append({"company":phone["company"], "location":phone["location"]})
            # for email in person["emailAddresses"]:
            #     emailAddresses.append(email["emailAddress"])
            # result.append({"name": person["name"], "locations": person["locations"], "addresses":addresses,
            #                "phoneNumbers":phoneNumbers, "emailAddresses": emailAddresses,
            #                "fullName": person["fullName"]})
        return response.json(), coords
    else:
        # If not successful, print the error
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
        return response.text, []
    
    
def get_endato_data(phone):
    GALAXY_AP_NAME = os.getenv("GALAXY_AP_NAME")
    GALAXY_AP_PASSWORD = os.getenv("GALAXY_AP_PASSWORD")
    
    url = "https://devapi.endato.com/ReversePhoneSearch"

    payload = { "Phone": phone }
    headers = {
        "accept": "application/json",
        "galaxy-ap-name": GALAXY_AP_NAME,
        "galaxy-ap-password": GALAXY_AP_PASSWORD,
        "galaxy-search-type": "ReversePhone",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    # Checking if the request was successful
    if response.status_code == 200:
        # If successful, print the JSON response
        data = response.json()
        data = data["reversePhoneRecords"]
        result = []
        coords = []
        for row in data:
            result.append({"addresses":row["addresses"], "names":row["names"],
                          "latitude":row["latitude"], "longitude":row["longitude"]})
            coords.append((float(row["latitude"]), float(row["longitude"])))
        return result, coords
    else:
        # If not successful, print the error
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
        return response.text, []