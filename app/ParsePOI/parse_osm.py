import json
import os
import typing

from app import messages
from app.ParsePOI import map_urls


OSM_SETS = {
    "Памятники и мемориалы": [
        "historic~memorial",
    ],
    "Исторические места": [
        "historic",
    ],
    "Точки обзора": [
        'tourism~viewpoint',
    ],
    "Информация для туристов": [
        'tourist~information',
    ],
    "Театры, музеи, выставки": [
        'amenity~theatre', 'tourism~museum', 'tourism~gallery', 'tourism~artwork', 'amenity~arts_centre',
    ],
    "Развлечения": [
        'tourism~theme_park', 'tourism~aquarium', 'tourism~zoo', "tourism~planetarium",
    ],
    "Фонтаны": [
        "tourism~fountain",
    ],
}


class OverpassAroundQueryConstructor:

    out_format = 'json'
    query_timeout = 25

    def __init__(self, lat, lon, radius):
        self.lat = lat
        self.lon = lon
        self.radius = radius

        self.nodes = list()

    def construct_query(self):
        nodes_def = '\n'.join(self.nodes)
        return f"[out:{self.out_format}][timeout:{self.query_timeout}];\n" \
               f"(\n{nodes_def}\n);\n" \
               f"out;"

    def set_around_nodes(self, sets: dict):
        params = {'lat': self.lat, 'lon': self.lon, 'radius': self.radius}
        for category, tags in sets.items():
            for tag in tags:
                node = OverpassNode(filter_='around', filter_params=params, node_set=tag)
                self.nodes.append(node.make_node())


class OverpassNode:
    def __init__(self, filter_: str, filter_params: dict, node_set: str):
        self.filter = filter_
        self.filter_params = filter_params
        self.node_set = node_set

        self.filter_definition = self.construct_filters()

    def make_node(self) -> str:
        return f"node({self.filter_definition})[{self.node_set}];"

    def construct_filters(self) -> str:
        if self.filter == 'around':
            required_params = ['lat', 'lon', 'radius']
            if len(set(required_params) & set(list(self.filter_params.keys()))) != len(required_params):
                raise ValueError("Set required parameters for around filter")

            return self.around_definition(
                lat=self.filter_params['lat'],
                lon=self.filter_params['lon'],
                radius=self.filter_params['radius'],
            )
        else:
            raise NotImplementedError

    @staticmethod
    def around_definition(lat: (int, float), lon: (int, float), radius: (int, float)) -> str:
        return f"around:{radius}, {lat}, {lon}"


def query_func(lat, lon, radius) -> str:
    def __test_query():
        with open(os.path.join(os.path.dirname(__file__), 'osm_query_test.txt'), 'w') as file:
            query = constructor.construct_query()
            file.write(query)

    constructor = OverpassAroundQueryConstructor(lat=lat, lon=lon, radius=radius)
    constructor.set_around_nodes(sets=OSM_SETS)
    __test_query()
    return constructor.construct_query()


def create_answer(content) -> dict:
    osm_categories = __reverse_osm_sets()

    content = json.loads(content)
    answer = {"count": 0, "places": []}
    for place in content['elements']:
        #print(place)
        if 'name' in place['tags']:
            name = place['tags']['name']
            answer['count'] += 1
        else:
            continue

        if 'description' in place['tags']:
            description = place['tags']['description'] if place['tags']['description'] != name else None
        elif 'inscription' in place['tags']:
            description = place['tags']['inscription'] if place['tags']['inscription'] != name else None
        else:
            description = None

        msg = messages.build_place_message(
            position=answer['count'],
            name=name,
            google=map_urls.googlemaps_location_url(lat=place['lat'], lon=place['lon']),
            yandex=map_urls.yandexmaps_location_url(lat=place['lat'], lon=place['lon']),
            description=description
        )
        answer['places'].append(msg)

    return answer


def __answer_constructor(name, description, position_urls):
    ans_name = f"Название: {name}\n\n"
    ans_description = f"Описание: {description}\n\n" if description else ""
    ans_position = f"Google: {position_urls['google']}\n\n" \
                   f"Яндекс: {position_urls['yandex']}\n\n"

    return ans_name + ans_description + ans_position


def __reverse_osm_sets(split_by_tilda=True):
    new_dict = dict()
    for category, tags in OSM_SETS.items():
        for tag in tags:
            if split_by_tilda:
                new_dict[tag.split('~')[1] if len(tag.split('~')) > 1 else tag] = category
            else:
                new_dict[tag] = category

    return new_dict


SOURCE = {
    'url': r"https://lz4.overpass-api.de/api/interpreter",
    'query_func': query_func,
    'create_answer': create_answer,
}
