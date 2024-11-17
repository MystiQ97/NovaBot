import discord
from discord.ext import commands

class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


async def setup(bot):
    await bot.add_cog(TestCommands(bot))