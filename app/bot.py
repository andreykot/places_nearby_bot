from aiogram import Bot, Dispatcher

from app.configs.bot import API_TOKEN
from app import routes


bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

routes.set_routes(dispatcher)
