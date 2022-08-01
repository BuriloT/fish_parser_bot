import os
import logging
import requests

from requests import RequestException
from aspose.cells import Workbook

from exceptions import ConvertToPdfException


def get_response(url):
    """Получает ответ с сайтов."""
    try:
        session = requests.Session()
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def remove_prices(filename, pdf_filename):
    """Удаляет прайсы."""
    try:
        os.remove(filename)
        os.remove(pdf_filename)
    except OSError:
        logging.exception(
            'Возникла ошибка при удалении прайсов',
            stack_info=True
        )


def convert_wb_to_pdf(dir_path, filename, pdf_filename):
    """Конвертирует Excel в pdf формат."""
    if os.path.exists(dir_path):
        os.chdir(dir_path)
    try:
        new_base_price_wb = Workbook(filename)
        new_base_price_wb.save(pdf_filename)
    except ConvertToPdfException:
        logging.exception(
            'Возникла ошибка при конверсии прайсов',
            stack_info=True
        )
