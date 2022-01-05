import discord
import pathlib
from pathlib import Path
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import re
import asyncio
import datetime
from datetime import timedelta

time_units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}

this_file_directory = Path(__file__).parent.resolve()
other_file = this_file_directory / "scammer.txt"

with open(other_file, "r+") as file:
	scammer = [scammer.strip().lower() for scammer in file.readlines()]

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
			
	@commands.Cog.listener('on_message')
	async def scammeralert(self, message: discord.Message):
		role = message.guild.get_role(824549659988197386)
		if message.author.bot:
			return
		if role in message.author.roles:
			if any(word in message.content.lower() for word in scammer):
				if message.mentions:	
					embed=discord.Embed(title=f":warning: {message.author} is a scammer  :warning: ", description="Hey, thought you should know the user you are engaging in a deal with is a **scammer** and has unpaid dues. Proceed with caution and/or use a middle man from <#756004818866405376> ", color=0xff0000)
					embed.set_footer(text="- The Farm")
					await message.channel.send(embed=embed)
		else:
			members = [m.name for m in message.mentions if role in m.roles]
			if members:
				if any(word in message.content.lower() for word in scammer):
					if len(members) > 1:						
						embed=discord.Embed(title=f":warning:  {', '.join(members)} are scammers  :warning: ", description="Hey, thought you should know the user you are engaging in a deal with is a **scammer** and has unpaid dues. Proceed with caution and/or use a middle man from <#756004818866405376> ", color=0xff0000)
						embed.set_footer(text="- The Farm")
						await message.channel.send(embed=embed)
					elif len(members) == 1:
						embed=discord.Embed(title=f":warning:  {' '.join(members)} is a scammer  :warning: ", description="Hey, thought you should know the user you are engaging in a deal with is a **scammer** and has unpaid dues. Proceed with caution and/or use a middle man from <#756004818866405376> ", color=0xff0000)
						embed.set_footer(text="- The Farm")
						await message.channel.send(embed=embed)
					
	@commands.command()
	@commands.has_any_role(790290355631292467,855877108055015465,723035638357819432,814004142796046408,682698693472026749,658770981816500234,663162896158556212,658770586540965911)
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
	@commands.has_any_role(790290355631292467,855877108055015465,723035638357819432,814004142796046408,682698693472026749,658770981816500234,663162896158556212,658770586540965911)
	async def whois(self, ctx, member: discord.Member = None):
		if member == None:
			member = ctx.message.author

		roles = [role for role in member.roles]
		embed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)
		embed.set_author(name=member.name, icon_url=member.avatar_url)
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

	@commands.command()
	@checks.has_permissions(PermissionLevel.MODERATOR)
	async def raw(self, ctx, msg: discord.Message):
		if not msg.embeds:
			return await ctx.send(embed=discord.Embed(title="Please provide the message ID of an embedded message."))

		await ctx.send(f"``` {msg.embeds[0].description} ```")


	@commands.command()
	@checks.thread_only()
	async def id(self, ctx):
		"""Returns the Recipient's ID"""
		await ctx.send(ctx.thread.id)
		
	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if str(before.activity) == str(after.activity):
			return

		guild = self.bot.get_guild(645753561329696785)

		if after in guild.members:
			if re.search(r'\bdiscord.gg/dank\b', str(after.activity)) or re.search(r'\b.gg/dank\b', str(after.activity)) or re.search(r'\bgg/dank\b', str(after.activity)):
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
	@checks.has_permission(PermissionLevel.MODERATOR)
	async def stats(self,ctx, member: discord.Member):
		if member == None:
			member = ctx.message.author
			
		embed=discord.Embed(title=ctx.bot.user.name Statistics", color=0xa01df7,timestamp=ctx.message.created_at)
		embed.set_author(name=member.name, icon_url=member.avatar_url)
		embed.add_field(name="​", value="​", inline=False)
		embed.add_field(name="Logs closed (last 7 days)", value="{value}", inline=True)
		embed.add_field(name="Logs closed (last 30 days)", value="{value}", inline=True)
		embed.add_field(name="Logs closed (all time)", value="{value}", inline=True)
		embed.add_field(name="​", value="​", inline=False)
		embed.add_field(name="Logs replied (last 7 days)", value="{value}", inline=True)
		embed.add_field(name="Logs replied (last 30 days)", value="{value}", inline=True)
		embed.add_field(name="Logs replied (all time)", value="{value}", inline=True)
		embed.set_footer(text=f"ID {member.id}")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Extras(bot))
