from struct import pack
import asyncio
import inspect
import json
import utils.ghunt_email.config as config
from utils.ghunt_email.knowledge import get_origin_of_key, get_api_key, get_package_sig
from utils.ghunt_email.base import GHuntCreds
from utils.ghunt_email.utils import *
from utils.ghunt_email.errors import *
from utils.ghunt_email.parsers import Calendar, CalendarEvents, PlayedGames, PlayerAchievements
from datetime import datetime, timezone
from typing import *
from utils.ghunt_email.player.search_player_pb2 import PlayerSearchProto
from utils.ghunt_email.player.search_player_results_pb2 import PlayerSearchResultsProto
from utils.ghunt_email.player.get_player_pb2 import GetPlayerProto
from utils.ghunt_email.player.get_player_response_pb2 import GetPlayerResponseProto
from utils.ghunt_email.parsers import PlayerSearchResults
from utils.ghunt_email.parsers import PlayerProfile


class EndpointConfig(SmartObj):
    def __init__(self, headers: Dict[str, str], cookies: str):
        self.headers = headers
        self.cookies = cookies

class GAPI(SmartObj):
    def __init__(self):
        self.loaded_endpoints: Dict[str, EndpointConfig] = {}
        self.creds: GHuntCreds = None
        self.headers: Dict[str, str] = {}
        self.cookies: Dict[str, str] = {}
        self.gen_token_lock: asyncio.Semaphore = None

        self.authentication_mode: str = ""
        self.require_key: str = ""
        self.key_origin: str = ""

    def _load_api(self, creds: GHuntCreds, headers: Dict[str, str]):
        if not creds.are_creds_loaded():
            raise GHuntInsufficientCreds(f"This API requires a loaded GHuntCreds object, but it is not.")

        if not is_headers_syntax_good(headers):
            raise GHuntCorruptedHeadersError(f"The provided headers when loading the endpoint seems corrupted, please check it : {headers}")

        if self.authentication_mode == "oauth":
            self.gen_token_lock = asyncio.Semaphore(1)

        cookies = {}
        if self.authentication_mode in ["sapisidhash", "cookies_only"]:
            if not (cookies := creds.cookies):
                raise GHuntInsufficientCreds(f"This endpoint requires the cookies in the GHuntCreds object, but they aren't loaded.")

        if (key_name := self.require_key):
            if not (api_key := get_api_key(key_name)):
                raise GHuntInsufficientCreds(f"This API requires the {key_name} API key in the GHuntCreds object, but it isn't loaded.")
            if not self.key_origin:
                self.key_origin = get_origin_of_key(key_name)
            headers = {**headers, "X-Goog-Api-Key": api_key, **headers, "Origin": self.key_origin, "Referer": self.key_origin}

        if self.authentication_mode == "sapisidhash":
            if not (sapisidhash := creds.cookies.get("SAPISID")):
                raise GHuntInsufficientCreds(f"This endpoint requires the SAPISID cookie in the GHuntCreds object, but it isn't loaded.")

            headers = {**headers, "Authorization": f"SAPISIDHASH {gen_sapisidhash(sapisidhash, self.key_origin)}"}

        self.creds = creds
        self.headers = headers
        self.cookies = cookies

    def _load_endpoint(self, endpoint_name: str,
                        headers: Dict[str, str]={}, ext_metadata: Dict[str, str]={}):
        if endpoint_name in self.loaded_endpoints:
            return

        headers = {**headers, **self.headers}

        # https://github.com/googleapis/googleapis/blob/f8a290120b3a67e652742a221f73778626dc3081/google/api/context.proto#L43
        for ext_type,ext_value in ext_metadata.items():
            ext_bin_headers = {f"X-Goog-Ext-{k}-{ext_type.title()}":v for k,v in ext_value.items()}
            headers = {**headers, **ext_bin_headers}
        
        if not is_headers_syntax_good(headers):
            raise GHuntCorruptedHeadersError(f"The provided headers when loading the endpoint seems corrupted, please check it : {headers}")

        self.loaded_endpoints[endpoint_name] = EndpointConfig(headers, self.cookies)

    def _check_and_gen_authorization_token(self, as_client: httpx.Client, creds: GHuntCreds):
        # with self.gen_token_lock:
            present = False
            if self.api_name in creds.android.authorization_tokens:
                present = True
                token = creds.android.authorization_tokens[self.api_name]["token"]
                expiry_date = datetime.utcfromtimestamp(creds.android.authorization_tokens[self.api_name]["expiry"]).replace(tzinfo=timezone.utc)

            # If there are no registered authorization token for the current API, or if the token has expired
            if (not self.api_name in creds.android.authorization_tokens) or (present and datetime.now(timezone.utc) > expiry_date):
                token, _, expiry_timestamp = android_oauth_app(as_client, creds.android.master_token, self.package_name, self.scopes)
                creds.android.authorization_tokens[self.api_name] = {
                    "token": token,
                    "expiry": expiry_timestamp
                }
                creds.save_creds(silent=True)
                print(f"\n[+] New token for {self.api_name} has been generated")
            return token

    def _query(self, as_client: httpx.Client, verb: str, endpoint_name: str, base_url: str, params: Dict[str, Any], data: Any, data_type: str) -> httpx.Response:
        endpoint = self.loaded_endpoints[endpoint_name]
        headers = endpoint.headers
        if self.authentication_mode == "oauth":
            token = self._check_and_gen_authorization_token(as_client, self.creds)
            headers = {**headers, "Authorization": f"OAuth {token}"}

        if verb == "GET":
            req =  as_client.get(f"{self.scheme}://{self.hostname}{base_url}",
                params=params, headers=headers, cookies=endpoint.cookies)
        elif verb == "POST":
            if data_type == "data":
                req =  as_client.post(f"{self.scheme}://{self.hostname}{base_url}",
                    params=params, data=data, headers=headers, cookies=endpoint.cookies)
            elif data_type == "json":
                req =  as_client.post(f"{self.scheme}://{self.hostname}{base_url}",
                    params=params, json=data, headers=headers, cookies=endpoint.cookies)
            else:
                raise GHuntUnknownRequestDataTypeError(f"The provided data type {data_type} wasn't recognized by GHunt.")
        else:
            raise GHuntUnknownVerbError(f"The provided verb {verb} wasn't recognized by GHunt.")

        return req



def android_oauth_app(as_client: httpx.Client, master_token: str,
                package_name: str, scopes: List[str]) -> Tuple[str, List[str], int]:
    """
        Uses the master token to ask for an authorization token,
        with specific scopes and app package name.

        Returns the authorization token, granted scopes and expiry UTC timestamp.
    """
    client_sig = get_package_sig(package_name)

    data = {
        "app": package_name,
        "service": f"oauth2:{' '.join(scopes)}",
        "client_sig": client_sig,
        "Token": master_token
    }

    req =  as_client.post("https://android.googleapis.com/auth", data=data)
    resp = parse_oauth_flow_response(req.text)
    for keyword in ["Expiry", "grantedScopes", "Auth"]:
        if keyword not in resp:
            raise GHuntAndroidAppOAuth2Error(f'Expected "{keyword}" in the response of the Android App OAuth2 Authentication.\nThe master token may be revoked.')
    return resp["Auth"], resp["grantedScopes"].split(" "), int(resp["Expiry"])

class Parser(SmartObj):
    def _merge(self, obj) -> any:
        """Merging two objects of the same class."""

        def recursive_merge(obj1, obj2, module_name: str) -> any:
            directions = [(obj1, obj2), (obj2, obj1)]
            for direction in directions:
                from_obj, target_obj = direction
                for attr_name, attr_value in from_obj.__dict__.items():
                    class_name = get_class_name(attr_value)
                    if class_name.startswith(module_name) and attr_name in target_obj.__dict__:
                        merged_obj = recursive_merge(attr_value, target_obj.__dict__[attr_name], module_name)
                        target_obj.__dict__[attr_name] = merged_obj

                    elif not attr_name in target_obj.__dict__ or \
                        (attr_value and not target_obj.__dict__.get(attr_name)):
                        target_obj.__dict__[attr_name] = attr_value
            return obj1

        class_name = get_class_name(self)
        module_name = self.__module__
        if not get_class_name(obj).startswith(class_name):
            raise GHuntObjectsMergingError("The two objects being merged aren't from the same class.")

        self = recursive_merge(self, obj, module_name)

class CalendarHttp(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        
        if not headers:
            headers = config.headers

        base_headers = {}

        headers = {**headers, **base_headers}

        self.hostname = "clients6.google.com"
        self.scheme = "https"

        self.authentication_mode = "sapisidhash" # sapisidhash, cookies_only, oauth or None
        self.require_key = "calendar" # key name, or None

        self._load_api(creds, headers)

    def get_calendar(self, as_client: httpx.Client, calendar_id: str) -> Tuple[bool, Calendar]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/calendar/v3/calendars/{calendar_id}"
        data_type = None # json, data or None

        self._load_endpoint(endpoint_name)
        req =  self._query(as_client, verb, endpoint_name, base_url, None, None, data_type)

        # Parsing
        data = json.loads(req.text)

        calendar = Calendar()
        if "error" in data:
            return False, calendar
        
        calendar._scrape(data)

        return True, calendar

    def get_events(self, as_client: httpx.Client, calendar_id: str, params_template="next_events",
                        time_min=datetime.today().replace(tzinfo=timezone.utc).isoformat(), max_results=250, page_token="") -> Tuple[bool, CalendarEvents]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/calendar/v3/calendars/{calendar_id}/events"
        data_type = None # json, data or None
        params_templates = {
            "next_events": {
                "calendarId": calendar_id,
                "singleEvents": True,
                "maxAttendees": 1,
                "maxResults": max_results,
                "timeMin": time_min # ISO Format
            },
            "from_beginning": {
                "calendarId": calendar_id,
                "singleEvents": True,
                "maxAttendees": 1,
                "maxResults": max_results
            },
            "max_from_beginning": {
                "calendarId": calendar_id,
                "singleEvents": True,
                "maxAttendees": 1,
                "maxResults": 2500 # Max
            }
        }

        if not params_templates.get(params_template):
            raise GHuntParamsTemplateError(f"The asked template {params_template} for the endpoint {endpoint_name} wasn't recognized by GHunt.")

        params = params_templates[params_template]
        if page_token:
            params["pageToken"] = page_token

        self._load_endpoint(endpoint_name)
        req = self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)

        events = CalendarEvents()
        if not data:
            return False, events
        
        events._scrape(data)

        return True, events
    
class PlayGames(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        
        if not headers:
            headers = config.headers

        base_headers = {}

        headers = {**headers, **base_headers}

        # Android OAuth fields
        self.api_name = "playgames"
        self.package_name = "com.google.android.play.games"
        self.scopes = [
            "https://www.googleapis.com/auth/games.firstparty",
            "https://www.googleapis.com/auth/googleplay"
        ]
        
        self.hostname = "www.googleapis.com"
        self.scheme = "https"

        self.authentication_mode = "oauth" # sapisidhash, cookies_only, oauth or None
        self.require_key = None # key name, or None

        self._load_api(creds, headers)

    def get_profile(self, as_client: httpx.Client, player_id: str) -> Tuple[bool, PlayerProfile]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/games/v1whitelisted/players/{player_id}"
        data_type = None # json, data or None

        self._load_endpoint(endpoint_name)
        req =  self._query(as_client, verb, endpoint_name, base_url, None, None, data_type)

        # Parsing
        data = json.loads(req.text)
        player_profile = PlayerProfile()
        if not "displayPlayer" in data:
            return False, player_profile

        player_profile._scrape(data["displayPlayer"])
        player_profile.id = player_id

        return True, player_profile

    def get_played_games(self, as_client: httpx.Client, player_id: str, page_token: str="") -> Tuple[bool, str, PlayedGames]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/games/v1whitelisted/players/{player_id}/applications/played"
        data_type = None # json, data or None

        params = {}
        if page_token:
            params = {"pageToken": page_token}

        self._load_endpoint(endpoint_name)
        req = self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)
        played_games = PlayedGames()
        if not "items" in data:
            print(req)
            print(req.text)
            return False, "", played_games

        next_page_token = data.get("nextPageToken", "")

        played_games._scrape(data["items"])

        return True, next_page_token, played_games

    def get_achievements(self, as_client: httpx.Client, player_id: str, page_token: str="") -> Tuple[bool, str, PlayerAchievements]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "POST"
        base_url = f"/games/v1whitelisted/players/{player_id}/achievements"
        data_type = "json" # json, data or None

        params = {
            "state": "UNLOCKED",
            "returnDefinitions": True,
            "sortOrder": "RECENT_FIRST"
        }

        data = {}

        if page_token:
            params["pageToken"] = page_token

        self._load_endpoint(endpoint_name)
        req = self._query(as_client, verb, endpoint_name, base_url, params, data, data_type)

        # Parsing
        data = json.loads(req.text)
        achievements = PlayerAchievements()
        if not "items" in data:
            print(req)
            print(req.text)
            return False, "", achievements
        
        next_page_token = ""
        if "nextPageToken" in data:
            next_page_token = data["nextPageToken"]

        achievements._scrape(data)

        return True, next_page_token, achievements
    


class PlayGatewayPaGrpc(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()

        # Android OAuth fields
        self.api_name = "playgames"
        self.package_name = "com.google.android.play.games"
        self.scopes = [
            "https://www.googleapis.com/auth/games.firstparty",
            "https://www.googleapis.com/auth/googleplay"
        ]

        if not headers:
            headers = config.android_headers
            headers["User-Agent"] = headers["User-Agent"].format(self.package_name)

        headers = {**headers, **{
            "Content-Type": "application/grpc",
            "Te": "trailers"
        }}

        # Normal fields

        self.hostname = "playgateway-pa.googleapis.com"
        self.scheme = "https"

        self.authentication_mode = "oauth" # sapisidhash, cookies_only, oauth or None
        self.require_key = None # key name, or None

        self._load_api(creds, headers)

    def search_player(self, as_client: httpx.Client, query: str) -> PlayerSearchResults:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "POST"
        base_url = "/play.gateway.adapter.interplay.v1.PlayGatewayInterplayService/GetPage"
        data_type = "data"

        ext_metadata = {
            "bin": {
                "158709649": "CggaBgj22K2aARo4EgoI+aKnlZf996E/GhcQHhoPUkQyQS4yMTEwMDEuMDAyIgIxMToICgZJZ0pHVWdCB1BpeGVsIDU",
                "173715354": "CgEx"
            }
        }

        player_search = PlayerSearchProto()
        player_search.search_form.query.text = query
        payload = player_search.SerializeToString()

        prefix = bytes(1) + pack(">i", len(payload))
        data = prefix + payload

        self._load_endpoint(endpoint_name, {}, ext_metadata)
        req = self._query(as_client, verb, endpoint_name, base_url, None, data, data_type)

        # Parsing
        player_search_results = PlayerSearchResultsProto()
        player_search_results.ParseFromString(req.content[5:])

        parser = PlayerSearchResults()
        parser._scrape(player_search_results)

        return parser

    def get_player_stats(self, as_client: httpx.Client, player_id: str) -> PlayerProfile:
        """
            This endpoint client isn't finished, it is only used to get total played applications & achievements count.
            To get all the details about a player, please use get_player method of PlayGames (HTTP API).
        """

        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "POST"
        base_url = "/play.gateway.adapter.interplay.v1.PlayGatewayInterplayService/GetPage"
        data_type = "data"

        ext_metadata = {
            "bin": {
                "158709649": "CggaBgj22K2aARo4EgoI+aKnlZf996E/GhcQHhoPUkQyQS4yMTEwMDEuMDAyIgIxMToICgZJZ0pHVWdCB1BpeGVsIDU",
                "173715354": "CgEx"
            }
        }

        player_profile = GetPlayerProto()
        player_profile.form.query.id = player_id
        payload = player_profile.SerializeToString()

        prefix = bytes(1) + pack(">i", len(payload))
        data = prefix + payload

        self._load_endpoint(endpoint_name, {}, ext_metadata)
        req = self._query(as_client, verb, endpoint_name, base_url, None, data, data_type)

        # Parsing
        player_profile = GetPlayerResponseProto()
        player_profile.ParseFromString(req.content[5:])

        parser = PlayerProfile()
        parser._scrape(player_profile)

        return parser