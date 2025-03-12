"""
https://t.me/SecretQuizBot
"""

import telebot
from telebot import types
from SQUIZ_parser import get_squiz
from WOW_parser import get_wow
from PLIZ_parser import get_pliz
from preprocess_lst import filters_quiz, get_main_character, set_lst_string


__token = r'6440167133:AAFgV3PQKTCRQkpsMDAZCHYjrbbo3fDYCHM'
bot = telebot.TeleBot(__token)


def try_error(func):
    def wrapper(*args, **kwargs):
        res = None
        try:
            res = func(*args, **kwargs)
        except Exception:
            pass
        return res
    return wrapper


@bot.message_handler(commands=['help'])
def get_help(message):
    string = """
    /start - начало\n/filters - настройка фильтров\n/poll - меню по созданию\n/poll_add - добавить отфильтрованные опросы\n/__del - удалить последнее сообщение бота\n/__reboot - очистить фильтр
    """
    bot.reply_to(message, string)


@bot.message_handler(commands=['start'])
@try_error
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для создания опросов. "
                          "Введите /poll, чтобы создать опрос или /filters чтобы сформировать фильтры.\n"
                          "/help - описание всех команд")


# Обработчик команды /poll
@bot.message_handler(commands=['poll'])
@try_error
def set_poll(message):
    global f_quiz, lst_all_quiz, my_filters, f_str_quiz

    if lst_all_quiz is None:
        lst_all_quiz = sorted(get_wow() + get_squiz() + get_pliz(), key=lambda key: key['number'])

    f_quiz = filters_quiz(lst_all_quiz, **my_filters)
    f_str_quiz = set_lst_string(f_quiz)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Список отфильтрованных квизов', callback_data=f'poll@lst'))
    markup.add(types.InlineKeyboardButton(text='Добавить фильтры вручную', callback_data=f'poll@add'))
    markup.add(types.InlineKeyboardButton(text='Создать опрос(ы)', callback_data=f'poll@create_poll'))

    text_message = 'Выберите команду'
    try:
        bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML', reply_to_message_id=2)
    except Exception:
        bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@bot.message_handler(commands=['poll_add'])
# @try_error
def poll_add(message):
    print('poll_add')
    create_poll(message)


@bot.callback_query_handler(func=lambda call: call.data == 'close')
@bot.message_handler(commands=['filters'])
@try_error
def change_filters(message):
    global all_organ, all_address, lst_all_quiz

    if lst_all_quiz is None:
        lst_all_quiz = sorted(get_wow() + get_squiz() + get_pliz(), key=lambda key: key['number'])
        all_organ, all_address = get_main_character(lst_all_quiz)

    markup = types.InlineKeyboardMarkup()
    for string, func_name in zip(('Организация', 'Адрес', 'Период', 'День недели', 'Время', 'Готово', 'Очистить фильтр'),
                      ('change_org', 'change_address', 'change_date', 'change_weekday', 'change_time', 'complete', 'all_clear')):
        markup.add(types.InlineKeyboardButton(text=string, callback_data=func_name))

    try:
        bot.send_message(message.chat.id, text="Выберите фильтр", reply_markup=markup)
    except AttributeError:
        bot.send_message(message.message.chat.id, text="Выберите фильтр", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'all_clear')
@try_error
def clear_filters(call):
    global my_filters
    message = call.message
    my_filters = {'fMain': None, 'fDate': None, 'fTime': None, 'fAddress': None}
    bot.send_message(message.chat.id, 'Фильтр очищен /filters')


@bot.callback_query_handler(func=lambda call: call.data == 'change_org')
@try_error
def organization_change_filters(call):
    global all_organ, all_address, lst_all_quiz
    message = call.message

    markup = types.InlineKeyboardMarkup()
    for i, organ in enumerate(all_organ):
        markup.add(types.InlineKeyboardButton(text=organ, callback_data=f'org@{i}'))

    btn_all = types.InlineKeyboardButton(text="Все", callback_data='org@all')
    btn_clear = types.InlineKeyboardButton(text="Очистить фильтр", callback_data='org@clear')
    btn_check = types.InlineKeyboardButton(text="Пропустить\Готово", callback_data='close')
    markup.add(btn_all)
    markup.add(btn_clear, btn_check)

    text_message = 'Выберите организацию.\n' \
                   '- Когда Вы нажимаете на одну из организаций, то она добавляется в список.\n' \
                   '- Чтобы очистить список нажмите <b>"Очистить фильтр"</b>.\n' \
                   '- Чтобы закончить выбор нажмите <b>"Пропустить\Готово"</b>'
    bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'change_address')
@try_error
def address_change_filters(call):
    global all_address
    message = call.message

    markup = types.InlineKeyboardMarkup()
    for i, address in enumerate(all_address):
        markup.add(types.InlineKeyboardButton(text=address, callback_data=f'adrs@{i}'))

    btn_all = types.InlineKeyboardButton(text="Все", callback_data='adrs@all')
    btn_clear = types.InlineKeyboardButton(text="Очистить фильтр", callback_data='adrs@clear')
    btn_check = types.InlineKeyboardButton(text="Пропустить\Готово", callback_data='close')
    markup.add(btn_all)
    markup.add(btn_clear, btn_check)

    text_message = 'Выберите адрес\n'\
                   '- Когда Вы нажимаете на один из адресов, то он добавляется в список.\n' \
                   '- Чтобы очистить список нажмите <b>"Очистить фильтр"</b>.\n' \
                   '- Чтобы закончить выбор нажмите <b>"Пропустить\Готово"</b>'
    bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'change_date')
@try_error
def date_change_filters_question(call):
    message = call.message

    msg = 'Напишите дату до какого числа фильтровать. Месяц в родительном падеже.\nНапример:\n<b>"16 марта", "1 июня"</b> или <b>11 марта 31 марта </b>'
    bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(message, date_change_filters_answer)


@try_error
def date_change_filters_answer(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'date@{message.text}'))
    markup.add(types.InlineKeyboardButton(text='Отмена', callback_data=f'close'))

    text_message = f'Вы выбрали: <b>{message.text}</b>'
    bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'change_time')
@try_error
def time_change_filters_question(call):
    message = call.message

    msg = 'Напишите промежуток времени через проблем, например:\n<b>14 16</b> или <b>19 20</b>'
    bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(message, time_change_filters_answer)


@try_error
def time_change_filters_answer(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'time@{message.text}'))
    markup.add(types.InlineKeyboardButton(text='Отмена', callback_data=f'close'))

    text_message = f'Вы выбрали: <b>{message.text}</b>'
    bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'change_weekday')
@try_error
def change_weekday_filters_question(call):
    global lst_week_day
    message = call.message

    markup = types.InlineKeyboardMarkup()
    btn_lst = [types.InlineKeyboardButton(text=weekday, callback_data=f'weekday@{weekday}') for weekday in lst_week_day]
    markup.add(*btn_lst)

    btn_all = types.InlineKeyboardButton(text="Все", callback_data='weekday@all')
    btn_clear = types.InlineKeyboardButton(text="Очистить фильтр", callback_data='weekday@clear')
    btn_check = types.InlineKeyboardButton(text="Пропустить\Готово", callback_data='close')
    markup.add(btn_all)
    markup.add(btn_clear, btn_check)
    text_message = 'Выберите организацию.\n' \
                   '- Когда Вы нажимаете на один из дней, то он добавляется в список.\n' \
                   '- Чтобы очистить список нажмите <b>"Очистить фильтр"</b>.\n' \
                   '- Чтобы закончить выбор нажмите <b>"Пропустить\Готово"</b>'
    bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@try_error
def change_weekday_filters_answer(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'weekday@{message.text}'))
    markup.add(types.InlineKeyboardButton(text='Отмена', callback_data=f'close'))

    text_message = f'Вы выбрали: <b>{message.text}</b>'
    bot.send_message(message.chat.id, text=text_message, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'poll@add')
@try_error
def add_filters_question(call):
    message = call.message
    bot.send_message(message.chat.id, 'Пришлите фильтр', parse_mode='HTML')
    bot.register_next_step_handler(message, add_filters_answer)


@try_error
def add_filters_answer(message):
    global my_filters
    try:
        my_filters = eval(message.text)
        bot.send_message(message.chat.id, 'Готово. /poll', parse_mode='HTML')
    except Exception:
        pass


# @try_error
def create_poll(message):
    global f_quiz, lst_all_quiz, my_filters, f_str_quiz

    if f_str_quiz is None:
        lst_all_quiz = sorted(get_wow() + get_squiz() + get_pliz(), key=lambda key: key['number'])

        f_quiz = filters_quiz(lst_all_quiz, **my_filters)
        f_str_quiz = set_lst_string(f_quiz)

    options = f_str_quiz

    len_options = len(options)
    flag = True

    step = 10 if len_options % 10 > 1 else 9
    rng = [(i, i + step) for i in range(0, len_options - step, step)]
    rng.append((step * (len_options//step), step * (len_options//step) + len_options % step))

    for (start, end) in rng:
        question = f"КВИЗЫ МОИ КВИЗЫ ({f_quiz[start]['date'][0]} - {f_quiz[end - 1]['date'][0]})"

        try:
            # Создать опросы в чате номер 2
            bot.send_poll(message.chat.id, question, f_str_quiz[start: end], is_anonymous=False,
                        allows_multiple_answers=True, reply_to_message_id=2)
        except Exception:
            # Создать опросы в чате номер 1
            bot.send_poll(message.chat.id, question, f_str_quiz[start: end], is_anonymous=False,
                        allows_multiple_answers=True)


        if not flag:
            break


@bot.callback_query_handler(func=lambda call: True)
@try_error
def callback_button(call):
    global my_filters, all_organ, all_address, f_quiz, lst_week_day
    message = call.message
    if '@' in call.data:
        command, text = call.data.split('@')

        if command == 'org':
            if text == 'all':
                my_filters['fMain'] = all_organ
            elif text == 'clear':
                my_filters['fMain'] = None
            else:
                text = all_organ[int(text)]
                if my_filters['fMain'] is None:
                    my_filters['fMain'] = {text}
                else:
                    my_filters['fMain'].add(text)

            fMainData = my_filters['fMain']
            fMainString = "- " + ";\n-".join(fMainData) if fMainData is not None else 'None'
            bot.send_message(message.chat.id, f'Фильтр по:\n{fMainString}')

        if command == 'adrs':
            if text == 'all':
                my_filters['fAddress'] = all_address
            elif text == 'clear':
                my_filters['fAddress'] = None
            else:
                text = all_address[int(text)]
                if my_filters['fAddress'] is None:
                    my_filters['fAddress'] = {text}
                else:
                    my_filters['fAddress'].add(text)

            fAddressData = my_filters['fAddress']
            fAddressString = "- " + ";\n- ".join(fAddressData) if fAddressData is not None else 'None'
            bot.send_message(message.chat.id, f'Фильтр по:\n{fAddressString}')

        if command == 'date':
            lst_date = text.split()

            if len(lst_date) == 2:
                my_filters['fDate'] = (int(lst_date[0]), lst_date[1])
            elif len(lst_date) == 4:
                my_filters['fDate'] = (int(lst_date[0]), lst_date[1], int(lst_date[2]), lst_date[3])

            fData = my_filters['fDate']
            fDataString = text if fData is not None else 'None'
            bot.send_message(message.chat.id, f'Фильтр по:\n{fDataString}\n/filters')

        if command == 'time':
            my_filters['fTime'] = tuple(map(int, text.split()))

            fTime = my_filters['fTime']
            fTimeString = f'{fTime[0]} {fTime[1]}' if fTime is not None else 'None'
            bot.send_message(message.chat.id, f'Фильтр по:\n{fTimeString}\n/filters')

        if command == 'weekday':
            if text == 'all':
                my_filters['fWeekDay'] = lst_week_day
            elif text == 'clear':
                my_filters['fWeekDay'] = None
            else:
                if my_filters['fWeekDay'] is None:
                    my_filters['fWeekDay'] = {text}
                else:
                    my_filters['fWeekDay'].add(text)

            fWeekDay = my_filters['fWeekDay']
            fWeekDayString = " ".join(fWeekDay) if fWeekDay is not None else 'None'
            bot.send_message(message.chat.id, f'Фильтр по:\n{fWeekDayString}')

        if command == 'poll':
            if text == 'lst':
                global f_str_quiz
                msg = ''
                count = 1
                for q in (f_str_quiz):
                    if len(msg) >= 3800:
                        bot.send_message(message.chat.id, msg)
                        msg = ''
                    msg += f'{count}. {q}\n\n'
                    count += 1
                bot.send_message(message.chat.id, msg)
            elif text == 'create_poll':
                create_poll(message)

    if call.data == 'complete':
        bot.send_message(message.chat.id, str(my_filters) + '\n/poll')


@bot.message_handler(commands=['__del'])
def delete(message):
    try:
        for i in range(100):
            bot.delete_message(message.chat.id, message.message_id - i)
    except Exception:
        ...


@bot.message_handler(commands=['__reboot'])
def reboot(message):
    global all_organ, all_address, all_weekday, lst_all_quiz, f_quiz, f_str_quiz
    all_organ, all_address, all_weekday = None, None, None
    lst_all_quiz = None
    f_quiz = None
    f_str_quiz = None
    bot.send_message(message.chat.id, "Готово")


# Запускаем бота
if __name__ == '__main__':
    my_filters = {'fMain': None, 'fDate': None, 'fTime': None, 'fAddress': None, 'fWeekDay': None}

    all_organ, all_address, all_weekday = None, None, None
    lst_all_quiz = None
    f_quiz = None
    f_str_quiz = None

    print('QuizBot Бот запущен')
    bot.polling()
