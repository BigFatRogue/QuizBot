from datetime import datetime
import requests
import re

from variant import *



def get_squiz() -> list:
    link = r'https://store.tildacdn.com/api/getproductslist/?storepartuid=111979372401&getparts=true&getoptions=true&slice=1&size=100'
    response: dict = requests.get(link).json()

    lst = []
    for i, product in enumerate(response['products']):
        char = product['characteristics']
        if len(char) >= 2:  # не резерв
            form = char[0]['value']
            if form != 'Онлайн':
                dates = product['title']
                date, time = dates.split('::')
                data_number, mouth = date.split()[:2]
                data_number, mouth = data_number.strip().replace(',', ''), mouth.strip().replace(',', '')
                week_day = LST_WEEKDAY[datetime(NOW_YEAR, LST_MOUTH.index(mouth) + 1, int(data_number)).weekday()]
                hours, minutes = time.split(':')

                price = int(product['price'].split('.')[0])
                tp = char[1]['value']
                desc: str = product['text']
                address = re.findall(r';">(.*?)</a>', desc)
                address_0 = address[0].replace('"', '').replace('ул. ', '')
                address_1 = address[1].replace('"', '').replace('ул. ', '')
                name = re.findall(r'Описание: "(.*?)"', desc)[0]

                value = {'main': 'SQUIZ',
                         'name': name.strip(),
                         'date': (data_number, mouth, week_day),
                         'time': (hours.strip().replace(',', ''), minutes.strip().replace(',', '')),
                         'price': price,
                         'form': form.strip(),
                         'type': tp.strip(),
                         'address': f'{address_0.strip()}::{address_1.strip()}',
                         'number': int(str(LST_MOUTH.index(mouth)) + data_number)
                         }

                lst.append(value)
    return lst


if __name__ == '__main__':
    squiz_lst = get_squiz()
    for item in squiz_lst:
        print(item)
