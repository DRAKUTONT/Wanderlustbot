from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData


class UserAddressCheckCallbackFactory(CallbackData, prefix="address_check"):
    is_valid: bool


def get_address_check_inline_keyboard():
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(
        text="Да",
        callback_data=UserAddressCheckCallbackFactory(
            is_valid=True,
        ),
    )
    builder.button(
        text="Нет",
        callback_data=UserAddressCheckCallbackFactory(
            is_valid=False,
        ),
    )

    builder.adjust(2)
    return builder.as_markup()
