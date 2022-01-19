from bs4 import BeautifulSoup
import time
import requests
import pickle
import threading
import telebot
from telebot import types

bot = telebot.TeleBot("2103027208:AAFedt2lIax0kZraXsqSgAe8VSW6VHLx8ZQ")

#with open('users.pickle', 'wb') as f:
#    pickle.dump([], f) #1731254825, 1639768908, 199945910, 298536200, 1769307034

with open('users.pickle', 'rb') as f:
    users = pickle.load(f)
    print(users)

def get_name(car):
    return car.find(class_='card__title').text

def get_price(car):
    return car.find(class_='caption__top currentBid').find('strong').text


def get_link(car):
    return "https://auktion.biliaoutlet.se" + car.find('a', class_='card__inner').get('href')


def reset_mem():
    with open('cars.dat', 'wb') as f:
        pickle.dump([], f)

#reset_mem()

def check_car(link):
    with open('cars.dat', 'rb') as f:
        cars_mem = pickle.load(f)
    if link not in cars_mem:
        cars_mem.append(link)
        if len(cars_mem) > 30:
            cars_mem = cars_mem[-20:]
        with open('cars.dat', 'wb') as f:
            pickle.dump(cars_mem, f)
        return True
    return False


def main():
    while True:
        try:
            r = requests.get('https://auktion.biliaoutlet.se/Home/Search?Search=&submit-button=Sök')
            soup = BeautifulSoup(r.text, 'lxml')
            cars = soup.find_all(class_='card') + BeautifulSoup(requests.get('https://auktion.biliaoutlet.se').text, 'lxml').find_all(class_='card')
            car = cars[0]
            
            if check_car(get_link(car)):

                print(get_name(car))
                
                with open('users.pickle', 'rb') as f:
                    users = pickle.load(f)
                    print(users)
                
                for user in users:
                    #print("sending " + str(user))
                    try:
                        bot.send_message(user, f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}") #user
                        print(f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                    except Exception as ex:
                        print(ex)
                
        except Exception as ex:
            print(ex)
            time.sleep(3)
            
        time.sleep(1.5)

bot.send_message(1731254825, "run")

x = threading.Thread(target=main)
x.start()

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.split(" ")[0] == "yes":
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
            
        users.append( int(call.data.split(" ")[1]) )
        
        with open('users.pickle', 'wb') as f:
                pickle.dump(users, f)

        bot.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Ваш запрос подтвердили. Теперь бот будет присылать вам ссылки.")
        
    elif call.data.split(" ")[0] == "no":
        bot.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Ваш запрос отклонили.")
        bot.send_message(call.from_user.id, "Запрос отклонен.")

    else:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
            
        users.remove( int(call.data.split(" ")[1]) )
                     
        with open('users.pickle', 'wb') as f:
                pickle.dump(users, f)

        bot.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Вы были отключены от бота.")
        bot.send_message(call.from_user.id, "Юзер отключен.")  

@bot.message_handler(commands=['removeuser'])
def remove_user(message):
    if message.from_user.id == 1731254825 or message.from_user.id == 1639768908:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
            
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        for user in users:
            markup.add(types.InlineKeyboardButton(user, callback_data=f'remove {user}'))
        
        bot.send_message(message.from_user.id, text=f'Укажите айди:', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.from_user.id != 1731254825 and message.from_user.id != 1639768908:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)

        if message.from_user.id not in users:
            bot.send_message(message.from_user.id, "Запрос на регистрацию отправлен админу. Ждите подтверждения")

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("подтвердить", callback_data=f'yes {message.from_user.id}')
            item2 = types.InlineKeyboardButton("отклонить", callback_data=f'no {message.from_user.id}')
            markup.add(item1, item2)
            
            bot.send_message(1731254825, text=f'Запрос от {message.from_user.first_name}. Айди: {message.from_user.id}', reply_markup=markup)
            
        else:
            bot.send_message(message.from_user.id, "Вы уже зарегистрированы в боте, можете им пользоваться.")
    else:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
        if message.text not in users:
            users.append(int(message.text))
            with open('users.pickle', 'wb') as f:
                pickle.dump(users, f)
            bot.send_message(message.from_user.id, "Пользователь успешно добавлен.")
        else:
            bot.send_message(message.from_user.id, "Пользователь уже в базе.")

bot.infinity_polling()
