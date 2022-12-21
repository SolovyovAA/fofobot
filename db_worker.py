import sqlite3

class DBWorker:
    def __init__(self, pathToDb):
        self.pathToDb = pathToDb

    def connectToDatabase(self):
        self.conn = sqlite3.connect(self.pathToDb, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def writeToDatabase(self, nickname: str, name: str, bday: str, congratulate: bool):
        self.cursor.execute('INSERT INTO Users (nickname, name, bday, congratulate) VALUES (?, ?, ?, ?)',
                            (nickname, name, bday, congratulate))
        self.conn.commit()

