
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import re


def extract_product_id(url):
    match = re.search(r'/catalog/(\d+)/', url)
    if match:
        return match.group(1)
    else:
        return None

def is_valid_data(item):
    """Проверка корректности данных"""
    try:
        # Проверка, что все поля заполнены
        if not all([item['id'], item['name'], item['price'], item['rating'], item['reviews_numb']]):
            return False
        # Проверка, что цена является числом
        if not item['price'].isdigit():
            return False
        # Проверка, что рейтинг является числом
        if not item['rating'].replace('.', '', 1).isdigit():
            return False
        # Проверка, что количество отзывов является числом
        if not item['reviews_numb'].isdigit():
            return False
        return True
    except Exception as e:
        print(f"Ошибка при проверке данных: {e}")
        return False


def main():
    #настройки selenium
    firefox_options = Options()
    #firefox_options.add_argument("--headless")
    firefox_options.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    page = 1
    data = []
    print(1)
    while True:
        print(2)
        url0 = f"https://www.wildberries.ru/catalog/mebel/divany-i-kresla/divany?sort=popular&page={page}"
        print(url0)
        driver.get(url0)
        print(3)
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
        except:
            break

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')
        div_class = 'product-card__wrapper'
        items = soup.find_all('div', class_=div_class)

        for item in items:
            id = extract_product_id(item.find('a', class_="product-card__link").get("href"))
            name = item.find('a', class_="product-card__link").get("aria-label")
            price_text = item.find('span', class_='price__wrap').find('ins', class_='price__lower-price').text.strip()
            price_text = price_text.replace('\xa0', ' ')

            price_number = re.sub(r'\D', '', price_text)

            rating = item.find('span', class_='address-rate-mini').text.strip()

            reviews_numb = item.find('span', class_='product-card__count').text.strip()
            reviews_numb = re.sub(r'\D', '', reviews_numb)

            product_data = {
                "id": id,
                "name": name,
                "price": price_number,
                "rating": rating,
                "reviews_numb": reviews_numb
            }

            if is_valid_data(product_data):
                data.append(product_data)

        page += 1

    print(data)
    driver.quit()


main()
