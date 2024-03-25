from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import peewee

from bot.fsm.friends import AddFriend
from bot.keyboards.journey import JourneyActionsCallbackFactory
from bot.keyboards.friends import (
    FriendsActionsCallbackFactory,
    AllFriendsCallbackFactory,
    get_friends_inline_keyboard,
    get_friends_actions_inline_keyboard,
)
from models.models import Journey, User
from service.journey import get_format_journey
from service.profile import get_format_user_profile
import loader

router = Router()


@router.callback_query(
    JourneyActionsCallbackFactory.filter(F.action == "friends"),
)
async def callback_get_all_friends(
    callback: CallbackQuery,
    callback_data: JourneyActionsCallbackFactory,
):
    friends = Journey.get(
        Journey.id == callback_data.journey_id,
    ).users.where(User.id != callback.from_user.id)

    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(
            reply_markup=get_friends_inline_keyboard(
                friends=friends,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )
    await callback.answer()


@router.callback_query(
    FriendsActionsCallbackFactory.filter(F.action == "add_friend"),
)
async def callback_add_friend(
    callback: CallbackQuery,
    callback_data: FriendsActionsCallbackFactory,
    state: FSMContext,
):
    await callback.message.answer(
        "Чтобы добавить друга в путешествие, "
        "тебе необходимо знать его ID(он указан в его профиле). "
        "Попроси его отправить его тебе",
    )
    await callback.message.answer("Напиши ID друга")
    await state.update_data(journey_id=callback_data.journey_id)
    await state.set_state(AddFriend.id)
    await callback.answer()


@router.message(F.text, AddFriend.id)
async def process_add_friend(message: Message, state: FSMContext):
    data = await state.get_data()
    if not User.select().where(User.id == message.text).exists():
        await message.answer("Такого пользователя не существует(")

    else:
        try:
            journey = Journey.get(Journey.id == data.get("journey_id"))
            User.get(User.id == message.text).journeys.add(
                journey,
            )
            for user in journey.users:
                await loader.bot.send_message(
                    text=f"В путешествие '{journey.name}' добавлен новый участник!",  # noqa: E501
                    chat_id=user.id,
                )

            friends = Journey.get(
                Journey.id == journey.id,
            ).users.where(User.id != message.from_user.id)

            await message.answer(
                text=get_format_journey(name=journey.name),
                reply_markup=get_friends_inline_keyboard(
                    friends=friends,
                    journey_id=journey.id,
                    user_type="owner",
                ),
            )

        except peewee.IntegrityError:
            await message.answer("Друг уже добавлен в ваше путешествие")

    await state.clear()


@router.callback_query(
    AllFriendsCallbackFactory.filter(F.action == "get_friend"),
)
async def callback_get_friend(
    callback: CallbackQuery,
    callback_data: AllFriendsCallbackFactory,
):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            get_format_user_profile(id=callback_data.friend_id),
            reply_markup=get_friends_actions_inline_keyboard(
                journey_id=callback_data.journey_id,
                friend_id=callback_data.friend_id,
                user_type=callback_data.user_type,
            ),
        )
    await callback.answer()


@router.callback_query(
    FriendsActionsCallbackFactory.filter(F.action == "delete"),
)
async def callback_delete_friend(
    callback: CallbackQuery,
    callback_data: FriendsActionsCallbackFactory,
):
    journey = Journey.get(Journey.id == callback_data.journey_id)
    journey.users.remove(User.get(User.id == callback_data.friend_id))
    await callback.message.delete()
    await callback.answer("Друг исключен из путешествия")
