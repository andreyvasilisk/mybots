import sqlite3
import telebot
from fake_useragent import UserAgent
from config import TOKEN
import time
useragent = UserAgent()

# create db
db = sqlite3.connect("db.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id TEXT,
    name TEXT
)""")
db.commit()


# bot
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('on', 'off')
    #bot.send_message(message.chat.id, "<b>Привет!</b> &#128075;&#128075;&#128075;\nПодпишись чтобы быть в курсе о новый "
                                      #"криптоволют &#9989;\n&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;\n<b>Hello!</b> &#128075;&#128075;&#128075;\nSubscribe "
                                      #"to "
                                      #"stay informed about the new cryptocurrency &#9989;", reply_markup=keyboard, parse_mode='html')
    
    bot.send_message(message.chat.id, "Привет!", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'on':
        cursor.execute(f"SELECT id FROM users WHERE id = '{message.chat.id}'")
        if cursor.fetchone() is None:
            db.execute(f"INSERT INTO users VALUES(?,?)", (message.chat.id, message.from_user.first_name))
            db.commit()
            bot.send_message(message.chat.id, 'Вы подписаны! &#128512;\n&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;\nyou are subscribed! &#128512;', parse_mode='html')
            bot.send_message(1639768908,
                             f'Новый пользователь <b>{message.from_user.first_name}</b> подписался на бота &#129321;\nТекущиее число подписчиков: <b>{len(list(cursor.execute("SELECT * FROM users")))}</b>',
                             parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вы уже подписаны!\n&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;\nYou are already subscribed!', parse_mode='html')
    if message.text == 'off':
        cursor.execute(f"SELECT id FROM users WHERE id = '{message.chat.id}'")
        if cursor.fetchone() is not None:
            cursor.execute(f"DELETE FROM users WHERE id = '{message.chat.id}'")
            bot.send_message(message.chat.id, 'Вы отписаны &#128532;\n&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;\nYou are unsubscribed &#128532;', parse_mode='html')
            bot.send_message(1639768908,
                             f'Пользователь <b>{message.from_user.first_name}</b> отписался от бота &#128532;\nТекущиее число подписчиков: {len(list(cursor.execute("SELECT * FROM users")))}',
                             parse_mode='html')
            bot.send_message(1792076176,
                             f'Пользователь <b>{message.from_user.first_name}</b> отписался от бота &#128532;\nТекущиее число подписчиков: {len(list(cursor.execute("SELECT * FROM users")))}',
                             parse_mode='html')

        else:
            bot.send_message(message.chat.id, "Вы и так та не подписаны &#128516;\n&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;&#10134;\nYou are not "
                                              "subscribed "
                                              "anyway &#128516; (on - subscribe)", parse_mode='html')


def connect():
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(60)
        connect()


if __name__ == '__main__':
    connect()

