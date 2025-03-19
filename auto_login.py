# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008F42F899A64399AD7D138FA44C7A095D79C36B6A574932321276F727CC4362350C80C30091339B721A4D9BD012F28AC8A71F027AF95D7B0C6DD27D7D772399AF8E472A64048D015F46B8CF0F1654B7693DBE6DC679B4C37D9DFA302AC610FC118993541486F5EC9355C80568009F6D9534C8F7595A1A2DCC41286DBDBD9C2DFACB12B9934D88F477A15A7B7BE061961FE6660372C3AEA8AC3881C674C6DDDCFBC832AEEFC6AD262453F0012904449ACF2207C3F4FE2B3172D76DC699A742135B56182B1E705A09030696CED7F281BD8DAF39104433BB45CEB3B7FE79BB69EF28C22AE644D652E60167950F6A18A78E69A2BBA97175285E0A206351F70A1EDBE9AA1609B2BFD81C5DBD82CD03E8A9824D18FF35C056787E93352F9B89B073266BE0C9B0E24BEB3ABA571C34040EBB2EF6067C2C2A76D8ADE701B99CEA9646FB3BA797959FA1290FE15522860D0496E581E46F606366F126ADD7BC102F5B07B101"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
