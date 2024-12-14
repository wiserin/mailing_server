from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

router = Router()
storage = MemoryStorage()

class Add_user(StatesGroup):
    add_user_name = State()

@router.message(F.text == '/start')
async def start(message: Message, state = FSMContext):
    await message.answer('Введите свое имя')
    await state.set_state(Add_user.add_user_name)

@router.message(Add_user.add_user_name)
async def add_name(message: Message, state: FSMContext):
    user_name = message.text
    await message.answer(f'Добро пожаловать, {user_name}')
    await state.clear()