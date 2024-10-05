from aiogram import F
from aiogram import Router
import requests
from aiogram.types import Message, FSInputFile
from datetime import datetime
from urllib.parse import quote
from utils.get_reviews_screenshot import get_reviews_screenshot


import subprocess
from aiogram import Router


# from selenium_driverless import webdriver
# from selenium_driverless.types.by import By
import asyncio
# from capmonstercloudclient import CapMonsterClient, ClientOptions
# from capmonstercloudclient.requests import HcaptchaProxylessRequest
from bs4 import BeautifulSoup
import csv
import os
from dotenv import load_dotenv
from utils.phone.endato_api import get_endato_data, get_endato_person_data
from utils.phone.leak_osint_api import get_leak_osint_data
from utils.phone.phonevalidator_api import get_phonevalidator_data
from utils.phone.quidam_api import get_forgot_password_data
from utils.phone.uber_api import check_uber_forgot_password
from utils.phone.userbox_api import get_userbox_data
from utils.phone.facebook_api import get_facebookdata


load_dotenv()

LEAKOSINT_TOKEN = os.getenv('LEAKOSINT_TOKEN')
SEON_API_KEY = os.getenv('SEON_API_KEY')
PHONE_VALIDATOR_API_KEY = os.getenv('SEON_API_KEY')

phone_router = Router()

async def send_text_file(message: Message, file_content, file_path, file_name):
    """Sends an in-memory text file to a Telegram chat."""
    with open(file_path , "w") as f:
        f.write(file_content)
    document = FSInputFile(file_path, filename=file_name)
    await message.answer_document(document=document)
    os.remove(file_path)

@phone_router.message(F.text.regexp(r'^(?!.*@.*)(.*\d.*){8,}$'))
async def command_search_handler(message: Message) -> None:
    phone = message.text
    print("\n\n*** searching for phone:" , phone , "\n\n")
    try:
        await message.answer("getting FACEBOOK forgot password data: \n")
        # result = check_uber_forgot_password(phone)
        result = get_facebookdata(phone)
        await message.answer(str(result))
    except Exception as e:
        print("error in getting FACEBOOK forgot password data", e)
        await message.answer(f"error in getting FACEBOOK forgot password data: {e} \n")
    try:
        await message.answer("getting endato data: \n")
        result, coords = get_endato_data(phone)   
        if len(coords) > 0:
            screenshot_path, map_path = await get_reviews_screenshot(coords, message.message_id)
            photo = FSInputFile(screenshot_path )
            await message.answer_photo(photo=photo)
            os.remove(screenshot_path)
            os.remove(map_path)
        print("result of endato data " , result, "\n\n")
          
        await message.answer(str(result))
    except Exception as e:
        print("error in getting endato data:" , e )
        await message.answer(f"error in getting endato data: {e} \n")

    try:
        await message.answer("getting endato person data: \n")
        result, coords = get_endato_person_data(phone)
        if result and len(result) > 0 :
            now = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
            current_directory = os.getcwd()
            messages_filename = f"messages_{message.message_id}_{now}.txt"
            messages_path = os.path.join(current_directory, messages_filename)
            await  send_text_file(message, str(result), messages_path, messages_filename)
        if len(coords) > 0:
            screenshot_path, map_path = await get_reviews_screenshot(coords, message.message_id)
            photo = FSInputFile(screenshot_path )
            await message.answer_photo(photo=photo)
            os.remove(screenshot_path)
            os.remove(map_path)
        # print("result of endato data " , result, "\n\n")
        
    except Exception as e:
        print("error in getting endato person data:" , e )
        await message.answer(f"error in getting endato person data: {e} \n")

    try:
        await message.answer("getting phonevalidator data: \n")        
        result, data = get_phonevalidator_data(phone)
        if result :
            await message.answer(str(data))
        else: 
            await message.answer("error in getting phonevalidator" + str(data))
    except Exception as e:
        print("error in getting phonevalidator data", e)
        await message.answer(f"error in getting phonevalidator data: {e} \n")
        

    try:
        await message.answer("getting userbox data: \n")
        result = get_userbox_data(phone)
        await message.answer(str(result))
    except Exception as e:
        print("error in getting userbox data", e)
        await message.answer(f"error in getting userbox data: {e} \n")
        
    try:
        await message.answer("getting leak osint data: \n")
        result = get_leak_osint_data(phone)
        await message.answer(str(result))
    except Exception as e:
        print("error in getting leak osint data", e)
        await message.answer(f"error in getting leak osint data: {e} \n")


    try:
        await message.answer("getting QUIDAM forgot password data: \n")
        # result = check_uber_forgot_password(phone)
        result = get_forgot_password_data(phone)
        await message.answer(str(result))
    except Exception as e:
        print("error in getting forgot password data", e)
        await message.answer(f"error in getting forgot password data: {e} \n")

    #leakosint
    # data = {"token": LEAKOSINT_TOKEN, "request": phone, "limit": 100, 'lang': 'en'} 
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

    # #fastpeoplesearch
    # url = "https://devapi.endato.com/Phone/Enrich"

    # payload = { "Phone": "(123) 456-7890" }
    # headers = {
    #     "accept": "application/json",
    #     "galaxy-ap-name": "x",
    #     "galaxy-ap-password": "x",
    #     "galaxy-search-type": "x",
    #     "galaxy-client-session-id": "x",
    #     "galaxy-client-type": "x",
    #     "content-type": "application/json"
    # }

    # response = requests.post(url, json=payload, headers=headers)

    # print(response.text)

    # #seon
    # headers = {                 
    #     "X-API-KEY": SEON_API_KEY
    # }

    # r = requests.get(f"https://api.seon.io/SeonRestService/phone-api/v1/{phone}", headers=headers)
    # await message.answer(r)


    # #phone

    # ph = requests.get(f'https://api.phonevalidator.com/api/v3/phonesearch?apikey={PHONE_VALIDATOR_API_KEY}&phone={phone}&type=fake,basic').json()
    # await message.answer(ph)
