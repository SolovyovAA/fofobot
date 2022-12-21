import telebot

import config

import db_worker

bot = telebot.TeleBot(config.TOKEN)

worker = db_worker.DBWorker(config.DATABASE_PATH + config.DATABASE_NAME)


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
