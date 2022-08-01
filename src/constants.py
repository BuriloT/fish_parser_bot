import os
from pathlib import Path
from telegram import Bot
from telegram.ext import Updater
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

NEW_BASE_URL = 'https://basenew.ru/'
NEW_BASE_PRICE_URL = 'https://basenew.ru/www.basenew.ru/price/'

SMOL_PORT_URL = 'http://port-smol.ru/'
SMOL_PORT_PRICE_URL = 'http://port-smol.ru/disk'

bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)
