from app.markups import *

main_buttons = [
    {'text': 'Найти достопримечательности', 'request_location': True},
]
MAIN = build_replykeyboard(Buttons(items=main_buttons))

radius_buttons = [
    {'text': '0.5 km', 'callback_data': '500'},
    {'text': '1 km', 'callback_data': '1000'},
    {'text': '2 km', 'callback_data': '2000'},
]
RADIUS = build_inlinekeyboard(Buttons(items=radius_buttons, order=[3]), row_width=3)

source_buttons = [
    {'text': 'OpenStreetMap', 'callback_data': 'osm'},
    {'text': 'Google', 'callback_data': 'google'},
    {'text': 'Yandex', 'callback_data': 'yandex'},
]

SOURCES = build_inlinekeyboard(Buttons(items=source_buttons), row_width=1)
