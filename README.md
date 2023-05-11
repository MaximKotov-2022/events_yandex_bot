# events_yandex_bot
Телеграм-бота для получении информацию о событиях на сайте "events.yandex.ru".

### Бот умеет выполнять следующие команды:
+ **/start** - запуск бота и получение информации о его возможностях;
+ **Все мероприятия** - получение информации о всех актуальных мероприятиях; 
+ **Подписаться** - подписка на обновления информации о мероприятиях. При изменении информации на сайте "events.yandex.ru" пользователь будет получать уведомления;
+ **Отписаться** - отписка от уведомлений.


Основная логика работы бота состоит в парсинге информации с сайта "events.yandex.ru", обработке полученных данных и отправке сообщений пользователю.

### Процесс работы бота:
Для парсинга используется библиотека ```beautifulsoup4```, а для отправки сообщений - библиотека ```python-telegram-bot```.
+ Класс **GetData** содержит методы для парсинга и обработки данных с сайта.
+ Класс **ProcessingDataBot** содержит методы для отправки сообщений пользователю, а также логику работы с подписками на обновления информации о мероприятиях.

При запуске бота создается объект класса **Updater**, который обрабатывает полученные от пользователя сообщения. Каждый раз, когда пользователь отправляет сообщение, вызывается соответствующий метод класса **ProcessingDataBot**.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MaximKotov-2022/events_yandex_bot
```

```
cd events_yandex_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
