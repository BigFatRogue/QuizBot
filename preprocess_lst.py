from SQUIZ_parser import get_squiz
from WOW_parser import get_wow
from datetime import datetime


def get_main_character(lst_quiz: list[dict]) -> tuple[list]:
    sMain = set()
    sAddress = set()

    for dct in lst_quiz:
        sMain.add(dct['main'])
        sAddress.add(dct['address'])

    return list(sMain), list(sAddress)


def filters_quiz(lst_quiz: list[dict],
            fMain=None,
            fDate=None,
            fTime=None,
            fWeekDay=None,
            fAddress=None) -> list:

    lst_mouth = ['января', 'февраля', "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "декабря", "ноября", "декабря"]
    lst_day_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    new_lst = []

    for dct in lst_quiz:
        f1, f2, f3, f4, f5 = [False] * 5
        # WOW или SQUIZ и др.
        if fMain is not None:
            if dct['main'] in fMain:
                f1 = True
        else:
            f1 = True

        # До какого месяца выдать результаты
        if fDate is not None:
            data_number, mouth, week_day = dct['date']
            mouth_str_to_number = lambda x: lst_mouth.index(x)
            number = int(f'{mouth_str_to_number(mouth)}{data_number}')
            if len(fDate) == 2:
                fDay, fMouth = fDate
                fDay = f'{fDay:02}'
                fNumber = int(f'{mouth_str_to_number(fMouth)}{fDay}')
                if number <= fNumber:
                    f2 = True
            elif len(fDate) == 4:
                fDay_0, fMouth_0, fDay_1, fMouth_1 = fDate
                fDay_0, fDay_1 = f'{fDay_0:02}', f'{fDay_1:02}'

                fNumber_0 = int(f'{mouth_str_to_number(fMouth_0)}{fDay_0}')
                fNumber_1 = int(f'{mouth_str_to_number(fMouth_1)}{fDay_1}')

                if fNumber_0 <= number <= fNumber_1:
                    f2 = True
        else:
            f2 = True

        # Время начало игры
        if fTime is not None:
            h, m = dct['time']
            if fTime[0] <= int(h) <= fTime[1]:
                f3 = True
        else:
            f3 = True

        # Место игры
        if fAddress is not None:
            if dct['address'] in fAddress:
                f4 = True
        else:
            f4 = True

        if fWeekDay is not None:
            data_number, mouth, week_day_str = dct['date']
            fWeekDay_lst = [lst_day_week.index(i) for i in fWeekDay]
            week_day = lst_day_week.index(week_day_str)
            if week_day in fWeekDay_lst:
                f5 = True
        else:
            f5 = True

        if all((f1, f2, f3, f4, f5)):
            new_lst.append(dct)

    return new_lst


def set_lst_string(lst: list) -> list:
    string_lst = []
    for item in lst:
        item: dict
        main = item["main"].upper()
        name = item["name"].replace('WOW', '')

        new_name = ''
        flag = True
        for i in name:
            if i == '(':
                flag = False
            elif i == ')':
                flag = True
                continue
            if flag:
                new_name += i

        day, mouth, weekday = item["date"]
        date = f'{day} {weekday}'
        address = item['address']
        time = ':'.join(map(str, item['time']))

        if name and name != '""':
            s = f'{main[0]}, {new_name}, {date}::{time}, {address}'[0:100]
        else:
            s = f'{main[0]}, {date}::{time}, {address}'[0:100]

        string_lst.append(s)
    return string_lst


if __name__ == '__main__':
    lst_quiz = get_wow() + get_squiz()

    f = {'fMain': ['WOW', 'SQUIZ'], 'fDate': (10, 'марта', 7, 'апреля'), 'fTime': (14, 20), 'fAddress': {'BarBQ Night::Ломоносова, 16', 'ул. Белинского, 13::Чешская Пивница'}, 'fWeekDay': {'Пт', 'Вс', 'Сб'}}

    # print(get_main_character(lst_quiz))
    new_lst_quiz = filters_quiz(lst_quiz=lst_quiz, **f)

    print( set_lst_string(new_lst_quiz))
    # for dct in new_lst_quiz:
    #     print(dct['date'])
