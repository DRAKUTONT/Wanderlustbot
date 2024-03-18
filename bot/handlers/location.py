from contextlib import suppress
from datetime import datetime

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.fsm.journey import NewLocation
from bot.keyboards.journey import (
    JourneyActionsCallbackFactory,
)
from bot.keyboards.location import (
    AllLocationsCallbackFactory,
    get_locations_inline_keyboard,
)
from models.models import Location
from service.geosuggest import is_object_exists


router = Router()


@router.callback_query(
    JourneyActionsCallbackFactory.filter(F.action == "add_location"),
)
async def callback_journey_add_location(
    callback: CallbackQuery,
    callback_data: JourneyActionsCallbackFactory,
    state: FSMContext,
):
    await callback.message.answer("Какую страну хочешь посетить?")
    await state.update_data(journey_id=callback_data.journey_id)
    await state.set_state(NewLocation.country)
    await callback.answer()


@router.message(F.text, NewLocation.country)
async def process_new_location_country(message: Message, state: FSMContext):
    if is_object_exists(message.text, types="country"):
        await state.update_data(country=message.text)
        await state.set_state(NewLocation.city)
        await message.answer("Какой город хочешь посетить?")
    else:
        await message.answer("Такой страны не существует:( Попробуй еще раз")


@router.message(F.text, NewLocation.city)
async def process_city(message: Message, state: FSMContext):
    if is_object_exists(message.text, types="locality"):
        await state.update_data(city=message.text)
        await state.set_state(NewLocation.start_date)
        await message.answer(
            "Напиши дату приезда в локацию в формате "
            "YYYY-MM-DD, например 2024-03-18",
        )
    else:
        await message.answer(
            "Такого города не существует:( Попробуй еще раз",
        )


@router.message(F.text, NewLocation.start_date)
async def process_new_journey_start_date(message: Message, state: FSMContext):
    try:
        await state.update_data(
            start_date=datetime.strptime(message.text, "%Y-%m-%d"),  # noqa: DTZ007
        )
        await state.set_state(NewLocation.end_date)
        await message.answer(
            "Напиши дату отъезда из локации в формате "
            "YYYY-MM-DD, например 2024-03-18",
        )
    except ValueError:
        await message.answer("Неправильный формат даты:(")


@router.message(F.text, NewLocation.end_date)
async def process_new_journey_end_date(message: Message, state: FSMContext):
    try:
        await state.update_data(
            end_date=datetime.strptime(message.text, "%Y-%m-%d"),  # noqa: DTZ007
        )
        location_data = await state.get_data()
        Location.create(
            journey=location_data.pop("journey_id"),
            **location_data,
        )

        await message.answer("Локация добавлена!")
        await state.clear()

    except ValueError:
        await message.answer("Неправильный формат даты:(")


@router.callback_query(
    JourneyActionsCallbackFactory.filter(F.action == "locations"),
)
async def callback_journey_show_locations(
    callback: CallbackQuery,
    callback_data: JourneyActionsCallbackFactory,
):
    locations = Location.select().where(
        Location.journey == callback_data.journey_id,
    )
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            reply_markup=get_locations_inline_keyboard(locations=locations),
        )
    await callback.answer()
