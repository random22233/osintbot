import sys
from aiogram import F
import base64
import time
import requests
import sys
from aiogram import Router
import io

from aiogram.types import Message


from aiogram import Bot, Router
from aiogram.enums import ParseMode

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

# bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

photo_router = Router()

@photo_router.message(F.content_type.in_({'photo'}))
async def command_search_handler(message: Message) -> None:
    chat_id = message.chat.id
    photo_file_id = message.photo[-1].file_id

    downloadDir = 'images/'

    # photo_path = f"images/{photo_file_id}.jpg"
    photo_path = os.path.join(os.path.dirname(__file__), downloadDir, f"{photo_file_id}.jpg")
    file = await bot.get_file(photo_file_id)
    await bot.download_file(file.file_path, photo_path)
    try:
        site = 'https://facecheck.id'
        FACE_CHECK_TOKEN = os.getenv('FACECHECK_API_KEY') # Replace with your actual token
        imageUrls = [f'{photo_file_id}.jpg']

        print(os.path.join(os.path.dirname(__file__), downloadDir, imageUrls[0]))

        files = {'images': open(os.path.join(os.path.dirname(__file__), downloadDir, imageUrls[0]), 'rb'), 'id_search': None}

        print("image searching...")
        await message.answer("image searching...")

        headers = {
            'accept': 'application/json',
            'Authorization': FACE_CHECK_TOKEN,
        }

        url = site + '/api/upload_pic'

        response = requests.post(url, files=files, headers=headers).json()

        id_search = response['id_search']
        print(response['message'], 'id_search='+id_search)
        json_data = {'id_search': id_search, 'with_progress': True, 'status_only': False, 'demo': False}

        while True:
            response = requests.post(site+'/api/search', headers=headers, json=json_data).json()
            print(response)
            if response['error']:
                await message.answer("ERROR!")
                break
            if response['output']:
                count = 1
                for im in response['output']['items']:
                    score = im['score']
                    url = im['url']
                    # image_base64 = im['base64']
                    # print(f"{score} {url} {image_base64[:32]}...")
                    # imagebytes = base64.b64decode(image_base64)
                    # input_file = io.BytesIO(imagebytes)
                    await message.answer(f'Score: {score}\nSource: {url}')
                    # await bot.send_photo(chat_id, input_file, caption=f"Score: {score}\nSource: {url}")0
                    if(count == 10):
                        break
                    count += 1
                break
            await message.answer(f'{response["message"]} progress: {response["progress"]}%')
            time.sleep(1)
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)