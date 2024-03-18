from typing import List

from aiogram import types
from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from models.models import Journey


class JourneyActionsCallbackFactory(CallbackData, prefix="journey"):
    action: str
    journey_id: int


class AllJourneysCallbackFactory(CallbackData, prefix="journeys"):
    action: str
    journey_id: int


def get_journeys_inline_keyboard(journeys: List[Journey]):  # noqa: FA100
    builder = keyboard.InlineKeyboardBuilder()
    for journey in journeys:
        builder.button(
            text=journey.name,
            callback_data=AllJourneysCallbackFactory(
                action="get_journey",
                journey_id=journey.id,
            ),
        )

    builder.adjust(3)
    return builder.as_markup()


def get_journey_actions_inline_keyboard(journey_id: int):
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(
        text="Изменить путешествие",
        callback_data=JourneyActionsCallbackFactory(
            action="change",
            journey_id=journey_id,
        ),
    )
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
        ),
    )

    builder.adjust(2)
    return builder.as_markup()


def get_journey_keyboard() -> types.ReplyKeyboardMarkup:
    builder = keyboard.ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="Новое путешествие"),
        types.KeyboardButton(text="Мои путешествия"),
    )

    return builder.as_markup(resize_keyboard=True)
