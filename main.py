from bs4 import BeautifulSoup
import time
import requests
import sqlite3

# create db
db = sqlite3.connect("db.db", check_same_thread=False)
cursor = db.cursor()


def get_name(car):
    return car.find(class_='card__title').text


def get_price(car):
    return car.find(class_='caption__top currentBid').find('strong').text


def get_link(car):
    return "https://auktion.biliaoutlet.se" + car.find('a', class_='card__inner').get('href')


def send_message(chat_id, text):  # send telegram message
    try:
        URL = 'https://api.telegram.org/bot' + "2103027208:AAFedt2lIax0kZraXsqSgAe8VSW6VHLx8ZQ" + '/'
        url = URL + f'sendMessage?chat_id={chat_id}&text={text}'
        requests.get(url)
    except Exception as ex:
        print(ex)

send_message(1731254825, "run")

def write_file(src, car):  # write to file
    try:
        for line in src:
            if get_name(car) == str(line):
                return False
        return True
    except Exception as ex:
        print(ex)


def main():
    while True:
        try:
            r = requests.get('https://auktion.biliaoutlet.se/Home/Search?Search=&submit-button=Sök')
            soup = BeautifulSoup(r.text, 'lxml')
            cars = soup.find_all(class_='card') + BeautifulSoup(requests.get('https://auktion.biliaoutlet.se').text, 'lxml').find_all(class_='card')
            with open('cars.txt', 'r+', encoding='utf-8') as file:
                src = file.read().split('\n')
                for car in cars:
                    if write_file(src, car):
                        file.writelines(get_name(car) + "\n")
                        for value in cursor.execute("SELECT id FROM users"):
                            value = ''.join(sym for sym in value)
                            send_message(value, f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                            #print(f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                    else:
                        continue
        except Exception as ex:
            print(ex)
            send_message(1731254825, str(ex))
        time.sleep(30)


if __name__ == '__main__':
    main()
