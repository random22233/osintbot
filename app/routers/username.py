from flask import Blueprint, request, jsonify
import uuid
import re
import json
from datetime import datetime
import requests
import subprocess
import csv
import os
from utils.db_search import search_carderpro, search_discord_part1, search_discord_part2, search_inattack_part1 , search_inattack_part2, search_inattack_user, search_opensc_ws, search_xakepok, search_zloy_db

from utils.ghunt_email.ghunt import ghunt as run_ghunt

from dotenv import load_dotenv

from utils.get_reviews_screenshot import get_reviews_screenshot
from utils.onion_serch import scrape_onion

from utils.username import main as run_username

load_dotenv()
router = Blueprint('username', __name__)


@router.route('/username', methods=['POST'])
async def command_search_handler():
    # Get email from POST request body
    username = request.json.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
        
    print(f"Processing username: {username}")
    result = await run_username(username, "forums")
    return jsonify({'message': 'Username search completed', 'result': result}), 200

