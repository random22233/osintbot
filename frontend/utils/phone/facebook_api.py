from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_facebookdata(phone):
    # Set up Firefox options (e.g., headless mode if necessary)
    options = Options()
    # Uncomment the next line if you want to run in headless mode (no browser UI)
    options.add_argument("--headless")

    # Set up the Firefox WebDriver
    driver = webdriver.Firefox(options=options)

    try:
        # Open the Facebook recovery page
        driver.get('https://www.facebook.com/login/identify')

        # Give the page some time to load
        time.sleep(3)

        # Find the email/phone input field and enter the phone number
        email_or_phone_input = driver.find_element(By.ID, 'identify_email')
        email_or_phone_input.send_keys(phone)

        # Submit the form
        email_or_phone_input.send_keys(Keys.RETURN)

        # Wait for the results to load
        time.sleep(1)

        form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_form')))

        data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_9o4d')))

        print(form , data)
        tds = driver.find_elements(By.CLASS_NAME , "_9o4d")
        accounts = []
        for td in tds:
            # target_name = td.find_element(By.CLASS_NAME , "_9o4d")
            accounts.append(td.text)

        return str(accounts)
    except Exception as e:
        print( "Error in gettign facebook forgot password data" + str(e))
        return "No facebook account founded"
    finally:
        pass
        # Close the browser after the task is done
        driver.quit()