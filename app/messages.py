START = "Привет!\nДанный бот поможет тебе найти интересные места поблизости.\n" \
        "Могу искать интересные места по данным OpenStreetMap (Google и Яндекс - в разработке). Попробуем? :)"

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