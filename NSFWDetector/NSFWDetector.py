import discord
import re
import aiohttp
from discord.ext import commands


class NSFWDetector(commands.Cog):
    def __init__(self, bot, **options):
        super().__init__(**options)
        self.bot = bot
        self.DEEPAPI_KEY = "5d136013-1ff0-421d-bc67-4c13cdcdc71c"
        self.DEEPAPI_API_URL = "https://api.deepai.org/api/nsfw-detector"

    async def detect_nudity(self, link):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.DEEPAPI_API_URL, data={'image': link},
                                    headers={'api-key': self.DEEPAPI_KEY}) as response:
                data = await response.json()
                print(data)
                nsfw_score = data['output']['nsfw_score']
                if nsfw_score > 0.75:
                    return True
                else:
                    return False

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(url_regex, message.content)
        links = [link.strip("<>") for link in urls] + [file.url for file in message.attachments]

        for link in links:
            is_nude = await self.detect_nudity(link)
            if is_nude:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.DEEPAPI_API_URL, data={'image': link},
                                            headers={'api-key': self.DEEPAPI_KEY}) as response:
                        data = await response.json()
                        nsfw_score = data['output']['nsfw_score']
                channel = self.bot.get_channel(902574295245541456)
                await channel.send(
                    embed=discord.Embed(title='Detected and deleted potential NSFW image!', colour=discord.Colour.red(),
                                        description=f'**Posted by** : {message.author} `{message.author.id}` \n \n **NSFW Score (Out of 1)**: {nsfw_score} '))
                if message.author.top_role.id in (
                        658770981816500234, 682698693472026749, 663162896158556212, 658770586540965911,
                        699505897654845500,
                        703700908361383967, 674054652882452493):
                    return

                else:
                    await message.channel.send(
                        f"Something is sus, I deleted your image {message.author.mention}. If you feel your image is appropriate please dm me!")
                    await message.delete()

                break


def setup(bot):
    bot.add_cog(NSFWDetector(bot))
