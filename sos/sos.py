import discord
from discord.ext import commands
from dislash import slash_commands, ActionRow, Button, ButtonStyle, MessageInteraction

class SplitOrSteal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(self.bot, "inter_client"):
            slash_commands.InteractionClient(self.bot)
    
    @commands.command()
    async def sos(self, ctx: commands.Context, player1: discord.Member, player2: discord.Member):
        actions = ActionRow(
            Button(style = ButtonStyle.green, label = "Split", custom_id = "split"),
            Button(style = ButtonStyle.red, label = "Steal", custom_id = "steal"),
        )

        decision_embed = discord.Embed(title = "Split or Steal?", description = "You have 30 seconds to decide!", colour = 0x90EE90)

        message = await ctx.send(embed = decision_embed, components = [actions])
        on_click = message.create_click_listener(timeout = 30)

        # choices for both players
        choices = {player1: None, player2: None}

        # player1's choice
        @on_click.from_user(player1, cancel_others = False, reset_timeout = False)
        async def response(inter: MessageInteraction):
            choice = inter.component.custom_id
            if choices[player1] is None:
                choices[player1] = choice

                if choice == "steal":
                    return await inter.reply("You chose: `steal`, go big or go home!", ephemeral = True)
                
                if choice == "split":
                    return await inter.reply("You chose: `split`, let's hope the other person does the same!", ephemeral = True)

            return await inter.reply("You already chose, be patient!", ephemeral = True)

        # player2's choice
        @on_click.from_user(player2, cancel_others = False, reset_timeout = False)
        async def response(inter: MessageInteraction):
            choice = inter.component.custom_id
            if choices[player2] is None:
                choices[player2] = choice

                if choice == "steal":
                    return await inter.reply("You chose: `steal`, go big or go home!", ephemeral = True)
                
                if choice == "split":
                    return await inter.reply("You chose: `split`, let's hope the other person does the same!", ephemeral = True)

            return await inter.reply("You already chose, be patient!", ephemeral = True)

        # acts as a check for both players
        @on_click.no_checks(cancel_others = False, reset_timeout = False)
        async def check(inter: MessageInteraction):
            if inter.author not in (player1, player2):
                return await inter.reply("These aren't your buttons! >:(", ephemeral = True)
            
            if None not in choices.values():
                # kills the manager
                on_click.kill()
                
                if choices[player1] == split:
                    if choices[player2] == split:
                        final = f"Since both {player1.mention} and {player2.mention} chose split, both get half!"
                    elif choices[player2] == steal:
                        final = f"Since {player1.mention} chose split BUT {player2.mention} chose split, so {player2.mention} takes everything!"
                        
                elif choices[player1] == steal:
                    if choices[player2] == split:
                        final = f"Since {player2.mention} chose split BUT {player1.mention} chose steal, so {player1.mention} takes everything!"
                    elif choices[player2] == steal:
                        final = f"Since both {player1.mention} and {player2.mention} chose steal, no one gets anything"
                        
                result_embed = discord.Embed(
                    title = "Split or Steal?",
                    description = f"{player1.mention} chose **{choices[player1]}** \n"
                                  f"{player2.mention} chose **{choices[player2]}** \n",
                                  f"{final}",                    
                    colour = 0x90EE90
                )
                return await message.edit(embed = result_embed, components = [])

        @on_click.timeout
        async def on_timeout():
            unresponsive_users = [user.mention for user, choice in choices.items() if choice is None]
            
            unresponsive_reply = " and ".join(unresponsive_users) + " did not reply in time!"
            await message.edit(content = unresponsive_reply, embed = None, components = [])

def setup(bot):
    bot.add_cog(SplitOrSteal(bot))
