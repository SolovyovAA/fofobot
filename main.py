import telebot

import config

import db_worker

from telebot import custom_filters

conf = config.Config()

bot = telebot.TeleBot(conf.getToken())
worker = db_worker.DBWorker(conf.getDatabasePath())
worker.connectToDatabase()


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Связаться с разработчиком', url='telegram.me/pihost'
        )
    )
    bot.send_photo(
        message.chat.id,
        "https://sun9-88.userapi.com/impg/B-eZpakYBL7JiCP3FJeuBb5GUFDKp7p_2zvSHQ/P3c5rZghzag.jpg?size=1280x1280"
        "&quality=95&sign=49718e812dadda3bfa16dfa16c520412&type=album",
        "Список команд доступен через меню\n" 
        "Чтобы посмотреть информацию о себе отправь - /show\n" 
        "Для получения списка наших социальных сетей отправь - /links\n"
        "Хочешь узнать о нас подробнее? - /about\n",
        reply_markup=keyboard
    )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    fullname = ''
    fullname += us_name if us_name is not None else ''  # Применение тернарного оператора

    if us_sname is not None:
        fullname += ' ' + us_sname

    if worker.userExist(us_id):
        bot.send_message(message.from_user.id, 'Привет, %s!' % (username))
    else:
        bot.send_message(message.from_user.id, 'Привет, %s! Ваше имя добавленно в базу данных!' % (username))
        worker.writeToDatabase(us_id, username, fullname, "", False)


@bot.message_handler(commands=['getnude'])
def get_nude(message):
    bot.send_photo(message.chat.id, 'https://www.meme-arsenal.com/memes/906057dd785388a0fa893ca85dc9b6b5.jpg');
    # bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


# Обрабатываем команду от администратора
@bot.message_handler(chat_id=[95597235, 1120038921],  # chat_id проверяем, в списке ли идентификатор пользователя
                     commands=['admin'])
def admin_rep(message):
    bot.send_message(message.chat.id, "You are allowed to use this command.")


# Обрабатываем команду от пользователя
@bot.message_handler(commands=['admin'])
def not_admin(message):
    bot.send_message(message.chat.id, "You are not allowed to use this command")
    # bot.send_message(95597235, 'Оповещение типо =)')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        fullname = ''
        fullname += us_name if us_name is not None else ''  # Применение тернарного оператора

        if us_sname is not None:
            fullname += ' ' + us_sname

        if worker.userExist(us_id):
            bot.send_message(message.from_user.id, 'Привет, %s!' % (username))
        else:
            bot.send_message(message.from_user.id, 'Привет, %s! Ваше имя добавленно в базу данных!' % (username))
            worker.writeToDatabase(us_id, username, fullname, "", False)


# Регистрируем фильтр
bot.add_custom_filter(custom_filters.ChatFilter())

bot.polling(none_stop=True, interval=0)
