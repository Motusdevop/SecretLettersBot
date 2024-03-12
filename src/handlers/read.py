from aiogram import Router, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import ReadLetter
from api import get_letter
from exceptions import InvalidToken, WrongPassword, NoneConnection

router = Router()


@router.message(Command('read'))
async def read_letter(message: Message, state: FSMContext):
    await state.set_state(ReadLetter.token)
    await message.answer("Введите токен вашего письма:")

@router.message(ReadLetter.token)
async def get_token(message: Message, state: FSMContext):
    await state.update_data(token=message.text)
    await state.set_state(ReadLetter.password)
    await message.answer("Введите пароль от письма:")

@router.message(ReadLetter.password)
async def try_get(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        letter = get_letter(**data)
        await message.answer(f"""
<b>{letter['title']}</b>

<i>{letter['body'] if not letter['body'] is None else ''}</i>

Автор: {letter['author'] if not letter['author'] is None else 'Неизвестен'}""", parse_mode=ParseMode.HTML)

    except InvalidToken:
        await state.set_state(ReadLetter.token)
        await message.answer('Неверный токен или письмо уже было прочитано.')

    except WrongPassword:
        await state.set_state(ReadLetter.token)
        await message.answer("Неверный токен или пароль.")

    except NoneConnection:
        await message.answer("Отсутсвует подключение к серверу...")

