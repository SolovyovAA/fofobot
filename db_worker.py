import sqlite3

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

