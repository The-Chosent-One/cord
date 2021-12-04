import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import json
import re
import asyncio
from re import match
from datetime import datetime, timedelta

time_units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}


class extras(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def _error(self, msg):
		return discord.Embed(description="** " + msg + " **",
							 color=discord.Color.red())

  def to_seconds(self, s):
      return int(timedelta(**{
          time_units.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
          for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', s, flags=re.I)
      }).total_seconds()) 
  
  @commands.command()
  async def timer(self, ctx, seconds):
      try:
          text = (seconds)
          in_seconds = {'h': 60 * 60, 'm': 60, 's': 1, ' ': 1}
          seconds = sum(int(num) * in_seconds[weight if weight else 's'] for num, weight in
                        re.findall(r'(\d+)\s?(m|s|h)?', text))
          if seconds > 21600:
              await ctx.message.reply("I don't think I want you to go over 6h right now")
              raise BaseException
          if seconds < 0:
              await ctx.message.reply("I don't think you want to do negatives")
              raise BaseException
          message = await ctx.send(f"Timer: {seconds}")
          while True:
              seconds -= 5
              if seconds < 0:
                  await message.edit(content="Ended!")
                  break
              await message.edit(content=f"Timer: {seconds}")
              await asyncio.sleep(5)
          await ctx.message.reply(f"{ctx.author.mention}, Your countdown has ended!")
      except ValueError:
          await ctx.message.reply('You must enter a number!')
  
	@commands.command()
	@checks.has_permissions(PermissionLevel.MODERATOR)
	async def raw(self, ctx, msg: int = None):
		if msg is None:
			return await ctx.send(embed=self._error(msg="Please provide a message ID."))

		try:
			msg = await ctx.fetch_message(msg)
		except commands.CommandInvokeError:
			return await ctx.send(embed=self._error(msg="Invalid message ID provided."))

		if not msg.embeds:
			return await ctx.send(embed=self._error(msg="Please provide the message ID of an embedded message."))
		await ctx.send(f"``` {msg.embeds[0].description} ```")

	@commands.command()
	@checks.thread_only()
	async def id(self, ctx):
		"""Returns the Recipient's ID"""
		await ctx.send(ctx.thread.id)
		
def setup(bot):
	bot.add_cog(extras(bot))
