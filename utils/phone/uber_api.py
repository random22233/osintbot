import requests
from bs4 import BeautifulSoup

def check_uber_forgot_password(phone):

    # Step 1: Create a session
    session = requests.Session()

    # Step 2: Make a GET request to the login or reset password page to fetch the CSRF token
    url = "https://auth.uber.com/v2"  # Adjust this URL to Uber's reset password page if needed
    response = session.get(url, allow_redirects=True)
    print(response.status_code, response.text)
    # print(response.headers , response.cookies , session.cookies, session.headers)

    # Step 3: Parse the page with BeautifulSoup to extract the CSRF token
    # soup = BeautifulSoup(response.content, 'html.parser')
    # verification_token = soup.find('input', {'name': 'verification-token'})['value']  # Modify according to the actual field name
    # fc_token = soup.find('input', {'name': 'fc-token'})['value']
    # Step 4: Prepare your POST data, including the CSRF token
    post_data = {
        "email": phone,  # Replace with actual phone number
        # "verification-token": verification_token,  # Add the CSRF token to the form data
        # "fc-token": fc_token
    }

    # Step 5: Include the CSRF token in the request headers (if required by the website)
    headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Step 6: Send the POST request with the CSRF token and session
    post_url = "https://auth.uber.com/v2/submit-form"  # Adjust as needed for the correct POST URL
    response = session.post(post_url, data=post_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Request successful")
    else:
        print(response.status_code , response.text)
        print(f"Failed: {response.status_code}, {response.content}")
