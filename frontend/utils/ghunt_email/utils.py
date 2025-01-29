import hashlib
import httpx
import imagehash
from io import BytesIO
from PIL import Image
from typing import *
from time import time
from utils.ghunt_email.base import SmartObj
from dateutil.parser import isoparse
from datetime import timezone

class TMPrinter(SmartObj):
    def __init__(self):
        self.max_len = 0

    def out(self, text: str):
        if len(text) > self.max_len:
            self.max_len = len(text)
        else:
            text += (" " * (self.max_len - len(text)))
        print(text, end='\r')

    def clear(self):
    	print(" " * self.max_len, end="\r")

class Client(httpx.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _merge_cookies(self, cookies: dict):
        """Don't save the cookies in the client."""
        return cookies

def ppnb(nb: float|int) -> float:
    """
        Pretty print float number
        Ex: 3.9 -> 3.9
            4.0 -> 4
            4.1 -> 4.1
    """
    try:
        return int(nb) if nb % int(nb) == 0.0 else nb
    except ZeroDivisionError:
        if nb == 0.0:
            return 0
        else:
            return nb

def get_datetime_utc(date_str):
    """Converts ISO to datetime object in UTC"""
    date = isoparse(date_str)
    margin = date.utcoffset()
    return date.replace(tzinfo=timezone.utc) - margin

def get_class_name(obj) -> str:
        return str(obj).strip("<>").split(" ")[0]

def unicode_patch(txt: str):
    bad_chars = {
        "é": "e",
        "è": "e",
        "ç": "c",
        "à": "a"
    }
    return txt.replace(''.join([*bad_chars.keys()]), ''.join([*bad_chars.values()]))


def get_url_image_flathash(as_client: httpx.AsyncClient, image_url: str) -> str:
    req =  as_client.get(image_url)
    img = Image.open(BytesIO(req.content))
    flathash = imagehash.average_hash(img)
    return str(flathash)

def is_default_profile_pic(as_client: httpx.Client, image_url: str) -> Tuple[bool, str]:
    """
        Returns a boolean which indicates if the image_url
        is a default profile picture, and the flathash of
        the image.
    """
    flathash = get_url_image_flathash(as_client, image_url)
    if imagehash.hex_to_flathash(flathash, 8) - imagehash.hex_to_flathash("000018183c3c0000", 8) < 10 :
        return True, str(flathash)
    return False, str(flathash)

def get_httpx_client() -> httpx.Client:
    """
        Returns a customized to better support the needs of GHunt CLI users.
    """
    return Client(http2=True, timeout=15)
    # return AsyncClient(http2=True, timeout=15, proxies="http://127.0.0.1:8282", verify=False)


def is_headers_syntax_good(headers: Dict[str, str]) -> bool:
    try:
        httpx.Headers(headers)
        return True
    except:
        return False
    

def gen_sapisidhash(sapisid: str, origin: str, timestamp: str = str(int(time()))) -> str:
    return f"{timestamp}_{hashlib.sha1(' '.join([timestamp, sapisid, origin]).encode()).hexdigest()}"

def parse_oauth_flow_response(body: str):
    """
        Correctly format the response sent by android.googleapis.com
        during the Android OAuth2 Login Flow.
    """
    return {sp[0]:'='.join(sp[1:]) for x in body.split("\n") if (sp := x.split("="))}