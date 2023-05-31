import os
from multiprocessing import Process


def run_telegram_bot():
    """Метод запуска Telegram-бота."""
    os.chdir('events/events/')
    os.system('python bot_main.py')


def run_django_server():
    """Метод запуска сервера Django. Работа API."""
    os.chdir('events/')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    # создание процесса запуска
    bot_process = Process(target=run_telegram_bot)
    django_process = Process(target=run_django_server)

    # запуск процесса
    bot_process.start()
    django_process.start()

    # ожидание завершения процесса
    bot_process.join()
    django_process.join()
