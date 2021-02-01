from typing import NamedTuple
from aiogram import types


class Buttons(NamedTuple):
    """
    Class to provide comfortable way to initialize buttons for reply/inline markups.

    :param items: list of dicts.
        List of buttons with parameters.
        Format of input dict in list: {'text': str, 'callback': str, 'params': dict},
        where text - button name, callback_data - text to call callback,
        params - dict of params for aiogram.types.reply_keyboard.KeyboardButton
        (ex.: reply_location=True, query location from user by button).
    :param order: list.
        List of integers. Each number - count of buttons from items in line.
    """

    items: list
    order: list = []

    def __repr__(self):
        return "items: {}, order: {}".format(self.items, self.order)

    def make_reply_button(self, index):
        return types.reply_keyboard.KeyboardButton(**self.items[index])


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

    elif isinstance(buttons, list):  # TODO
        name_is_callback = True if not isinstance(buttons[0], (list, tuple)) else False
        for button in buttons:
            if name_is_callback:
                markup.add(button)
            else:
                markup.add(button[0])
    else:
        raise TypeError('Unknown type of buttons in app.buttons.build_replykeyboard')

    return markup


    #markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    #markup.add(*iterable)
    #return markup


def build_inlinekeyboard(buttons, row_width: int = 3):
    """
    :param buttons: list or Buttons object.
        If callback is different from the button name - list of tuples: ({button name}, {button callback data}).
    :param row_width: int.
    :return: types.InlineKeyboardMarkup
    """
    markup = types.InlineKeyboardMarkup(row_width=row_width)

    if isinstance(buttons, Buttons):
        if buttons.order and len(buttons.items) != sum(buttons.order):
            raise ValueError("The count of buttons and their count in order list isn't equal.")

        name_is_callback = True if not isinstance(buttons.items[0], (list, tuple)) else False
        accumulated = 0
        order = buttons.order if buttons.order else [1 for _ in range(len(buttons.items))]
        for n in order:
            if name_is_callback:
                inline_buttons = [types.InlineKeyboardButton(text=buttons.items[accumulated+i],
                                                             callback_data=buttons.items[accumulated+i])
                                  for i in range(n)]
            else:
                inline_buttons = [types.InlineKeyboardButton(text=buttons.items[accumulated+i][0],
                                                             callback_data=buttons.items[accumulated+i][1])
                                  for i in range(n)]
            markup.row(*inline_buttons)
            accumulated += n
    elif isinstance(buttons, list):
        name_is_callback = True if not isinstance(buttons[0], (list, tuple)) else False
        for button in buttons:
            if name_is_callback:
                markup.add(types.InlineKeyboardButton(text=button, callback_data=button))
            else:
                markup.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    else:
        raise TypeError('Unknown type of buttons in app.buttons.build_inlinekeyboard')

    return markup


EMPTY_MARKUP = types.ReplyKeyboardRemove()



