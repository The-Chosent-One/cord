import discord
import asyncio
from discord.ext import commands


class bfping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def gaw(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&672889430171713538> {messages}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def partner(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&793454145897758742> {messages}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def heist(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&684987530118299678> {messages}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ev(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&684552219344764934> {messages}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def friendly(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&750908803704160268> {messages}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def sale(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&724438185601663077> {messages}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lot(self, ctx, *, message="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f' <@&732949595633614938> {message}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def maf(self, ctx, *, messages="^_^"):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@&713898461606707273> {messages}')

    @commands.command()
    @commands.has_any_role(682698693472026749, 663162896158556212, 658770981816500234, 855877108055015465)
    async def eventsponsor(self, ctx, member: discord.Member):
        role = ctx.guild.get_role(787572079573598220)
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send("The role has been added")
            await asyncio.sleep(300)
            await member.remove_roles(role)
            await ctx.send("The role has expired since 5 minutes are up")

def setup(bot):
    bot.add_cog(bfping(bot))
