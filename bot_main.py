import os
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater, CommandHandler
from telegram import ReplyKeyboardMarkup

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
RETRY_PERIOD = 3600


class GetData:
    def site_parsing():
        """Получение данных сайта (парсинг)."""
        url = "https://events.yandex.ru/"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        events = soup.find(class_='events__container')

        return events

    def processing_data_website():
        """Обработка данных сайта после парсинга."""
        events = GetData.site_parsing()
        data_events = []

        for event in events:
            if len(event) != 0:
                date = event.find(class_='event-card__date').text
                name = event.find(class_='event-card__title').text
                if 'https' not in event.find('a').get('href'):
                    site = (
                        'https://events.yandex.ru'
                        + event.find('a').get('href')
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


class ProcessingDataBot():
    def hi_say_first_message(update, context):
        chat = update.effective_chat
        context.bot.send_message(
            chat_id=chat.id,
            text=(
                "Привет! Это бот для получения информации о событиях "
                "Яндекса.\n"
                "Тут можно узнать о всех мероприятиях, подписаться на "
                "обновления, а также узнать о мероприятиях в Москве."
            )
        )

    def process_information_parsing(update, context):
        """Обработка информации после парсинга."""
        data = GetData.processing_data_website()
        text = []
        for event in data:
            date = event['date']
            name = event['name']
            site = event['site']
            text.append(f'Дата: {date}\nНазвание: {name}\nСайт: {site}\n\n\n')
        return text

    def send_message(update, context):
        """Отправка сообщений."""
        text = ProcessingDataBot.process_information_parsing(update, context)
        chat = update.effective_chat

        buttons = ReplyKeyboardMarkup([
            ['Подписаться', 'Отписаться'],
            ['Все мероприятия', 'Мероприятия в Москве'],
        ],
            resize_keyboard=True,
        )
        context.bot.send_message(
            chat_id=chat.id,
            text=''.join(text),
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

    def subscribe_updates(update, context):
        """Подписаться на все обновления мероприятий."""
        old_data = ProcessingDataBot.send_message(update, context)
        time.sleep(RETRY_PERIOD)
        while True:
            if old_data != GetData.send_message(update, context):
                GetData.send_message(update, context)

    def events_city(update, context):
        """Подписаться на обновления мероприятий в Москве."""
        ...


def main():
    """Запуск бота."""
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler(
        'start', ProcessingDataBot.hi_say_first_message)
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Все мероприятия'),
        ProcessingDataBot.send_message
        )
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Подписаться'),
        ProcessingDataBot.subscribe_updates
        )
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Мероприятия в Москве'),
        ProcessingDataBot.events_city
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
