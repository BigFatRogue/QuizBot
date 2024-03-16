import requests
import bs4
from datetime import datetime


def get_wow() -> list:
    lst_mouth = ['января', 'февраля', "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "декабря", "ноября", "декабря"]
    lst_weekday = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    link = r'https://spb.wowquiz.ru/schedule'
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    func_get_text = lambda lst: [i.text for i in lst]
    all_title = func_get_text(soup.findAll('div', class_='game-item__title'))
    all_price = func_get_text(soup.findAll('div', class_='game-item__price'))
    all_date = func_get_text(soup.findAll('span', class_='date'))
    all_date = [f'{all_date[i]}, {all_date[i + 1]}' for i in range(0, len(all_date) - 1, 2)]

    all_time = func_get_text(soup.findAll('span', class_='time'))
    all_place = func_get_text(soup.findAll('span', class_='place'))
    all_address = func_get_text(soup.findAll('span', class_='address'))
    all_status = func_get_text(soup.findAll('a', class_='game-item__btn active register_team'))

    lst = []
    for title, date, time, place, address, status, price in zip(all_title, all_date, all_time, all_place, all_address, all_status, all_price):
        if status == 'регистрация':
            data_number, mouth = date.split(',')[0].split()
            week_day = lst_weekday[datetime(2024, lst_mouth.index(mouth) + 1, int(data_number)).weekday()]
            hours, minutes = list(map(int, time.split(':')))

            value = {'main': 'WOW',
                     'name': title,
                     'date': (int(data_number), mouth, week_day),
                     'time': (int(hours), minutes),
                     'price': price,
                     'form': None,
                     'type': None,
                     'address': f'{address}::{place}',
                     'number': int(str(lst_mouth.index(mouth)) + data_number)
                     }
            lst.append(value)

    return lst


if __name__ == '__main__':
    # lst_weekday = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    # print()
    wow_lst = get_wow()
    for item in wow_lst:
        print(item)