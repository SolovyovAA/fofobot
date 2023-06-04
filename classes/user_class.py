class User:
    def __init__(self, user_id=0, nickname='', name=''):
        self.id = user_id
        self.nickname = nickname
        self.name = name
        self.date = ""
        self.congratulate = False

    def setId(self, user_id: int):
        self.id = user_id

    def setNickname(self, nick: str):
        self.nickname = nick

    def setName(self, name: str):
        self.name = name

    def setDate(self, date: str, congrat: bool):
        self.date = date
        self.congratulate = congrat

    def getId(self):
        return self.id

    def getNickname(self):
        return self.nickname

    def getName(self):
        return self.name

    def getDate(self) -> str:
        return self.date

    def isCongratulated(self):
        return self.congratulate

    def clear(self):
        self.id = 0
        self.nickname = ''
        self.name = ''
        self.date = ''
        self.congratulate = False
