import time
import threading
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
import os
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.common.exceptions import WebDriverException


# Cài đặt ChromeDriver 1 lần duy nhất
chromedriver_autoinstaller.install()

# Khóa để tránh tranh chấp file khi khởi tạo trình duyệt
lock = threading.Lock()

def create_driver():
    with lock:
        chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

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
        # driver.execute_script("window.scrollBy(0, 250);")
        # time.sleep(1)

def run_thread(keyword, email, password):
    driver = create_driver()

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

        # Truy cập playlist
        driver.get("https://www.youtube.com/@Boymuscleworkout/playlists")
        time.sleep(10)

        driver.save_screenshot(f"screenshot_{keyword}_{time.time()}.png")

        # Mở video theo từ khóa
        watch_video = driver.find_element(By.XPATH, f'//*[@title="{keyword}"]')
        watch_video.click()
        time.sleep(10)



        # Vòng lặp theo dõi và chụp ảnh màn hình
        run_time = random.randint(600, 900)  # Thời gian chạy random 10-15 phút
        start_time = time.time()

        while time.time() - start_time < run_time:
            try:
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
            except Exception as e:
                print(f"Login error: {e}")
                pass

            driver.save_screenshot(f"screenshot_{keyword}_{time.time()}.png")
            print(f"Screenshot for: {keyword}")
            run_time = random.randint(200, 260)
            time.sleep(run_time)  # Chụp ảnh mỗi 5 phút
            random_mouse_move(driver)
            if run_time == 250 or run_time == 230:
                try:
                    like_button_xpath = '//button[@title="I like this"]'
                    like_button = driver.find_element(By.XPATH, like_button_xpath)
                    like_button.click()
                    print("Liked the video successfully.")
                except Exception as e:
                    print(f"Failed to like the video: {e}")
                    continue
                

    except Exception as e:
        print(f"Error for keyword {keyword}: {e}")
        

    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Selenium YouTube bot")
    parser.add_argument("--email", required=True, help="Email for YouTube login")
    parser.add_argument("--password", required=True, help="Password for YouTube login")
    args = parser.parse_args()
    os.makedirs("screenshots", exist_ok=True)
    keywords = ["honguynvn04", "tindang", "abskwkws", "hieuvilai2007", "365ngynhem"]
    threads = []
    for keyword in keywords:
        thread = threading.Thread(target=run_thread, args=(keyword, args.email, args.password))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
