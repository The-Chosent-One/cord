import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
from core.thread import Thread

import psutil


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):
        msg = thread.genesis_message
        if initial_message.content in ("hi", "hii", "hey", "heyy", "hello",):
            msg = "Hey! Instead of just saying hi, please state your issue."
            await thread.reply(msg)

    @commands.command()
    @commands.is_owner()
    async def usage(self, ctx):
        await ctx.send(f'RAM memory % used: {psutil.virtual_memory()[2]}')
        await ctx.send(f'The CPU % usage is: {psutil.cpu_percent(4)}')

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.Member, *, message):
        await user.send(f'Message from Bot Owner: {message}')
        await ctx.channel.send("Sent the message")

    @commands.command(aliases=['logoff'])
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.send(f"Reboot the bot (Might crash)?? (y/n)")
        msg = await self.bot.wait_for("message",
                                      check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
        if msg.content.lower() in ("y", "yes"):
            await ctx.send("Ugh bye now")
            await self.bot.close()
        else:
            await ctx.send("Okay bro wyd here then?")

    @commands.command(aliases=['ed'])
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def enabledisable(self, ctx):
        embed = discord.Embed(title="Enables/Disables",
                              description = "`??disableautoban | ??enableautoban` \n \n `??disabledecancer | ??enabledecancer` \n \n `??disableextras | ??enableextras` \n \n `??disablelock | ??enablelock` \n \n `??disableping | ??enableping` \n \n `??disableshortcut | ??enableshortcut` \n \n `??disablesnipe | ??enablesnipe` \n \n `??disablesuggest | ??enablesuggest` \n \n `??disabletyperacer | ??enabletyperacer` \n \n `??disablear | ??enablear` \n \n `??disablecarl | ??enablecarl`")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def offline(self, ctx):
        """
        get all offline bots in a server
        """
        guild = ctx.guild
        offline_bots = []
        for member in guild.members:
            if not member.bot:
                continue
            if not member.status == discord.Status.offline:
                continue
            offline_bots.append(member)
        if not offline_bots:
            await ctx.send("No offline bots found")
            return
        await ctx.send(f"Found {len(offline_bots)} offline bots")
        for bot in offline_bots:
            await ctx.send(f"{bot.name}#{bot.discriminator}")

def setup(bot):
    bot.add_cog(Owners(bot))
