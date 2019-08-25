import requests

# сделать токен внутри функции
token = "950876534:AAHeSme1hi8gfkQwpk6UHvw0apBeasVgXkQ"


# сделать константой

class Bot:
    # Опишем атрибуты класса (то, что у нас будет по умолчанию)

    def __init__(self, token):
        token = token
        self.url = 'https://api.telegram.org/bot{}/'.format(token)
        self.course_url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'

    # получаем обновления чтобы иметь доступ к остальному
    def get_updates(self):
        method = 'getupdates'
        response = requests.get(self.url + method)
        return response.json()

    # получаем сообщение, берём последние
    def get_message(self):
        data = self.get_updates()
        chat_id = data['result'][-1]['message']['chat']['id']
        last_message = data['result'][-1]['message']['text']
        message_list = {'chat_id': chat_id,
                        'text': last_message}
        return message_list

    # реализуем отправку сообщения
    def send_message(self, chat_id, text):
        method = 'sendmessage'
        params = {'chat_id': chat_id,
                  'text': text}
        response = requests.post(self.url + method, params)
        return response

    # парсер валют, запись валют в переменные, подстановка в один текст для вывода
    def get_money(self):
        response = requests.get(self.course_url).json()
        for p in list(response):
            if p['Cur_Abbreviation'] == 'USD':
                usd_price = p['Cur_OfficialRate']
            if p['Cur_Abbreviation'] == 'EUR':
                eur_price = p['Cur_OfficialRate']
            if p['Cur_Abbreviation'] == 'PLN':
                pln_price = p['Cur_OfficialRate']
        return 'cost of one BYN today - {} USD, {} EUR, {} PLN'.format(usd_price, eur_price, pln_price)

    # запись последних сообщений
    def recorder(self):
        my_file = open("message.txt", "a+")
        my_file.write(self.get_updates()['result'][-2:-1][0]['message']['text'] + '\n')
        my_file.close()


test_bot = Bot(token)
test_bot.get_updates()

money = test_bot.get_money()
answer = test_bot.get_message()

chat_id = answer['chat_id']
text = answer['text']

if text == '/course':
    test_bot.send_message(chat_id, money)

if text == answer['text']:
    test_bot.send_message(chat_id, 'Эхо: ' + text)

if text == '/write':
    test_bot.send_message(chat_id, test_bot.recorder())
