import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

def runVin(message):
	markupVinRun = types.InlineKeyboardMarkup (row_width = 3)
	botn1 = types.InlineKeyboardButton ("У меня есть направление", callback_data = "napravlenie")
	botn2 = types.InlineKeyboardButton ("Только приступаю", callback_data = 'startOfVin')
	botn3 = types.InlineKeyboardButton ("Назад", callback_data = 'back')

	markupVinRun.add(botn1,botn2,botn3)

	bot.send_message(message.chat.id, 'Текст по ВИНу', reply_markup = markupVinRun)

def napravlenie(message):
	markupNapravlenie = types.InlineKeyboardMarkup (row_width = 3)
	botn1 = types.InlineKeyboardButton ("Передать даннные менеджеру", callback_data = 'prodanoVin')
	botn2 = types.InlineKeyboardButton ("Нет, спасибо", callback_data = 'vin')

	markupNapravlenie.add(botn1,botn2)

	bot.send_message(message.chat.id, 'Текст продажи за 15к', reply_markup = markupNapravlenie)

def startOfVin(message):
	markupStartProcess = types.InlineKeyboardMarkup (row_width = 3)
	botn1 = types.InlineKeyboardButton ("Передать даннные менеджеру", callback_data = 'prodanoVinKey')
	botn2 = types.InlineKeyboardButton ("Нет, спасибо", callback_data = 'vin')

	markupStartProcess.add(botn1,botn2)

	bot.send_message(message.chat.id, 'Рассказ про набивку\n+\nТекст продажа под ключ', reply_markup = markupStartProcess)