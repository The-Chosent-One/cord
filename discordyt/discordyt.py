import discord
from discord.ext import commands
from discord_together import DiscordTogether

class discordyt(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.togetherControl = DiscordTogether(client)
        
    
    @commands.command()
    @commands.is_owner()
    async def startyt(self, ctx):
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click the blue link!\n{link}")

def setup(client):
    client.add_cog(discordyt(client))
