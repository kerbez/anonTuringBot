import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("anonturingbot.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anonturingbot.firebaseio.com'})


class User:
    id = ""
    realUsername = ""
    fakeUsername = ""
    chatId = None
    defaultUser = None

    def __init__(self, realUsername, chatId):
        self.realUsername = realUsername
        self.chatId = chatId
        ref = db.reference('users')
        new_user_ref = ref.push({
            'realUsername': realUsername,
            'chatId': chatId,
        })
        self.id = new_user_ref.key

    def setFakeUsername(self, fakeUsername):
        self.fakeUsername = fakeUsername

    def setdefaultUser(self, defaultUser):
        self.defaultUser = defaultUser

    def getRealUsername(self):
        return self.realUsername

    def getFakeUsername(self):
        return self.fakeUserName

    def getChatId(self):
        return self.chatId

    def getDefaultUser(self):
        return self.defaultUser
