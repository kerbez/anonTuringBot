import firebase_admin
from firebase_admin import credentials, db
import telebot
import constants
from User import User
import telegram

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


@bot.message_handler(commands=['help'])
def handle_help(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    user_res = db.reference('users').child(user.id).get()
    fakeUsername = user.fakeUsername
    defaultUser = user.defaultUser
    bot.send_message(chatId, 'Hi ' + realUsername)
    if fakeUsername != '-':
        bot.send_message(chatId, 'Your fake username is *' + fakeUsername + '*', parse_mode=telegram.ParseMode.MARKDOWN)
    if defaultUser != '-':
        bot.send_message(chatId, 'Your default user is *' + defaultUser + '*', parse_mode=telegram.ParseMode.MARKDOWN)
    bot.send_message(chatId, 'Here you can send anonymous messages to user whom '
                             'I know, you can check it by \ncommand /ishere _username_ ', parse_mode=telegram.ParseMode.MARKDOWN)
    bot.send_message(chatId, 'You can write to user with \ncommand /write _username_ _message_', parse_mode=telegram.ParseMode.MARKDOWN)
    bot.send_message(chatId, 'All users need to set their fake username with command '
                             '\n/set_username fakeusername its a username that will see receiver of message')
    bot.send_message(chatId, 'To make chatting more comfortable you can set your '
                             'default user whom you are always writing with command \n/write_always_to username \nAlso you can delete your default user with command /del_write_always_to \nYou can check you default user with command '
                             '/my_default_user')


@bot.message_handler(commands=['my_default_user'])
def handle_my_default_user(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    defaultUser = user.defaultUser
    if defaultUser != '-':
        bot.send_message(chatId, 'Your default user is *' + defaultUser + '*', parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chatId, "You don\' have default user, you can set it with command /write_always_to *username*", parse_mode=telegram.ParseMode.MARKDOWN)


@bot.message_handler(commands=['set_username'])
def handle_set_username(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    print(len(message.text.split()))
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
def handle_ishere(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    print(len(message.text.split()))
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


@bot.message_handler(commands=['write'])
def handle_write(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    fakeUsername = user.fakeUsername
    print(len(message.text.split()))
    if len(message.text.split()) >= 3:
        m = message.text.split()
        user_ref = db.reference('users').get()
        is_ok = 0
        if fakeUsername != '-':
            for id in user_ref:
                if user_ref[id]['realUsername'] == m[1]:
                    mes = ''
                    secChatId = user_ref[id]['chatId']
                    for i in range(2, len(m)):
                        mes += m[i] + ' '
                    bot.send_message(secChatId, 'from *' + fakeUsername + '*\n' + mes, parse_mode=telegram.ParseMode.MARKDOWN)
                    is_ok = 1
            if is_ok == 0:
                bot.send_message(user.chatId, 'no such user')
        else:
            bot.send_message(chatId, 'You can\'t send anonymous message without fake username')
            bot.send_message(chatId, 'Please create fake username with command /set_username')
            bot.send_message(chatId, 'Example: /set_username yourfakeusername')
    else:
        bot.send_message(user.chatId, 'incorrect command format')


@bot.message_handler(commands=['write_always_to'])
def handle_write_always_to(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    fakeUsername = user.fakeUsername
    print(len(message.text.split()))
    if len(message.text.split()) == 2:
        print('ok')
        m = message.text.split()
        user_ref = db.reference('users').get()
        is_ok = 0
        if fakeUsername != '-':
            for id in user_ref:
                if user_ref[id]['realUsername'] == m[1]:
                    user.setdefaultUser(m[1], user_ref[id]['chatId'])
                    bot.send_message(chatId, '*You set default user as* _' + m[1] + '_', parse_mode=telegram.ParseMode.MARKDOWN)
                    bot.send_message(chatId, 'Any message you write without command will be automatically send to this user')
                    bot.send_message(chatId, 'You can cancel this setting using \n/del_write_always_to command')
                    is_ok = 1
            if is_ok == 0:
                bot.send_message(user.chatId, 'no such user')
        else:
            bot.send_message(chatId, 'You can\'t send anonymous message without fake username')
            bot.send_message(chatId, 'Please create fake username with command /set_username')
            bot.send_message(chatId, 'Example: /set_username yourfakeusername')
    else:
        bot.send_message(user.chatId, 'incorrect command format')


@bot.message_handler(commands=['del_write_always_to'])
def handle_del_write_always_to(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    fakeUsername = user.fakeUsername
    print(len(message.text.split()))
    if len(message.text.split()) == 1:
        print('ok')
        m = message.text.split()
        user_ref = db.reference('users').get()
        is_ok = 0
        if fakeUsername != '-':
            defaultUser = user.defaultUser
            if defaultUser == '-':
                bot.send_message(chatId, 'You dont have default user')
            else:
                user.setdefaultUser('-', '-')
                bot.send_message(chatId, 'successfully deleted default user')
        else:
            bot.send_message(chatId, 'You can\'t send anonymous message without fake username')
            bot.send_message(chatId, 'Please create fake username with command /set_username')
            bot.send_message(chatId, 'Example: /set_username yourfakeusername')
    else:
        bot.send_message(user.chatId, 'incorrect command format')


@bot.message_handler()
def handle_message(message):
    chatId = message.chat.id
    realUsername = message.from_user.username
    user = User(realUsername, chatId)
    fakeUsername = user.fakeUsername
    defaultUser = user.defaultUser
    defaultUserChatId = user.defaultUserChatId
    if fakeUsername != '-':
        if defaultUser != '-':
            bot.send_message(defaultUserChatId, 'from *' + fakeUsername + '*:\n' + message.text, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(chatId, 'You don\'t have default user to write to')
            bot.send_message(chatId, 'you can set default user with /write_always_to command')
            bot.send_message(chatId, 'Example: /write_always_to almas')
    else:
        bot.send_message(chatId, 'You can\'t send anonymous message without fake username')
        bot.send_message(chatId, 'Please create fake username with command /set_username')
        bot.send_message(chatId, 'Example: /set_username your_fake_username')


bot.polling(none_stop=True, interval=0)