import os

from random import random
from time import sleep
from datetime import datetime

from dotenv import load_dotenv

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from super_eureka import logging

load_dotenv()

def create_driver():
    user_data_dir = os.getenv('CHROME_USER_DATA_DIR')
    profile_folder = os.getenv('CHROME_PROFILE_FOLDER')
    chromedriver_execurable_path = os.getenv('CHROMEDRIVER_EXECUTABLE_PATH')

    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument(f'--profile-folder={profile_folder}')
    driver = Chrome(executable_path=chromedriver_execurable_path, options=options)
    return driver

def begin_export() -> None:
    now = datetime.now()

    logging.initialize()
    logging.info(f'Initializing export. Current time: {repr(now)}')

    driver = create_driver()
    driver.get(os.getenv('EXPORT_START_URL'))

    try:
        sign_w_google_link = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in with Google']")))
        sleep(random() * 2.0 + 1.0)
        sign_w_google_link.click()
    except:
        logging.info('Could not find \'Sign in with Google\' button. Maybe the page took too long to load.')
        return

    try:
        login_email = os.getenv('HUBSPOT_LOGIN_EMAIL')
        sign_in_email = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{login_email}')]")))
        sleep(random() * 2.0 + 1.0)
        sign_in_email.click()
    except:
        logging.info(f'Could not find the desired login email ({login_email}) to login. Maybe you don\'t have it currently on the browser storage or the page took too long to load.')
        return

    try:
        export_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//i18n-string[text()='Export']")))
        sleep(random() * 2.0 + 1.0)
        export_btn.click()
    except:
        logging.info('Could not find the (gray) export button. Maybe the page took too long to load.')
        return
    
    try:
        export_confirm_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//i18n-string[@data-key='exportDialog.exportCta']")))
        export_confirm_btn.click()
    except:
        logging.info('Could not find the confirmation button (orange). Maybe the page took too long to load.')
        return
    
    sleep(10)
    driver.quit()

if __name__ == '__main__':
    begin_export()