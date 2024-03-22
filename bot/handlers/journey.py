from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.fsm.journey import NewJourney
from bot.keyboards.journey import (
    JourneyActionsCallbackFactory,
    AllJourneysCallbackFactory,
    get_journey_keyboard,
    get_journey_actions_inline_keyboard,
    get_journeys_inline_keyboard,
)
from models.models import Journey, User
from service.journey import get_format_journey

router = Router()


@router.message(F.text == "Путешествия")
@router.message(Command("journey"))
async def journey(message: Message):
    await message.answer(
        "инфа про путешествия",
        reply_markup=get_journey_keyboard(),
    )


@router.message(F.text == "Новое путешествие")
@router.message(Command("new_journey"))
async def new_journey(message: Message, state: FSMContext):
    await message.answer("новое путешествие")
    await state.set_state(NewJourney.name)
    await message.answer(
        "Как будет называться твое "
        "путешествие(название должно быть уникальным)?",
    )


@router.message(F.text, NewJourney.name)
async def process_new_journey_name(message: Message, state: FSMContext):
    if not Journey.select().where(Journey.name == message.text).exists():
        await state.update_data(name=message.text)
        await state.set_state(NewJourney.about)
        await message.answer("Расскажи, что будет в путешествии")

    else:
        await message.answer(
            "Путешествие с таким названием уже существует, попробуй еще раз",
        )


@router.message(F.text, NewJourney.about)
async def process_new_journey_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    journey_data = await state.get_data()
    user = User.get(User.id == message.from_user.id)
    journey = Journey(
        owner_id=user,
        **journey_data,
    )
    journey.save()
    user.journeys.add(journey)

    await message.answer("Путешествие создано!")
    await message.answer(
        get_format_journey(journey_data.get("name")),
        reply_markup=get_journey_actions_inline_keyboard(
            journey_id=journey.id,
            user_id=message.from_user.id,
        ),
    )
    await state.clear()

@router.callback_query(
    JourneyActionsCallbackFactory.filter(F.action == "delete"),
)
async def callback_journey_delete(
    callback: CallbackQuery,
    callback_data: JourneyActionsCallbackFactory,
):
    Journey.get(Journey.id == callback_data.journey_id).delete_instance()
    await callback.message.delete()
    await callback.answer("Путешествие удалено!")


@router.message(F.text == "Мои путешествия")
@router.message(Command("my_journeys"))
async def my_journeys(message: Message):
    journeys = Journey.select().where(Journey.owner == message.from_user.id)
    if journeys:
        await message.answer(
            "Твои путешествия",
            reply_markup=get_journeys_inline_keyboard(journeys=journeys),
        )

    else:
        await message.answer("У тебя пока что нет путешествий")


@router.message(F.text == "Путешествия моих друзей")
@router.message(Command("friends_journeys"))
async def friends_journeys(message: Message):
    journeys = User.get(User.id == message.from_user.id).journeys

    if journeys:
        await message.answer(
            "Путешествия в которых ты состоишь",
            reply_markup=get_journeys_inline_keyboard(
                journeys=journeys,
                user_type="friend",
            ),
        )

    else:
        await message.answer("Тебя пока что не добавили ни в одно путешествие")


@router.callback_query(
    AllJourneysCallbackFactory.filter(F.action == "get_journey"),
)
async def callback_journey_get(
    callback: CallbackQuery,
    callback_data: AllJourneysCallbackFactory,
):
    journey = Journey.get(Journey.id == callback_data.journey_id)

    await callback.message.answer(
        get_format_journey(journey.name),
        reply_markup=get_journey_actions_inline_keyboard(
            journey_id=journey.id,
            user_type=callback_data.user_type,
            user_id=callback.from_user.id,
        ),
    )
    await callback.answer()
