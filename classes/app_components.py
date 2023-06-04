from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from classes import db_worker, config


class AppComponents:
    def __int__(self):
        self.config = config.Config()
        if self.config:
            self.db_worker = db_worker.DBWorker(self.config.getDatabasePath())
            self.db_worker.connectToDatabase()
            # Инициализация бота и диспетчера с FSM
            self.bot = Bot(token=self.config.getToken())
            self.disp = Dispatcher(bot=self.bot, storage=MemoryStorage())

    def config(self):
        return self.config

    def database(self):
        if self.db_worker is None:
            print("Database is not initialized")
            return None
        return self.db_worker

    def bot(self):
        if self.bot:
            return self.bot

    def disp(self):
        if self.disp:
            return self.disp


components = AppComponents()
