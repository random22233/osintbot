from flask import Blueprint, request, jsonify, Response
import uuid
import re
import json
from datetime import datetime
import requests
import subprocess
import csv
import os
import asyncio  

from utils.db_search import search_carderpro, search_discord_part1, search_discord_part2, search_inattack_part1 , search_inattack_part2, search_inattack_user, search_opensc_ws, search_xakepok, search_zloy_db
from utils.ghunt_email.ghunt import ghunt as run_ghunt



# from selenium_driverless import webdriver
# from selenium_driverless.types.by import By
# from capmonstercloudclient import CapMonsterClient, ClientOptions
# from capmonstercloudclient.requests import HcaptchaProxylessRequest
from dotenv import load_dotenv

from utils.get_reviews_screenshot import get_reviews_screenshot
from utils.onion_serch import scrape_onion

load_dotenv()

CAPMONSTER_API_KEY = os.getenv('CAPMONSTER_API_KEY')
LEAKOSINT_TOKEN = os.getenv('LEAKOSINT_TOKEN')
WOXY_API_KEY = os.getenv('WOXY_API_KEY')
AVATAR_API_USER = os.getenv('AVATAR_API_USER')
AVATAR_API_PASS = os.getenv('AVATAR_API_PASS')
WOXY_API_KEY = os.getenv('WOXY_API_KEY')
SEON_API_KEY = os.getenv('SEON_API_KEY')

REVERSE_CONTACT_API_KEY = os.getenv('REVERSE_CONTACT_API_KEY')

def search_email_in_file(email, filename):
    result = None
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if email in line:
                result = line
    return result


def search_in_sql_file(file_path, search_term):
    with open(file_path, 'r', encoding='latin1') as file:
        lines = file.readlines()

    matching_lines = [line.strip() for line in lines if search_term.lower() in line.lower()]
    
    return matching_lines



def search_in_csv(file_path, column_name, search_value):
    result = None
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row[column_name] == search_value:
                result = row
                break
    return result

async def send_text_file(file_content, file_path, file_name):
    """Creates a text file and returns its content and metadata as a JSON response."""
    try:
        # Write content to file
        with open(file_path, "w") as f:
            f.write(file_content)
        
        # Read file content
        with open(file_path, "r") as f:
            content = f.read()
            
        # Create response
        response = {
            "success": True,
            "data": {
                "file_name": file_name,
                "content": content,
                "size": os.path.getsize(file_path)
            }
        }
        
        # Clean up
        os.remove(file_path)
        
        return response
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def search_db(email):
    results = []
    try:
        data = search_zloy_db(email)
        results.append(data)
    except Exception as e:
        print("error in search_zloy_db", e)
    try:
        user_data, messages = search_inattack_part1(email)
        results.append(user_data)
        results.append(messages)
        if messages and len(messages) > 0:
            now = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
            current_directory = os.getcwd()
            unique_id = str(uuid.uuid4())
            messages_filename = f"messages_{unique_id}_{now}.txt"
            messages_path = os.path.join(current_directory, messages_filename)
            
            results.append(await send_text_file(messages, messages_path, messages_filename))
    except Exception as e:
        print("error in search_inattack_part1", e)
    try:
        user_data, messages = search_inattack_part2(email)
        results.append(user_data)
        results.append(messages)
        if messages and len(messages) > 0:
            now = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
            current_directory = os.getcwd()
            unique_id = str(uuid.uuid4())
            messages_filename = f"posts_{unique_id}_{now}.txt"
            messages_path = os.path.join(current_directory, messages_filename)
            
            results.append(await send_text_file(messages, messages_path, messages_filename))
    except Exception as e:
        print("error in search_inattack_part2", e)
    try:
        user_data, messages = search_xakepok(email)
        results.append(user_data)
        results.append(messages)
        if messages and len(messages) > 0:
            now = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
            current_directory = os.getcwd()
            unique_id = str(uuid.uuid4())
            messages_filename = f"posts_{unique_id}_{now}.txt"
            messages_path = os.path.join(current_directory, messages_filename)
            
            results.append(await send_text_file(messages, messages_path, messages_filename))
    except Exception as e:
        print("error in search_inattack_part2", e)
    try:
        data = search_carderpro(email)
        results.append(data)
    except Exception as e:
        print("error in search_carderpro", e)
    try:
        data = search_opensc_ws(email)
        results.append(data)
    except Exception as e:
        print("error in search_opensc_ws", e)
       
    try:
        data = search_inattack_user(email)
        results.append(data)
    except Exception as e:
        print("error in search_inattack_user", e) 
    try:
        data = search_discord_part1(email)
        results.append(data)
    except Exception as e:
        print("error in search_discord_part1", e) 
    try:
        data = search_discord_part2(email)
        results.append(data)
    except Exception as e:
        print("error in search_discord_part2", e) 
            
    # print("method_1_result" , method_1_result)
    # method_2_result = serch_inattack_ru_db(email)
    # print("method_2_result" , method_2_result)
    # await message.answer(f"database search result:\n{method_1_result}\n\n{method_2_result}")
    return results



async def ghunt(email):
    ghunt_data, review_locations = run_ghunt(str(email))
    response = {
        "ghunt_data": ghunt_data,
        "photo_data": None
    }
    
    if ghunt_data:
        try:
            if review_locations and len(review_locations) > 0:
                unique_id = str(uuid.uuid4())
                screenshot_path, map_path = await get_reviews_screenshot(review_locations, unique_id)
                
                if screenshot_path and map_path:  # Only process if both paths exist
                    # Read the image file as base64
                    with open(screenshot_path, "rb") as image_file:
                        import base64
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                        response["photo_data"] = encoded_image

                    # Clean up files
                    os.remove(screenshot_path)
                    os.remove(map_path)
            else:
                response["message"] = "No review locations found"
                
        except Exception as e:
            print("error in getting review photo", e)
            response["error"] = str(e)
    else:
        response["message"] = "Registered on Google : False"
        
    return response



# async def search0t(email, message):
#     client_options = ClientOptions(api_key=CAPMONSTER_API_KEY)
#     cap_monster_client = CapMonsterClient(options=client_options)
#     recaptcha2request = HcaptchaProxylessRequest(websiteUrl="https://search.0t.rocks/",
#                                                         websiteKey="bb0d021f-a411-4d21-91fd-797aff5f1d58")
#     responses =  await cap_monster_client.solve_captcha(recaptcha2request)
    
#     cap = responses['gRecaptchaResponse']


#     options = webdriver.ChromeOptions()
#     async with webdriver.Chrome(options=options) as driver:
#         await driver.get(f"https://search.0t.rocks/records?emails={email}&token={cap}")
#         await driver.sleep(6)
#         await driver.find_element(By.XPATH, '/html/body', timeout=10)
#         txt = await driver.page_source
#         soup = BeautifulSoup(txt, 'html.parser')
#         dd_elements = soup.find_all('dd')
#         mainres = ''
#         for dd in dd_elements:
#             mainres += dd.get_text(strip=True)
#         if len(mainres) > 4096:
#             for x in range(0, len(mainres), 4096):
#                 await message.answer(mainres[x:x+4096])
#         else:
#             await message.answer(mainres)
        # elem = await driver.find_element(By.XPATH, '/html/body/div[1]', timeout=10)
        # # time.sleep(5)
        
        # txt = await elem.text
        # res = re.sub(r'.+Visualize.', '', txt)
        # mainres = res.replace('  ', '')
        # # return f'0t:{mainres.strip()}'
        # await message.answer(f'0t:{mainres.strip()}')


async def onion_search(email):
    data = scrape_onion(email)
    return str(data)


def check_email_with_holehe(email):
    """
    Runs the Holehe tool to check the provided email address and returns the output.
    """
    try:
        # Run holehe using subprocess
        result = subprocess.run(
            ["holehe", email],
            text=True,
            capture_output=True
        )
        return result.stdout
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_existing_accounts(output):
    """
    Extracts existing accounts (lines with [+]) from Holehe output.
    """
    existing_accounts = []
    lines = output.splitlines()
    
    for line in lines:
        # Match only lines where email is used: [+] service
        if "[+]" in line:
            service = line.split(" ")[-1]  # Extract the service (last part of the line)
            existing_accounts.append(service)
    
    return existing_accounts

def holehe(email_to_check):
    try:
        # Run Holehe and get the output
        print("Running Holehe...")
        holehe_output = check_email_with_holehe(email_to_check)

        # Extract existing accounts
        print("Extracting existing accounts...")
        existing_accounts = extract_existing_accounts(holehe_output)

        # Prepare JSON data
        output_data = {
            "email": email_to_check,
            "existing_accounts": existing_accounts
        }

        return json.dumps(output_data, indent=4, ensure_ascii=False)
    except Exception as e:
        return f"An error occurred: {str(e)}"

def fetch_and_filter_leak_data(email):
    # Your API token
    token = "6653420429:jJSmds3a"
    
    # Search request (update this to the email or query you are searching for)
    search_request = email
    
    # API request payload
    data = {
        "token": token,
        "request": search_request,
        "limit": 100,
        "lang": "en"
    }
    
    # API URL
    url = 'https://leakosintapi.com/'

    # Define the fields to extract
    fields_to_extract = [
        'email', 'phone', 'address', 'postcode', 'state', 'ip', 'username',
        'ssn', 'fullname', 'relatives', 'houseprice', 'housebuiltyear', 
        'dob', 'jobtitle', 'facebookid', 'regdate', 'bday', 'industry', 
        'nickname', 'password'
    ]

    # Function to filter relevant fields from each entry
    def filter_fields(data_entry):
        filtered_entry = {}
        for key, value in data_entry.items():
            # Normalize the key to lowercase alphanumeric characters
            normalized_key = re.sub(r'[\W_]+', '', key).lower()
            
            # Check if the normalized key matches any field in fields_to_extract
            for field in fields_to_extract:
                if field in normalized_key:
                    filtered_entry[field.capitalize()] = value  # Capitalize for neat output
                    break
        return filtered_entry

    # Make the POST request
    response = requests.post(url, json=data)
    
    # Check if the response is successful and contains data
    if response.status_code != 200:
        return json.dumps({
            "error": f"API request failed with status code: {response.status_code}",
            "details": response.text
        })
        
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return json.dumps({
            "error": "Invalid JSON response from API",
            "response_text": response.text[:1000]  # Include first 1000 chars of response for debugging
        })

    # Process the response data
    filtered_data = {}
    if 'List' in response_data:
        for database_name, database_content in response_data['List'].items():
            if 'Data' in database_content:
                # Filter each entry in the 'Data' list for relevant fields
                filtered_entries = [filter_fields(entry) for entry in database_content['Data']]
                
                # Remove empty entries after filtering
                filtered_entries = [entry for entry in filtered_entries if entry]
                
                if filtered_entries:
                    filtered_data[database_name] = filtered_entries
    print("email: ", email)
    print("filtered_data: ", filtered_data)
    # Convert to JSON format
    return json.dumps(filtered_data, indent=4, ensure_ascii=False)

router = Blueprint('email', __name__)


@router.route('/email', methods=['POST'])
def command_search_handler():
    email = request.json.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    def generate_response():
        # # FIRST PART - All synchronous API calls
        # first_results = []  

        # # Fetch and filter the leak data  
        # filtered_json = fetch_and_filter_leak_data(email)  
        # first_results.append({"leak_data": filtered_json})  

        # # whoxy  
        # url = f'https://api.whoxy.com/?key={WOXY_API_KEY}&reverse=whois&email={email}'  
        # response = requests.get(url)  
        # data = response.json()  

        # if data['status'] == 1:  
        #     if data['total_results'] != 0:  
        #         whois = ''  
        #         for res in data['search_result']:  
        #             whois += f"Email: {res['domain_name']}\n"  
        #             for key, value in res['registrant_contact'].items():  
        #                 whois += f"{str(key).replace('_', ' ').capitalize()}: {value}\n"  
        #             whois += '\n'  
        #         first_results.append({"whois": whois})  
        #     else:  
        #         first_results.append({"whois": 'No domain registered on this email address!'})  

        # # LinkedIn  
        # url = "https://api.reversecontact.com/enrichment"  
        # querystring = {"email": email, "apikey": REVERSE_CONTACT_API_KEY}  
        # response = requests.get(url, params=querystring).json()  
        # if response['success']:  
        #     fname = response['person']['firstName']  
        #     lname = response['person']['lastName']  
        #     photourl = response['person']['photoUrl']  
        #     first_results.append({  
        #         "linkedin": {  
        #             "name": f"{fname} {lname}",  
        #             "photo_url": photourl  
        #         }  
        #     })  

        # # SEON  
        # headers = {"X-API-KEY": SEON_API_KEY}  
        # r = requests.get(f"https://api.us-east-1-main.seon.io/SeonRestService/email-api/v2/{email}", headers=headers)  
        # first_results.append({"seon": r.json()})  

        # # WOXY  
        # r = requests.get(f'https://api.whoxy.com/?key=6f74300ecd4db96ct5a7d9148ca47c13f&reverse=whois&email={email}')  
        # first_results.append({"woxy": r.json()})  

        # # Onion search
        # try:  
        #     onion_results = asyncio.run(onion_search(email))  
        #     first_results.append({"onion": onion_results})  
        # except Exception as e:  
        #     first_results.append({"onion_error": str(e)})  

        # # DB Search  
        # try:  
        #     db_results = asyncio.run(search_db(email))  
        #     first_results.append({"db_search": db_results})  
        # except Exception as e:  
        #     first_results.append({"db_search_error": str(e)})  

        # # First yield - all results except holehe and ghunt
        # yield json.dumps({"status": "first_part", "data": first_results}) + "\n"

        # SECOND PART - Holehe and Ghunt only
        second_results = []

        # # Holehe  
        # try:
        #     holehe_result = holehe(email)  
        #     second_results.append({"holehe": holehe_result})  
        # except Exception as e:
        #     second_results.append({"holehe_error": str(e)})

        # GHUNT  
        try:  
            ghunt_result = asyncio.run(ghunt(email))  
            second_results.append({"ghunt": ghunt_result})  
        except Exception as e:  
            second_results.append({"ghunt_error": str(e)})  

        # Second yield - holehe and ghunt results
        yield json.dumps({"status": "second_part", "data": second_results}) + "\n"

    return Response(generate_response(), mimetype='application/json')
