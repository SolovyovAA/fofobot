import datetime

import telebot

import config

import db_worker

import user_class

from dateutil import parser

from telebot import custom_filters

from datetime import datetime

user = user_class.User()

conf = config.Config()

bot = telebot.TeleBot(conf.getToken())
worker = db_worker.DBWorker(conf.getDatabasePath())
worker.connectToDatabase()


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


# Обрабатываем запрос "помощи"
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


# Обрабатываем запрос информации о клубе
@bot.message_handler(commands=['about'])
def about_command(message):
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


# Обрабатываем запрос информации о сохраненной информации об участнике
@bot.message_handler(commands=['show'])
def show_command(message):
    us_id = message.from_user.id
    username = message.from_user.username

    if worker.userExist(us_id):
        # TODO: Запрос данных о пользователе
        userData = worker.getUserData(us_id)
        if userData:
            dataMsg = f"Итак, что же мы передаем в __FBI Open Up__ о неком *{userData[0]}\n*" \
                      f"Мы зовем тебя: *{userData[1]}*\n"\
                      f"Дата рождения: *{userData[2] if len(userData[2])>0 else 'TOP SECRET'}*\n"\
                      f"И что мы тебя *{ 'уже поздравляли в этом году' if userData[3] == True else 'еще не поздравляли в этом году.'}*"

        bot.send_message(message.from_user.id, dataMsg, parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id, f'{username}, к сожалению, нам пока ничего о тебе неизвестно')


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
@bot.message_handler(chat_id=[95597235, 1120038921],  # chat_id проверяем, в списке ли идентификатор участника
                     commands=['admin'])
def admin_rep(message):
    menu = telebot.types.InlineKeyboardMarkup()
    menu.add(telebot.types.InlineKeyboardButton(text="Добавить данные участника", callback_data='add_user_info'))
    menu.add(telebot.types.InlineKeyboardButton(text="Изменить данные участника", callback_data='edit_user_info'))
    menu.add(telebot.types.InlineKeyboardButton(text="Удалить данные участника", callback_data='delete_user_info'))
    menu.add(telebot.types.InlineKeyboardButton(text="Создать встречу", callback_data='make_event'))

    bot.send_message(message.chat.id, "Что будем делать?", reply_markup=menu)


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    menu = telebot.types.InlineKeyboardMarkup()
    if call.data == "add_user_info":
        menu.add(telebot.types.InlineKeyboardButton(text="Да", callback_data='add_with_id'))
        menu.add(telebot.types.InlineKeyboardButton(text="Нет", callback_data='add_with_forward_message'))
        menu.add(telebot.types.InlineKeyboardButton(text="Вернуться к упарвлению", callback_data="back_to_admin"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Занесение данных нового участника в БД.\n Известен ли ID участника?", reply_markup=menu)
    elif call.data == "add_with_id":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Введите ID участника:", reply_markup=menu)
        bot.register_next_step_handler(call.message, process_add_id_step)
    elif call.data == "add_with_forward_message":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Перешли сообщение от участника:", reply_markup=menu)
        bot.register_next_step_handler(call.message, process_add_message_step)
    elif call.data == "back_to_admin":
        admin_rep(call.message)


def send_answer(chatid, message, menu):
    if menu:
        bot.send_message(chat_id=chatid, text=message, reply_markup=menu)
    else:
        bot.send_message(chat_id=chatid, text=message)


def process_add_id_step(message):
    try:
        if message.text.isdigit():
            chat_id = message.chat.id
            user_id = int(message.text)
            user.clear()
            user.setId(user_id)

            if worker.userExist(user_id):
                menu = telebot.types.InlineKeyboardMarkup()
                menu.add(telebot.types.InlineKeyboardButton(text="Вернуться в начало", callback_data="add_user_info"))
                send_answer(chat_id, "Такой пользователь уже существует", menu)
            else:
                msg = bot.reply_to(message, 'Введите имя участника?')
                bot.register_next_step_handler(msg, process_add_name_step)
        else:
            menu = telebot.types.InlineKeyboardMarkup()
            menu.add(telebot.types.InlineKeyboardButton(text="Вернуться в начало", callback_data="add_user_info"))
            bot.send_message(chat_id=message.chat.id, text="Идентификатор участника должен быть числом", reply_markup=menu)
    except (Exception,):
        bot.reply_to(message, "Что-то пошло не так")


def process_add_message_step(message):
    try:
        # forward_date - поле
        chat_id = message.chat.id
        name = message.text
        user.clear()
        # user = uc.User(name)
        # user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        # bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так")


def process_add_name_step(message):
    user.setName(message.text)
    msg = bot.reply_to(message, 'Введите никнейм участника?')
    bot.register_next_step_handler(msg, process_add_nick_step)


def process_add_nick_step(message):
    user.setNickname(message.text)
    msg = bot.reply_to(message, 'Введите дату рождения участника?')
    bot.register_next_step_handler(msg, process_add_bday_step)


def process_add_bday_step(message):
    try:
        date = parser.parse(message.text)
        user.setDate(date.date(), date.date() < datetime.datetime.now().date())
        bot.reply_to(message, 'Данные участника заполнены. Добавляем его в базу данных')
        worker.writeToDatabase(user.getId(), user.getNickname(), user.getName(), user.getDate(), user.isCongratualted())
        send_answer(message.chat.id, "Добавление завершено успешно")
    except (Exception,):
        bot.reply_to(message, "Что-то пошло не так")


# Обрабатываем команду от участника
@bot.message_handler(commands=['admin'])
def not_admin(message):
    bot.send_message(message.chat.id, f"Прости {message.from_user.username}, но у тебя нет прав на выполнение этой команды =)")


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


if __name__ == "__main__":
    # Регистрируем фильтр
    bot.add_custom_filter(custom_filters.ChatFilter())


    # Enable saving next step handlers to file "./.handlers-saves/step.save".
    # Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
    # saving will happen after delay 2 seconds.
    # bot.enable_save_next_step_handlers(delay=2)


    # Load next_step_handlers from save file (default "./.handlers-saves/step.save")
    # WARNING It will work only if enable_save_next_step_handlers was called!
    # bot.load_next_step_handlers()

    bot.polling(none_stop=True, interval=0)
