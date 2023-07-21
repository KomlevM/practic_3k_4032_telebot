import telebot
import config
import bot

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

def runPereoborudovanie(chat_id):
	bot.send_message(chat_id, 'Pereoborudovanie')