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

smiles = {
    'done': u'\U00002705',
    'not_done': u'\U0000274C',
    'thumbs_up': u'\U0001F44D',
    'cake': u'\U0001F382',
    'present': u'\U0001F381',
    'popper': u'\U0001F389'
}

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
        bot.send_message(message.from_user.id, 'Привет, %s!' % username)
    else:
        bot.send_message(message.from_user.id, 'Привет, %s! Ваше имя добавленно в базу данных!' % username)
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
        dataMsg = "Данные повреждены"
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
    menu.add(telebot.types.InlineKeyboardButton(text="Проверить дни рождения", callback_data='check_bday'))

    bot.send_message(message.chat.id, "Что будем делать?", reply_markup=menu)


def make_event(message):
    a = 1


def process_congratulate_everyone(message):
    try:
        text = ""
        bdays = worker.getTodayBdaysUncong(datetime.now().date().strftime("%m-%d"))
        if bdays:
            cong_ids = list()
            if len(bdays) > 1:
                text = f"Сегодня день рождения сразу у несокльких наших участников!" \
                       f"Поздравляем:"
                for person in bdays:
                    text += f"\n@{person[0]}"
                    cong_ids.append(person[1])

                text += f"\n\nС Днем Рождения {smiles['present']}{smiles['popper']} " \
                        f"\nЖелаем вам крепкого здоровья, счастья, благополучия, только ровных дорог, пусть все у вас будет в жизни."
            else:
                cong_ids.append(bdays[0][1])
                text = f"Сегодня день рождения у @{bdays[0][0]}! {smiles['cake']}" \
                       f"\nС Днем Рождения {smiles['present']}{smiles['popper']} " \
                       f"\nЖелаем тебе крепкого здоровья, счастья, благополучия, только ровных дорог, пусть все у тебя будет в жизни."

            # try:
                # worker.makeCongratulate(cong_ids)
            # except (Exception,):
                # bot.reply_to(message, "Произошла ошибка во время внесения изменений в БД")

            done_text = f"Всех поздравили {smiles['thumbs_up']} (выполнено {message.from_user.username})"
            send_answer(conf.getAdminGroupId(), text, None)
            send_answer(message.chat.id, done_text, None)
            if message.chat.id != conf.getAdminGroupId():
                send_answer(conf.getAdminGroupId(), done_text, None)
    except (Exception,):
        bot.reply_to(message, "Что-то пошло не так")


def check_bday(message):
    # Получаем список дней рождений на сегодня (имя - поздравлен ли)
    bdays = worker.getTodayBdays(datetime.now().date().strftime("%m-%d"))

    text = "Сегодня дней рождений не найдено"
    menu = telebot.types.InlineKeyboardMarkup()
    if bdays:
        text = "Дни рождения сегодня:"
        for person in bdays:
            text += f"\n@{person[0]} ({smiles['done'] + 'Поздравлен' if person[1] else smiles['not_done'] + 'Надо поздравить'})"
        menu.add(telebot.types.InlineKeyboardButton(text="Поздравить всех", callback_data="congratulate_everyone"))

    send_answer(conf.getAdminGroupId(), text, None)
    send_answer(message.chat.id, text, menu if menu else None)


    # Проверяем, если список пуст - выводим, что некого поздравлять
    # Если список не пуст, то выводим списком всех именинников
    # Если в списке 1 непоздравленный, то предлагаем поздравить
    # Если в списке много непоздравленных, то предлагаем каждого отдельно (кнопками) или всех сразу


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    menu = telebot.types.InlineKeyboardMarkup()
    if call.data == "add_user_info":
        menu.add(telebot.types.InlineKeyboardButton(text="Да", callback_data='add_with_id'))
        menu.add(telebot.types.InlineKeyboardButton(text="Нет", callback_data='add_with_forward_message'))
        menu.add(telebot.types.InlineKeyboardButton(text="Вернуться к упарвлению", callback_data="back_to_admin"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Занесение данных нового участника в БД.\nИзвестен ли ID участника?", reply_markup=menu)
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
    elif call.data == "make_event":
        make_event(call.message)
    elif call.data == "check_bday":
        check_bday(call.message)
    elif call.data == "congratulate_everyone":
        process_congratulate_everyone(call.message)


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
        if message.forward_from:
            user_data = message.forward_from
            user.clear()
            user.setId(user_data.id)
            user.setName(user_data.full_name)
            user.setNickname(user_data.username)
            msg = bot.reply_to(message, 'Введите дату рождения участника? Формат: год-месяц-число (например, 1990-01-29)')
            bot.register_next_step_handler(msg, process_add_bday_step)
        else:
            bot.reply_to(message, "К сожалению, пользователь скрыл свои данные. Попроси его написать нам")
    except (Exception,):
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
        cong = date.date() < datetime.now().date()
        user.setDate(date.date().strftime("%Y-%m-%d"), cong)
        bot.reply_to(message, 'Данные участника заполнены. Добавляем его в базу данных')
        worker.writeToDatabase(id=user.getId(), nickname=user.getNickname(), name=user.getName(),
                               bday=user.getDate(), congratulate=user.isCongratulated())
        send_answer(message.chat.id, "Добавление завершено успешно", None)
    except (Exception,):
        bot.reply_to(message, "Что-то пошло не так")


# Обрабатываем команду от участника
@bot.message_handler(commands=['admin'])
def not_admin(message):
    bot.send_message(message.chat.id, f"Прости {message.from_user.username}, но у тебя нет прав на выполнение этой команды =)")
    bot.send_message(chat_id=conf.getAdminGroupId(), text=f"Некий негодяй {message.from_user.username}(id: {message.from_user.id}) пытался зайти в админку")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Привет, %s!' % message.from_user.username)
    # if message.text.lower() == 'привет':


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
