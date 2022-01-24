import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel


class Carl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def addtrigger(self, ctx, trigger: str, title: str, description: str,
                         channels: commands.Greedy[discord.TextChannel] = None):
        check = await self.coll.find_one({"trigger": trigger})
        if check:
            await ctx.send("Trigger already exists")
        else:
            if channels is None:
                await self.coll.insert_one(
                    {"trigger": trigger.lower(), "title": title, "description": description, "channel": "None"})
                await ctx.send("Added trigger")
            else:
                chaid = [c.id for c in channels]
                await self.coll.insert_one(
                    {"trigger": trigger.lower(), "title": title, "description": description, "channel": chaid})
                await ctx.send("Added trigger")

    @commands.command(alias=["deltrigger"])
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def deletetrigger(self, ctx, trigger: str):
        check = await self.coll.find_one({"trigger": trigger})
        if check:
            await self.coll.delete_one(check)
            await ctx.send("Deleted trigger")
        else:
            await ctx.send("Trigger does not exist")

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def trigger(self, ctx, trigger: str):
        if trigger is None:
            s = ""
            fetchall = self.coll.find({})
            async for x in fetchall:
                trigger = x["trigger"]
                s += f"{trigger} \n"
                embed = discord.Embed(title="All triggers", description=s, color=0x00ff00)
                await ctx.send(embed=embed)
        else:
            find = await self.coll.find_one({"trigger": trigger})
            if find:
                description = find["description"]
                title = find["title"]
                channel = find["channel"]
                embed = discord.Embed(title=title, description=description, color=0x00ff00)
                for chamention in channel:
                    chamen = self.bot.get_channel(chamention)
                await ctx.send(f"Channels this is allowed in {chamen})
                await ctx.send(embed=embed)
            else:
                await ctx.send("Trigger does not exist, try `??trigger` to see available triggers")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith('??'):
            return
        check = await self.coll.find_one({"trigger": message.content.lower()})
        if not check:
            return
        else:
            channel = check["channel"]
            if channel == 'None':
                title = check["title"]
                description = check["description"]
                embed = discord.Embed(title=title, description=description)
                await message.channel.send(embed=embed)
            else:
                if message.channel.id in channel:
                    title = check["title"]
                    description = check["description"]
                    embed = discord.Embed(title=title, description=description)
                    await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Carl(bot))
