import discord, random, string, time, asyncio
from discord.ext import commands


class Scattegories(commands.Cog):
    total_categories = [
        "Animals",
        "Food",
        "Country",
        "Color",
        "Girl's name",
        "Boy's name",
        "Four letter word",
        "Movie",
        "Body part",
        "TV show",
        "3 letter words",
        "Diet food",
        "Reptiles/Amphibians",
        "Sport team",
        "Things Granny would say",
        "Something People Are Afraid Of",
        "Gift for girlfriend",
        "Shop",
        "Things you replace",
        "Websites (without www)",
        "Items in a suitcase",
        "Provinces or States",
        "Not to do in front of your crush",
        "Things that are green",
        "Asian food",
        "Things at a circus",
        "Song titles",
        "Disney Character",
        "5 Letter Word",
        "Insects",
    ]
    games = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Game(name="Scattering words muahahahahaha")
        )
        print("Bot is ready!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "You need to specify the number of categories and the total time!"
            )
            return
        else:
            await ctx.send(error)

    def generate_categories(self, category_count: int):
        categories = []
        for _ in range(category_count):
            category = random.choice(self.total_categories)
            if category in categories:
                continue
            categories.append(category)
        return categories

    @commands.command()
    async def scattergory(
        self, ctx, category_count: int = None, total_time: int = None
    ):
        try:
            assert 2 < category_count < 13
        except AssertionError:
            await ctx.send(
                "Category count must be lower than or equal to 12 and greater than or equal to 3."
            )
            return
        self.games[str(ctx.author.id)] = {}
        self.games[str(ctx.author.id)]["total_time"] = total_time
        self.games[str(ctx.author.id)]["character"] = random.choice(
            string.ascii_letters
        )
        self.games[str(ctx.author.id)]["categories"] = self.generate_categories(
            category_count
        )
        self.games[str(ctx.author.id)]["answers"] = []
        await ctx.send(
            f"You have {total_time} seconds to answer the following questions! Your character is `{self.games[str(ctx.author.id)]['character'].upper()}`."
        )

        def check(msg):
            msgc = msg.content.lower()
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and msgc.startswith(self.games[str(ctx.author.id)]["character"].lower())
                and msg.content != ""
            )

        while True:
            for category in self.games[str(ctx.author.id)]["categories"]:
                e = discord.Embed(
                    title=category,
                    description=f"{self.games[str(ctx.author.id)]['character'].upper()}.....",
                    color=0xFFA500,
                )
                e.set_footer(
                    text=f"Command Invoked by {ctx.author} | Made by: SockYeh#0001",
                    icon_url=ctx.author.avatar_url,
                )
                await ctx.send(embed=e)

                stime = time.time()
                try:
                    answer = await self.bot.wait_for(
                        "message", timeout=total_time, check=check
                    )
                except asyncio.TimeoutError:
                    await ctx.send("Time's up!")
                    break
                self.games[str(ctx.author.id)]["total_time"] = total_time - round(
                    time.time() - stime
                )
                self.games[str(ctx.author.id)]["answers"].append(
                    (category, answer.content)
                )
                if self.games[str(ctx.author.id)]["total_time"] <= 0:
                    await ctx.send("Time's up!")
                    return
                if len(self.games[str(ctx.author.id)]["answers"]) == len(
                    self.games[str(ctx.author.id)]["categories"]
                ):
                    await ctx.send("You're done!")
                    break
            break
        e = discord.Embed(title="Scattergory Results", color=0xFFA500)
        e.set_footer(
            text=f"Command Invoked by {ctx.author} | Made by: SockYeh#0001",
            icon_url=ctx.author.avatar_url,
        )
        for category, answer in self.games[str(ctx.author.id)]["answers"]:
            e.add_field(name=category, value=answer, inline=False)

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Scattegories(bot))
