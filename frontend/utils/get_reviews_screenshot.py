import math
from datetime import datetime

import folium
# from PIL import Image
# import io
from selenium_driverless import webdriver
import time
import os


async def create_map_with_custom_markers(coordinates, zoom, id):
    m = folium.Map(location=calculate_middle(coordinates)[0], zoom_start=zoom)
    icon = './utils/marker.webp'
    for coord in coordinates:
        folium.Marker(
            location=coord,
            icon=folium.CustomIcon(icon, icon_size=(15, 30))  # Adjust icon size as needed
        ).add_to(m)
    now = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
    current_directory = os.getcwd()
    map_filename = f"map_{id}_{now}.html"
    map_path = os.path.join(current_directory, map_filename)
    m.save(map_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = await webdriver.Chrome(options=options)
    await driver.get('file://' + os.path.realpath(map_path))
    time.sleep(2)
    #await driver.get_screenshot_as_png()
    screenshot_filename = f"google_maps_map_element_{id}_{now}.png"
    screenshot_path = os.path.join(current_directory, screenshot_filename)
    await driver.save_screenshot(screenshot_path)
    await driver.quit()
    return screenshot_path, map_path

def calculate_middle(coordinates):
    latitudes = [coord[0] for coord in coordinates]
    longitudes = [coord[1] for coord in coordinates]
    if len(coordinates) == 1:
       return [(latitudes[0],longitudes[0])]

    # Determine the min and max lat/lon
    max_lat = max(latitudes)
    min_lat = min(latitudes)
    max_lon = max(longitudes)
    min_lon = min(longitudes)
    center_lat = (max_lat + min_lat)/2
    center_lon = (max_lon + min_lon)/2
    print([(center_lat,center_lon)])
    return [(center_lat,center_lon)]
def calculate_zoom_level(coordinates):
    # Extract latitude and longitude separately
    latitudes = [coord[0] for coord in coordinates]
    longitudes = [coord[1] for coord in coordinates]

    # Determine the min and max lat/lon
    max_lat = max(latitudes)
    min_lat = min(latitudes)
    max_lon = max(longitudes)
    min_lon = min(longitudes)

    # Calculate the latitude and longitude differences
    delta_lat = max_lat - min_lat
    delta_lon = max_lon - min_lon

    # Calculate the maximum of the differences
    max_delta = max(delta_lat, delta_lon)

    if max_delta == 0:
        return 18
    # Basic zoom level formula
    zoom = math.log2(360 / max_delta)

    print("zoom:" , zoom)

    # Clamp the zoom level to folium's typical range (1 to 18)
    zoom = max(4, min(zoom, 18))

    return round(zoom)


async def get_reviews_screenshot(coords , id):
    print("\n\n" , coords)
    zoom = calculate_zoom_level(coords)
    return await create_map_with_custom_markers(coords, zoom, id)
