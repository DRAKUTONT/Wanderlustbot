from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.filters.exception import ExceptionTypeFilter

from peewee import DoesNotExist

router = Router()


@router.error(ExceptionTypeFilter(DoesNotExist))
async def handle_object_does_not_exists(event: ErrorEvent):
    if event.update.callback_query:
        await event.update.callback_query.answer("Объект не существует")
