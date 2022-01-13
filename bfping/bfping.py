import discord
import asyncio
from discord.ext import commands

class bfping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def gaw(self, ctx, *, messages="^_^"):
        if ctx.message.raw_role_mentions or '@everyone' in ctx.message.content or '@here' in ctx.message.content:
             await ctx.send("Pretty sure you dont want to do that man")
        if ctx.channel.id == 658779198688722944:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&672889430171713538> {messages}')
        else:
            await ctx.send('You can only use this command in <#658779198688722944>')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def partner(self, ctx, *, messages="^_^"):
        if ctx.channel.id == 688431055489073180:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&793454145897758742> {messages}')
        else:
            await ctx.send('You can only use this command in <#688431055489073180>')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def heist(self, ctx, *, messages="^_^"):
        if ctx.channel.id == 688581086078304260:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&684987530118299678> {messages}')
        else:
            await ctx.send('You can only use this command in <#688581086078304260>')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ev(self, ctx, *, messages="^_^"):
        if ctx.channel.id == 709088851234258944:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&684552219344764934> {messages}')
        else:
            await ctx.send('You can only use this command in <#709088851234258944>')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def friendly(self, ctx, *, messages="^_^"):
        if ctx.channel.id == 709088851234258944:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&750908803704160268> {messages}')
        else:
            await ctx.send('You can only use this command in <#709088851234258944>')
               
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lot(self, ctx, *, message="^_^"):
        if ctx.channel.id == 732604674108030987:
            await ctx.channel.purge(limit=1)
            await ctx.send(f' <@&732949595633614938> {message}')
        else:
            await ctx.send('You can only use this command in <#732604674108030987>')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def maf(self, ctx, *, messages="^_^"):
        if ctx.channel.id == 756566417456889965:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@&713898461606707273> {messages}')
        else:
            await ctx.send('You can only use this command in <#756566417456889965>')
        
    @commands.command()
    @commands.has_any_role(682698693472026749, 663162896158556212, 658770981816500234, 855877108055015465)
    async def esponsor(self, ctx, member: discord.Member):
        role = ctx.guild.get_role(787572079573598220)
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send("The role has been added")
            await asyncio.sleep(300)
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"The Event Sponsor role has has been removed from {member.mention}")
        else:
            await member.remove_roles(role)
            await ctx.send("The role has been removed from them!")
            
def setup(bot):
    bot.add_cog(bfping(bot))
