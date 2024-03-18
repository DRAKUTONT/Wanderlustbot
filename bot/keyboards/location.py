from typing import List

from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from models.models import Location


class AllLocationsCallbackFactory(CallbackData, prefix="location"):
    action: str
    location_id: int


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
