import discord
import asyncio

from discord import Color
from discord.utils import get
from discord.ext import commands
from dislash import slash_commands, ActionRow, Button, ButtonStyle

class selfbutton(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		if not hasattr(self.bot, "inter_client"):
			slash_commands.InteractionClient(self.bot)

	@commands.command()
	async def selfroles(self,ctx):
		row_of_buttons1 = ActionRow(
			Button(style=ButtonStyle.green,label="G01",custom_id="green1"),
			Button(style=ButtonStyle.green,label="G02",custom_id = "green2"),
			Button(style=ButtonStyle.green, label="G03", custom_id="green3"),
			Button(style=ButtonStyle.green, label="G04", custom_id="green4"),
			Button(style=ButtonStyle.green, label="G05", custom_id="green5"),
		)
		row_of_buttons2 = ActionRow(
			Button(style=ButtonStyle.green,label="G06",custom_id="green6"),
			Button(style=ButtonStyle.green,label="G07",custom_id = "green7"),
			Button(style=ButtonStyle.green, label="G08", custom_id="green8"),
			Button(style=ButtonStyle.green, label="G09", custom_id="green9"),
			Button(style=ButtonStyle.green, label="G10", custom_id="green10"),
		)
		row_of_buttons3 = ActionRow(
			Button(style=ButtonStyle.green,label="G11",custom_id="green11"),
			Button(style=ButtonStyle.green,label="G12",custom_id = "green12"),
			Button(style=ButtonStyle.green, label="G13", custom_id="green13"),
			Button(style=ButtonStyle.green, label="G14", custom_id="green14"),
			Button(style=ButtonStyle.green, label="G15", custom_id="green15"),
		)
		row_of_buttons4 = ActionRow(
			Button(style=ButtonStyle.green,label="G16",custom_id="green16"),
			Button(style=ButtonStyle.green,label="G17",custom_id = "green17"),
			Button(style=ButtonStyle.green, label="G18", custom_id="green18"),
			Button(style=ButtonStyle.green, label="G19", custom_id="green19"),
			Button(style=ButtonStyle.green, label="G20", custom_id="green20"),
		)
		row_of_buttons5 = ActionRow(
			Button(style=ButtonStyle.green,label="G21",custom_id="green21"),
			Button(style=ButtonStyle.green,label="G22",custom_id = "green22"),
			Button(style=ButtonStyle.green, label="G23", custom_id="green23"),
			Button(style=ButtonStyle.green, label="G24", custom_id="green24"),
			Button(style=ButtonStyle.green, label="G25", custom_id="green25"),
		)
		embed = discord.Embed(Title="Example of buttons",description="Do you like this?",color=Color.green())
		msg = await ctx.send(embed=embed, components=[row_of_buttons1,row_of_buttons2,row_of_buttons3,row_of_buttons4,row_of_buttons5])

		def check(inter):
			return inter.author == ctx.author
		try:
			inter = await msg.wait_for_button_click(check=check)

		except asyncio.exceptions.TimeoutError:
			tembed= discord.Embed(Title="Timeout!",description="You didnt choose a color in time!",color=Color.red())
			await msg.edit(embed=tembed,components=[row_of_buttons1,row_of_buttons2,row_of_buttons3,row_of_buttons4,row_of_buttons5],disabled = True)
			await asyncio.sleep(3)
			await msg.delete
			return
		if inter.component.custom_id == "green1":
			member = ctx.author
			mroles = discord.utils.find(lambda r: r.name == "ButtonsTest",ctx.message.guild.roles)
			roles = get(member.guild.roles,name="ButtonsTest")
			if mroles in member.roles:
				await inter.respond(f"You already tested this so I didnt add any role",ephemeral = True)
			else:
				await member.add_roles(roles)
				await inter.respond(f"Thank you for clicking G1 as a test adding `ButtonsTest` role",ephemeral = True)
		else:
			await inter.respond(f"Sorry but other roles are not yet ready", ephemeral = True)
		

def setup(bot):
	bot.add_cog(selfbutton(bot))
