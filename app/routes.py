from aiogram import types

from app import handlers


def set_routes(dp):
    dp.register_message_handler(handlers.start, commands=['start'])
    dp.register_message_handler(handlers.search_by_point, content_types=types.ContentType.LOCATION)
    dp.register_message_handler(handlers.settings, text="Настройки")
