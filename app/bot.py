import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageIsTooLong, InvalidQueryID

from app import messages, buttons
from app.ParsePOI.main import find_places, SOURCES

from app.configs.bot import API_TOKEN


storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply(text=messages.START, reply_markup=buttons.MAIN)


@dp.message_handler(commands='info')
async def info(message: types.Message):
    await message.reply(text=messages.INFO)


class Steps(StatesGroup):
    radius = State()
    # source = State()


@dp.message_handler(state='*', content_types=types.ContentType.LOCATION)
async def set_location(message: types.Message, state: FSMContext):
    await state.reset_state()

    await state.update_data({'lat': message.location.latitude, 'lon': message.location.longitude})
    await set_radius(message, state)


async def set_radius(message: types.Message, state: FSMContext):
    await message.reply(text=messages.SET_RADIUS, reply_markup=buttons.RADIUS)
    await Steps.next()


@dp.callback_query_handler(state=Steps.radius)
async def step4(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lat, lon, radius, source = data['lat'], data['lon'], query.data, 'osm'

    await dp.bot.send_message(chat_id=query.from_user.id, text=messages.START_SEARCH(SOURCES[source]['name']))

    radius_collection = [(item['callback_data'], item['text'])
                         for item in sorted(buttons.radius_buttons, key=lambda x: int(x['callback_data']))
                         if int(item['callback_data']) <= int(radius)]
    radius_collection.insert(0, ('250', '0.25 km'))  # test it
    radius_collection.insert(0, ('100', '0.1 km'))  # test it
    limit = 50
    last_result = None
    while True:
        radius, radius_txt = radius_collection.pop()
        try:
            answer = await find_places(lat, lon, radius, source)
            if answer['count'] > limit and len(radius_collection) > 0:
                await dp.bot.send_message(chat_id=query.from_user.id,
                                          text=messages.CHANGE_RADIUS(limit, radius_txt, radius_collection[-1][1]))
            elif answer['count'] > limit and len(radius_collection) == 0:
                await dp.bot.send_message(chat_id=query.from_user.id,
                                          text=messages.KEEP_RADIUS(limit, radius_collection[-1][1]))
                break
            else:
                break
            last_result = (answer, radius, radius_txt)
            await asyncio.sleep(1.5)
        except:
            traceback.print_exc()
            await dp.bot.send_message(chat_id=query.from_user.id, text=messages.ERROR)
            return

    if last_result and answer['count'] == 0:
        answer, radius, radius_txt = last_result
        await dp.bot.send_message(chat_id=query.from_user.id, text=messages.KEEP_PREVIOUS_RADIUS(radius_txt))

    pos = messages.RESULT_COUNT(answer['count'])
    await dp.bot.send_message(chat_id=query.from_user.id, text=pos)

    await state.finish()
    for place in answer['places']:
        await asyncio.sleep(1.5)
        try:
            await dp.bot.send_message(chat_id=query.from_user.id, text=place['text'],
                                      parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
            await asyncio.sleep(0.3)
            await dp.bot.send_location(chat_id=query.from_user.id,
                                       latitude=place['lat'],
                                       longitude=place['lon'])
        except MessageIsTooLong:
            pass

    try:
        await query.answer()
    except InvalidQueryID:
        pass


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(messages.ECHO)


@dp.callback_query_handler()
async def echo(query: types.CallbackQuery):
    await query.answer(messages.ECHO_CALLBACK)
