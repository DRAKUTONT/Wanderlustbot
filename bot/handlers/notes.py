from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.fsm.notes import AddNote
from bot.keyboards.journey import JourneyActionsCallbackFactory
from bot.keyboards.notes import (
    NotesActionsCallbackFactory,
    AllNotesCallbackFactory,
    get_notes_inline_keyboard,
    get_note_actions_inline_keyboard,
)
from models.models import Note

router = Router()


@router.callback_query(
    JourneyActionsCallbackFactory.filter(F.action == "notes"),
)
async def callback_get_all_notes(
    callback: CallbackQuery,
    callback_data: JourneyActionsCallbackFactory,
):
    notes = Note.select().where(Note.journey == callback_data.journey_id)
    if callback_data.user_type != "owner":
        notes = notes.where(Note.is_private == False)  # noqa: E712

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            callback.message.text,
            reply_markup=get_notes_inline_keyboard(
                notes=notes,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )
    await callback.answer()


@router.callback_query(
    NotesActionsCallbackFactory.filter(F.action == "add_note"),
)
async def callback_add_note(
    callback: CallbackQuery,
    callback_data: NotesActionsCallbackFactory,
    state: FSMContext,
):
    await callback.message.answer("Как будет называться заметка?")
    await state.update_data(journey_id=callback_data.journey_id)
    await state.set_state(AddNote.title)
    await callback.answer()


@router.message(F.text, AddNote.title)
async def process_add_note_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddNote.note)
    await message.answer(
        "Пришли текст заметки, или файл, который хочешь добавить "
        "(а можешь все сразу, но только одним сообщением)",
    )


@router.message(AddNote.note)
async def process_add_note(message: Message, state: FSMContext):
    await state.update_data(text=message.text or message.caption)

    if message.photo:
        await state.update_data(file_id=message.photo[0].file_id)

    if message.document:
        await state.update_data(file_id=message.document.file_id)

    data = await state.get_data()
    Note.create(**data)

    await message.answer("Заметка добавлена!")
    await state.clear()


@router.callback_query(
    AllNotesCallbackFactory.filter(F.action == "get_note"),
)
async def callback_get_note(
    callback: CallbackQuery,
    callback_data: AllNotesCallbackFactory,
):
    note = Note.get(Note.id == callback_data.note_id)
    if note.file_id:
        await callback.message.edit_text(
            document=note.file_id,
            caption=note.text,
            reply_markup=get_note_actions_inline_keyboard(
                note_id=callback_data.note_id,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )

    elif note.text:
        await callback.message.answer(
            note.text,
            reply_markup=get_note_actions_inline_keyboard(
                note_id=callback_data.note_id,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )

    await callback.answer()


@router.callback_query(
    NotesActionsCallbackFactory.filter(F.action == "delete"),
)
async def callback_delete_note(
    callback: CallbackQuery,
    callback_data: AllNotesCallbackFactory,
):
    Note.get(Note.id == callback_data.note_id).delete_instance()
    await callback.message.delete()
    await callback.answer()


@router.callback_query(
    NotesActionsCallbackFactory.filter(F.action == "hide_note"),
)
async def callback_hide_note(
    callback: CallbackQuery,
    callback_data: AllNotesCallbackFactory,
):
    note = Note.get(Note.id == callback_data.note_id)
    note.is_private = True
    note.save()

    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(
            reply_markup=get_note_actions_inline_keyboard(
                note_id=callback_data.note_id,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )

    await callback.answer("Теперь заметка видна только тебе")


@router.callback_query(
    NotesActionsCallbackFactory.filter(F.action == "show_note"),
)
async def callback_show_note(
    callback: CallbackQuery,
    callback_data: AllNotesCallbackFactory,
):
    note = Note.get(Note.id == callback_data.note_id)
    note.is_private = False
    note.save()

    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(
            reply_markup=get_note_actions_inline_keyboard(
                note_id=callback_data.note_id,
                journey_id=callback_data.journey_id,
                user_type=callback_data.user_type,
            ),
        )

    await callback.answer(
        "Теперь заметка видна только всем участникам путешествия",
    )
