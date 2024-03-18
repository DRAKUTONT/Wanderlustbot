from models.models import Journey


def get_format_journey(name: str) -> str:
    journey = Journey.get(Journey.name == name)

    return (f"ID путешествия: {journey.id}\nНазвание: {journey.name}\n"
           f"Дата начала: {journey.start_date}\n"
           f"Дата окончания: {journey.end_date}\n\n{journey.about}")
