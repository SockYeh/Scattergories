import discord, os
from discord.ext import commands

bot = commands.Bot(
    command_prefix="-",
    case_insensitive=False,
    help_command=None,
    intents=discord.Intents.all(),
)
TOKEN = ""


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
