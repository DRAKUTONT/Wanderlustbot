from aiogram.fsm.state import StatesGroup, State


class NewJourney(StatesGroup):
    name = State()
    about = State()


class NewLocation(StatesGroup):
    address = State()
    start_date = State()
    end_date = State()
