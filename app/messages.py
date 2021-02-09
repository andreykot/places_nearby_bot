START = "Привет!\n\n" \
        "Данный бот поможет тебе найти интересные места поблизости.\n\n" \
        "Интересные места могут быть найдены по данным OpenStreetMap (Google и Яндекс - в разработке).\n\n" \
        "Под полем ввода сообщения уже появилась кнопка, которая поможет тебе найти места поблизости :)"

INFO = "Пишется..."

SET_RADIUS = "Задайте радиус поиска"

SET_SOURCE = "Выберите поисковой ресурс"

START_SEARCH = "Ищем..."

RESULT_COUNT = lambda number: f"Найдено мест: {number}\n"

CALLBACK_SET_ANSWER = "Принято!"

NOT_IMPLEMENTED_SOURCE = "Выбранный ресурс еще не реализован.\n" \
                         "На данный момент можно воспользоваться данными OpenStreetMap."

ECHO = "Неизвестная команда :("
ECHO_CALLBACK = "Начните поиска сначала"
ERROR = "Что-то пошло не так... Попробуйте еще раз."


def build_place_message(position: int, name: str, google: str, yandex: str, description: str = None):
    description = '\n\n' + '<i>' + description + '</i>' if description else ""
    text = f'{position}. <b>{name}</b>' \
           f'{description}' \
           f'\n\nПосмотреть на карте:\n<a href="{google}">Google Maps</a>   |   <a href="{yandex}">Яндекс.Карты</a>'

    return text
