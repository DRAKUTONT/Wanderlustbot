from typing import List

from aiogram import types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from models.models import Journey
from service.journey import get_all_journey_locations
from service.route import create_route


class JourneyActionsCallbackFactory(CallbackData, prefix="journey_actions"):
    action: str
    journey_id: int
    user_type: str = "owner"


class AllJourneysCallbackFactory(CallbackData, prefix="journeys"):
    action: str
    journey_id: int
    user_type: str = "owner"


def get_journeys_inline_keyboard(
    journeys: List[Journey],
    user_type: str = "owner",
):
    """Get all journeys for user"""

    builder = keyboard.InlineKeyboardBuilder()
    for journey in journeys:
        builder.button(
            text=journey.name,
            callback_data=AllJourneysCallbackFactory(
                action="get_journey",
                journey_id=journey.id,
                user_type=user_type,
            ),
        )

    builder.adjust(3)
    return builder.as_markup()


def get_journey_actions_inline_keyboard(
    journey_id: int,
    user_id: int,
    user_type: str = "owner",
):
    """Get action for journey: change, delete, add_location, etc."""

    builder = keyboard.InlineKeyboardBuilder()
    if user_type == "owner":
        builder.button(
            text="Удалить путешествие",
            callback_data=JourneyActionsCallbackFactory(
                action="delete",
                journey_id=journey_id,
            ),
        )
        builder.button(
            text="Добавить локацию",
            callback_data=JourneyActionsCallbackFactory(
                action="add_location",
                journey_id=journey_id,
            ),
        )

    builder.button(
        text="Локации",
        callback_data=JourneyActionsCallbackFactory(
            action="locations",
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.button(
        text="Заметки к путешествию",
        callback_data=JourneyActionsCallbackFactory(
            action="notes",
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.button(
        text="Участники",
        callback_data=JourneyActionsCallbackFactory(
            action="friends",
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.button(
        text="Построить маршрут путешествия",
        web_app=WebAppInfo(
            url=create_route(
                get_all_journey_locations(
                    journey_id=journey_id,
                    user_id=user_id,
                ),
                profile="car",
            ),
        ),
    )

    builder.adjust(2, 1)
    return builder.as_markup()


def get_journey_keyboard() -> types.ReplyKeyboardMarkup:
    """Main keyboard for journeys"""

    builder = keyboard.ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="Путешествия моих друзей"),
        types.KeyboardButton(text="Мои путешествия"),
    )

    builder.row(
        types.KeyboardButton(text="Новое путешествие"),
    )

    return builder.as_markup(resize_keyboard=True)
