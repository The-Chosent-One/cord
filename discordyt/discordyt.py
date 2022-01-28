from discord.ext import commands
from discord_together import DiscordTogether


class DiscordYT(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.discord_TC: DiscordTogether = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.discord_TC = await DiscordTogether(self.bot)

    @commands.command()
    @commands.is_owner()
    async def startyt(self, ctx):
        link = await self.discord_TC.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click the blue link!\n{link}")


def setup(client):
    client.add_cog(DiscordYT(client))
