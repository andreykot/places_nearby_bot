from typing import NamedTuple
from aiogram import types


class Buttons(NamedTuple):
    """Class to provide comfortable way to initialize buttons for reply/inline markups."""

    items: list
    order: list = []

    def __repr__(self):
        return "items: {}, order: {}".format(self.items, self.order)

    def make_reply_button(self, index):
        return types.reply_keyboard.KeyboardButton(**self.items[index])

    def make_inline_button(self, index):
        return types.InlineKeyboardButton(**self.items[index])


def build_replykeyboard(buttons: Buttons) -> types.ReplyKeyboardMarkup:
    """Set reply keyboard by Buttons class object."""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if isinstance(buttons, Buttons):
        if buttons.order and len(buttons.items) != sum(buttons.order):
            raise ValueError("The count of buttons and their count in order list isn't equal.")

        accumulated = 0
        order = buttons.order if buttons.order else [1 for _ in range(len(buttons.items))]
        for n in order:
            reply_buttons = [buttons.make_reply_button(accumulated + i) for i in range(n)]
            markup.add(*reply_buttons)
            accumulated += n

    else:
        raise TypeError('Unknown type of buttons in app.buttons.build_replykeyboard')

    return markup


def build_inlinekeyboard(buttons, row_width: int = 3):
    """
    :param buttons: list or Buttons object.
    :param row_width: int.
    :return: types.InlineKeyboardMarkup
    """
    markup = types.InlineKeyboardMarkup(row_width=row_width)

    if isinstance(buttons, Buttons):
        if buttons.order and len(buttons.items) != sum(buttons.order):
            raise ValueError("The count of buttons and their count in order list isn't equal.")

        accumulated = 0
        order = buttons.order if buttons.order else [1 for _ in range(len(buttons.items))]
        for n in order:
            inline_buttons = [buttons.make_inline_button(accumulated + i) for i in range(n)]
            markup.add(*inline_buttons)
            accumulated += n

    else:
        raise TypeError('Unknown type of buttons in app.buttons.build_inlinekeyboard')

    return markup


EMPTY_MARKUP = types.ReplyKeyboardRemove()



