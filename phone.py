from aiogram import F
from aiogram import Router
import requests
from aiogram.types import Message

from urllib.parse import quote


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

load_dotenv()

LEAKOSINT_TOKEN = os.getenv('LEAKOSINT_TOKEN')
SEON_API_KEY = os.getenv('SEON_API_KEY')
PHONE_VALIDATOR_API_KEY = os.getenv('SEON_API_KEY')

phone_router = Router()

@phone_router.message(F.text.regexp(r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'))
async def command_search_handler(message: Message) -> None:
    phone = message.text

    #leakosint
    data = {"token": LEAKOSINT_TOKEN, "request": phone, "limit": 100, 'lang': 'en'} 
    url = 'https://server.leakosint.com/' 
    response = requests.post(url, json=data)
    data = response.json()

    if(data['NumOfResults'] == 1):
        await message.answer('Email has no breaches!')
    else:
        leakosint = ''
        for info in data['List']:
            leakosint += f'{info}\n'
            for res in data['List'][info]['Data']:
                for key, value in res.items():
                    leakosint += f"\n{key}: {value}"
            leakosint += '\n\n'
        if len(leakosint) > 4096:
            for x in range(0, len(leakosint), 4096):
                await message.answer(leakosint[x:x+4096])
        else:
            await message.answer(leakosint)

    #fastpeoplesearch
    url = "https://devapi.endato.com/Phone/Enrich"

    payload = { "Phone": "(123) 456-7890" }
    headers = {
        "accept": "application/json",
        "galaxy-ap-name": "x",
        "galaxy-ap-password": "x",
        "galaxy-search-type": "x",
        "galaxy-client-session-id": "x",
        "galaxy-client-type": "x",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    #seon
    headers = {                 
        "X-API-KEY": SEON_API_KEY
    }

    r = requests.get(f"https://api.seon.io/SeonRestService/phone-api/v1/{phone}", headers=headers)
    await message.answer(r)


    #phone

    ph = requests.get(f'https://api.phonevalidator.com/api/v3/phonesearch?apikey={PHONE_VALIDATOR_API_KEY}&phone={phone}&type=fake,basic').json()
    await message.answer(ph)
