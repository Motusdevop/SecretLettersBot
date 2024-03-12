from aiogram import Router, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import CreateLetter
from api import create_letter
from exceptions import InvalidToken, WrongPassword, NoneConnection

router = Router()


@router.message(Command('create'))
async def read_letter(message: Message, state: FSMContext):
    await state.set_state(CreateLetter.title)
    await message.answer("Введите заголовок вашего письма:")

@router.message(CreateLetter.title)
async def title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(CreateLetter.body)
    await message.answer("Напишите тело письма, если не хотите, то напишите: none")

@router.message(CreateLetter.body)
async def title(message: Message, state: FSMContext):

    if message.text.lower() == 'none':
        body = None
    else:
        body = message.text

    await state.update_data(body=body)
    await state.set_state(CreateLetter.author)
    await message.answer("Укажите автора, если не хотите, то напишите: none")


@router.message(CreateLetter.author)
async def title(message: Message, state: FSMContext):
    if message.text.lower() == 'none':
        author = None
    else:
        author = message.text

    await state.update_data(author=author)
    await state.set_state(CreateLetter.password)
    await message.answer("""Напишите пароль для письма, его вы будете сказать получателю.
**Поэтому ни в коем случае не используйте реальные пароли**, воспользуйтесь чем-то простым например: `pass`""", parse_mode=ParseMode.MARKDOWN)

@router.message(CreateLetter.password)
async def last_step(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    try:
        token = create_letter(**data)
        await state.clear()
        await message.answer(f"""
Реквизиты для прочтения письма:

**Токен:** `{token}`
    
**Пароль:** `{data['password']}`
    """, parse_mode=ParseMode.MARKDOWN)

    except NoneConnection:
        await message.answer("Что-то пошло не так возможно отсуствует подключение к серверу...")

