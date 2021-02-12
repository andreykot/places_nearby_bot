START = "Привет!\n\n" \
        "Данный бот поможет тебе найти исторические и туристические места поблизости.\n\n" \
        "Интересные места будем искать по данным OpenStreetMap.\n\n" \
        "Под полем ввода сообщения уже появилась кнопка, которая поможет тебе найти места рядом.\n\n" \
        "Кстати, ты можешь искать места не только рядом с собой, но и рядом с любым местом. " \
        "Для этого нужно к сообщению боту прикрепить геопозицию и выбрать интересующее тебя место."

INFO = "Пишется..."

SET_RADIUS = "Задайте радиус поиска"

SET_SOURCE = "Выберите источник данных для поиска"

START_SEARCH = lambda source: f"Ищем по данным {source}..."

CHANGE_RADIUS = lambda limit, radius, radius_next: f"Найдено более {limit} мест для {radius}. Уменьшаю радиус до {radius_next}."
KEEP_RADIUS = lambda limit, radius: f"Даже с минимальным радиусом мест более {limit}. Выдаю результат для {radius}."
KEEP_PREVIOUS_RADIUS = lambda radius: f"Показываю все результаты с радиусом {radius}."

RESULT_COUNT = lambda number: f"Найдено мест: {number}\n"

CALLBACK_SET_ANSWER = "Принято!"

NOT_IMPLEMENTED_SOURCE = "Использование выбранного ресурса еще не реализовано.\n" \
                         "Сейчас доступны данные OpenStreetMap."

ECHO = "Неизвестная команда :("
ECHO_CALLBACK = "Начните поиск сначала"
ERROR = "Что-то пошло не так... Попробуйте еще раз."


def build_place_message(position: int, name: str, tags: list, google: str, yandex: str, description: str = None):
    tags = "  ".join(["#" + tag for tag in tags])
    description = '\n\n' + '<i>' + description + '</i>' if description else ""
    text = f'{position}. <b>{name}</b>' \
           f'\n\n{tags}' \
           f'{description}' \
           f'\n\nПосмотреть на карте:\n<a href="{google}">Google Maps</a>   |   <a href="{yandex}">Яндекс.Карты</a>'

    return text
