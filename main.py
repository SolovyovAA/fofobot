import telebot

import config

import db_worker

conf = config.Config()

bot = telebot.TeleBot(conf.getToken())
worker = db_worker.DBWorker(conf.getDatabasePath())

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет! Ваше имя добавленно в базу данных!')
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        worker.writeToDatabase(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Связаться с разработчиком', url='telegram.me/pihost'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) Бот нихера пока не умеет.\n' +
        '2) Хочешь начать? отправь /start или /reg\n' +
        '3) Для получения сюрприза отправь /getnude.',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(commands=['getnude'])
def get_nude(message):
    bot.send_photo(message.chat.id, 'https://www.meme-arsenal.com/memes/906057dd785388a0fa893ca85dc9b6b5.jpg');
    # bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


bot.polling(none_stop=True, interval=0)
