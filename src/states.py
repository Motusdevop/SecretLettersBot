from aiogram.fsm.state import State, StatesGroup

class CreateLetter(StatesGroup):
    title = State()
    body = State()
    author = State()
    password = State()

class ReadLetter(StatesGroup):
    token = State()
    password = State()