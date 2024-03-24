from typing import List

from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from bot.keyboards.journey import (
    AllJourneysCallbackFactory,
    JourneyActionsCallbackFactory,
)
from models.models import Location


class AllLocationsCallbackFactory(CallbackData, prefix="location"):
    action: str
    location_id: int
    journey_id: int
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
    journey_id: int
    user_type: str


class LandmarksCallbackFactory(CallbackData, prefix="landmarks"):
    action: str
    xid: str
    location_id: int
    journey_id: int
    user_type: str


def get_location_actions_inline_keyboard(
    location_id: int,
    journey_id: int,
    user_type: str = "owner",
):
    """Get location action: delete"""

    builder = keyboard.InlineKeyboardBuilder()

    builder.button(
        text="🗽 Достопримечательности",
        callback_data=LocationActionCallbackFactory(
            action="landmarks",
            location_id=location_id,
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.button(
        text="🌥 Погода",
        callback_data=LocationActionCallbackFactory(
            action="weather",
            location_id=location_id,
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    if user_type == "owner":
        builder.button(
            text="🗑 Удалить",
            callback_data=LocationActionCallbackFactory(
                action="delete",
                location_id=location_id,
                journey_id=journey_id,
                user_type=user_type,
            ),
        )

    builder.button(
        text="🔙 Назад",
        callback_data=JourneyActionsCallbackFactory(
            action="locations",
            journey_id=journey_id,
            user_type=user_type,
        ),
    )
    builder.adjust(1)

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
    journey_id: int,
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
                journey_id=journey_id,
                user_type=user_type,
            ),
        )

    if user_type == "owner":
        builder.button(
            text="➕ Добавить локацию",
            callback_data=LocationActionCallbackFactory(
                action="add_location",
                journey_id=journey_id,
                location_id=0,
                user_type=user_type,
            ),
        )

    builder.button(
        text="🔙 Назад",
        callback_data=AllJourneysCallbackFactory(
            action="get_journey",
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    adjust = filter(
        lambda x: x != 0,
        [*[3 for _ in range(len(locations) // 3)], len(locations) % 3, 1],
    )
    builder.adjust(*adjust)

    return builder.as_markup()


def get_location_weather_inline_leyboard(
    journey_id: int,
    location_id: int,
    user_type: str = "owner",
):
    builder = keyboard.InlineKeyboardBuilder()

    builder.button(
        text="🔙 Назад",
        callback_data=AllLocationsCallbackFactory(
            action="get_location",
            location_id=location_id,
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.adjust(1)
    return builder.as_markup()


def get_location_landmarks_inline_leyboard(
    landmarks: list,
    journey_id: int,
    location_id: int,
    user_type: str = "owner",
):
    builder = keyboard.InlineKeyboardBuilder()

    for landmark in landmarks:
        builder.button(
            text=landmark.get("name"),
            callback_data=LandmarksCallbackFactory(
                action="get_landmark",
                xid=landmark.get("xid"),
                location_id=location_id,
                journey_id=journey_id,
                user_type=user_type,
            ),
        )

    builder.button(
        text="🔙 Назад",
        callback_data=AllLocationsCallbackFactory(
            action="get_location",
            location_id=location_id,
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    adjust = filter(
        lambda x: x != 0,
        [*[3 for _ in range(len(landmarks) // 3)], len(landmarks) % 3, 1],
    )
    builder.adjust(*adjust)
    return builder.as_markup()


def get_landmark_action_keyboard(
    journey_id: int,
    location_id: int,
    user_type: str = "owner",
):
    builder = keyboard.InlineKeyboardBuilder()

    builder.button(
        text="🔙 Назад",
        callback_data=LocationActionCallbackFactory(
            action="landmarks",
            location_id=location_id,
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.adjust(1)
    return builder.as_markup()
