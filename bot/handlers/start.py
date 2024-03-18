from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
import peewee

from models.models import User
from bot.fsm.user_data import UserData
from bot.keyboards.main_keyboard import get_main_keyboard
from service.geosuggest import is_object_exists
from service.profile import get_format_user_profile

router = Router()


# TODO: адекватные приветствия


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not User.select().where(User.id == message.from_user.id).exists():
        await message.answer(
            "Привет! Это бот - планировщик путешествий. "
            "Но прежде чем начать работу немобходимо заполнить анкету",
        )
        await state.set_state(UserData.name)
        await message.answer("Введите ваше имя")

    else:
        await message.answer("Вы уже зарегестрированы")
        await message.answer(
            get_format_user_profile(id=message.from_user.id),
            reply_markup=get_main_keyboard(),
        )


@router.message(Command("edit"))
@router.message(F.text == "Изменить профиль")
async def edit(message: Message, state: FSMContext):
    await state.set_state(UserData.name)
    await message.answer("Введите ваше имя")


@router.message(F.text, UserData.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserData.age)
    await message.answer("Введите ваш возраст")


@router.message(F.text, UserData.age)
async def process_age(message: Message, state: FSMContext):
    try:
        await state.update_data(age=int(message.text))
        await state.set_state(UserData.country)
        await message.answer("Введите вашу страну")

    except ValueError:
        await message.answer("Введите корректное значение")


@router.message(F.text, UserData.country)
async def process_country(message: Message, state: FSMContext):
    if is_object_exists(message.text, types="country"):
        await state.update_data(country=message.text)
        await state.set_state(UserData.city)
        await message.answer("Введите ваш город")
    else:
        await message.answer("Такой страны не существует:( Попробуйте еще раз")


@router.message(F.text, UserData.city)
async def process_city(message: Message, state: FSMContext):
    if is_object_exists(message.text, types="locality"):
        await state.update_data(city=message.text)
        await state.set_state(UserData.bio)
        await message.answer("Расскажите о себе")
    else:
        await message.answer(
            "Такого города не существует:( Попробуйте еще раз",
        )


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

    await message.answer("Ваш профиль")
    await message.answer(
        get_format_user_profile(id=message.from_user.id),
        reply_markup=get_main_keyboard(),
    )
    await state.clear()
