import discord
from discord.ext import commands
from modules.football_api import FootballAPI
from datetime import datetime

class Football(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command()
    async def nextgame(self, ctx):
        api = FootballAPI()
        data = api.next_game()
        referee = data["response"][0]["fixture"]["referee"]
        date = data["response"][0]["fixture"]["date"]
        venue_id = data["response"][0]["fixture"]["venue"]["id"]
        venue = data["response"][0]["fixture"]["venue"]["name"]
        league = data["response"][0]["league"]["logo"]
        home = data["response"][0]["teams"]["home"]["name"]
        away = data["response"][0]["teams"]["away"]["name"]
        venue_data = api.get_venue(venue_id)
        venue_image = venue_data["response"][0]["image"]
        adress = venue_data["response"][0]["address"]
        city = venue_data["response"][0]["city"]
        capacity = venue_data["response"][0]["capacity"]
        surface = venue_data["response"][0]["surface"]

        embed = discord.Embed(title=f'__**{home} vs {away}**__',
                              description=f'Date: {date}\n Referee: {referee}\n Venue: {venue}',
                              color=discord.Color.dark_red(),
                              timestamp=datetime.now())

        embed.set_image(url=venue_image)
        embed.set_thumbnail(url=league)
        embed.set_footer(text=f'capacity: {capacity}')
        await ctx.send(embed=embed)

# syncs cog to bot
async def setup(bot):
    await bot.add_cog(Football(bot))