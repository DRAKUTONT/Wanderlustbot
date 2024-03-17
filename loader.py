import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from peewee import SqliteDatabase

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUGGEST_API_KEY = os.getenv("SUGGEST_API_KEY")
DIR = Path(__file__).absolute().parent

bot = Bot(token=BOT_TOKEN)


database = SqliteDatabase(f"{DIR}/database.sqlite3")

dp = Dispatcher()
