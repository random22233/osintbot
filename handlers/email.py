from aiogram import F
from aiogram import Router
import requests
from aiogram.types import Message
import urllib.parse

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

from ghunt.helpers.gmail import is_email_registered


async def ghunt(email, message):
    as_client = httpx.AsyncClient()
    is_registered = await is_email_registered(as_client, str(email))
    if is_registered:
        return await message.answer("Registered on Google : True")
    return await message.answer("Registered on Google : False")



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

    #seon
    
    headers = {
        "X-API-KEY": "f06cfbbb-4d96-4ce4-87eb-dba1479eaeff"
    }

    r = requests.get(f"https://api.us-east-1-main.seon.io/SeonRestService/email-api/v2/{email}", headers=headers)
    seon = r.text

    # await message.answer()
    if len(seon) > 4096:
        for x in range(0, len(seon), 4096):
            await message.answer(seon[x:x+4096])
    else:
        await message.answer(seon)

    #woxy
    r = requests.get(f'https://api.whoxy.com/?key=6f74300ecd4db96ct5a7d9148ca47c13f&reverse=whois&email={email}').text
    woxy = r

    if len(woxy) > 4096:
        for x in range(0, len(woxy), 4096):
            await message.answer(woxy[x:x+4096])
    else:
        await message.answer(woxy)

    #ghunt

    

    # asyncio.run(ghunt())
    asyncio.create_task(ghunt(email, message))

    #avtar api
    # url = "https://avatarapi.com/v2/api.aspx"

    # payload = f'{{"username":"{AVATAR_API_USER}","password":"{AVATAR_API_PASS}","email":"{email}"}}'
    # headers = {
    # 'Content-Type': 'text/plain'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # res = response.json()
    # await message.answer(f"Avatar: {res['Image']}")
