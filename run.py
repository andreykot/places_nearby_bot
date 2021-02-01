from aiogram import executor
import logging

from app import bot


def main():
    logging.basicConfig(level=logging.DEBUG)

    # loop = bot.dispatcher.loop
    executor.start_polling(bot.dispatcher,
                           skip_updates=True,
                           )


if __name__ == '__main__':
    main()
