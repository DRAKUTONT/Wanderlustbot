from aiogram import types
from aiogram.utils import keyboard


def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    builder = keyboard.ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="Новое путешествие"),
    )

    builder.row(
        types.KeyboardButton(text="Путешествия моих друзей"),
        types.KeyboardButton(text="Мои путешествия"),
    )

    builder.row(
        types.KeyboardButton(text="Изменить профиль"),
        types.KeyboardButton(text="Мой профиль"),
    )

    return builder.as_markup(resize_keyboard=True)
