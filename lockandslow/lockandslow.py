import discord
import re
from re import match
from discord.ext import commands
from datetime import timedelta


class lockandslow(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Lock the server
    @commands.command()
    @commands.has_any_role(682698693472026749, 658770981816500234, 663162896158556212, 658770586540965911,
                           814004142796046408, 855877108055015465)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        if channel.overwrites_for(ctx.guild.default_role).send_messages == None or channel.overwrites_for(
                ctx.guild.default_role).send_messages == True:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send(f"🔒 Locked `{channel}`")
        else:
            await ctx.send(f"🔒 Looks like {channel} is already locked")

    @commands.command()
    @commands.has_any_role(682698693472026749, 658770981816500234, 663162896158556212, 658770586540965911,
                           814004142796046408, 855877108055015465)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        if channel.overwrites_for(ctx.guild.default_role).send_messages == False:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await ctx.send(f"🔓 Unlocked `{channel}`")
        else:
            await ctx.send(f"🔓 Looks like {channel} is already locked")
            
    def to_seconds(self, s):
        return int(timedelta(**{
            time_units.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
            for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', s, flags=re.I)
        }).total_seconds())

    @commands.command(aliases=['slowmode', 'slow'])
    @commands.has_permissions(manage_messages=True)
    async def sm(self, ctx, delay):
        slomo_embed = discord.Embed(
            title=f" A slowmode of {delay} has been activated by a moderator.",
            color=0x363940, timestamp=ctx.message.created_at)
        slomo_embed.set_footer(text=f'Applied by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.message.delete()
        await ctx.channel.edit(slowmode_delay=self.to_seconds(delay))
        await ctx.send(content=None, embed=slomo_embed)

    # Show current slowmode
    @commands.command()
    async def slownow(self, ctx):
        await ctx.send(f' The current slowmode in the channel is {ctx.channel.slowmode_delay} seconds ')



def setup(bot):
    bot.add_cog(lockandslow(bot))
