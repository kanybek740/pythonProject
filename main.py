
import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://www.detmir.ru/catalog/index/name/lego/'

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
           'accept': '*/*'}
HOST = 'https://www.detmir.ru/'
FILE = 'legos.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_= 'mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='be80pr-1') # Здесь обращаемся к объекту суп и ищем элементы.
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('a', class_='cpshbz-0').get_text(strip=True), # Берем заголовок карточки
                'price': item.find('span', class_='price').get_text(strip=True),
                'city': item.find('span', class_='item region').get_text(
                    strip=True),
                'promo': item.find('div', class_='promo').get_text(),
                'link': HOST + item.find('div', class_='link').find('a').get('href'), # Получаем ссылку
            }
        )
    return cards


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование', 'Цена', 'Город', 'Промо цена',
                          'Ссылка на страницу с товаром'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['city'],
                             item['promo'], item['link']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        legos = []
        print(get_content(html.text))
        pages = get_pages_count(html.text)
        for page in range(1, pages + 1):
            html = get_html(URL, params={'pages': page})
            legos.extend(get_content(html.text))
            if len(legos) > 5:
                save_file(legos, FILE)
            else:
                print('Количество элементов меньше 500!')
        print(legos)
    else:
        print('Error')


parser()


