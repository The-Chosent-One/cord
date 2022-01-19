import discord
from discord.ext import commands
from dislash import slash_commands, ActionRow, Button, ButtonStyle, MessageInteraction
from itertools import zip_longest
import traceback
import sys

class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.regular_colour_roles = {
            "Cat": 669807217444126731,
            "Dog": 659498316991692832,
            "Chicken": 658771095167565834,
            "Pig": 658771078075908136,
            "Cow": 658771090792906812,
            "Random": 766382104539693066,
        }

        self.premium_colour_roles = {
            "Duck": 658787907091300381, 
            "Goose": 671225083020312587, 
            "Bee": 670306986742644798, 
            "Turkey": 820406630004686848, 
            "Opossum": 658771088704274438, 
            "Bunny": 658771071050317844, 
            "Sheep": 670206078742560768, 
            "Donkey": 820405761413742619, 
            "Horse": 658771086422573067, 
            "Zebu": 820406409308405790, 
            "Raccoon": 820406441138454592, 
            "Deer": 820406476379258921, 
            "Frog": 820406552816648262, 
            "Fox": 820406606595751976, 
            "Monkey": 820406515063062588, 
            "Turtle": 700056188859056261, 
            "Owl": 820406654137794560, 
            "Wolf": 820406679996596244, 
            "Moose": 820406719209144332, 
        }

        if not hasattr(self.bot, "inter_client"):
            slash_commands.InteractionClient(self.bot)
    
    @commands.command(hidden = True)
    @commands.has_role(658770981816500234) # Farmer
    async def send_embed(self, ctx: commands.Context):
        row = ActionRow(
            Button(
                style = ButtonStyle.green,
                label = "Get your roles!",
                custom_id = "self_roles"
            )
        )

        await ctx.send("Click me to get your roles!", components = [row])
    
    @send_embed.error
    async def not_allowed(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            return await ctx.send("That's illegal >:(")
        
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener("on_button_click")
    async def give_roles(self, inter: MessageInteraction):
        if inter.component.custom_id != "self_roles":
            return

        available_roles = self.regular_colour_roles.copy()

        if bool( set(inter.author._roles) & {658770981816500234} ): # Farmer
            available_roles.update(self.premium_colour_roles)
        
        components = []
        
        # splits it into at most 5 items long
        for role_names in zip_longest(*([iter(available_roles)] * 5)):
            components.append(ActionRow(
                *[Button(style = ButtonStyle.blurple, label = role_name, custom_id = f"change_self_role:{available_roles[role_name]}")
                for role_name in role_names if role_name is not None]
            ))

        await inter.create_response("Which roles do you want to add/remove?", components = components, ephemeral = True)
    
    @commands.Cog.listener("on_button_click")
    async def change_self_roles(self, inter: MessageInteraction):
        if not inter.component.custom_id.startswith("change_self_role"):
            return
        
        role_id = int(inter.component.custom_id[17:])

        if inter.author._roles.has(role_id):
            await inter.author.remove_roles(discord.Object(role_id))
            return await inter.create_response(f"Removed <@&{role_id}>!", ephemeral = True)
    
        # does not have the role
        await inter.author.add_roles(discord.Object(role_id))
        await inter.create_response(f"Added <@&{role_id}>!", ephemeral = True)

def setup(bot):
    bot.add_cog(SelfRoles(bot))
