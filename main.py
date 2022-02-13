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
async def invite(ctx):
    embed = discord.Embed(
        title="Invite Me!",
        description="You can invite me [here](https://discord.com/oauth2/authorize?client_id=942371791874166785&permissions=8&scope=bot).",
        color=0xFFA500,
    )
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} | Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    await ctx.send(embed=embed)

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
