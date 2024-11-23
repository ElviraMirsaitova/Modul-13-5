from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# ВСТАВЬТЕ_СВОЙ_КЛЮЧ_API в строку ниже
api = '_________________________'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)
#kb.row kb.insert



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer('Введите свой рост, см:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(gr=message.text)
    await message.answer('Введите свой вес, кг:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(we=message.text)
    data = await state.get_data()
    cal = int(data['we']) * 10 + 6.25 * int(data['gr']) - 5 * int(data['ag']) + 5
    await message.answer(f'Если вы мужчина, Ваша норма калорий в день составляет {cal}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет!', reply_markup=kb)

@dp.message_handler(text='Информация')
async  def inform(message):
    await message.answer('Информация о боте!')


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
