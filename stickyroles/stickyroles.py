from discord.ext import commands
import discord


class StickyRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    async def add_sticky(self, unique, role: discord.Role):
        await self.coll.find_one_and_update({"unique": unique}, {"$push": {"role_id": role.id}}, upsert=True)

    async def remove_sticky(self, unique, role: discord.Role):
        await self.coll.find_one_and_update({"unique": unique}, {"$pull": {"role_id": role.id}})

    @commands.command()
    async def addsticky(self, ctx, role: discord.Role):
        """Adds a sticky role to the database"""
        await self.add_sticky("1", role)
        await ctx.send(f"Added {role.name} to the sticky roles")

    @commands.command()
    async def removesticky(self, ctx, role: discord.Role):
        """Removes a sticky role from the database"""
        await self.remove_sticky("1", role)
        await ctx.send(f"Removed {role.name} from the sticky roles")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("someone left")
        s = []
        for role in member.roles:
            check = await self.coll.find_one({"role_id": role.id})
            if not check:
                return
            s.append(role.id)
        print("trying to insert ok?")
        await self.coll.insert_one({"member_id": member.id, "role_id": s})
        print("inserted tadaa")

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        if self.coll.find_one({"member_id": member.id}) is not None:
            for role in self.coll.find_one({"member_id": member.id})["role_id"]:
                sticky = ctx.guild.get_role(role)
                await member.add_roles(sticky)


def setup(bot):
    bot.add_cog(StickyRoles(bot))
