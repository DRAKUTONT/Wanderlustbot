import asyncio
import logging

from loader import bot, dp, DIR, database
from models.models import User, Journey, Location
from bot.handlers import start, profile, journey, location, friends
from bot.errors import errors_handler


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{DIR}/logs.log"),
            logging.StreamHandler(),
        ],
    )
    database.create_tables(
        [
            User,
            User.journeys.get_through_model(),
            Journey,
            Location,
        ],
    )

    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(journey.router)
    dp.include_router(location.router)
    dp.include_router(friends.router)
    dp.include_router(errors_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
