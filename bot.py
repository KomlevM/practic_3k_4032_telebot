import telebot
import config
import zapros
import vin
import os

from vin import *
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
folder = ''

class User:
	name = "gay"
	user_id = None
	phone = None
	theme = None

	def __init__(self, userTheme):
		self.theme = userTheme

	def __del__(self):
		self.name = "gay"

@bot.message_handler(commands=['start'])
def welcom(message):
	markup = types.InlineKeyboardMarkup (row_width = 3)
	botn1 = types.InlineKeyboardButton ("ВИН", callback_data = 'vin')
	botn2 = types.InlineKeyboardButton ("Ввоз ТС", callback_data = 'vvoz')
	botn3 = types.InlineKeyboardButton ("Переоборудование", callback_data = 'pereob')

	markup.add(botn1, botn2, botn3)

	bot.send_message(message.chat.id, "Текст приветствие", reply_markup = markup)

@bot.message_handler(content_types = ['photo'])
def photo_handler(message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    downloaded_file = bot.download_file(file_path)

    file_name = f'1_{message.chat.id}_{file_id}.jpg'
    file_location = str(message.from_user.id) + '/' + file_name

    with open(file_location, 'wb') as new_file:
        new_file.write(downloaded_file)

@bot.message_handler(content_types = ['text'])
def answerToReakt(message):
	if (message.text == 'Отправить данные менеджеру'):
		zapros.send_email(str(message.from_user.id) + '/')
	elif (message.text == 'Вернуться в начало'): 
		welcom2(message)
	else bot.send_message(message.chat.id, "Мы не можем овтетить на Ваш вопрос(")



def welcom2(message):
	markup = types.InlineKeyboardMarkup (row_width = 3)
	botn1 = types.InlineKeyboardButton ("ВИН", callback_data = 'vin')
	botn2 = types.InlineKeyboardButton ("Ввоз ТС", callback_data = 'vvoz')
	botn3 = types.InlineKeyboardButton ("Переоборудование", callback_data = 'pereob')

	markup.add(botn1, botn2, botn3)

	bot.send_message(message.chat.id, "Текст приветствие2", reply_markup = markup)

def zaprosName(message, user):
	bot.send_message(message.chat.id, "Как нашему менеджеру к Вам обращаться?")
	bot.register_next_step_handler(message, lambda msg: zaprosTelephone(msg, user))

def zaprosTelephone(message, user):
	user.user_id = str(message.from_user.id)
	user.name = message.text

	bot.send_message(message.chat.id, "Укажите свой номер телефона, что бы наш менеджер мог связаться с Вами")
	bot.register_next_step_handler(message, lambda msg: zaprosComment(msg, user))

def zaprosComment(message, user):
	user.phone = message.text
	bot.send_message(message.chat.id, "Оставьте комментарий, что бы наш менеджер лучше смог понять Вашу ситуцаию")
	bot.register_next_step_handler(message, lambda msg: zaprosPhoto(msg, user))

def ifEnd(message, user):
	# Указываем путь и имя папки

	markup = types.InlineKeyboardMarkup (row_width = 2)
	botn1 = types.InlineKeyboardButton ("Да, отправить", callback_data = 'end')
	botn2 = types.InlineKeyboardButton ("Нет, вернуться в начало", callback_data = 'back')
	markup.add(botn1, botn2)

	msg = bot.send_message(message.chat.id, "Передать данные менеджеру?", reply_markup = markup)

def zaprosPhoto(message, user):

	os.mkdir(user.user_id)

	file = open('test.txt', 'w')

	file.write("Тема обращения: " + user.theme + "\n")
	file.write("Имя пользователя: " + user.name + "\n")
	file.write("ID пользователя: " + user.user_id + "\n")
	file.write("Номер телефона: " + user.phone + "\n")
	file.write("Комментарий: " + message.text + "\n")

	file.close()

	os.replace('test.txt', user.user_id + '/test.txt')

	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	botn1 = types.KeyboardButton("Отправить данные менеджеру", )
	botn2 = types.KeyboardButton("Вернуться в начало")
	markup.add(botn1, botn2)

	match user.theme:
		case "ВИН с направлением":
			bot.send_message(message.chat.id, "Пришлите фотографии направления и пломбы, для записи на нанесение дополнительной маркировки", reply_markup = markup)
		case "ВИН под ключ":
			bot.send_message(message.chat.id, "Пришлите фотографии нечитаемого VIN-номера и первой страницы ПТС, для согласования с Техотделом", reply_markup = markup)
	del user

@bot.callback_query_handler(func=lambda call: True)
def callback_inline (call):
	try:
		if call.message:
			match call.data:
				case 'vin':
					vin.runVin(call.message)
				case 'back':
					welcom2(call.message)
				case 'napravlenie':
					vin.napravlenie(call.message)
				case 'startOfVin':
					vin.startOfVin(call.message)
				case 'back':
					os.rmtree(str(call.message.from_user.id))
					welcom2(call.message)
				case 'prodanoVin':
					user = User("ВИН с направлением")
					zaprosName(call.message, user)
				case 'prodanoVinKey':
					user = User("ВИН под ключ")
					zaprosName(call.message, user)
	except Exception as e:
		print(repr(e))

# RUN
bot.polling(none_stop = True)