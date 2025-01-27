from typing import List

from models.models import Journey, Location, User


def get_format_journey(name: str) -> str:
    journey = Journey.get(Journey.name == name)

    return (
        f"ID путешествия: {journey.id}\nНазвание: {journey.name}\n"
        f"Описание: {journey.about}"
    )


def get_all_journey_locations(journey_id: int, user_id: int) -> List[tuple]:
    locations = [
        (location.lat, location.lon)
        for location in Location.select().where(Location.journey == journey_id)
    ]
    owner = Journey.get(Journey.id == journey_id).owner

    locations.insert(0, (owner.lat, owner.lon))
    if owner.id != user_id:
        user = User.get(User.id == user_id)
        locations.insert(0, (user.lat, user.lon))

    return locations
