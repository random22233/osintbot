from utils.ghunt_email.errors import GHuntKnowledgeError
from utils.ghunt_email.keys import keys

services_baseurls = {
    "cloudconsole": "console.cloud.google.com",
    "cl": "calendar.google.com"
}

sigs = {
    "com.google.android.play.games": "38918a453d07199354f8b19af05ec6562ced5788",
    "com.google.android.apps.docs": "38918a453d07199354f8b19af05ec6562ced5788",
    "com.google.android.youtube": "24bb24c05e47e0aefa68a58a766179d9b613a600",
    "com.android.chrome": "38918a453d07199354f8b19af05ec6562ced5788"
}

services_baseurls = {
    "cloudconsole": "console.cloud.google.com",
    "cl": "calendar.google.com"
}

user_types = {
    "USER_TYPE_UNKNOWN": "The user type is not known.", # Official
    "GOOGLE_USER": "The user is a Google user.", # Official
    "GPLUS_USER": "The user is a Currents user.", # Official
    "GOOGLE_APPS_USER": "The user is a Google Workspace user.", # Official
    "OWNER_USER_TYPE_UNKNOWN": "The user type is not known.", # Guess
    "GPLUS_DISABLED_BY_ADMIN": "This user's Currents account has been disabled by an admin.", # Guess
    "GOOGLE_APPS_USER": "The user is a Google Apps user.", # Guess
    "GOOGLE_FAMILY_USER": "The user is a Google Family user.", # Guess
    "GOOGLE_FAMILY_CHILD_USER": "The user is a Google Family child user.", # Guess
    "GOOGLE_APPS_ADMIN_DISABLED": "This admin of Google Apps has been disabled.", # Guess
    "GOOGLE_ONE_USER": "The user is a Google One user.", # Guess
    "GOOGLE_FAMILY_CONVERTED_CHILD_USER": "This Google Family user was converted to a child user." # Guess
}

types_translations = {
    'airport': 'Airport',
    'atm': 'ATM',
    'bar': 'Bar',
    'bank_intl': 'Bank',
    'bus': 'Bus',
    'cafe': 'Café',
    'camping': 'Camping',
    'cemetery': 'Cemetery',
    'civic_bldg': 'Civic building',
    'ferry': 'Ferry',
    'gas': 'Gas',
    'generic': 'Generic',
    'golf': 'Golf',
    'hospital_H': 'Hospital H',
    'library': 'Library',
    'lodging': 'Lodging',
    'monument': 'Monument',
    'movie': 'Movie',
    'museum': 'Museum',
    'parking': 'Parking',
    'police': 'Police',
    'postoffice': 'Post office',
    'restaurant': 'Restaurant',
    'school': 'School',
    'shoppingbag': 'Shopping bag',
    'shoppingcart': 'Shopping cart',
    'train': 'Train',
    'tram': 'Tram',
    'tree': 'Park',
    'worship_buddhist': 'Worship Buddhist',
    'worship_christian': 'Worship Christian',
    'worship_hindu': 'Worship Hindu',
    'worship_islam': 'Worship Islam',
    'worship_jewish': 'Worship Jewish',
    'worship_sikh': 'Worship Sikh',
    'worship_jain': 'Worship Jain'
}

def get_gmaps_type_translation(type_name: str) -> str:
    if type_name not in types_translations:
        raise GHuntKnowledgeError(f'The gmaps type "{type_name}" has not been found in GHunt\'s knowledge.\nPlease open an issue on the GHunt Github or submit a PR to add it !')
    return types_translations.get(type_name)

def get_user_type_definition(type_name: str) -> str:
    if type_name not in user_types:
        raise GHuntKnowledgeError(f'The user type "{type_name}" has not been found in GHunt\'s knowledge.\nPlease open an issue on the GHunt Github or submit a PR to add it !')
    return user_types.get(type_name)

def get_domain_of_service(service: str) -> str:
    if service not in services_baseurls:
        raise GHuntKnowledgeError(f'The service "{service}" has not been found in GHunt\'s services knowledge.')
    return services_baseurls.get(service)

def get_origin_of_key(key_name: str) -> str:
    if key_name not in keys:
        raise GHuntKnowledgeError(f'The key "{key_name}" has not been found in GHunt\'s API keys knowledge.')
    return keys.get(key_name, {}).get("origin")

def get_api_key(key_name: str) -> str:
    if key_name not in keys:
        raise GHuntKnowledgeError(f'The key "{key_name}" has not been found in GHunt\'s API keys knowledge.')
    return keys.get(key_name, {}).get("key")

def get_package_sig(package_name: str) -> str:
    if package_name not in sigs:
        raise GHuntKnowledgeError(f'The package name "{package_name}" has not been found in GHunt\'s SIGs knowledge.')
    return sigs.get(package_name)