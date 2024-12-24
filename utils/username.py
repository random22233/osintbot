import subprocess
import threading
import requests
import re
import json
from serpapi.google_search import GoogleSearch

import os
from datetime import datetime
import uuid
from utils.db_search_username import search_zloy_db, search_inattack_part1, search_inattack_part2, search_xakepok, search_carderpro, search_opensc_ws, search_inattack_user, search_discord_part1, search_discord_part2
import csv
from io import StringIO

# Define categories with site names as recognized by Sherlock
categories = {
    "social_media": ["Twitter", "Instagram", "Facebook", "LinkedIn"],
    "programming_technology": ["GitHub", "GitLab", "Bitbucket"],
    "forums": ["Reddit", "Disqus", "Slashdot"],
    # ... other categories can be added here
}

# LeakOSINT API token and endpoint
leakosint_token = "6653420429:jJSmds3a"
leakosint_url = 'https://leakosintapi.com/'
fields_to_extract = [
    'email', 'phone', 'address', 'postcode', 'state', 'ip', 'username',
    'ssn', 'fullname', 'relatives', 'houseprice', 'housebuiltyear', 
    'dob', 'jobtitle', 'facebookid', 'regdate', 'bday', 'industry', 'nickname'
]

# ScamSearch API key and endpoint
scamsearch_api_key = "az4k5xiqfw3chmlj7ndeog6try2801"
scamsearch_url = "https://scamsearch.io/api/search"

# Email Validation API key and endpoint
email_validation_api_key = "80d4d8a36d494008b10efd0a356ee729"
email_validation_url = "https://api.emailvalidation.com"

# List of domains to check for email validation
email_domains = ["mail.ru", "gmail.com", "yahoo.com", "hotmail.com", "protonmail.com"]

def run_sherlock(username, category_name):
    """
    Run Sherlock to search for a specified username on sites within the chosen category.
    """
    results = {"sherlock_output": None, "google_dork": None}
    sites = categories.get(category_name)
    if not sites:
        return {"error": f"Category '{category_name}' not found."}

    command = ["python", r"C:\Project\sherlock\sherlock_project\sherlock.py", username]
    for site in sites:
        command.extend(["--site", site])

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        if result.stdout:
            results["sherlock_output"] = result.stdout
        elif result.stderr:
            results["error"] = result.stderr
        else:
            results["error"] = "No output received from Sherlock."
    except subprocess.TimeoutExpired:
        results["error"] = "Sherlock process took too long and was terminated."

    if category_name == "forums":
        results["google_dork"] = search_username_google_dork(username)
    
    return results

def search_username_google_dork(username):
    """
    Perform a Google Dork search for the username on selected forums.
    """
    try:
        search = GoogleSearch({
            "q": f'intext:"{username}" site:breachforums.com OR site:nulled.to OR site:cracked.io',
            "num": 3,
            "api_key": "4d56c0d6386bcd9a7ea951e9332323c0b609e44f560ac0d279cb5026553e86e7"
        })

        results = search.get_dict()
        return results.get("organic_results", [])[:3]
    except Exception as e:
        return {"error": f"Google Dork search error: {str(e)}"}

def run_leakosint_search(username_to_search):
    """
    Run LeakOSINT API search and filter the results based on specified fields.
    """
    data = {"token": leakosint_token, "request": username_to_search, "limit": 100, "lang": "en"}
    try:
        response = requests.post(leakosint_url, json=data)
        response_data = response.json()
        
        def filter_fields(data_entry):
            filtered_entry = {}
            for key, value in data_entry.items():
                normalized_key = re.sub(r'[\W_]+', '', key).lower()
                for field in fields_to_extract:
                    if field in normalized_key:
                        filtered_entry[field.capitalize()] = value
                        break
            return filtered_entry

        filtered_data = {}
        if 'List' in response_data:
            for db_name, db_content in response_data['List'].items():
                if 'Data' in db_content:
                    filtered_entries = [filter_fields(entry) for entry in db_content['Data']]
                    filtered_entries = [entry for entry in filtered_entries if entry]
                    if filtered_entries:
                        filtered_data[db_name] = filtered_entries

        return filtered_data

    except Exception as e:
        return {"error": f"LeakOSINT search error: {str(e)}"}

def run_scamsearch(username):
    """
    Run Scamsearch API query for the specified username.
    """
    query = username
    search_type = "user"
    url = f"https://scamsearch.io/api/search?search={query}&type={search_type}&api_token={scamsearch_api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Scamsearch Error: {response.status_code} - {response.text}"}

    except Exception as e:
        return {"error": f"Scamsearch error: {str(e)}"}

def run_email_validation(username):
    """
    Validate potential email addresses for the username on specified domains using Maileroo's API.
    """
    valid_emails = []
    errors = []
    maileroo_api_key = "5b1606b007c5f248332a059ff39332545150aa7a0039a047187a1de2e8faa2e2"
    url = "https://verify.maileroo.net/check"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": maileroo_api_key
    }

    for domain in email_domains:
        email = f"{username}@{domain}"
        data = {
            "email_address": email
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result["data"].get("format_valid") and result["data"].get("mx_found"):
                    valid_emails.append(email)
            else:
                errors.append(f"Error validating {email}: {response.status_code}")
        except Exception as e:
            errors.append(f"Exception for {email}: {str(e)}")

    return {
        "valid_emails": valid_emails,
        "errors": errors if errors else None
    }

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
    

async def db_search_cm_users(username):
    """
    Search for a specific username in SQL dump file
    Returns a list of matching rows as dictionaries
    """
    filename = "data/verified.cm_users.sql"
    results = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace("INSERT INTO `user` VALUES ", "")
            # Process each row that starts with a parenthesis
            for line in content.split('\n'):
                line = line.strip()
                if not line.startswith('('):
                    continue
                    
                # Remove the leading/trailing parentheses
                values = line.strip('(),').split(',')
                
                # Username is the 5th field (index 4)
                if len(values) > 4 and values[4].lower().replace("'", "") == username.lower():
                    user_data = {
                        'userid': values[0],
                        'usergroupid': values[1],
                        'username': values[4].replace("'", ""),
                        'email': values[7].replace("'", ""),
                        'usertitle': values[15].replace("'", ""),
                        'joindate': values[17],
                        'lastactivity': values[19]
                    }
                    results.append(user_data)
                    # print("user_data: ", user_data)
        return results
        
    except Exception as e:
        print(f"Error reading database file: {e}")
        return results

async def search_db(username):
    # data = await db_search_cm_users(username)
    # return data
    results = []
    try:
        data = search_zloy_db(username)
        results.append(data)
    except Exception as e:
        print("error in search_zloy_db", e)
    try:
        user_data, messages = search_inattack_part1(username)
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
        user_data, messages = search_inattack_part2(username)
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
        user_data, messages = search_xakepok(username)
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
        data = search_carderpro(username)
        results.append(data)
    except Exception as e:
        print("error in search_carderpro", e)
    try:
        data = search_opensc_ws(username)
        results.append(data)
    except Exception as e:
        print("error in search_opensc_ws", e)
       
    try:
        data = search_inattack_user(username)
        results.append(data)
    except Exception as e:
        print("error in search_inattack_user", e) 
    try:
        data = search_discord_part1(username)
        results.append(data)
    except Exception as e:
        print("error in search_discord_part1", e) 
    try:
        data = search_discord_part2(username)
        results.append(data)
    except Exception as e:
        print("error in search_discord_part2", e) 
    
    try:
        data = await db_search_cm_users(username)
        results.append(data)
    except Exception as e:
        print("error in db_search_username", e) 
    return results




# Example usage
username_to_search = "intelbroker"
run_email_validation(username_to_search)


# Main function to run all searches concurrently
async def main(username, category_name):
    # Create a dictionary to store results from threaded functions
    thread_results = {}
    
    # First run the async search_db
    db_search_result = await search_db(username)
    
    # Modify sync functions to store their results
    def run_sync_functions():
        thread_results['sherlock'] = run_sherlock(username, category_name)
        thread_results['leakosint'] = run_leakosint_search(username)
        thread_results['scamsearch'] = run_scamsearch(username)
        thread_results['email_validation'] = run_email_validation(username)

    # Run synchronous functions in a separate thread
    thread = threading.Thread(target=run_sync_functions)
    thread.start()
    thread.join()

    # Combine all results
    all_results = {
        'db_search': db_search_result,
        **thread_results
    }
    
    return all_results


# Specify the username and category you want to search
# username_to_search = "IntelBroker"
# category_to_search = "forums"  # Change to the desired category name

# main(username_to_search, category_to_search)
