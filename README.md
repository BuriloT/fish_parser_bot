# fish_parser_bot
## Telegram-бот для парсинга прайсов

> Telegram-бот создан для удобства получения прайсов с сайтов. Telegram-бот умеет получать прайс, конвертировать его из excel в pdf, проверять время обновления прайса, логировать действия и отправлять нужные данные пользователю.

## Технологии проекта

- Python — высокоуровневый язык программирования.
- BeautifulSoup4 - библиотека для парсинга.
- Python-telegram-bot - библиотека для Telegram-бота.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/BuriloT/fish_parser_bot.git
```

```
cd fish_parser_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл .env и заполнить его данными:

```
TELEGRAM_TOKEN=Токен вашего бота в Telegram
```

Выполнить команду:

```
python main.py
```
