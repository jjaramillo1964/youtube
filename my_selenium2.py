import time
import threading
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
from random import shuffle
import os
import json
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
# Auto-install ChromeDriver
chromedriver_autoinstaller.install()

def create_driver(user_agent):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver
# Mouse movement simulation
def random_mouse_move(driver):
    try:
        window_width = driver.execute_script("return window.innerWidth;")
        window_height = driver.execute_script("return window.innerHeight;")
        action = ActionChains(driver)
        x_offset = random.randint(-window_width // 2, window_width // 2)
        y_offset = random.randint(-window_height // 2, window_height // 2)
        action.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"Mouse move error: {e}")

# Main function
def run_thread(keyword, email, password):
    # options = webdriver.ChromeOptions()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--start-maximized')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-gpu')

    # driver = uc.Chrome(options=options)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    ]

    
    user_agent = random.choice(user_agents)
    driver = create_driver(user_agent)
    # YouTube login
    driver.get("https://www.youtube.com/")
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@aria-label="Sign in"]').click()
        time.sleep(2)
        driver.find_element(By.ID, "identifierId").send_keys(email, Keys.RETURN)
        time.sleep(10)
        driver.find_element(By.NAME, "Passwd").send_keys(password, Keys.RETURN)
        time.sleep(5)
    except Exception as e:
        print(f"Login error: {e}")

    # Play the playlist
    driver.get("https://www.youtube.com/@Boymuscleworkout/playlists")
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, f'//*[@title="{keyword}"]').click()
        time.sleep(5)
        loop_button = driver.find_element(By.XPATH, '//button[@aria-label="Loop playlist"]')
        driver.execute_script("arguments[0].click();", loop_button)
    except Exception as e:
        print(f"Error playing playlist: {e}")

    # Keep running and take screenshots
    while True:
        driver.save_screenshot(f"screenshots/screenshot_{keyword}_{int(time.time())}.png")
        print(f"Screenshot taken for {keyword}")
        time.sleep(300)  # 5 mins
        random_mouse_move(driver)

    driver.quit()

# CLI args
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Selenium YouTube bot")
    parser.add_argument("--email", required=True, help="Email for YouTube login")
    parser.add_argument("--password", required=True, help="Password for YouTube login")
    args = parser.parse_args()

    keywords = ["honguynvn04", "tindang", "abskwkws", "hieuvilai2007", "365ngynhem"]
    threads = []
    for keyword in keywords:
        thread = threading.Thread(target=run_thread, args=(keyword, args.email, args.password))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
