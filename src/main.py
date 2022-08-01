import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters

from configs import configure_logging
from constants import (BASE_DIR, NEW_BASE_URL, NEW_BASE_PRICE_URL,
                       SMOL_PORT_URL, SMOL_PORT_PRICE_URL, bot, updater)
from exceptions import (TelegramSendDocumentException,
                        TelegramSendMessageExeption)
from utils import get_response, remove_prices, convert_wb_to_pdf


def send_message(update, context, message, bot=bot):
    """Отправляет сообщение в Telegram чат."""
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup([['Новая база'], ['Порт'],
                                   ['Проверить обновления']],
                                  resize_keyboard=True)
    try:
        context.bot.send_message(
            chat_id=chat.id,
            text=message,
            reply_markup=buttons)
        logging.info('Бот отправил сообщение в Telegram.')
    except TelegramSendMessageExeption:
        logging.exception(
            'Произошла ошибка при отправке сообщения в Telegram.'
        )


def send_document(update, context, document, bot=bot):
    """Отправляет документ в Telegram чат."""
    chat = update.effective_chat
    try:
        context.bot.sendDocument(
            chat.id,
            document=open(document, 'rb'))
        logging.info('Бот отправил прайс в Telegram.')
    except TelegramSendDocumentException:
        logging.exception(
            'Произошла ошибка при отправке прайса в Telegram.',
            stack_info=True
            )


def port_document(update, context):
    """Парсит прайс с Порта."""
    logging.info('Начинается парсинг прайса Порта.')
    response = get_response(SMOL_PORT_PRICE_URL)

    soup = BeautifulSoup(response.text, 'lxml')

    p_tag = soup.find_all('p')[1]
    a_tag = p_tag.find('a')
    href = a_tag['href']

    port_price_list_link = urljoin(SMOL_PORT_URL, href)

    filename = port_price_list_link.split('/')[-1]
    smol_port_dir = BASE_DIR / 'smol-port-prices'
    smol_port_dir.mkdir(exist_ok=True)
    smol_port_price_path = smol_port_dir / filename
    smol_port_price_pdf = filename.split('.')[0] + '.pdf'
    response = get_response(port_price_list_link)

    with open(smol_port_price_path, 'wb') as file:
        file.write(response.content)

    convert_wb_to_pdf(smol_port_dir, filename, smol_port_price_pdf)

    send_document(update, context, smol_port_price_pdf)

    remove_prices(filename, smol_port_price_pdf)
    logging.info('Парсинг прайса Порта завершён')


def new_base_date_parsing():
    """Парсит дату обновления прайса"""
    logging.info('Начинается парсинг обновлений Новой Базы.')
    response = get_response(NEW_BASE_PRICE_URL)

    soup = BeautifulSoup(response.text, 'lxml')

    a_tag = soup.find('a', class_='black')
    update_date = a_tag.text.split(' ')[-1]
    message = f'Последнее обновление новой базы было: {update_date}'

    return message


def new_base_document(update, context):
    """Парсит прайс с Новой Базы."""
    logging.info('Начинается парсинг Новой Базы.')
    response = get_response(NEW_BASE_PRICE_URL)

    soup = BeautifulSoup(response.text, 'lxml')

    a_tag = soup.find('a', class_='black')
    href = a_tag['href']

    new_base_price_list_link = urljoin(NEW_BASE_URL, href)

    filename = new_base_price_list_link.split('=')[-1]
    new_base_dir = BASE_DIR / 'new-base-prices'
    new_base_dir.mkdir(exist_ok=True)
    new_base_price_list_path = new_base_dir / filename
    new_base_price_pdf = filename.split('.')[0] + '.pdf'
    response = get_response(new_base_price_list_link)

    with open(new_base_price_list_path, 'wb') as file:
        file.write(response.content)

    convert_wb_to_pdf(new_base_dir, filename, new_base_price_pdf)

    send_document(update, context, new_base_price_pdf)

    remove_prices(filename, new_base_price_pdf)

    logging.info('Парсинг прайса Новой Базы завершён.')


def start_bot(update, context):
    """Обрабатывает команду /start в Telegram боте."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    logging.info(f'{chat.id} - {name} активирова(л/ла) бота')
    message = (f'{name} cпасибо, что включили меня,'
               f'можете попробывать скачать прайсы.')
    send_message(update, context, message)


def priceHandler(update, context):
    """Обрабатывает текст для выдачи нужного прайса."""
    if 'Новая база' in update.message.text:
        message = 'Что-же Алексей на этот раз нам приготовил?'
        send_message(update, context, message)
        new_base_document(update, context)
    if 'Порт' in update.message.text:
        message = 'Сейчас посмотрю что там в порту.'
        send_message(update, context, message)
        port_document(update, context)
    if 'Проверить обновления' in update.message.text:
        message = new_base_date_parsing()
        send_message(update, context, message)


def main():
    configure_logging()
    logging.info('Бот запущен!')

    updater.dispatcher.add_handler(CommandHandler('start', start_bot))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, priceHandler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
    logging.info('Бот завершил работу!')
