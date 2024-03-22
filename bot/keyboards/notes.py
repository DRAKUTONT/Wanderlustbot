from typing import List

from aiogram.utils import keyboard

from aiogram.filters.callback_data import CallbackData

from models.models import Note


class AllNotesCallbackFactory(CallbackData, prefix="notes"):
    action: str
    journey_id: int
    note_id: int
    user_type: str = "owner"


class NotesActionsCallbackFactory(CallbackData, prefix="note_actions"):
    action: str
    journey_id: int
    note_id: int
    user_type: str = "owner"


def get_notes_inline_keyboard(
    notes: List[Note],
    journey_id: int,
    user_type: str = "owner",
):
    """Get all notes in journey"""

    builder = keyboard.InlineKeyboardBuilder()
    for note in notes:
        builder.button(
            text=note.title,
            callback_data=AllNotesCallbackFactory(
                action="get_note",
                journey_id=journey_id,
                note_id=note.id,
                user_type=user_type,
            ),
        )
    builder.adjust(3)
    if user_type == "owner":
        builder.button(
            text="Добавить заметку",
            callback_data=NotesActionsCallbackFactory(
                action="add_note",
                journey_id=journey_id,
                note_id=0,
                user_type=user_type,
            ),
        )
    return builder.as_markup()


def get_note_actions_inline_keyboard(
    note_id: int,
    journey_id: int,
    user_type: str = "owner",
):
    """Get notes actions"""

    builder = keyboard.InlineKeyboardBuilder()

    if user_type == "owner":
        if not Note.get(Note.id == note_id).is_private:
            builder.button(
                text="Скрыть заметку",
                callback_data=NotesActionsCallbackFactory(
                    action="hide_note",
                    journey_id=journey_id,
                    note_id=note_id,
                    user_type=user_type,
                ),
            )
        else:
            builder.button(
                text="Сделать заметку открытой",
                callback_data=NotesActionsCallbackFactory(
                    action="show_note",
                    journey_id=journey_id,
                    note_id=note_id,
                    user_type=user_type,
                ),
            )

        builder.button(
            text="Удалить",
            callback_data=NotesActionsCallbackFactory(
                action="delete",
                journey_id=journey_id,
                note_id=note_id,
                user_type=user_type,
            ),
        )

    builder.adjust(1)
    return builder.as_markup()
