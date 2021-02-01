from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, Update, callback_query
from aiogram.utils.exceptions import MessageToDeleteNotFound

from app import messages, buttons
from app.ParsePOI.parse_osm import test_result


async def start(message: types.Message):
    await message.reply(text=messages.START, reply_markup=buttons.MAIN)


async def help(message: types.Message):
    pass


async def settings(message: types.Message):
    await message.reply(text="В разработке")


async def search_by_point(message: types.Message):
    result = test_result(message.location.longitude, message.location.latitude)
    await message.reply(text="Your position: lon={}, lat={}\n\nРезультат:\n{}".format(message.location.longitude,
                                                                                    message.location.latitude,
                                                                                    result)
                        )
