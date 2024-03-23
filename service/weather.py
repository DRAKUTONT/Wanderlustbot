from datetime import datetime, time
import logging
import requests

from loader import OPENWEATHER_API_KEY


def get_weather(lat, lon) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "lang": "ru",
        "units": "metric",
    }

    request = requests.get(
        url="https://api.openweathermap.org/data/2.5/forecast",
        params=params,
        timeout=5,
    )

    logging.warning(f"Openweather status code: {request.status_code}")
    return request.json()


def get_format_weaher(lat, lon):
    weather = get_weather(lat=lat, lon=lon)
    weather_day_list = []

    for i in weather["list"]:
        if datetime.fromtimestamp(i["dt"]).time() == time(15, 0, 0):  # noqa: DTZ006
            format_weather = (f"Погода на ближайшие 5 дней\n"
            f"Дата: {i["dt_txt"]}\n"
            f"{i["weather"][0]["description"].capitalize()}\n"
            f"Температура: {i["main"]["temp"]} °C\n"
            f"Влажность: {i["main"]["humidity"]}%")

            weather_day_list.append(format_weather)
    return "\n\n".join(weather_day_list)
