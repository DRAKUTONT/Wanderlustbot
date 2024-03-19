from typing import List

from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from models.models import Location


class AllLocationsCallbackFactory(CallbackData, prefix="location"):
    action: str
    location_id: int


class LocationAddressCheckCallbackFactory(
    CallbackData,
    prefix="location_address_check",
):
    is_valid: bool


def get_location_address_check_inline_keyboard():
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(
        text="Да",
        callback_data=LocationAddressCheckCallbackFactory(
            is_valid=True,
        ),
    )
    builder.button(
        text="Нет",
        callback_data=LocationAddressCheckCallbackFactory(
            is_valid=False,
        ),
    )

    builder.adjust(2)
    return builder.as_markup()


def get_locations_inline_keyboard(locations: List[Location]):  # noqa: FA100
    builder = keyboard.InlineKeyboardBuilder()
    for location in locations:
        builder.button(
            text=location.city,
            callback_data=AllLocationsCallbackFactory(
                action="get_location",
                location_id=location.id,
            ),
        )

    builder.adjust(3)
    return builder.as_markup()
