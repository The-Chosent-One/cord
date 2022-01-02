import re
import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

import psutil


class Owners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
				
	@commands.Cog.listener()
	async def on_thread_ready(self,thread,creator,category,initial_message):
		msg = thread.genesis_message
		if initial_message.content in ("hi","hii","hey","heyy","hello",):
			await thread.send(f"Hey! Instead of just saying {initial_message.content}, please state your issue.")

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
		msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
		if msg.content.lower() in ("y", "yes"):
			await ctx.send("Ugh bye now")
			await self.bot.close()
		else:
			await ctx.send("Okay bro wyd here then?")

def setup(bot):
	bot.add_cog(Owners(bot))
