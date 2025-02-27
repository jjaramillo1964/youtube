import time
import threading
import random
import platform
import argparse  # Import argparse for command-line arguments
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

# Automatically install the ChromeDriver and get its path
chromedriver_autoinstaller.install()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
]

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

def scroll_down(driver):
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 300);")
        random_delay(1, 3)

def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def perform_human_like_actions(driver, element):
    actions = ActionChains(driver)
    
    try:
        actions.move_to_element(element).perform()
        random_delay(0.5, 1.0)

        offset_x = random.randint(-element.size['width'] // 4, element.size['width'] // 4)
        offset_y = random.randint(-element.size['height'] // 4, element.size['height'] // 4)

        actions.move_by_offset(offset_x, offset_y).click().perform()
        print(f"Clicked at offset ({offset_x}, {offset_y})")
        actions.move_by_offset(-offset_x, -offset_y).perform()

    except WebDriverException as e:
        print(f"Failed to click element: {e}")

def run_thread(links, thread_id, email, password):
    MAX_DRIVERS = 5
    drivers = []
    os.makedirs("screenshots", exist_ok=True)

    for i in range(min(len(links), MAX_DRIVERS)):
        driver = create_driver(user_agents[i % len(user_agents)])
        drivers.append(driver)
        try:
            driver.get("https://www.youtube.com/")

            time.sleep(2)
            sign_in_button = driver.find_element(By.XPATH, '//*[@aria-label="Sign in"]')
            sign_in_button.click()
            
            email_field = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
            email_field.send_keys(email)
            email_field.send_keys(Keys.RETURN)
            
            time.sleep(10)
            
            password_field = driver.find_element(By.XPATH, '//*[@name="Passwd"]')
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
            driver.get(links[i])
            
            driver.save_screenshot(f"screenshots/screenshot_{thread_id}_{time.time()}.png")
            perform_human_like_actions(driver, driver.find_element(By.XPATH, '//body'))
        except Exception as e:
            print(f"Error with driver {i}: {e}")

    run_time = random.randint(600, 900)
    start_time = time.time()

    while time.time() - start_time < run_time:
        sleep_time = random.randint(200, 300)
        time.sleep(sleep_time)
        for j in range(len(drivers)):
            try:
                sleep_time = random.randint(1, 10)
                drivers[j].refresh()
                perform_human_like_actions(drivers[j], drivers[j].find_element(By.XPATH, '//body'))
           
                run = random.randint(1, 10)
                if run == 5:
                    try:
                        like_button_xpath = '//button[@title="I like this"]'
                        like_button = drivers[j].find_element(By.XPATH, like_button_xpath)
                        like_button.click()
                        print("Liked the video successfully.")
                    except Exception as e:
                        print(f"Failed to like the video: {e}")
                    
                drivers[j].save_screenshot(f"screenshots/screenshot_{thread_id}_{time.time()}.png")
            except Exception as e:
                print(f"Error with driver {j}: {e}")

    for drv in drivers:
        drv.quit()

def main():
    parser = argparse.ArgumentParser(description="Selenium Bot")
    parser.add_argument('--email', type=str, required=True, help="Email for login")
    parser.add_argument('--password', type=str, required=True, help="Password for login")
    args = parser.parse_args()

    email = args.email
    password = args.password

    user_agent = random.choice(user_agents)
    driver = create_driver(user_agent)
    driver.get("https://www.youtube.com/@Boymuscleworkout/videos")
    
    driver.implicitly_wait(10)
    
    links = []
    while len(links) < 500:
        elements = driver.find_elements(By.XPATH, '//a[@id="video-title-link"]')
        new_links = [element.get_attribute('href') for element in elements]
        links.extend([link for link in new_links if link not in links])
        print(f"Number of unique links: {len(links)}")
        scroll_down(driver)
    
    driver.quit()

    shuffle(links)
    
    chunk_size = 5
    chunks = [links[i:i + chunk_size] for i in range(0, len(links), chunk_size)]
    
    threads = []
    for i, chunk in enumerate(chunks):
        thread = threading.Thread(target=run_thread, args=(chunk, i, email, password))
        threads.append(thread)
        random_delay(60, 300)
        thread.start()

        if len(threads) >= 5:
            for t in threads:
                t.join()
            threads = []
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
