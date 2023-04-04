import os
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
RETRY_PERIOD = 3600


class GetData:
    """Класс с методами для обработки данных с сайта."""
    def site_parsing() -> str:
        """Получение данных сайта (парсинг)."""
        url = "https://events.yandex.ru/"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        events = soup.find(class_='events__container')

        return events

    def processing_data_website() -> list:
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

    def process_information_parsing(update, context) -> list:
        """Обработка информации после парсинга."""
        data = GetData.processing_data_website()
        text = []
        for event in data:
            date = event['date']
            name = event['name']
            site = event['site']
            text.append(f'Дата: {date}\nНазвание: {name}\nСайт: {site}\n\n\n')
        return text


class ProcessingDataBot():
    """Класс для работы с ботом."""
    def send_message(update, context):
        """Отправка сообщений."""
        text = GetData.process_information_parsing(update, context)
        chat = update.effective_chat

        buttons = ReplyKeyboardMarkup([
            ['Все мероприятия', 'Мероприятия в Москве'],
            ['Подписаться', 'Отписаться'],
        ],
            resize_keyboard=True,
        )

        context.bot.send_message(
            chat_id=chat.id,
            text=''.join(text),
            reply_markup=buttons,
            disable_web_page_preview=True,
        )
        return 0

    def checking_data_changes(update, context):
        """Проверка изменений/обновлений данных с сайта.
        Если данные изменились, то возарвращается True
        Если нет - False."""
        while True:
            old_data = GetData.process_information_parsing(update, context)
            time.sleep(5)  # Интервал проверки обновлений на сайте
            new_data = GetData.process_information_parsing(update, context)
            print(old_data, new_data, end='\n')  # Для проверки работы запросов
            if old_data != new_data:
                old_data = new_data
                return True
            return False

    def subscribe_updates(update, context):
        """Подписаться на все обновления мероприятий."""
        while True:
            if (ProcessingDataBot.checking_data_changes(update, context) is
                    True):
                ProcessingDataBot.send_message(update, context)

    def unsubscribe(update, context):
        """Отписка от обновлений мероприятий.
        Остановка функции подписки на обновления (subscribe_updates)."""
        ...

    def hi_say_first_message(update, context):
        """Отправка первого сообщения.
        Получение инфо о возможностях бота."""
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
        ProcessingDataBot.send_message(update, context)


def main():
    """Запуск бота. Создание обработчиков сообщений."""
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler(
        'start', ProcessingDataBot.hi_say_first_message,
        run_async=True,
        )
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Все мероприятия'),
        ProcessingDataBot.send_message,
        run_async=True,
        )
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Подписаться'),
        ProcessingDataBot.subscribe_updates,
        run_async=True,
        )
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Отписаться'),
        ProcessingDataBot.unsubscribe,
        run_async=True,
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
