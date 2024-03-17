from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from models.models import User
from bot.fsm.user_data import UserData

router = Router()


# TODO: сделать проверки на валидность страны\города

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Start")
    if not User.select().where(User.id == message.from_user.id).exists():
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
    await state.update_data(country=message.text)
    await state.set_state(UserData.city)
    await message.answer("Введите ваш город")


@router.message(F.text, UserData.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(UserData.bio)
    await message.answer("Расскажите о себе")


@router.message(F.text, UserData.bio)
async def process_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    user_data = await state.get_data()
    User.create(id=message.from_user.id, **user_data)

    await message.answer("спасибо")
    await state.clear()
