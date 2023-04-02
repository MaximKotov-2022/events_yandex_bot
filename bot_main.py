import os
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
RETRY_PERIOD = 3600


def site_parsing():
    """Получение данных сайта (парсинг)."""
    url = "https://events.yandex.ru/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    events = soup.find(class_='events__container')

    return events


def processing_data_website():
    """Обработка данных сайта после парсинга. Получение информации"""
    events = site_parsing()
    data_events = []

    for event in events:
        if len(event) != 0:
            date = event.find(class_='event-card__date').text
            name = event.find(class_='event-card__title').text
            if 'https' not in event.find('a').get('href'):
                site = (
                    'https://events.yandex.ru' + event.find('a').get('href')
                )
            else:
                site = event.find('a').get('href')

            data_events.append(
                {
                    "date": date,
                    "name": name,
                    "site": site,
                }
            )

    return data_events


def send_message(update, context):
    """Отправка сообщений.

    Работает при отправке любого сообщения только один раз.
    """
    chat = update.effective_chat
    data = processing_data_website()
    text = []

    for event in data:
        date = event['date']
        name = event['name']
        site = event['site']
        text.append(f'Дата: {date}\nНазвание: {name}\nСайт: {site}\n\n\n')

    context.bot.send_message(
        chat_id=chat.id,
        text=''.join(text),
        disable_web_page_preview=True,
    )

    text.clear()


def main():
    """Запуск бота."""
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, send_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
