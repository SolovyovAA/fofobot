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


# Обрабатываем запрос ссылок
@bot.message_handler(commands=['links'])
def get_links(message):
    links = telebot.types.InlineKeyboardMarkup()
    links.add(telebot.types.InlineKeyboardButton(text='VK', url='https://vk.com/fofodmd'))
    links.add(telebot.types.InlineKeyboardButton(text='Telegram', url='https://t.me/fo_fo_dmd'))
    links.add(telebot.types.InlineKeyboardButton(text='Telegram Чат', url='https://t.me/+NZ3ioiHi2_E4ZmZi'))
    links.add(telebot.types.InlineKeyboardButton(text='Instagram*', url='https://www.instagram.com/focus_club_dmd/'))

    bot.send_message(message.chat.id, text='Наши социальные сети:', reply_markup=links)
    bot.send_message(message.chat.id, text="*Запрещенная организация на территории РФ")


# Обрабатываем команду от администратора
@bot.message_handler(chat_id=[95597235, 1120038921],  # chat_id проверяем, в списке ли идентификатор пользователя
                     commands=['admin'])
def admin_rep(message):
    bot.send_message(message.chat.id, "You are allowed to use this command.")


# Обрабатываем команду от пользователя
@bot.message_handler(commands=['admin'])
def not_admin(message):
    bot.send_message(message.chat.id, "Прости, но у тебя нет прав на выполнение этой команды =)")


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
