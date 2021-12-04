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
    
    @commands.command()
    @commands.is_owner()
    async def memory(self,ctx):
        await ctx.send(f'RAM memory % used: {psutil.virtual_memory()[2]}')
    
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
