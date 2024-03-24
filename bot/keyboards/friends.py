from typing import List

from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from bot.keyboards.journey import (
    AllJourneysCallbackFactory,
    JourneyActionsCallbackFactory,
)
from models.models import User


class AllFriendsCallbackFactory(CallbackData, prefix="friends"):
    action: str
    journey_id: int
    friend_id: int
    user_type: str = "owner"


class FriendsActionsCallbackFactory(CallbackData, prefix="friend_actions"):
    action: str
    journey_id: int
    friend_id: int
    user_type: str = "owner"


def get_friends_inline_keyboard(
    friends: List[User],
    journey_id: int,
    user_type: str = "owner",
):
    """Get all friends in journey"""

    builder = keyboard.InlineKeyboardBuilder()
    for friend in friends:
        builder.button(
            text=friend.name,
            callback_data=AllFriendsCallbackFactory(
                action="get_friend",
                journey_id=journey_id,
                friend_id=friend.id,
                user_type=user_type,
            ),
        )
    if user_type == "owner":
        builder.button(
            text="➕ Добавить друга в путешествие",
            callback_data=FriendsActionsCallbackFactory(
                action="add_friend",
                journey_id=journey_id,
                friend_id=0,
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
        [*[3 for _ in range(len(friends) // 3)], len(friends) % 3, 1, 1],
    )
    builder.adjust(*adjust)
    return builder.as_markup()


def get_friends_actions_inline_keyboard(
    journey_id: int,
    friend_id: int,
    user_type: str = "owner",
):
    builder = keyboard.InlineKeyboardBuilder()

    if user_type == "owner":
        builder.button(
            text="🗑 Удалить",
            callback_data=FriendsActionsCallbackFactory(
                action="delete",
                journey_id=journey_id,
                friend_id=friend_id,
                user_type=user_type,
            ),
        )

    builder.button(
        text="🔙 Назад",
        callback_data=JourneyActionsCallbackFactory(
            action="friends",
            journey_id=journey_id,
            user_type=user_type,
        ),
    )

    builder.adjust(1)
    return builder.as_markup()
