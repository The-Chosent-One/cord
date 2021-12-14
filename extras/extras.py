import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import re
import asyncio
from datetime import timedelta

time_units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}


class Extras(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@staticmethod
	def _error(msg):
		return discord.Embed(description="** " + msg + " **", color=discord.Color.red())

	@staticmethod
	def to_seconds(s):
		return int(timedelta(**{
			time_units.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
			for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', s, flags=re.I)
		}).total_seconds())

	@commands.Cog.listener('on_message')
	async def deleteall(self, message: discord.Message):
		if message.channel.id == 882758609921015839:
			await message.delete()

	@commands.command()
	@checks.has_permissions(PermissionLevel.MODERATOR)
	async def inrole(self, ctx, role1: discord.Role, role2: discord.Role):
		first = role1.members

		second = role2.members
		firstlen = len(role1.members)
		secondlen = len(role2.members)
		Unique = len(list(set(first + second)))
		await ctx.send(embed=discord.Embed(title='Here is the requested information!', colour=discord.Colour.green(),
										   description=f'**Users in {role1}**: {firstlen} \n**Users in {role2}**: {secondlen} \n **Unique in {role1} and {role2}**: {Unique}'))

	@commands.command()
	@checks.thread_only()
	async def unmute(self, ctx):
		member = ctx.guild.get_member(ctx.thread.id)

		role = discord.utils.get(member.guild.roles, name='Muted')
		if role in member.roles:
			await member.remove_roles(role, reason=f'Unmute requested by {str(ctx.author.id)}')
			await ctx.channel.send("Unmuted")
		else:
			await ctx.channel.send("They arent muted")

	@commands.command()
	async def whois(self, ctx, member: discord.Member = None):
		if member == None:
			member = ctx.message.author

		roles = [role for role in member.roles]
		embed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"Requested by {ctx.author}")
		embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
						inline=True)
		embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
						inline=True)
		embed.add_field(name="​", value="​", inline=False)
		embed.add_field(name="ID:", value=member.id, inline=True)
		embed.add_field(name="Display Name:", value=member.display_name, inline=True)
		embed.add_field(name="​", value="​", inline=False)
		embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	async def timer(self, ctx, seconds):
		try:
			text = (seconds)
			seconds = sum(
				int(num) * {'h': 60 * 60, 'm': 60, 's': 1, ' ': 1}[weight if weight else 's'] for num, weight in
				re.findall(r'(\d+)\s?(m|s|h)?', text))

			if not 4 < seconds < 21600:
				await ctx.message.reply("Please keep the time between 5 seconds to 6 hours")
				raise BaseException

			message = await ctx.send(f"Timer: {seconds}")

			while True:
				seconds -= 5
				if seconds < 0:
					await message.edit(content="Ended!")
					return await ctx.message.reply(f"{ctx.author.mention}, Your countdown has ended!")
				await message.edit(content=f"Timer: {seconds}")
				await asyncio.sleep(5)
		except ValueError:
			await ctx.message.reply('You must enter a number!')

	@staticmethod
	@commands.command()
	@checks.has_permissions(PermissionLevel.MODERATOR)
	async def raw(ctx, msg: discord.Message = None):
		await ctx.send(f"``` {msg.embeds[0].description} ```" if msg and msg.embeds else "Please provide a valid message link / ID")

	@commands.command()
	@checks.thread_only()
	async def id(self, ctx):
		"""Returns the Recipient's ID"""
		await ctx.send(ctx.thread.id)


def setup(bot):
	bot.add_cog(Extras(bot))
