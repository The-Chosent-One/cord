import discord
from discord.ext import commands
from discord.ui import view


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=30):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Spilt", style=discord.ButtonStyle.green, custom_id="spilt")
    async def spilt(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("You chose: `split`, let's hope the other person does the same!",
                                                ephemeral=True)

    @discord.ui.button(label="Steal", style=discord.ButtonStyle.red, custom_id="steal")
    async def steal(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("You chose: `steal`, go big or go home!", ephemeral=True)

class SplitOrSteal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sos(self, ctx: commands.Context, player1: discord.Member, player2: discord.Member):
        embed = discord.Embed(title="Split or Steal?", description="You have 30 seconds to decide!",
                              colour=0x90EE90)
        await ctx.send(embed=embed, view=view())


def setup(bot):
    bot.add_cog(SplitOrSteal(bot))
