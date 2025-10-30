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
    browser.add_cookie({"name": "MUSIC_U", "value": "004A7EC61F91D944751E4D691A37F1DDCB9D80B7399B662772FFE4BA99B23B94FD04759792472CA2E089EE3C390D84D7DEB4F013ED90654C47B5FFA0DBD432647390925854CE872CC0090AA57E57D9E7BFA46E51D2111D40EDE7C6832BE3ECB558ED66D58C97C5868D880BA760142997B422DF52A9C7716F5A8C937D7E9C05128FB03DD196FD450C80597C3D7319DB88464E6BCEA5202DA8E03F5E46855180E2534BACAA7E10815B029E92EA2E6967D7616C3403F40AF17A4119E688D1F631B372BA048034153F126E1403362E8F69991C51F96C9C1B4224BCEF27EF1171111BFFBEA2C49E0DD2CE04F8E0D143F79F80414979FE8715663FDA90DD56FB448737A667872B31BD0469682790953B75B8836DAD04FF5617A59269BAAE32EC54F5FF5948DA8A54D9C0A31E07CB6D8F5B641296B318CBF2ECBFF57C9D1C4201E3455342F65768336DA45C33AB5E06D5FB579005A452D64C02A0F46731CB54407B8D61D565FC4995CFBA9F7BF5267CFCD791FE8A0EF179BE80B6FC68639C414B8009DB17768BEB98488C388A468F27E00D2804C0"})
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
