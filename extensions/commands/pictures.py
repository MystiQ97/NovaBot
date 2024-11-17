import random
import discord
from datetime import datetime
from discord.ext import commands
from modules import json_handler as json
from modules import API



class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    # Generate a random number by how many pictures there is, then returns path to that picture,
    # for now it needs to be updated manually when more pictures are added.
    def fetch_nova(self):
        number = random.randint(1, 80)
        path = f'./media/nova/{number}.jpg'
        filehandler = json.file_handler(f'./json/{number}.json')
        if not filehandler.exists():
            filehandler.create_json({"likes":0})
        return path, number

    def picture_embed(self, filepath):
        file = discord.File(filepath[0], filename = f'{filepath[1]}.jpg')
        embed = discord.Embed(title = f'ID: {filepath[1]}', color = discord.Color.pink(), timestamp = datetime.now())
        embed.set_image(url = f'attachment://{filepath[1]}.jpg')

        filehandler = json.file_handler(f'./json/{filepath[1]}.json')
        likes = filehandler.get_value('likes')

        embed.set_footer(text = f'\u2764\ufe0f: {likes}')
        return file, embed

    @commands.command()
    async def nova(self, ctx):
        filepath = self.fetch_nova()
        embed = self.picture_embed(filepath)

        message = await ctx.send(file = embed[0], embed=embed[1])

        await message.add_reaction("❤️")

        # Add a listener to capture reactions on this message
        def check(reaction, user):
            return (
                    reaction.message.id == message.id and
                    str(reaction.emoji) == "❤️" and
                    not user.bot
            )

        # Keep listening and updating the like count each time someone reacts
        while True:
            try:
                # Wait for a new reaction (with a timeout to prevent infinite loops)
                reaction, user = await self.bot.wait_for("reaction_add", timeout=300.0, check=check)

                # Increment the likes count in JSON
                filehandler = json.file_handler(f'./json/{filepath[1]}.json')
                current_likes = filehandler.get_value('likes')
                new_likes = current_likes + 1
                filehandler.update_json({"likes" : new_likes})

                # Update the embed with the new likes count
                new_embed = message.embeds[0]
                new_embed.set_footer(text=f'\u2764\ufe0f: {new_likes}')
                new_embed.set_image(url=new_embed.image.url)
                await message.edit(embed=new_embed, attachments=[])

            except TimeoutError:
                # Stop listening after a timeout
                break

    @commands.command()
    async def pokemon(self, ctx, pokemon):
        pokemon = str.lower(pokemon)
        data = API.get_data(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
        embed = discord.Embed(title = f'Pokemon: {pokemon}', color = discord.Color.pink())
        sprite = data['sprites']
        sprite = sprite['front_default']
        print(sprite)
        embed.set_image(url = sprite)
        await ctx.send(embed=embed)

# syncs cog to bot
async def setup(bot):
    await bot.add_cog(Pictures(bot))
