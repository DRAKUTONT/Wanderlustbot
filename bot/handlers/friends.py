from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import peewee

from bot.fsm.friends import AddFriend
from bot.keyboards.journey import JourneyActionsCallbackFactory
from bot.keyboards.friends import (
    get_friends_inline_keyboard,
    FriendsActionsCallbackFactory,
    AllFriendsCallbackFactory,
)
from models.models import Journey, User
from service.profile import get_format_user_profile
import loader

router = Router()


@router.callback_query(
    JourneyActionsCallbackFactory.filter(F.action == "friends"),
)
async def callback_journey_delete(
    callback: CallbackQuery,
    callback_data: JourneyActionsCallbackFactory,
):
    friends = Journey.get(
        Journey.id == callback_data.journey_id,
    ).users
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            callback.message.text,
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
            User.get(User.id == message.text).journeys.add(
                Journey.get(Journey.id == data.get("journey_id")),
            )
            await message.answer("Друг добавлен!")
            await loader.bot.send_message(
                chat_id=message.text,
                text="Вас добавили в путешествие!",
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
    await callback.message.answer(
        get_format_user_profile(id=callback_data.friend_id),
    )
    await callback.answer()
