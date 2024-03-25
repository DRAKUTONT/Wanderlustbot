from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
import peewee

from models.models import User
from bot.fsm.user_data import UserData
from bot.keyboards.main_keyboard import get_main_keyboard
from bot.keyboards.start import (
    UserAddressCheckCallbackFactory,
    get_address_check_inline_keyboard,
)
from service.geosuggest import is_object_exists
from service.profile import get_format_user_profile
from service.route import get_place_coord


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not User.select().where(User.id == message.from_user.id).exists():
        await message.answer(
            "Привет! Это бот - планировщик путешествий. "
            "Но прежде чем начать работу необходимо заполнить анкету",
        )
        await state.set_state(UserData.name)
        await message.answer("Как тебя зовут?")

    else:
        await message.answer(
            "Ты уже зарегестрирован",
            reply_markup=get_main_keyboard(),
        )


@router.message(Command("edit"))
@router.message(F.text == "Изменить профиль")
async def edit(message: Message, state: FSMContext):
    await state.set_state(UserData.name)
    await message.answer("Как тебя зовут?")


@router.message(F.text, UserData.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserData.age)
    await message.answer("Сколько тебе лет?")


@router.message(F.text, UserData.age)
async def process_age(message: Message, state: FSMContext):
    try:
        if int(message.text) <= 1 or int(message.text) > 120:
            raise ValueError

        await state.update_data(age=int(message.text))
        await state.set_state(UserData.address)
        await message.answer(
            "Напиши свой адрес в удобном для тебя формате, "
            "например страна, город, улица",
        )

    except ValueError:
        await message.answer("Напиши корректное значение")


@router.message(F.text, UserData.address)
async def process_address(message: Message, state: FSMContext):
    address = is_object_exists(message.text)
    if address:
        address = address[0]["address"]["formatted_address"]
        await message.answer(
            f"Твой адрес {address}, верно?",
            reply_markup=get_address_check_inline_keyboard(),
        )

        lat, lon = get_place_coord(address)
        await state.update_data(address=address, lat=lat, lon=lon)
    else:
        await message.answer(
            "Такого адреса не существует:( Попробуй еще раз",
        )


@router.callback_query(
    UserAddressCheckCallbackFactory.filter(),
)
async def callback_user_address_check(
    callback: CallbackQuery,
    callback_data: UserAddressCheckCallbackFactory,
    state: FSMContext,
):
    if callback_data.is_valid:
        await state.set_state(UserData.bio)
        await callback.message.answer("Расскажи немного о себе")
    else:
        await state.set_state(UserData.address)
        await callback.message.answer(
            "Напиши свой адрес, в формате страна, город",
        )

    await callback.message.delete()
    await callback.answer()


@router.message(F.text, UserData.bio)
async def process_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    user_data = await state.get_data()

    try:
        User.create(id=message.from_user.id, **user_data)

    except peewee.IntegrityError:
        User.update(**user_data).where(
            User.id == message.from_user.id,
        ).execute()

    await message.answer("Так выглядит твой профиль:")
    await message.answer(
        get_format_user_profile(id=message.from_user.id),
        reply_markup=get_main_keyboard(),
    )
    await state.clear()
