import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from peewee import SqliteDatabase

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUGGEST_API_KEY = os.getenv("SUGGEST_API_KEY")
GEOCODER_API_KEY = os.getenv("GEOCODER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")
DIR = Path(__file__).absolute().parent

bot = Bot(token=BOT_TOKEN)


database = SqliteDatabase(
    f"{DIR}/database.sqlite3",
    pragmas={"foreign_keys": 1},
)

dp = Dispatcher()
