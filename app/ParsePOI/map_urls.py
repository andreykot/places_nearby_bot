def googlemaps_location_url(lat, lon):
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"


def yandexmaps_location_url(lat, lon):
    return f"https://yandex.ru/maps/?pt={lon},{lat}&z=18&l=map"
