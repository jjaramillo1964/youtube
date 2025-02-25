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

# Auto-install ChromeDriver
chromedriver_autoinstaller.install()

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
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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
