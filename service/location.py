from models.models import Location


def get_format_location(location_id: int) -> str:
    location = Location.get(Location.id == location_id)

    return (f"Адрес: {location.address}\n"
           f"Дата посещения: {location.start_date}\n"
           f"Дата отъезда: {location.end_date}\n")
