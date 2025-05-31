import coolname
from db.repositories.bot_repository import BotRepository
import random
import asyncio

class UsernameGenerator:
    """Generates a random username using the coolname library."""

    @staticmethod
    async def generate() -> str:
        """Generate a random username."""
        username = '-'.join(coolname.generate(2)) + '-' + str(coolname.random.randint(0, 9999))
        if len(username) > 20:
            username = username[:20]
        return username

    @staticmethod
    async def generate_username(bot_repository: BotRepository) -> str:
        """Generate a unique username. If taken, mutate one character to a digit until unique."""
        username = await UsernameGenerator.generate()
        while await bot_repository.get_bot_by_name(username):
            username_list = list(username)
            for i in range(len(username_list)):
                if not username_list[i].isdigit():
                    username_list[i] = str(random.randint(0, 9))
                    break
            username = ''.join(username_list)
        return username