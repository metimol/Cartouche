import coolname
from app.db.repositories.bot_repository import BotRepository
import random


class UsernameGenerator:
    """Generates a random username using the coolname library."""

    @staticmethod
    async def generate() -> str:
        """Generate a random username."""
        username = "_".join(coolname.generate(2)) + "_" + str(random.randint(0, 9999))
        if len(username) > 20:
            username = username[:20]
        return username

    @staticmethod
    async def generate_username(bot_repository: BotRepository) -> str:
        """Generate a unique username. If taken, mutate one character to a digit until unique."""
        username = await UsernameGenerator.generate()
        while bot_repository.get_bot_by_name(username):
            username_list = list(username)
            for i in range(len(username_list)):
                if not username_list[i].isdigit():
                    username_list[i] = str(random.randint(0, 9))
                    break
            username = "".join(username_list)
        return username
