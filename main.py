from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import TOKEN
import time
import requests
import sqlite3
useragent = UserAgent()

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
        URL = 'https://api.telegram.org/bot' + TOKEN + '/'
        url = URL + f'sendMessage?chat_id={chat_id}&text={text}'
        requests.get(url)
    except Exception as ex:
        pass


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
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Cookie': 'ASP.NET_SessionId=qqez0ml3nkfahyerpnauvrea; __utmc=204301824; __utmz=204301824.1627062623.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1073684940.1627062623; _gid=GA1.2.760241878.1627062623; imbox={"imboxUid":"1vj5ORC0RstSf3KAUWBcD9NCE8c"}; cookie-accept=accepted; imboxInteraction={"interaction":{"default":1627063223739}}; googtrans=/sv/en; googtrans=/sv/en; __atuvc=1%7C29%2C10%7C30; __utma=204301824.1073684940.1627062623.1627236511.1627275194.7; __utmt=1; imboxStats={"seen":true}; _gat_UA-6976370-1=1; __utmb=204301824.6.10.1627275194',
                'Host': 'auktion.biliaoutlet.se',
                'Origin': 'https://auktion.biliaoutlet.se',
                'Referer': 'https://auktion.biliaoutlet.se/Home/',
                'sec-ch-ua': '"Opera GX";v="77", "Chromium";v="91", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': useragent.random
            }

            r = requests.get('https://auktion.biliaoutlet.se/Home/Search?Search=&submit-button=Sök')
            soup = BeautifulSoup(r.text, 'lxml')
            cars = soup.find_all(class_='card') + BeautifulSoup(
                requests.get('https://auktion.biliaoutlet.se', headers=headers).text, 'lxml').find_all(class_='card')
            with open('cars.txt', 'r+', encoding='utf-8') as file:
                src = file.read().split('\n')
                for car in cars:
                    if write_file(src, car):
                        file.writelines(get_name(car) + "\n")
                        for value in cursor.execute("SELECT id FROM users"):
                            value = ''.join(sym for sym in value)
                            send_message(value, f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                            print(f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                    else:
                        continue
        except Exception as ex:
            print(ex)
        time.sleep(20)


if __name__ == '__main__':
    main()
