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
    LocationActionCallbackFactory,
    LandmarksCallbackFactory,
    get_location_actions_inline_keyboard,
    get_locations_inline_keyboard,
    get_location_address_check_inline_keyboard,
    get_location_landmarks_inline_leyboard,
    get_landmark_action_keyboard,
    get_location_weather_inline_leyboard,
)
from models.models import Location
from service.geosuggest import is_object_exists
from service.landmarks import get_landmarks, get_format_landmark
from service.location import get_format_location
from service.route import get_place_coord
from service.weather import get_format_weaher


router = Router()


@router.callback_query(
    LocationActionCallbackFactory.filter(F.action == "add_location"),
)
async def callback_journey_add_location(
    callback: CallbackQuery,
    callback_data: LocationActionCallbackFactory,
    state: FSMContext,
):
    await callback.message.answer("Что хочешь посетить? Напиши адрес места")
    await state.update_data(journey_id=callback_data.journey_id)
    await state.set_state(NewLocation.address)
    await callback.answer()


@router.message(F.text, NewLocation.address)
async def process_location_address(message: Message, state: FSMContext):
    address = is_object_exists(
        message.text,
    )
    if address:
        address = address[0]["address"]["formatted_address"]
        await message.answer(
            f"Адрес локации {address}, верно?",
            reply_markup=get_location_address_check_inline_keyboard(),
        )

        await state.update_data(address=address)
    else:
        await message.answer(
            "Такого адреса не существует:( Попробуй еще раз",
        )


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
        await state.set_state(NewLocation.address)
        await callback.message.answer(
            "Что хочешь посетить? Напиши адрес места",
        )

    await callback.message.delete()
    await callback.answer()


@router.message(F.text, NewLocation.start_date)
async def process_new_journey_start_date(message: Message, state: FSMContext):
    try:
        if datetime.strptime(message.text, "%Y-%m-%d") < datetime.now():  # noqa: DTZ005, DTZ007
            await message.answer(
                "Дата начала путешествия не может быть раньше текущей даты",
            )
        else:
            await state.update_data(
                start_date=datetime.strptime(message.text, "%Y-%m-%d"),  # noqa: DTZ007
            )
            await state.set_state(NewLocation.end_date)
            await message.answer(
                "Напиши дату отъезда из локации в формате "
                "YYYY-MM-DD, например 2024-03-18",
            )
    except ValueError:
        await message.answer("Неправильный формат даты(")


@router.message(F.text, NewLocation.end_date)
async def process_new_journey_end_date(message: Message, state: FSMContext):
    try:
        if datetime.strptime(message.text, "%Y-%m-%d") < datetime.now():  # noqa: DTZ005, DTZ007
            await message.answer(
                "Дата окончания путешествия не может быть раньше текущей даты",
            )
        else:
            await state.update_data(
                end_date=datetime.strptime(message.text, "%Y-%m-%d"),  # noqa: DTZ007
            )
            location_data = await state.get_data()
            lat, lon = get_place_coord(location_data.get("address"))
            location = Location.create(
                journey=location_data.pop("journey_id"),
                lat=lat,
                lon=lon,
                **location_data,
            )
            location.save()

            await message.answer("Локация добавлена!")
            await message.answer(
                get_format_location(location_id=location.id),
                reply_markup=get_location_actions_inline_keyboard(
                    location_id=location.id,
                    journey_id=location.journey.id,
                    user_type="owner",
                ),
            )
            await state.clear()

    except ValueError:
        await message.answer("Неправильный формат даты(")


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
            reply_markup=get_locations_inline_keyboard(
                locations=locations,
                user_type=callback_data.user_type,
                journey_id=callback_data.journey_id,
            ),
        )
        await callback.answer()


@router.callback_query(
    AllLocationsCallbackFactory.filter(F.action == "get_location"),
)
async def callback_location_get(
    callback: CallbackQuery,
    callback_data: AllLocationsCallbackFactory,
):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            get_format_location(location_id=callback_data.location_id),
            reply_markup=get_location_actions_inline_keyboard(
                location_id=callback_data.location_id,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )
    await callback.answer()


@router.callback_query(
    LocationActionCallbackFactory.filter(F.action == "delete"),
)
async def callback_location_delete(
    callback: CallbackQuery,
    callback_data: LocationActionCallbackFactory,
):
    Location.get(Location.id == callback_data.location_id).delete_instance()
    await callback.message.delete()
    await callback.answer("Локация удалена!")


@router.callback_query(
    LocationActionCallbackFactory.filter(F.action == "weather"),
)
async def callback_location_weather(
    callback: CallbackQuery,
    callback_data: LocationActionCallbackFactory,
):
    location = Location.get(Location.id == callback_data.location_id)
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            get_format_weaher(lat=location.lat, lon=location.lon),
            reply_markup=get_location_weather_inline_leyboard(
                journey_id=callback_data.journey_id,
                location_id=callback_data.location_id,
                user_type=callback_data.user_type,
            ),
        )
    await callback.answer()


@router.callback_query(
    LocationActionCallbackFactory.filter(F.action == "landmarks"),
)
async def callback_location_landmarks(
    callback: CallbackQuery,
    callback_data: LocationActionCallbackFactory,
):
    location = Location.get(Location.id == callback_data.location_id)
    landmarks = get_landmarks(
        lat=location.lat,
        lon=location.lon,
    )
    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(
            reply_markup=get_location_landmarks_inline_leyboard(
                landmarks=landmarks,
                journey_id=callback_data.journey_id,
                location_id=callback_data.location_id,
                user_type=callback_data.user_type,
            ),
        )

    await callback.answer()


@router.callback_query(
    LandmarksCallbackFactory.filter(F.action == "get_landmark"),
)
async def callback_location_get_landmark(
    callback: CallbackQuery,
    callback_data: LandmarksCallbackFactory,
):
    landmark = get_format_landmark(xid=callback_data.xid)

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=landmark,
            reply_markup=get_landmark_action_keyboard(
                journey_id=callback_data.journey_id,
                location_id=callback_data.location_id,
                user_type=callback_data.user_type,
            ),
        )

    await callback.answer()
