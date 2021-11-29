from bs4 import BeautifulSoup
import time
import requests
import pickle
import threading
import telebot

with open('users.pickle', 'wb') as f:
    pickle.dump([1731254825, 1639768908, 199945910, 298536200], f)

def get_name(car):
    return car.find(class_='card__title').text


def get_price(car):
    return car.find(class_='caption__top currentBid').find('strong').text


def get_link(car):
    return "https://auktion.biliaoutlet.se" + car.find('a', class_='card__inner').get('href')


def reset_mem():
    with open('cars.dat', 'wb') as f:
        pickle.dump([], f)

        
reset_mem()


def send_message(chat_id, text):  # send telegram message
    try:
        URL = 'https://api.telegram.org/bot' + "2103027208:AAFedt2lIax0kZraXsqSgAe8VSW6VHLx8ZQ" + '/'
        url = URL + f'sendMessage?chat_id={chat_id}&text={text}'
        requests.get(url)
    except Exception as ex:
        print(ex)

send_message(1731254825, "run")

def check_car(link):
    with open('cars.dat', 'rb') as f:
        cars_mem = pickle.load(f)
    if link not in cars_mem:
        cars_mem.append(link)
        if len(cars_mem) > 6:
            cars_mem = cars_mem[-6:]
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
            with open('users.pickle', 'rb') as f:
                users = pickle.load(f)
                print(users)
                
            car = cars[0]

            print(get_name(car))
            print(check_car(get_link(car)))
            
            if check_car(get_link(car)):
                for user in users:
                    try:
                        send_message(user, f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}") #user
                        #print(f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                    except Exception as ex:
                        print(ex)
                
        except Exception as ex:
            print(ex)
            time.sleep(2)
            
        time.sleep(2)


x = threading.Thread(target=main)
x.start()

bot = telebot.TeleBot("2103027208:AAFedt2lIax0kZraXsqSgAe8VSW6VHLx8ZQ")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    
    with open('users.pickle', 'rb') as f:
        users = pickle.load(f)

    if message.from_user.id not in users:
        users.append(message.from_user.id)
        bot.send_message(message.chat.id, "Поздравляю, теперь вы можете пользоваться ботом.")
        with open('users.pickle', 'wb') as f:
            pickle.dump(users, f)
    else:
        bot.send_message(message.chat.id, "Вы уже можете пользоваться ботом!")

bot.infinity_polling()
