import utils.ghunt_email.auth as auth
import sys
import utils.ghunt_email.gmaps as gmaps
import utils.ghunt_email.gcalendar as gcalendar
import httpx
from utils.ghunt_email.utils import get_httpx_client
from utils.ghunt_email.login import check_and_login
from utils.ghunt_email.peoplepa import PeoplePaHttp
from utils.ghunt_email.knowledge import get_user_type_definition


# from ghunt.helpers import gmaps, ,  calendar as gcalendar, ia


def hunt(as_client: httpx.Client, email_address: str, json_file= True):
    all_result = ""
    if not as_client:
        as_client = get_httpx_client()
 
    ghunt_creds = auth.load_and_auth(as_client)


    people_pa = PeoplePaHttp(ghunt_creds)
    is_found, target = people_pa.people_lookup(as_client, email_address, params_template="max_details")
    if not is_found:
        return "[GHUNT][-] The target wasn't found."

    if json_file:
        json_results = {}

    containers = target.sourceIds

    if len(containers) > 1 or not "PROFILE" in containers:
        print("[!] You have this person in these containers :")
        for container in containers:
            print(f"- {container.title()}")

    if not "PROFILE" in containers:
        return "[GHUNT][-] Given information does not match a public Google Account."

    container = "PROFILE"
    
    all_result += "🙋 Google Account data\n"
    

    # if container in target.names:
        # print(f"Name : {target.names[container].fullname}\n")

    if container in target.profilePhotos:
        if target.profilePhotos[container].isDefault:
            print("[-] Default profile picture")
            all_result += "[-] Default profile picture\n"
        else:
            print("[+] Custom profile picture !")
            all_result += "[+] Custom profile picture !\n"
            print(f"=> {target.profilePhotos[container].url}")
            all_result += f"=> {target.profilePhotos[container].url}\n"
            
            # await ia.detect_face(vision_api, as_client, target.profilePhotos[container].url)
            print()

    if container in target.coverPhotos:
        if target.coverPhotos[container].isDefault:
            print("[-] Default cover picture\n")
            all_result += "[-] Default cover picture\n"
        else:
            print("[+] Custom cover picture !")
            all_result += "[+] Custom cover picture !\n"
            print(f"=> {target.coverPhotos[container].url}")
            all_result += f"=> {target.coverPhotos[container].url}\n"

            # await ia.detect_face(vision_api, as_client, target.coverPhotos[container].url)
            print()

    print(f"Last profile edit : {target.sourceIds[container].lastUpdated.strftime('%Y/%m/%d %H:%M:%S (UTC)')}\n")
    all_result += f"Last profile edit : {target.sourceIds[container].lastUpdated.strftime('%Y/%m/%d %H:%M:%S (UTC)')}\n"
    
    if container in target.emails:
        print(f"Email : {target.emails[container].value}")
        all_result += f"Email : {target.emails[container].value}\n"

    else:
        print(f"Email : {email_address}\n")
        all_result += f"Email : {email_address}\n"

    print(f"Gaia ID : {target.personId}")
    all_result += f"Gaia ID : {target.personId}\n"

    if container in target.profileInfos:
        print("\nUser types :")
        all_result += "\nUser types :\n"

        for user_type in target.profileInfos[container].userTypes:
            definition = get_user_type_definition(user_type)
            print(f"- {user_type} {definition}")
            all_result += f"- {user_type} {definition}\n"

    all_result += "\n📞 Google Chat Extended Data\n"
    #print(f"Presence : {target.extendedData.dynamiteData.presence}")
    #all_result += f"Presence : {target.extendedData.dynamiteData.presence}\n"

    print(f"Entity Type : {target.extendedData.dynamiteData.entityType}")
    all_result += f"Entity Type : {target.extendedData.dynamiteData.entityType}\n"

    #print(f"DND State : {target.extendedData.dynamiteData.dndState}")
    print(f"Customer ID : {x if (x := target.extendedData.dynamiteData.customerId) else 'Not found.'}")
    all_result += f"Customer ID : {x if (x := target.extendedData.dynamiteData.customerId) else 'Not found.'}\n"

    all_result += "\n🌐 Google Plus Extended Data\n"
    print(f"Entreprise User : {target.extendedData.gplusData.isEntrepriseUser}")
    all_result += f"Entreprise User : {target.extendedData.gplusData.isEntrepriseUser}\n"

    #print(f"Content Restriction : {target.extendedData.gplusData.contentRestriction}")
    
    if container in target.inAppReachability:
        print("\n[+] Activated Google services :")
        all_result += "\n[+] Activated Google services :\n"
        for app in target.inAppReachability[container].apps:
            print(f"- {app}")
            all_result += f"- {app}\n"


    # print("\n🎮 Play Games data")

    # player_results =  playgames.search_player(ghunt_creds, as_client, email_address)
    # if player_results:
    #     player_candidate = player_results[0]
    #     print("\n[+] Found player profile !")
    #     print(f"\nUsername : {player_candidate.name}")
    #     print(f"Player ID : {player_candidate.id}")
    #     print(f"Avatar : {player_candidate.avatar_url}")
    #     _, player =  playgames.get_player(ghunt_creds, as_client, player_candidate.id)
    #     playgames.output(player)
    # else:
    #     print("\n[-] No player profile found.")

    print("\n🗺️ Maps data")
    all_result += "\n🗺️ Maps data\n"
    err, stats, reviews, photos =  gmaps.get_reviews(as_client, target.personId)
    review_locations = []
    for review in reviews:
        print("review", review.location.address, review.location.position.latitude, review.location.position.longitude)
        review_locations.append((review.location.position.latitude, review.location.position.longitude))
    map_result = gmaps.output(err, stats, reviews, photos, target.personId)
    all_result += map_result
    print("\n🗓️ Calendar data\n")
    all_result += "\n🗓️ Calendar data\n"

    cal_found, calendar, calendar_events = gcalendar.fetch_all(ghunt_creds, as_client, email_address)

    if cal_found:
        print("[+] Public Google Calendar found !\n")
        all_result += "[+] Public Google Calendar found !\n"
        calendar_output = ""
        if calendar_events.items:
            if "PROFILE" in target.names:
                calendar_output = gcalendar.out(calendar, calendar_events, email_address, target.names[container].fullname)
            else:
                calendar_output = gcalendar.out(calendar, calendar_events, email_address)
            all_result += calendar_output
        else:
            print("=> No recent events found.")
            all_result += "=> No recent events found.\n"

    else:
        print("[-] No public Google Calendar.")
        all_result += "[-] No public Google Calendar.\n"

    # if json_file:
    #     if container == "PROFILE":
    #         json_results[f"{container}_CONTAINER"] = {
    #             "profile": target,
    #             # "play_games": player if player_results else None,
    #             "maps": {
    #                 "photos": photos,
    #                 "reviews": reviews,
    #                 "stats": stats
    #             },
    #             "calendar": {
    #                 "details": calendar,
    #                 "events": calendar_events
    #             } if cal_found else None
    #         }
    #     else:
    #         json_results[f"{container}_CONTAINER"] = {
    #             "profile": target
    #         }

    # if json_file:
    #     result = json.dumps(json_results, cls=GHuntEncoder, indent=4)
    return all_result, review_locations
    # await as_client.aclose()

def ghunt(email):
    version = sys.version_info
    if (version < (3, 10)):
        print('[-] GHunt only works with Python 3.10+.')
        print(f'Your current Python version : {version.major}.{version.minor}.{version.micro}')
        return "[GHUNT][-] System Error"
    check_and_login(None)
    print("---")
    return hunt(None , email)
