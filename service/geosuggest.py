import requests

from loader import SUGGEST_API_KEY


def is_object_exists(object_name: str) -> list | None:
    params = {
        "text": object_name,
        "lang": "ru",
        "apikey": SUGGEST_API_KEY,
        "print_address": 1,
    }
    request = requests.get(
        "https://suggest-maps.yandex.ru/v1/suggest",
        params=params,
        timeout=5,
    )
    return request.json().get("results", None)
