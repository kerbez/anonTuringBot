import firebase_admin
from firebase_admin import credentials, db
import telebot
import constants
from User import User

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
    print(user_res['realUsername'])
    print(user_res['fakeUsername'])
    if user_res is not None:
        if user.fakeUsername == '-':
            bot.send_message(user.chatId, 'If you want to chat with other users, you need to create fake username \nWhite your fake username followed by /set_username command')
        else:
            bot.send_message(user.chatId, 'hi ' + user.realUsername)
    else:
        bot.send_message(message.chat.id, 'doesnt')


@bot.message_handler(commands=['set_username'])
def handle_start(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    print(len(message.text.split()) )
    if len(message.text.split()) == 2:
        print('ok')
        m = message.text.split()[1]
        print(m)
        user.setFakeUsername(m)
        fakeUsername = user.fakeUsername
        print(fakeUsername)
    else:
        bot.send_message(user.chatId, 'incorrect command format')


@bot.message_handler(commands=['ishere'])
def handle_start(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    print(len(message.text.split()) )
    if len(message.text.split()) == 2:
        print('ok')
        m = message.text.split()[1]
        user_ref = db.reference('users').get()
        is_ok = 0
        for id in user_ref:
            if user_ref[id]['realUsername'] == m:
                bot.send_message(user.chatId, 'yes')
                is_ok = 1
        if is_ok == 0:
            bot.send_message(user.chatId, 'no(')
    else:
        bot.send_message(user.chatId, 'incorrect command format')


bot.polling(none_stop=True, interval=0)