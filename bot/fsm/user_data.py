from aiogram.fsm.state import StatesGroup, State


class UserData(StatesGroup):
    name = State()
    age = State()
    address = State()
    bio = State()
