import logging
import discord
import motor.motor_asyncio
import os

from discord.ext import commands

class NovaBot(commands.Bot):
    def __init__(self):
        # Configure intents
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.messages = True
        intents.presences = True

        #Initialize the settings
        super().__init__(
            command_prefix = "!",
            case_insensitive = True,
            strip_after_prefix = True,
            intents = intents,
            status = discord.Status.online,
            activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
        )

        self.discord_token = os.getenv("NovaBotToken")
        self.mongo_client = None
        self.db = None
        self.bot_extensions = ["test"]

        @self.event
        async def on_ready():
            print(f'Logged in as {self.user} ID: {self.user.id}')
            print("-------")

            await self.check_guild_collections()

    async def setup_hook(self):
        # MongoDB setup
        print("setting up hook to database...")
        mongo_uri = os.getenv("MongoUri")
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.mongo_client["NovaBase"]

        print("Loading extensions...")
        for extension in self.bot_extensions:
            await self.load_extension(extension)

    async def check_guild_collections(self):
        collections = await self.db.list_collection_names()
        print("Checking guilds...")
        for guild in self.guilds:

            if str(guild.id) not in collections:
                await self.db.create_collection(str(guild.id))
                print(f'Added {str(guild.id)} to database')
            else:
                print(f'Skipped {str(guild.id)} in database')

def main():

    bot = NovaBot()
    bot.run(token = bot.discord_token, log_level = logging.INFO )

if __name__ == "__main__":
    main()


