from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
import app.database.requests as db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import app.keyboard as kb
import requests
from dotenv import load_dotenv
import os

storage = MemoryStorage()
user_router = Router()
router = user_router
load_dotenv()

class reg(StatesGroup):
    start = State()
    add_name = State()
    add_last_name = State()
    add_email = State()
    check_code = State()

class Mailing(StatesGroup):
    _1 = State()
    _2 = State()
    _3 = State()

@router.message(F.text == '/start')
async def start(message: Message, state: FSMContext):
    init = await db.initialization(message.from_user.id)
    if init == True:
        await message.answer(text='Добро пожаловать!', reply_markup=kb.main_kb)

    elif init == False:
        await message.answer('Не нашел вас среди зарегистрированных пользователей.\n Пожалуйста, пройдите регистрацию. После этого, вы получите доступ ко всему функционалу бота и API', reply_markup=kb.reg_kb)
        await state.set_state(reg.start)

@router.message(lambda message: message.text != 'Зарегистрироваться', reg.start)
async def if_start(message: Message):
    await message.answer('Для того, чтобы получить доступ к полному функционалу бота, пожалуйста зарегистрируйтесь.')

@router.message(reg.start)
async def start_r(message: Message, state: FSMContext):
    await message.answer('Введите ваше имя:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(reg.add_name)

@router.message(reg.add_name)
async def add_n(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer('Введите вашу фамилию:')
    await state.set_state(reg.add_last_name)

@router.message(reg.add_last_name)
async def add_last(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('Введите ваш email')
    await state.set_state(reg.add_email)

@router.message(reg.add_email)
async def add_email(message: Message, state: FSMContext):
    email = message.text
    api_token = str(os.getenv('API_TOKEN'))

    for_server = {
        'token': api_token,
        'email': email
    }
    request = requests.post('http://89.248.207.112:5000/email_verification', json=for_server)

    req = request.json()
    code = str(req["email_code"])
    await state.update_data(email=email)
    await state.update_data(code=code)
    await message.answer('Введите код, пришедший вам на почту', reply_markup=kb.change_email_kb)
    await state.set_state(reg.check_code)


@router.message(reg.check_code)
async def add_last(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == data['code']:
        user_name = str(data['user_name'])
        user_last_name = str(data['last_name'])
        user_email = str(data['email'])

        for_server = {
            'name': user_name,
            'last_name': user_last_name,
            'email': user_email
        }
        request = requests.post('http://89.248.207.112:5000/add_user', json=for_server)
        req = request.json()
        token = req['token']
        await message.answer(text='Успешная регистрация\n'
                             f'Ваш токен: {token}', reply_markup=kb.main_kb)
        await db.add_user(message.from_user.id, user_name, user_last_name, 
                          user_email, token)
        await state.clear()

    elif message.text == 'Поменять email':
        await message.answer('Введите ваш email')
        await state.set_state(reg.add_email)

    elif message.text != data['code']:
        await message.answer('Попробуйте еще раз')
        await state.set_state(reg.check_code)


@router.message(F.text == 'Документация')
async def doc(message: Message):
    await message.answer('Выберите пункт', reply_markup=kb.api_doc_kb)

@router.message(F.text == 'Проверка email')
async def check_EM(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAIB0GUz2v-FioFzGXUu8chcQuj44jjKAAIk1DEbFzuhSUhk2cCKEPJjAQADAgADeQADMAQ',
                               caption='Для получения доступа к данной функции, отправьте POST запрос на адрес: \n'
                               'http://89.248.207.112:5000/email_verification\n'
                               'С полями:\n\n'
                               'token (ваш API токен)\n'
                               'email (почта на которую нужно выслать код)\n\n'
                               'В качестве ответа, вам вернется json файл со статусом и проверочным кодом, отправленным на почту', 
                               parse_mode='html', reply_markup=kb.main_kb)

@router.message(F.text == 'Рассылка на email')
async def mailing(message: Message, state: FSMContext):
    await message.answer('Для начала, вам нужно включить двухфакторную аунтификацию в настройках своего аккаунта Google\n\n'
                         'Это можно сделать по ссылке: https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Ftwo-step-verification%3Frapt%3DAEjHL4M0-E_vSm_-bSmWbX-Cx0b0ucME1cUQgXA50UV49ltkdSVlBB6Oj5w70_95elbdlLGSPzgJM0u0plkVqcNdeBwRyQ3PhA&followup=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Ftwo-step-verification%3Frapt%3DAEjHL4M0-E_vSm_-bSmWbX-Cx0b0ucME1cUQgXA50UV49ltkdSVlBB6Oj5w70_95elbdlLGSPzgJM0u0plkVqcNdeBwRyQ3PhA&ifkv=AVQVeyyOh04n_ihngmQEzjKJ7y5dxSYLfk769ZIDxEYg91sqzL0JqE3phx5UadHCH0nguUrT63xk&osid=1&passive=1209600&rart=ANgoxceEBeW40Tt3eugKDDHnj8RI-xXzPVcQWUv_z3bgBjZi0L-bmBEfAVz0jMkdVsXu5QCr7kdSyvJBN0TcwPxaH5toME-n8A&service=accountsettings&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S117848614%3A1697902551051626&theme=glif',
                         reply_markup=kb.resume_kb)
    await state.set_state(Mailing._1)

@router.message(Mailing._1)
async def mailing_1(message: Message, state: FSMContext):
    await message.answer('Далее, создайте новый пароль для приложения.\n\n'
                         'Сделать это можно по ссылке: https://myaccount.google.com/apppasswords?utm_source=google-account&utm_medium=myaccountsecurity&utm_campaign=tsv-settings&rapt=AEjHL4Pjo7CZylyGncPnOfD3IBe3RIRldqXM3S28hwNa3O9jtOFU3GsWobct6GSbP1jM28DaAYPhamxQTY8KhEUoGPAJT4bskQ',
                         reply_markup=kb.resume_kb)
    await state.set_state(Mailing._2)
    
@router.message(Mailing._2)
async def mailing_2(message: Message, state: FSMContext):
    await message.answer_photo(photo='AgACAgIAAxkBAAIB4GUz9lRh8ocYN2SKkoF79I_ydUkbAAKh1TEbFzuhSf1U30vd_x_KAQADAgADeAADMAQ',
                               caption='Теперь, вам нужно отправить POST запрос на адрес:\n'
                               'http://89.248.207.112:5000/mailing\n'
                               'С полями:\n\n'
                               'token (ваш API токен)\n'
                               'login (ваш gmail для рассылки)\n'
                               'password (ваш пароль для приложения)\n'
                               'topic (тема вашего письма)\n'
                               'text (текст вашей рассылки)\n'
                               'users (список пользователей, которым должна быть доставлена ваша рассылка)\n\n'
                               'В качестве ответа, вам вернется json файл со статусом вашей рассылки', reply_markup=kb.main_kb)
    await state.clear()

@router.message(F.text == 'Мой токен')
async def my_token(message: Message):
    token = await db.get_user_token(message.from_user.id)
    await message.answer(f'Ваш токен: {token}')

@router.message()
async def nothing(message: Message):
    await message.answer('Я вас не понимаю')

# @router.message()
# async def s(message: Message):
#     photo = message.photo[-1].file_id
#     await message.answer(photo)