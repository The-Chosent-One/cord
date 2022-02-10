import discord
from discord.ext import commands


class StickyRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    async def update_sticky(self, unique, role: discord.Role):
        await self.coll.find_one_and_update({"unique": unique}, {"$push": {"role_id": role.id}}, upsert=True)

    @commands.command()
    async def addsticky(self, ctx, role: discord.Role):
        """Adds a sticky role to the database"""
        await self.update_sticky("1", role)
        await ctx.send(f"Added {role.name} to the sticky roles")


def setup(bot):
    bot.add_cog(StickyRoles(bot))
