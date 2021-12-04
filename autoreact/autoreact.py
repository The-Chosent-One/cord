import discord
from discord.ext import commands
from discord.utils import get
from typing import Optional
from discord import Embed, Member
from core import checks
from core.models import PermissionLevel


class autoreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)
                       
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def addar(self, ctx, user_id: str, emoji: discord.Emoji):
        emoji1 = str(emoji)
        ar = {"user_id": user_id, "reaction": emoji1}
        await self.coll.insert_one(ar)
        await ctx.send(f"Added reaction {emoji} for {user_id}")

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def removear(self, ctx, user_id: str):
        ar = await self.coll.find_one({"user_id": str(user_id)})
        reaction1 = ar["reaction"]
        await self.coll.delete_one(ar)
        await ctx.send(f"Deleted reaction {reaction1} for {user_id}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        for x in message.mentions:
            uid = await self.coll.find_one({"user_id": str(x.id)})  # getting the user ID if in db then getting reaction
            if not uid:
                return
            reaction1 = uid["reaction"]
            await message.add_reaction(reaction1)
           
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def getars(self,ctx):
        s = ""
        fetchall = self.coll.find({})
        async for x in fetchall:
            convert = x['user_id']
            converted = self.bot.get_user(int(convert))
            s += f"{converted} (`{convert}`) : {x['reaction']} \n"
            
        await ctx.send(s)

def setup(bot):
    bot.add_cog(autoreact(bot))
