import json


class Config:
    def __init__(self):
        with open('../config.json', 'r') as json_file:
            config_json = json_file.read()
            json_data = json.loads(config_json)
            self.TOKEN = json_data["TOKEN"]
            self.CHANNEL_NAME = json_data["CHANNEL_NAME"]
            self.ADMIN_GROUP_ID = json_data["ADMIN_GROUP_ID"]
            self.DATABASE_NAME = json_data["DATABASE_NAME"]
            self.DATABASE_PATH = json_data["DATABASE_PATH"]
            json_file.close()


    def getToken(self):
        return self.TOKEN

    def getChannelName(self):
        return self.CHANNEL_NAME

    def getDatabasePath(self):
        return self.DATABASE_PATH + self.DATABASE_NAME

    def getAdminGroupId(self):
        return self.ADMIN_GROUP_ID