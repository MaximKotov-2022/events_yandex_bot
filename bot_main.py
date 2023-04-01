import os
from urllib.request import urlopen

import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
RETRY_PERIOD = 60


def site_parsing():
    """Получение данных сайта."""
    url = "https://events.yandex.ru/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    events = soup.find(class_='events__container')

    return events


def processing_data_website():
    """Обработка данных сайта после парсинга."""
    events = site_parsing()
    data_events = []
    for event in events:
        if len(event) != 0:
            date = 'Дата: ' + event.find(class_='event-card__date').text
            name = 'Название: ' + event.find(class_='event-card__title').text
            if 'https' not in event.find('a').get('href'):
                site = (
                    'Ссылка: ' + 'https://events.yandex.ru'
                    + event.find('a').get('href')
                )
            else:
                site = 'Ссылка: ' + event.find('a').get('href')
            data_events.append(
                {
                    'date': date,
                    'name': name,
                    'site': site,
                }
            )

    return data_events


def send_message(bot, message):
    """
    Провреяет доступность токенов.

    Возвращает: Returns
    True - если токены доступны,
    False - если хотя бы одного токена нет.
    """
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_message(bot, str(processing_data_website()))

    # while True:
    #     send_message(bot, str(processing_data_website()))
    #     time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
