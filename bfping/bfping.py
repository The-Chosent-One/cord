import discord
import asyncio
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

time_units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}

class BFPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def pings(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You are probably looking for `??pings config`")

    @pings.command(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You are probably looking for `??pings config enable`/`??pings config disable`")

    @config.command(name="enable")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def config_enable(self, ctx, command, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        if command == "gaw":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'gaw_channel': channel.id}}, upsert=True)
            await ctx.send(f"Enabled gaw in {channel.mention}")
        elif command == "partner":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'partner_channel': channel.id}},
                                                upsert=True)
            await ctx.send(f"Enabled partner in {channel.mention}")
        elif command == "heist":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'heist_channel': channel.id}},
                                                upsert=True)
            await ctx.send(f"Enabled heist in {channel.mention}")
        elif command == "ev":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'ev_channel': channel.id}}, upsert=True)
            await ctx.send(f"Enabled ev in {channel.mention}")
        elif command == "friendly":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'friendly_channel': channel.id}},
                                                upsert=True)
            await ctx.send(f"Enabled friendly in {channel.mention}")
        elif command == "lot":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'lot_channel': channel.id}}, upsert=True)
            await ctx.send(f"Enabled lot in {channel.mention}")
        elif command == "maf":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$push': {'maf_channel': channel.id}}, upsert=True)
            await ctx.send(f"Enabled maf in {channel.mention}")
        else:
            await ctx.send("Invalid command")

    @config.command(name="disable")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def config_disable(self, ctx, command, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        if command == "gaw":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'gaw_channel': channel.id}})
            await ctx.send(f"Disabled gaw in {channel.mention}")
        elif command == "partner":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'partner_channel': channel.id}})
            await ctx.send(f"Disabled partner in {channel.mention}")
        elif command == "heist":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'heist_channel': channel.id}})
            await ctx.send(f"Disabled heist in {channel.mention}")
        elif command == "ev":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'ev_channel': channel.id}})
            await ctx.send(f"Disabled ev in {channel.mention}")
        elif command == "friendly":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'friendly_channel': channel.id}})
            await ctx.send(f"Disabled friendly in {channel.mention}")
        elif command == "lot":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'lot_channel': channel.id}})
            await ctx.send(f"Disabled lot in {channel.mention}")
        elif command == "maf":
            await self.coll.find_one_and_update({'Cog': 'BFPing'}, {'$pull': {'maf_channel': channel.id}})
            await ctx.send(f"Disabled maf in {channel.mention}")
        else:
            await ctx.send("Invalid command")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def gaw(self, ctx, *, messages="^_^"):
        c = ""
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            gwm = ctx.guild.get_role(855877108055015465)
            await ctx.author.remove_roles(gwm)
            return await ctx.send("Pretty sure you don't want to do that man")
        find = await self.coll.find_one({'Cog': 'BFPing'})
        channel = find[gaw_channel]
        for chaid in channel:
            chai = self.bot.get_channel(chaid)
            c += f"{chai.mention}, "
        if ctx.channel.id in channel:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&672889430171713538> {messages}')
        else:

            await ctx.send(f'You can only use this command in {c}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def partner(self, ctx, *, messages="^_^"):
        c = ""
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            partner = ctx.guild.get_role(790290355631292467)
            await ctx.author.remove_roles(partner)
            return await ctx.send("Pretty sure you don't want to do that man")
        find = await self.coll.find_one({'Cog': 'BFPing'})
        channel = find[partner_channel]
        for chaid in channel

        if ctx.channel.id == 688431055489073180:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&793454145897758742> {messages}')
        else:
            await ctx.send('You can only use this command in <#688431055489073180>')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def heist(self, ctx, *, messages="^_^"):
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            heist = ctx.guild.get_role(723035638357819432)
            await ctx.author.remove_roles(heist)
            return await ctx.send("Pretty sure you don't want to do that man")
        if ctx.channel.id == 688581086078304260:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&684987530118299678> {messages}')
        else:
            await ctx.send('You can only use this command in <#688581086078304260>')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ev(self, ctx, *, messages="^_^"):
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            gwm = ctx.guild.get_role(855877108055015465)
            await ctx.author.remove_roles(gwm)
            return await ctx.send("Pretty sure you don't want to do that man")
        if ctx.channel.id == 709088851234258944:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&684552219344764934> {messages}')
        else:
            await ctx.send('You can only use this command in <#709088851234258944>')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def friendly(self, ctx, *, messages="^_^"):
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            gwm = ctx.guild.get_role(855877108055015465)
            await ctx.author.remove_roles(gwm)
            return await ctx.send("Pretty sure you don't want to do that man")
        if ctx.channel.id == 709088851234258944:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&750908803704160268> {messages}')
        else:
            await ctx.send('You can only use this command in <#709088851234258944>')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lot(self, ctx, *, message="^_^"):
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            gwm = ctx.guild.get_role(855877108055015465)
            await ctx.author.remove_roles(gwm)
            return await ctx.send("Pretty sure you don't want to do that man")
        if ctx.channel.id == 732604674108030987:
            await ctx.channel.purge(limit=1)
            await ctx.send(f' <@&732949595633614938> {message}')
        else:
            await ctx.send('You can only use this command in <#732604674108030987>')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def maf(self, ctx, *, messages="^_^"):
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
            gwm = ctx.guild.get_role(855877108055015465)
            await ctx.author.remove_roles(gwm)
            return await ctx.send("Pretty sure you don't want to do that man")
        if ctx.channel.id == 756566417456889965:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&713898461606707273> {messages}')
        else:
            await ctx.send('You can only use this command in <#756566417456889965>')

    @staticmethod
    def to_seconds(s):
        return int(timedelta(**{
            time_units.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
            for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', s, flags=re.I)
        }).total_seconds())

    @commands.command()
    @commands.has_any_role(682698693472026749, 663162896158556212, 658770981816500234, 855877108055015465)
    async def esponsor(self, ctx, member: discord.Member, seconds):
        try:
            text = seconds
            seconds = sum(
                int(num) * {'h': 60 * 60, 'm': 60, 's': 1, ' ': 1}[weight if weight else 's'] for num, weight in
                re.findall(r'(\d+)\s?([msh])?', text))

            if not 60 < seconds < 3600:
                return await ctx.message.reply("Please keep the time between 1 minute and 1 hour.")

        role = ctx.guild.get_role(787572079573598220)
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send("The role has been added")
            await asyncio.sleep(time)
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"The Event Sponsor role has has been removed from {member.mention}")
        else:
            await member.remove_roles(role)
            await ctx.send("The role has been removed from them!")


def setup(bot):
    bot.add_cog(BFPing(bot))
