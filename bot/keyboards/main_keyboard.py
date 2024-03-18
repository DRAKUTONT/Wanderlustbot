from aiogram import types
from aiogram.utils import keyboard


def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    builder = keyboard.ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="Изменить профиль"),
        types.KeyboardButton(text="Мой профиль"),
    )
    builder.row(
        types.KeyboardButton(text="Путешествия"),
    )

    return builder.as_markup(resize_keyboard=True)
