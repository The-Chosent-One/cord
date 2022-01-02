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
	async def sos(self,ctx, mem1: discord.Member, mem2: discord.Member):
		SOS = ActionRow(
			Button(style=ButtonStyle.green,label="Split",custom_id="split"),
			Button(style=ButtonStyle.red,label="Steal",custom_id = "steal"),
		)
		
		embed = discord.Embed(Title="Split or Steal?",description="ollla la oolaalala",color=Color.green())
		msg = await ctx.send(embed=embed, components=[SOS])
		def check(inter):
			return inter.author == ctx.author
		try:
			inter = await msg.wait_for_button_click(check=check)

		except asyncio.exceptions.TimeoutError:
			tembed= discord.Embed(Title="Timeout!",description="You didnt choose a color in time!",color=0x4ed0a4)
			await msg.edit(embed=tembed,components=[SOS],disabled = True)
			await asyncio.sleep(3)
			await msg.delete
			return
		if inter.component.custom_id == "split":
			await inter.respond(f"So you split?",ephemeral = True)
		else:
			await inter.respond(f"So you steal?", ephemeral = True)
		
def setup(bot):
	bot.add_cog(selfbutton(bot))
