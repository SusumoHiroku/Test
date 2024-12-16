import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_and_extract_promotions(url, proxy_ip, proxy_port, output_filename):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')

        proxy = f"http://{proxy_ip}:{proxy_port}"
        options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get(url)
        print(f"Переход по адресу: {url}")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(30)

        promotions = driver.find_elements(By.CLASS_NAME, "promotions-single")
        print(f"Знайдено {len(promotions)} акцій.")

        promotions_data = []

        for idx, promo in enumerate(promotions, start=1):
            try:
                title_element = promo.find_element(By.CLASS_NAME, "promotions-single__title")
                title = title_element.text.strip()

                desc_element = promo.find_element(By.CLASS_NAME, "promotions-single__txt")
                description = desc_element.text.strip()

                btn_wrap = promo.find_element(By.CLASS_NAME, "promotions-single__btn-wrap")
                links = btn_wrap.find_elements(By.TAG_NAME, "a")

                bonus_link = links[0].get_attribute('href').strip()
                info_link = links[1].get_attribute('href').strip()

                promotions_data.append({
                    'Title': title,
                    'Description': description,
                    'Bonus Link': bonus_link,
                    'Info Link': info_link
                })

                print(f"Акція {idx}: '{title}' парсинг.")

            except Exception as e:
                print(f"Помилка при обробці акції {idx}: {type(e).__name__}: {e}")

        # Записываем данные в текстовый файл
        with open(output_filename, 'w', encoding='utf-8') as f:
            for promo in promotions_data:
                f.write(f"Назва: {promo['Title']}\n")
                f.write(f"Опис: {promo['Description']}\n")
                f.write(f"Посилання на бонус: {promo['Bonus Link']}\n")
                f.write(f"Посилання на інформацію: {promo['Info Link']}\n")
                f.write("-" * 50 + "\n")

    except Exception as e:
        print(f"Виникла помилка: {type(e).__name__}: {e}")

    finally:
        driver.quit()


def main():
    target_url = "https://www.woocasino.com/promotions"
    output_filename = "promotions.txt"

    proxy_ip = "200.174.198.86"
    proxy_port = "8888"

    fetch_and_extract_promotions(target_url, proxy_ip, proxy_port, output_filename)


if __name__ == "__main__":
    main()
