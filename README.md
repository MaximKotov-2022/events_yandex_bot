# events_yandex_bot
Проект по получению информации о событиях Яндекса с сайта "events.yandex.ru" через Telegram-бот и API.

## Технологии
+ Python
+ beautifulsoup4
+ python-telegram-bot
+ multiprocessing


## Работа бота
### Бот умеет выполнять следующие команды:
+ **/start** - запуск бота и получение информации о его возможностях;
+ **Все мероприятия** - получение информации о всех актуальных мероприятиях; 
+ **Подписаться** - подписка на обновления информации о мероприятиях. При изменении информации на сайте "events.yandex.ru" пользователь будет получать уведомления;
+ **Отписаться** - отписка от уведомлений.


Работа бота состоит в парсинге информации с сайта "events.yandex.ru", обработке полученных данных и отправке сообщений пользователю.

### При нажатии на **Все мероприятия** Бот отправит пользователю сообщение со списком всех мероприятий.
### Формат полученных данных:
```
Дата: Ср, 07 Июнь
Название: SpeechKit Cases Night
Сайт: https://cloud.yandex.ru/events/795?utm_source=yamain


Дата: Чт, 08 Июнь
Название: Кто и как обучает искусственный интеллект
Сайт: https://ya.ru/project/ai/events/08-06-2023 
```

### Процесс работы бота:
Для парсинга используется библиотека ```beautifulsoup4```, а для отправки сообщений - библиотека ```python-telegram-bot```.
+ Класс **GetData** содержит методы для парсинга и обработки данных с сайта.
+ Класс **ProcessingDataBot** содержит методы для отправки сообщений пользователю, а также логику работы с подписками на обновления информации о мероприятиях.

При запуске бота создается объект класса **Updater**, который обрабатывает полученные от пользователя сообщения. Каждый раз, когда пользователь отправляет сообщение, вызывается соответствующий метод класса **ProcessingDataBot**.

## Работа API:
Обработка GET запроса для просмотра мероприятий с сайта.

### Формат запроса 
GET-запрос на ```http://127.0.0.1:8000/api/v1/events/```

### Формат полученных данных:
```
{
    "events": [
        {
            "date": "гггг-мм-дд",
                "name": "srting",
                "site": "srting"
        }
    ]
}
```

### Пример результата:
```
 {
    "events": [
        {
            "date": "2023-06-07",
            "name": "Как пишущему человеку попасть в IT",
            "site": "https://cloud.yandex.ru/events/787/"
        },
        {
            "date": "2023-06-08",
            "name": "Как перенос 1С в облако помогает ускорить цифровизацию бизнеса",
            "site": "https://cloud.yandex.ru/events/711/"
        },
    ]
}
```

## Как запустить проект:
В проекте можно запустить Бота и API как вместе, так и по отдельности. Сервисы работают независимо друг от друга.
Ниже приведён пример запуска всего проекта.

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
source venv/Scripts/activate
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
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```

Запустить проект (запуск Бота и Сервера одновременно):

```
python3 run_bot_api.py
```

## Автор
Котов Максим
