import json

import requests


overpass_api = r"https://lz4.overpass-api.de/api/interpreter"
overpass_query = lambda lat, lon, radius: f"""
[out:json][timeout:25];
(
node(around:{radius}, {lat}, {lon})["historic"];
node(around:{radius}, {lat}, {lon})["tourism"];
);
out;
    """


def test_result(lon, lat):
    response = requests.get(overpass_api,
                            params={'data': overpass_query(lon, lat, radius=1000)})
    data = response.json()
    print(data)
    return "\n\n".join(
        [str(info['tags']) + f"\nPosition: lat={info['lat']},lon={info['lon']}" for info in data['elements']]
    )


def write_response(data):
    import json
    with open(r"app\ParsePOI\result.json", 'w') as file:
        json.dump(data, file)
