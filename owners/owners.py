import discord
from discord.ext import commands
from discord.utils import get
from typing import Optional
from discord import Embed, Member
from core import checks
from core.models import PermissionLevel
import asyncio
import psutil


class owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
    
    @commands.Cog.listener()
    async def on_member_update(self,before, after):       
        guild = self.bot.get_guild(645753561329696785)
        member = after
        if after in guild.members:
            if 'discord.gg/dank' in str(after.activity):
                role = guild.get_role(916271809333166101)
                if role in after.roles:
                    return
                await after.add_roles(role)
            else:
                role = guild.get_role(916271809333166101)
                if role not in after.roles:
                    return
                await after.remove_roles(role)
    
    @commands.command()
    @commands.is_owner()
    async def ussage(self,ctx):
        await ctx.send(f'RAM memory % used: {psutil.virtual_memory()[2]}')
        await ctx.send(f'The CPU % usage is: {psutil.cpu_percent(4)}')
    
    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.Member, *, message):
        await user.send(f'Message from Bot Owner: {message}')
        await ctx.channel.send("Sent the message")
        
    @commands.command(aliases=['restart'])
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def reboot(self, ctx):
        await ctx.send(f"Reboot the bot?? (y/n)")
        msg = await self.bot.wait_for("message",
                                      check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
        if msg.content in ("y", "yes"):
            await ctx.send("Ugh bye now")
            await self.bot.logout()
        else:
            await ctx.send("Okay bro wyd here then?")
            

def setup(bot):
    bot.add_cog(owners(bot))
