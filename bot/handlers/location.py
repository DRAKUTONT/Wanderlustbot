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
    LocationAddressCheckCallbackFactory,
    get_locations_inline_keyboard,
    get_location_address_check_inline_keyboard,
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
    await state.update_data(country=message.text)
    await state.set_state(NewLocation.city)
    await message.answer("Какой город хочешь посетить?")


@router.message(F.text, NewLocation.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(NewLocation.address)
    await process_location_address_check(message, state)


async def process_location_address_check(message: Message, state: FSMContext):
    data = await state.get_data()
    address = is_object_exists(
        f"{data.get('country')}, {data.get('city')}",
        types="locality",
    )
    if address:
        await message.answer(
            f"Адрес локации {address[0]['address']['formatted_address']}, верно?",
            reply_markup=get_location_address_check_inline_keyboard(),
        )
    else:
        await message.answer(
            "Такого адреса не существует:( Попробуй еще раз",
        )
        await state.set_state(NewLocation.country)
        await message.answer("Какую страну хочешь посетить?")


@router.callback_query(
    LocationAddressCheckCallbackFactory.filter(),
)
async def callback_location_address_check(
    callback: CallbackQuery,
    callback_data: LocationAddressCheckCallbackFactory,
    state: FSMContext,
):
    if callback_data.is_valid:
        await state.set_state(NewLocation.start_date)
        await callback.message.answer(
            "Напиши дату приезда в локацию в формате "
            "YYYY-MM-DD, например 2024-03-18",
        )
    else:
        await state.set_state(NewLocation.country)
        await callback.message.answer("Из какой ты страны?")

    await callback.message.delete()
    await callback.answer()


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
            callback.message.text,
            reply_markup=get_locations_inline_keyboard(locations=locations),
        )
    await callback.answer()
