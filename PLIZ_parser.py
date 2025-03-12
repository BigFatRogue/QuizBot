import requests
import bs4
from datetime import datetime

from variant import *

def convert_date(date: str) -> tuple:
    day, mouth_str, week_day = date.split()
    day = int(''.join([i for i in day if i.isdigit()]))
    mouth_str = mouth_str.replace(',', '')
    return int(day), mouth_str, DICT_WEEKDAY_SHORT.get(week_day)


def get_pliz() -> list:
    link = r'https://spb.quizplease.ru/schedule'
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    func_get_text = lambda lst: [i.text for i in lst]

    all_title = func_get_text(soup.findAll('div', class_='h2 h2-game-card h2-left'))
    all_price = func_get_text(soup.findAll('span', class_='price'))
    all_date = func_get_text(soup.findAll('div', class_='h3 h3-green h3-mb10 block-date-with-language-game game-active'))
    all_date = [convert_date(date) for date in all_date]

    all_time, all_place, all_address = [], [], []
    res = soup.findAll('div', class_='schedule-info-block')

    for div in res:
        div: bs4.element.Tag
        data = div.findAll('div', class_='techtext')
        data = [string.text.strip().replace('\t', '').replace('Где это?', '').replace('Инфа о баре', '').replace('в ', '').strip() for string in data]
        data = [i for i in data if i]
        if len(data) == 3:
            place, address, time = data
            all_place.append(place)
            all_time.append(time)
            all_address.append(address)
    
    all_status = func_get_text(soup.findAll('a', class_='button button-green button-left button-small w-button customs_dis'))

    lst = []
    for title, date, time, place, address, status, price in zip(all_title, all_date, all_time, all_place, all_address, all_status, all_price):
        data_number, mouth_str, week_day = date
        
        value = {'main': 'PLIZ',
            'name': title,
            'date': date,
            'time': time.split(':'),
            'price': price,
            'form': None,
            'type': None,
            'address': f'{address}::{place}',
            'number': int(f'{LST_MOUTH.index(mouth_str)}{data_number}')
            }
        lst.append(value)

    return lst


def test():
    link = r'https://spb.quizplease.ru/schedule'
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    res = soup.findAll('div', class_='schedule-info-block')
    for div in res:
        div: bs4.element.Tag
        time = div.findAll('div', class_='techtext')
        time = [string.text.replace('\t', '').replace('Где это?', '').replace('Инфа о баре', '').strip() for string in time]

if __name__ == '__main__':
    # test()

    pliz_lst = get_pliz()
    for item in pliz_lst:
        print(item)