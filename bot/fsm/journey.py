from aiogram.fsm.state import StatesGroup, State


class NewJourney(StatesGroup):
    name = State()
    about = State()
    start_date = State()
    end_date = State()


class NewLocation(StatesGroup):
    country = State()
    city = State()
    start_date = State()
    end_date = State()
