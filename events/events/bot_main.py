import os
import threading
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
RETRY_PERIOD = 1800


class GetData:
    """Описание методов обработки данных с сайта."""

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
    """Описание методов работы бота."""

    def send_message(update, context, text):
        """Отправка сообщений."""
        chat = update.effective_chat

        buttons = ReplyKeyboardMarkup([
            ['Все мероприятия'],
            ['Подписаться', 'Отписаться'],
        ],
            resize_keyboard=True,
        )

        context.bot.send_message(
            chat_id=chat.id,
            text=text,
            reply_markup=buttons,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML,
        )
        return 0

    def all_events(update, context):
        """Актульаные меропрития."""
        text = ''.join(GetData.process_information_parsing(update, context))

        return ProcessingDataBot.send_message(
                update,
                context,
                text=text,
            )

    def checking_data_changes(update, context):
        """Проверка изменений/обновлений данных с сайта.

        Если данные изменились, то возарвращается True
        Если нет - False."""
        while True:
            old_data = GetData.process_information_parsing(update, context)
            time.sleep(RETRY_PERIOD)  # Интервал проверки обновлений на сайте
            new_data = GetData.process_information_parsing(update, context)

            if old_data != new_data:
                old_data = new_data
                return True
            return False

    stop_subscribe_updates = threading.Event()

    @staticmethod
    def subscribe_updates(update, context):
        """Подписаться на все обновления мероприятий."""
        text = (
            'Вы подписаны!\nПри обновлении данных Вы получите сообщение.'
        )
        ProcessingDataBot.send_message(update, context, text=text)

        while not ProcessingDataBot.stop_subscribe_updates.is_set():
            if ProcessingDataBot.checking_data_changes(update, context):
                ProcessingDataBot.all_events(update, context)

        # если подписка остановлена, сбрасываем флаг
        ProcessingDataBot.stop_subscribe_updates.clear()

    def unsubscribe(update, context):
        """Отписка от обновлений мероприятий.
    
        Остановка функции подписки на обновления (subscribe_updates)."""
        text = "Вы отписаны"
        ProcessingDataBot.send_message(update, context, text=text)

        # останавливаем подписку на обновления
        ProcessingDataBot.stop_subscribe_updates.set()

    def hi_say_first_message(update, context):
        """Отправка первого сообщения.
    
        Получение инфо о возможностях бота."""
        text = ("Привет! Это бот для получения информации о событиях "
                "Яндекса.\n"

                "<u>Все мероприятия</u> - узнать об актуальных событиях\n"

                "<u>Подписаться</u> - получать сообщения при обновлении "
                "информации.\n"

                "<u>Отписаться</u> - отписаться от уведомлений."
                )

        return ProcessingDataBot.send_message(
                update,
                context,
                text=text,
            )


def main():
    """Запуск бота. Создание обработчиков сообщений."""
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler(
        'start',
        ProcessingDataBot.hi_say_first_message,
        run_async=True,
        )
    )
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text('Все мероприятия'),
        ProcessingDataBot.all_events,
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
