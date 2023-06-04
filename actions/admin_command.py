from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from classes.app_components import components


class AdminCommands(StatesGroup):
    waiting_for_admin_action = State()
    waiting_for_food_size = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Выберите, что хотите заказать: напитки (/drinks) или блюда (/food).",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")


async def admin_reply(message: types.Message, state: FSMContext):
    if components.database():
        if components.database().isUserAdmin(message.from_user.id):
            menu = types.ReplyKeyboardMarkup()
            menu.add("Добавить данные участника")
            menu.add("Изменить данные участника")
            menu.add("Удалить данные участника")
            menu.add("Создать встречу")
            menu.add("Проверить дни рождения")

            await state.set_state(AdminCommands.waiting_for_admin_action.state)
            await message.answer("Что будем делать?", reply_markup=menu)
        else:
            await components.bot().send_message(message.chat.id,
                                   f"Прости {message.from_user.username}, но у тебя нет прав на выполнение этой команды =)")
            await components.bot().send_message(chat_id=components.config().getAdminGroupId(),
                                   text=f"Некий негодяй {message.from_user.username}(id: {message.from_user.id}) пытался зайти в админку")


def register_handlers_admin():
    dp = components.disp()
    dp.register_message_handler(callback=cmd_start, commands="add_user_info", state="*")
    dp.register_message_handler(cmd_cancel, commands="edit_user_info", state="*")
    dp.register_message_handler(cmd_cancel, commands="delete_user_info", state="*")
    dp.register_message_handler(cmd_cancel, commands="make_event", state="*")
    dp.register_message_handler(cmd_cancel, commands="check_bday", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(admin_reply, commands="admin")
