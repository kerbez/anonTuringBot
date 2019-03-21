import firebase_admin
from firebase_admin import credentials, db
import telebot
import constants
from User import User

# cred = credentials.Certificate("anonturingbot.json")
# firebase_admin.initialize_app('anonturingbot', cred, {
#     'databaseURL': 'https://anonturingbot.firebaseio.com'})
# firebase_admin.get_app()

if 'anonturingbot' not in firebase_admin._apps:
    cred = credentials.Certificate('anonturingbot.json')
    firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://anonturingbot.firebaseio.com',
            'storageBucket': 'anonturingbot.appspot.com'}, name='anonturingbot')



bot = telebot.TeleBot(constants.token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)

    user_res = db.reference('users').child(user.id).get()
    print(user_res)
    if user_res is not None:
        bot.send_message(user.chatId, 'it works')
    else:
        bot.send_message(message.chat.id, 'doesnt')


bot.polling(none_stop=True, interval=0)