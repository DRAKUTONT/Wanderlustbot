from aiogram.fsm.state import StatesGroup, State


class AddNote(StatesGroup):
    title = State()
    note = State()
