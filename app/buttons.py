from app.markups import *

main_buttons = [
    {'text': 'Найти достопримечательности', 'request_location': True},
    {'text': 'Настройки'},
]

MAIN = build_replykeyboard(Buttons(items=main_buttons))
