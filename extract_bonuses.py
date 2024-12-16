import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_bonuses(driver, base_url):
    bonuses = []

    try:
        bonuses_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.bonuses-app-list"))
        )
    except Exception as e:
        print("Не вдалось найти список бонусів на сторінці.")
        return bonuses

    # Ітерація по кожному елементу списка
    bonus_items = bonuses_list.find_elements(By.CSS_SELECTOR, "li.bonuses-app-list__item")
    for idx, item in enumerate(bonus_items, start=1):
        try:
            a_tag = item.find_element(By.CSS_SELECTOR, "a.bonuses-bonus-tile")

            bonus_title = a_tag.get_attribute('title').strip()
            if not bonus_title:
                try:
                    name_div = a_tag.find_element(By.CSS_SELECTOR, "div.bonuses-bonus-tile-name__compile")
                    bonus_title = name_div.text.strip()
                except:
                    bonus_title = 'Без назви'

            bonus_url = a_tag.get_attribute('href').strip()
            if bonus_url and not bonus_url.startswith('http'):
                bonus_url = webdriver.common.utils.urljoin(base_url, bonus_url)

            try:
                img_tag = a_tag.find_element(By.CSS_SELECTOR, "img.bonuses-bonus-tile__img")
                img_src = img_tag.get_attribute('src').strip()
            except:
                img_src = ''

            bonus = {
                'title': bonus_title,
                'url': bonus_url,
                'image': img_src
            }
            bonuses.append(bonus)

        except Exception as e:
            print(f"Помилка при обробці бонусів #{idx}: {e}")
            continue

    return bonuses


def save_bonuses_to_txt(bonuses, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, bonus in enumerate(bonuses, start=1):
                f.write(f"{idx}. {bonus['title']}\n")
                f.write(f"Посилання: {bonus['url']}\n")
                f.write(f"Зображення: {bonus['image']}\n\n")
        print(f"Збережено {len(bonuses)} бонусів в файл {output_file}")
    except Exception as e:
        print(f"Помилка при записі в файл: {type(e).__name__}: {e}")


def fetch_and_extract_bonuses(url):
    bonuses = []
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

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)
        bonuses = extract_bonuses(driver, url)
        return bonuses

    except Exception as e:
        print(f"Відбулася помилка: {type(e).__name__}: {e}")
        return bonuses

    finally:
        driver.quit()


def main():
    target_url = "https://betandyou-227625.top/pl/bonus/rules"
    output_filename = "bonuses_list.txt"
    bonuses = fetch_and_extract_bonuses(target_url)

    if bonuses:
        save_bonuses_to_txt(bonuses, output_filename)
    else:
        print("Бонусів не знайдено.")


if __name__ == "__main__":
    main()