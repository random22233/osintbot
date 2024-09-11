from aiogram import F
from aiogram import Router
import requests
from aiogram.types import Message
import urllib.parse

import time

from urllib.parse import quote


import subprocess
from aiogram import Router


from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import HcaptchaProxylessRequest
from bs4 import BeautifulSoup
import csv
import os
from dotenv import load_dotenv

load_dotenv()

CAPMONSTER_API_KEY = os.getenv('CAPMONSTER_API_KEY')
LEAKOSINT_TOKEN = os.getenv('LEAKOSINT_TOKEN')
WOXY_API_KEY = os.getenv('WOXY_API_KEY')
AVATAR_API_USER = os.getenv('AVATAR_API_USER')
AVATAR_API_PASS = os.getenv('AVATAR_API_PASS')
WOXY_API_KEY = os.getenv('WOXY_API_KEY')
SEON_API_KEY = os.getenv('SEON_API_KEY')
TELETYPE_API_KEY = os.getenv('SEON_API_KEY')

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


import sys
import httpx


async def ghunt(email, message):
    command_output = f'ghunt email {email}'
    result = subprocess.check_output(command_output, shell=True, text=True)
    # print(result)
    return await message.answer(result.replace('"', ''))

async def onion(email, message):
    command_output = f'onionsearch "{email}"'
    result = subprocess.check_output(command_output, shell=True, text=True)
    # print(result)
    return await message.answer(result)


varr = """First Name:	ANDREW
Last Name:	BOGOD
State:	NY
City:	BROOKLYN
Address:	21 HILL ST
Zip Code:	11208-2820


Name:	Andrew Bogod
Reported Date:	05/07/2018
Gender:	Male
Address:	2657 E 21st Street, Brooklyn, New York


Name:	ANDREW BOGOD
First Name:	ANDREW
Last Name:	BOGOD
Address:	21 HILL ST, NY, BROOKLYN, 11
City:	BROOKLYN
State:	11
Latitude:	0.000000
Longitude:	0.000000
Gender:	
Registration Date:	2019-09-11
Own Rent:	own
Source:	classmates.com
Domain:	gmail
Ip Address:	66.251.66.163

Name:	ANDREW BOGOD
First Name:	ANDREW
Last Name:	BOGOD
Address:	21 HILL ST, BROOKLYN, NY 11208
City:	BROOKLYN
State:	NY
Zip:	11208
Gender:	
Domain:	best-giveaways.com
Ip Address:	66.251.66.163


Full Name:	Andrew Bogod
First Name:	Andrew
Last Name:	Bogod
Address:	Brooklyn, NY, United States
Country Code:	US

Address:	2657 E 21st Street, Brooklyn, New York
Country:	US
City:	Brooklyn
State:	NY
Valid Since:	12/01/2020


Address:	21 Hill Street, Brooklyn, New York
Country:	US
City:	Brooklyn
State:	NY
Valid Since:	05/07/2018


Phone Number:	7183682117
Country Code:	1
Number:	7183682117
International Display:	+1 718-368-2117
Valid Since:	10/07/2021"""

varrr = """First Name:	SUZANNE
Last Name:	JACOB
State:	NY
City:	BROOKLYN
Address:	2657 E 21ST ST APT 2
Zip Code:	11235-2983

Name:	Suzanne Jacob
Reported Date:	03/21/2017
Gender:	Female

Name:	SUZANNE JACOB
First Name:	SUZANNE
Last Name:	JACOB
Latitude:	0.000000
Longitude:	0.000000
Gender:	
Registration Date:	2019-08-12
Own Rent:	own
Source:	work-from-home-directory.com
Domain:	gmail
Ip Address:	208.254.9.86

Full Name:	Suzanne Jacob
First Name:	Suzanne
Last Name:	Jacob
University Name N1:	Brooklyn College
University Degree N1:	Psychology
"""


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


async def holehe(email, message):
    command_output = f'holehe {email} --only-used --no-color'
    result = subprocess.check_output(command_output, shell=True, text=True)
    if result:
        res = result.split(' ')

        holehe = ''
        for x in res:
            if '\n[+]' in x and '*' not in x:
                holehe += x.strip('\n[+]')
                holehe += '\n'
        await message.answer(f'Email is registered on these websites:\n\n{holehe}')
    else:
        await message.answer(f'Email is not registered on any website!')

email_router = Router()

@email_router.message(F.text.regexp(r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'))
async def command_search_handler(message: Message) -> None:
    email = message.text

    import base64


    head = {'samu': '14d764ce3bf9708c2fb16b5e25289fbf963af290a%3A5%3A%7Bi%3A0%3BO%3A7%3A%22MongoId%22%3A1%3A%7Bs%3A8%3A%22objectID%22%3Bs%3A24%3A%2266e03e12c10085fefe0f4873%22%3B%7Di%3A1%3Bs%3A9%3A%22leo%20bogod%22%3Bi%3A2%3Bi%3A2592000%3Bi%3A3%3Ba%3A2%3A%7Bs%3A9%3A%22loginType%22%3Bs%3A8%3A%22customer%22%3Bs%3A9%3A%22ipAddress%22%3Bs%3A11%3A%2249.207.49.2%22%3B%7Di%3A4%3BO%3A7%3A%22MongoId%22%3A1%3A%7Bs%3A8%3A%22objectID%22%3Bs%3A24%3A%2266e1ae9f7fba74db99022f2c%22%3B%7D%7D'}

    
    r = requests.get(f'https://members.infotracer.com/customer/renderReport?id={base64.b32encode(bytearray("abc", 'ascii')).decode('utf-8')}', headers=head)
    if r:
        await message.answer(r.content)
    else:
        await message.answer("No result found or invalid response!")


    



    #search0t
    # asyncio.create_task(search0t(email, message))
    #holehe
    # asyncio.create_task(holehe(email, message))

    # chat_id = message.chat.id
    # url = "https://api.defastra.com/deep_email_check"

    # payload = {
    #     "timeout": "normal",
    #     "email": "dsfsdf@dsfsdf.sdf"
    # }
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/x-www-form-urlencoded",
    #     "X-API-KEY": "sdfsdf"
    # }
    # response = requests.post(url, data=payload, headers=headers)

    # print(response.text)

    #leakosint
    # data = {"token": LEAKOSINT_TOKEN, "request": email, "limit": 100, 'lang': 'en'} 
    # url = 'https://server.leakosint.com/' 
    # response = requests.post(url, json=data)
    # data = response.json()

    # if(data['NumOfResults'] == 1):
    #     await message.answer('Email has no breaches!')
    # else:
    #     leakosint = ''
    #     for info in data['List']:
    #         leakosint += f'{info}\n'
    #         for res in data['List'][info]['Data']:
    #             for key, value in res.items():
    #                 leakosint += f"\n{key}: {value}"
    #         leakosint += '\n\n'
    #     if len(leakosint) > 4096:
    #         for x in range(0, len(leakosint), 4096):
    #             await message.answer(leakosint[x:x+4096])
    #     else:
    #         await message.answer(leakosint)
    
    #whoxy
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
    #         await message.answer(whois)
    #     else:
    #         await message.answer('No domain registered on this email address!')
    
    
    #boardreader
    # r = requests.get(f'https://boardreader.com/return.php?query={email}&language=English')

    # data = r.json()

    # if data['TotalFound'] == 0:
    #     await message.answer(f'Email posted no website!')
    # else:
    #     boardreader = ''
    #     for info in data['SearchResults']:
    #         boardreader += f"{info['Url']}\n\n"
    #     await message.answer(f'Email posted one:\n\n{boardreader}')
    
    #dork
    # encoded_email = quote(email)
    # r = requests.get(f'https://www.google.com/search?q=%22{encoded_email}%22+site%3Acracked.io+OR+site%3Anulled.to+OR+site%3Aexplot.in+OR+site%3Areddit.com')


    # soup = BeautifulSoup(r.text, 'html.parser')
    # div_elements = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')

    # dork = ''
    # for div in div_elements:
    #     parent_a = div.find_parent('a')
    #     if parent_a:
    #         href = parent_a.get('href')
    #         text = div.text
    #         dork += f'{text}\nLink: {href.replace("/url?q=", "")}\n\n'
    # if dork:
    #     await message.answer(dork)
    # else:
    #     await message.answer('No dorks result!')

    #linkedin
    # url = "https://api.reversecontact.com/enrichment"

    # querystring = {"email":email,"apikey":REVERSE_CONTACT_API_KEY}

    # response = requests.request("GET", url, params=querystring).json()
    # if response['success']:
    #     fname = response['person']['firstName']
    #     lname = response['person']['lastName']
    #     photourl = response['person']['photoUrl']
    #     await message.answer(f"Linkedint:\n\nName: {fname} {lname}\nProfile picture: {photourl}")

    #files
    # email_to_search = email
    # filename = "data/text/@furyurl28042.txt"
    # search_result = search_email_in_file(email_to_search, filename)
    # if search_result:
    #     await message.answer(f'File Result 1: {search_result.strip()}')
    # filename = "data/text/@furyurl28043.txt"
    # search_result = search_email_in_file(email_to_search, filename)
    # if search_result:
    #     await message.answer(f'File Result 2: {search_result.strip()}')
    # filename = "data/text/discordUser2023_1.txt"
    # search_result = search_email_in_file(email_to_search, filename)
    # if search_result:
    #     with open(filename) as f:
    #         first_line = f.readline().strip('\n')
    #     await message.answer(f'Discord Result 3:\n\n{first_line}\n\n{search_result.strip()}')
    # filename = "data/text/discordUser2023_2.txt"
    # search_result = search_email_in_file(email_to_search, filename)
    # if search_result:
    #     with open(filename) as f:
    #         first_line = f.readline().strip('\n')
    #     await message.answer(f'Discord Result 4:\n\n{first_line}\n\n{search_result.strip()}')
    
    # csv_file_path = 'data/csv/disc.csv'
    # search_column = 'email'

    # matching_rows = search_in_csv(csv_file_path, search_column, email)
    # if matching_rows:
    #     await message.answer(f'Discord Result 5:\n\nUsername: {matching_rows}')


    # csv_file_path = 'data/csv/zloy.org.csv'
    # search_column = 'email'

    # matching_rows = search_in_csv(csv_file_path, search_column, email)
    # if matching_rows:
    #     await message.answer(f'Result 6:\n\n {matching_rows}')

    # csv_file_path = 'data/csv/opensc.ws.csv'
    # search_column = 'email'

    # matching_rows = search_in_csv(csv_file_path, search_column, email)
    # if matching_rows:
    #     await message.answer(f'Result 7:\n\n {matching_rows}')

    
    # csv_file_path = 'data/csv/inattack.ru_user.csv'
    # search_column = 'email'

    # matching_rows = search_in_csv(csv_file_path, search_column, email)
    # if matching_rows:
    #     await message.answer(f'Result 8:\n\n {matching_rows}')
    
    # csv_file_path = 'data/csv/carderpro.csv'
    # search_column = 'email'

    # matching_rows = search_in_csv(csv_file_path, search_column, email)
    # if matching_rows:
    #     await message.answer(f'Result 9:\n\n {matching_rows}')

    # sql_file_path = 'data/sql/opensc.ws.sql'

    # matching_lines = search_in_sql_file(sql_file_path, email)
    # if matching_lines:
    #     message.answer(f"SQL DB 1'{email}':")

    #     for line in matching_lines:
    #         await message.answer(line)

    # sql_file_path = 'data/sql/xakepok_xakepok.sql'

    # matching_lines = search_in_sql_file(sql_file_path, email)
    # if matching_lines:
    #     message.answer(f"SQL DB 2'{email}':")

    #     for line in matching_lines:
    #         await message.answer(line)

    # sql_file_path = 'data/sql/d.sql'

    # matching_lines = search_in_sql_file(sql_file_path, email)
    # if matching_lines:
    #     message.answer(f"SQL DB 3'{email}':")

    #     for line in matching_lines:
    #         await message.answer(line)

    # sql_file_path = 'data/sql/inattack.ru_user.sql'

    # matching_lines = search_in_sql_file(sql_file_path, email)
    # if matching_lines:
    #     message.answer(f"SQL DB 4'{email}':")

    #     for line in matching_lines:
    #         await message.answer(line)
    
    # sql_file_path = 'data/sql/zloy.org.sql'

    # matching_lines = search_in_sql_file(sql_file_path, email)
    # if matching_lines:
    #     message.answer(f"SQL DB 5'{email}':")

    #     for line in matching_lines:
    #         await message.answer(line)

    #seon
    
    # headers = {
    #     "X-API-KEY": SEON_API_KEY
    # }

    # r = requests.get(f"https://api.us-east-1-main.seon.io/SeonRestService/email-api/v2/{email}", headers=headers)
    # seon = r.text
    # if len(seon) > 4096:
    #     for x in range(0, len(seon), 4096):
    #         await message.answer(seon[x:x+4096])
    # else:
    #     await message.answer(seon)

    #woxy
    # r = requests.get(f'https://api.whoxy.com/?key=6f74300ecd4db96ct5a7d9148ca47c13f&reverse=whois&email={email}').text
    # woxy = r

    # if len(woxy) > 4096:
    #     for x in range(0, len(woxy), 4096):
    #         await message.answer(woxy[x:x+4096])
    # else:
    #     await message.answer(woxy)

    #teletype
    # headers = {
    #     "Authorization": TELETYPE_API_KEY
    # }

    # r = requests.get(f"api.usersbox.ru/v1/search?q={email}", headers=headers).json()
    

    #ghunt

    

    # asyncio.run(ghunt())
    # asyncio.create_task(ghunt(email, message))

    #avtar api
    # url = "https://avatarapi.com/v2/api.aspx"

    # payload = f'{{"username":"{AVATAR_API_USER}","password":"{AVATAR_API_PASS}","email":"{email}"}}'
    # headers = {
    # 'Content-Type': 'text/plain'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # res = response.json()
    # await message.answer(f"Avatar: {res['Image']}")
