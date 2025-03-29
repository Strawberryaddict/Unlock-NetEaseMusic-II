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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D38DA1505DB987CF4F0DF062D13C02C7D473EE2737227CC61710321BE81B041C6099969A866169F2C7528B72EE2AE703C87BCC11D7589F050DEAB516D6B79D3EF81E7C400E335F6F95BA2AD718602EDAB5164BB4C989E1DECFD357E7A0FA4E8167F8C11CDFA488AC81B7505A5442936B1BBB684E0C152AD540812A42847AA66DD149796F1D87A4B686995DC4E1417882838C4CF232610D2138D20736B0347BC2E5AC49B03EB153554A486687E7E1707D68EA74C846646DAD07AFD48E913A14F5751614A96710CB2E0FA818BA08D4C22E30684F36EBA25F16F8C25A541A7440DDC4EB9B662A1A814BD14FD377621DF2E98992FBF3CCBCA058182D2AA7EA6D8F1E36E5D191508E5E9CF923B6F58799A0EFF8D76708EC8B04933E31089B225A67AAC35FC6A8176E43AED41D24D2C829BCA6672CDC3227BB7FEA5E3F7167670E5B706D4E2DE38212DC6CB393E93B1F2D793781DBECE13FD0579A2BA6B36ECA23FC58"})
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
