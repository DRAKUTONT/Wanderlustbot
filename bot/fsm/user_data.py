from aiogram.fsm.state import StatesGroup, State


class UserData(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    bio = State()