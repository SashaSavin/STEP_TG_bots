import requests

# token = "950876534:AAHeSme1hi8gfkQwpk6UHvw0apBeasVgXkQ"

#При помощи базового URL делаем запрос на сервер
BaseURL = "https://api.telegram.org/bot950876534:AAHeSme1hi8gfkQwpk6UHvw0apBeasVgXkQ/"

#получаем словарь с обновлениями
def updates():
	CurrentURL = BaseURL + 'getupdates' #добавляем к базовому url запрос на получение обновлений
	request = requests.get(CurrentURL) #делаем запрос GET для просмотра обновлений
	return request.json() #получаем обновления в виде словаря json(для удобства работы)

#получение последнего сообщения, список с данными
def message():
	data = updates() # обращаемся к updates чтобы взять элементы
	chat_id = data['result'][-1]['message']['chat']['id'] #получаем id чата
	my_last_message = data['result'][-1]['message']['text'] #получаем последнее сообщение
	message_list = {'chat_id':chat_id,'text': my_last_message} #упаковываем данные в словарь
	return message_list

#отправление сообщения
def send_message(chat_id, text = '...'):
	url = BaseURL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text) #формируем url для отправки сообщения
	requests.get(url)


answer = message()
m = answer['text']
id = answer['chat_id']

send_message(id, m)

