import sqlite3
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from logic import *

bot = telebot.TeleBot(API_TOKEN)

	
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="/start")
    button2 = telebot.types.KeyboardButton(text="/faq")
    button3 = telebot.types.KeyboardButton(text="/helptech")
    keyboard.add(button1, button2, button3)
    bot.send_message(chat_id,
'''Здравствуйте, я бот техподдержки магазина "Продаем все на свете"
Чем могу помочь?:
	/start - Просмотреть команды еще раз
	/faq - Часто задаваемые вопросы
	/helptech - Написать вопрос техподдержке через бота''',reply_markup=keyboard)


@bot.message_handler(commands=['faq'])
def faq_handler(message):
	bot.reply_to(message, '''Напечатайте ваш вопрос:
		-Как оформить заказ?
		-Как узнать статус моего заказа?
		-Как отменить заказ?
		-Что делать, если товар пришел поврежденным?
		-Как связаться с вашей технической поддержкой?
		-Как узнать информацию о доставке?
Для связи с техподдержкой используйте /helptech чтобы задать вопрос которого здесь нету.''')
@bot.message_handler(commands=['helptech'])
def tech_handler(message):
	bot.reply_to(message, 'Напечатайте ваш вопрос который мы отправим нашим специалистам')
	bot.register_next_step_handler(message, add_question)

def add_question(message):
	if message.content_type == "text":
		bot.reply_to(message, f'Хорошо, ваш вопрос "{message.text}" был сохранен')
		con = sqlite3.connect("questions.db")
		cur = con.cursor()
		cur.execute(f"INSERT INTO user_questions VALUES ('{message.text}', '{message.from_user.username}', {message.from_user.id})")
		con.commit()
		con.close()
	else:
		pass

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if faq.get(message.text) != None:
		bot.reply_to(message, faq.get(message.text))
	else:
		pass

bot.infinity_polling()