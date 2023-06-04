import sqlite3
from datetime import datetime


class DBWorker:
    def __init__(self, pathToDb):
        self.pathToDb = pathToDb

    def connectToDatabase(self):
        self.conn = sqlite3.connect(self.pathToDb, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def writeToDatabase(self, id: int, nickname: str, name: str, bday: str, congratulate: bool):
        self.cursor.execute('INSERT INTO Users (user_id, nickname, name, bday, congratulate) VALUES (?, ?, ?, ?, ?)',
                            (id, nickname, name, bday, congratulate))
        self.conn.commit()

    def userExist(self, id: int ):
        exist = self.cursor.execute(f'SELECT * FROM Users WHERE user_id={id}').fetchone()
        if exist is None:
            return False
        else:
            return True

    def getUserData(self, id: int):
        data = self.cursor.execute(f'SELECT nickname, name, bday, congratulate FROM Users WHERE user_id={id} LIMIT 1').fetchone()
        return data

    def isUserAdmin(self, id: int) -> bool:
        data = self.cursor.execute(
            f'SELECT user_id FROM Users WHERE user_id={id} AND admin = 1 LIMIT 1').fetchone()
        if data is None:
            return False
        else:
            return True

    def getTodayBdays(self, date: datetime):
        data = self.cursor.execute(
            f'SELECT nickname, congratulate, user_id FROM Users WHERE bday LIKE \'%{date}\'').fetchall()
        return data

    def getTodayBdaysUncong(self, date: datetime):
        data = self.cursor.execute(
            f'SELECT nickname, user_id FROM Users WHERE congratulate = 0 AND bday LIKE \'%{date}\'').fetchall()
        return data

    def makeCongratulate(self, ids: list):
        data = self.cursor.execute()
