from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command

from service.profile import get_format_user_profile

router = Router()

@router.message(F.text == "Мой профиль")
@router.message(Command("profile"))
async def edit(message: Message):
    await message.answer(get_format_user_profile(id=message.from_user.id))

