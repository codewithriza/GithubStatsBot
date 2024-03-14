from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

initial_extensions = [
    'cogs.user',
    'cogs.repos'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(os.getenv('TOKEN'))
