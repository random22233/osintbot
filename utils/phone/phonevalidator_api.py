import math
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_phonevalidator_data(phone):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        # Open the PhoneValidator website
        driver.get("https://www.phonevalidator.com/")

        # Wait for the input field to be present
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "GpofOvnvs"))
        )

        # now = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
        # current_directory = os.getcwd()
        # detail_filename = f"phonevalidator_detail_{id}_{now}.png"
        # detail_path = os.path.join(current_directory, detail_filename)
        # map_filename = f"phonevalidator_map_{id}_{now}.png"
        # map_path = os.path.join(current_directory, map_filename)
        # Enter a phone number in the input field
        phone_number = phone  # Replace this with the phone number you want to validate
        phone_input.send_keys(phone_number)

        # Click the submit button
        submit_button = driver.find_element(By.ID, "uznevtopsvc")
        driver.execute_script("arguments[0].click();", submit_button)
        # submit_button.click()

        # Take a screenshot of the first div with the class name 'col-sm-6'
        col_sm_6_div = driver.find_element(By.CLASS_NAME, "col-sm-6")
        data = col_sm_6_div.text
        if not "Phone Company:" in data:
            return True , "Phone Company: UNKOWN"
        data = data[data.index("Phone Company:"):]
        data = data[:data.index("\n")]
        # col_sm_6_div.screenshot(detail_path)

        # Wait for the result page to load, specifically the mapDiv element
        # iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/iframe")))
        # driver.switch_to.frame(iframe)
        # WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".place-card.place-card-medium"))
        # )
        # map_div = driver.find_element(By.ID , "mapDiv")
        # map_div.screenshot(map_path)
        return True , data
    except Exception as e:
        print("error in get_phonevalidator_data" , e)
        return False , e 
    finally:
        driver.quit()