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
        res = ref.get()
        is_ok = 0
        for id in res:
            if res[id]['realUsername'] == realUsername:
                self.id = id
                self.fakeUsername = ref.child(id).child('fakeUsername').get()
                self.defaultUser = ref.child(id).child('defaultUser').get()
                print(self.fakeUsername, self.defaultUser)
                is_ok = 1

        if is_ok == 0:
            new_user_ref = ref.push({
                'realUsername': realUsername,
                'chatId': chatId,
                'fakeUsername': '-',
                'defaultUser': '-',
            })
            self.id = new_user_ref.key

    def setFakeUsername(self, fakeUsername):
        ref = db.reference('users')
        ref.child(self.id).update({
            'fakeUsername': fakeUsername
        })
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
