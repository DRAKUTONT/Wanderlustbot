from typing import List

from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from models.models import Location


class AllLocationsCallbackFactory(CallbackData, prefix="location"):
    action: str
    location_id: int
    user_type: str


class LocationAddressCheckCallbackFactory(
    CallbackData,
    prefix="location_address_check",
):
    is_valid: bool


class LocationActionCallbackFactory(
    CallbackData,
    prefix="location_actions",
):
    action: str
    location_id: int


def get_location_actions_inline_keyboard(
    location_id: int,
    user_type: str = "owner",
):
    """Get location action: delete"""

    builder = keyboard.InlineKeyboardBuilder()
    if user_type == "owner":
        builder.button(
            text="Удалить",
            callback_data=LocationActionCallbackFactory(
                action="delete",
                location_id=location_id,
            ),
        )

    return builder.as_markup()


def get_location_address_check_inline_keyboard():
    """Check is correct address"""

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


def get_locations_inline_keyboard(
    locations: List[Location],
    user_type: str = "owner",
):
    """Get all locations for journey"""

    builder = keyboard.InlineKeyboardBuilder()
    for location in locations:
        builder.button(
            text=location.address,
            callback_data=AllLocationsCallbackFactory(
                action="get_location",
                location_id=location.id,
                user_type=user_type,
            ),
        )

    return builder.as_markup()
