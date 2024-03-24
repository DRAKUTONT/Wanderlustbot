import logging
from typing import List

import requests

from loader import OPENTRIPMAP_API_KEY


def get_landmarks(lat, lon, radius: int = 10000, limit: int = 5) -> List[dict]:
    params = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "format": "json",
        "apikey": OPENTRIPMAP_API_KEY,
    }

    request = requests.get(
        url="https://api.opentripmap.com/0.1/ru/places/radius",
        params=params,
        timeout=5,
    )

    logging.warning(f"Opentripmap status code: {request.status_code}")

    places = []
    for place in request.json():
        places.append(
            {
                "name": place["name"],
                "xid": place["xid"],
                "rate": place["rate"],
            },
        )

    return sorted(places, key=lambda x: x.get("rate"), reverse=True)[:limit]


def landmark_info(xid: str) -> dict:
    params = {
        "apikey": OPENTRIPMAP_API_KEY,
    }

    request = requests.get(
        url=f"https://api.opentripmap.com/0.1/ru/places/xid/{xid}",
        params=params,
        timeout=5,
    )

    logging.warning(f"Opentripmap status code: {request.status_code}")

    return request.json()


def get_format_landmark(xid: str):
    landmark = landmark_info(xid=xid)

    address = ", ".join(landmark["address"].values())

    return (f"{landmark.get("name")}\n"
                       f"Адрес: {address}\nРейтинг: {landmark.get("rate")}")
