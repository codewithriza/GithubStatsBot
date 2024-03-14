import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.load_extension('cogs.repos')
bot.load_extension('cogs.user')

bot.run('TOKEN')
