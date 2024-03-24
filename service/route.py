import logging
from typing import List
import requests

from loader import GEOCODER_API_KEY


def create_route(places: List[tuple], profile: str = "car") -> str:
    """Get geohopper url"""
    params = {
        "point": [],
        "profile": profile,
        "layer": "Omniscale",
    }
    for place in places:
        coord = f"{place[0]}%2C{place[1]}"
        params["point"].append(coord)

    return (
        requests.Request("GET", "https://graphhopper.com/maps", params=params)
        .prepare()
        .url
    )


def get_place_coord(place: str) -> str:
    params = {
        "format": "json",
        "apikey": GEOCODER_API_KEY,
        "geocode": place.replace(" ", "+"),
    }
    request = requests.get(
        "https://geocode-maps.yandex.ru/1.x/",
        params=params,
        timeout=5,
    )

    logging.warning(f"Geocoder status code: {request.status_code}")
    coord = request.json()["response"]["GeoObjectCollection"]["featureMember"][
        0
    ]["GeoObject"]["Point"]["pos"]

    return coord.split()[::-1]
