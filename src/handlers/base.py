from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message

router = Router()


@router.message(F.text, CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        """Приветствую, я бот для создания секретных писем, которые удаляются после их прочтения,
чтобы создать такое письмо напиши: /create,
а чтобы прочитать введи: /read.""", parse_mode=ParseMode.MARKDOWN
    )