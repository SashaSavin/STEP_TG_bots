import requests

# token = "950876534:AAHeSme1hi8gfkQwpk6UHvw0apBeasVgXkQ"

# При помощи базового URL делаем запрос на сервер
BaseURL = "https://api.telegram.org/bot950876534:AAHeSme1hi8gfkQwpk6UHvw0apBeasVgXkQ/"


# получаем словарь с обновлениями
def updates():
    current_url = BaseURL + 'getupdates'  # добавляем к базовому url запрос на получение обновлений
    request = requests.get(current_url)  # делаем запрос GET для просмотра обновлений
    return request.json()  # получаем обновления в виде словаря json(для удобства работы)


# получение последнего сообщения
def message():
    data = updates()  # обращаемся к updates чтобы взять элементы
    chat_id = data['result'][-1]['message']['chat']['id']  # получаем id чата
    my_last_message = data['result'][-1]['message']['text']  # получаем последнее сообщение
    message_list = {'chat_id': chat_id, 'text': my_last_message}  # упаковываем данные в словарь
    return message_list


# отправление сообщения
def send_message(chat_id, text='...'):
    url = BaseURL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)  # формируем url для отправки сообщения
    requests.get(url)


# парсинг валют
def get_money():
    url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
    response = requests.get(url).json()  # пройдёмся по списку из множества валют, ищем по наименаванию
    for p in list(response):
        if p['Cur_Abbreviation'] == 'USD':
            usd_price = p['Cur_OfficialRate']
        if p['Cur_Abbreviation'] == 'EUR':
            eur_price = p['Cur_OfficialRate']
        if p['Cur_Abbreviation'] == 'PLN':
            pln_price = p['Cur_OfficialRate']
    return 'today cost of one BYN - {} USD, {} EUR, {} PLN'.format(usd_price, eur_price, pln_price)


# реализуем отправление сообщений
def bot_answer():
    answer = message()
    m = answer['text']
    id = answer['chat_id']

    if m == "/course":
        send_message(id, get_money())
    if m == answer['text']:
        send_message(id, m)


bot_answer()
