import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_body_html(url, output_file):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')

        # Инициализация драйвера Chrome
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get(url)
        print(f"Переход по адресу: {url}")

        # Ожидаем загрузки тега <body>
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # time.sleep(3)
        body = driver.find_element(By.TAG_NAME, "body")
        body_html = body.get_attribute('innerHTML')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(body_html)

    except Exception as e:
        print(f"Произошла ошибка: {type(e).__name__}: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = "https://go.slotimo.com/login/"
    output_filename = "login_html.html"
    save_body_html(target_url, output_filename)
