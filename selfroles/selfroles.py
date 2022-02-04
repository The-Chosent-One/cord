import discord
from discord.ext import commands
from dislash import slash_commands, ActionRow, Button, ButtonStyle, MessageInteraction
from itertools import zip_longest
import traceback
import sys

class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Name: id, emoji
        self.regular_colour_roles: dict[int, str] = {
            "Cat": (669807217444126731, "<:Cat:938660093124292618>"),
            "Dog": (659498316991692832, "<:Dog:938660094042857502>"),
            "Chicken": (658771095167565834, "<:Chicken:938660093619236914>"),
            "Pig": (658771078075908136, "<:Pig:938660094776852490>"),
            "Cow": (658771090792906812, "<:Cow:938660094592294912>"),
            "Random": (766382104539693066, "<a:Random:938826714820255765>"),
        }

        self.premium_colour_roles: dict[int, str] = {
            "Duck": (658787907091300381, "<:Duck:938660094856544256>"), 
            "Goose": (671225083020312587, "<:Goose:938660094541967391>"), 
            "Bee": (670306986742644798, "<:Bee:938660094340657152>"), 
            "Turkey": (820406630004686848, "<:Turkey:938660094239973446>"), 
            "Opossum": (658771088704274438, "<:Opossum:938660094428725248>"), 
            "Bunny": (658771071050317844, "<:Bunny:938660094147715092>"), 
            "Sheep": (670206078742560768, "<:Sheep:938660093715677214>"), 
            "Donkey": (820405761413742619, "<:Donkey:938660094034460762>"), 
            "Horse": (658771086422573067, "<:Horse:938660094739103754>"), 
            "Zebu": (820406409308405790, "<:Zebu:938660094349037598>"), 
            "Raccoon": (820406441138454592, "<:Raccoon:938660094613274654>"), 
            "Deer": (820406476379258921, "<:Deer:938660094567153755>"), 
            "Frog": (820406552816648262, "<:Frog:938660094818795570>"), 
            "Fox": (820406606595751976, "<:Fox:938660094147715093>"), 
            "Monkey": (820406515063062588, "<:Monkey:938660093849911306>"), 
            "Turtle": (700056188859056261, "<:Turtle:938660095150133358>"), 
            "Owl": (820406654137794560, "<:Owl:938660095355662356>"), 
            "Wolf": (820406679996596244, "<:Wolf:938660094709751818>"), 
            "Moose": (820406719209144332, "<:Moose:938660095271780382>"),
        }

        if not hasattr(self.bot, "inter_client"):
            slash_commands.InteractionClient(self.bot)
    
    def padding(self, string: str) -> str:
        # pads a string to the right with hair spaces

        # The number of hair spaces each character is (approximately)
        offset = {"a": 6, "b": 7, "c": 6, "d": 7, "e": 6, "f": 3, "g": 6, "h": 7, "i": 3, "j": 3, "k": 6, "l": 3, "m": 11, "n": 7, "o": 7, "p": 7, "q": 7, "r": 4, "s": 5, "t": 4, "u": 7, "v": 6, "w": 9, "x": 6, "y": 6, "z": 5, "A": 9, "B": 7, "C": 8, "D": 9, "E": 7, "F": 6, "G": 9, "H": 9, "I": 3, "J": 5, "K": 8, "L": 6, "M": 12, "N": 9, "O": 9, "P": 7, "Q": 9, "R": 7, "S": 7, "T": 7, "U": 9, "V": 9, "W": 13, "X": 8, "Y": 8, "Z": 7, " ": 3}

        hair_spaces = sum(offset[c] for c in string)

        # 51 is the widest role name (Opossum)
        # yes, this is bad if additional roles are added, but that's another problem for future me
        padding = "\u200a" * (51 - hair_spaces) 
        return string + padding
    
    @commands.command(hidden = True)
    @commands.has_role(658770981816500234) # Farmer
    async def send_colour_embed(self, ctx: commands.Context):
        row = ActionRow(
            Button(
                style = ButtonStyle.green,
                label = "Click me!",
                custom_id = "colour_roles"
            )
        )

        colour_embed = discord.Embed(title = "Get your colour roles here!")

        await ctx.send(embed = colour_embed, components = [row])
    
    @send_colour_embed.error
    async def not_allowed(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            return await ctx.send("Wait, that's illegal >:(")
        
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener("on_button_click")
    async def give_colour_roles(self, inter: MessageInteraction):
        if inter.component.custom_id != "colour_roles":
            return

        available_roles = self.regular_colour_roles.copy()

        if bool( set(inter.author._roles) & {867366006635364363} ): # Farmer
            available_roles.update(self.premium_colour_roles)
        
        components = []
        
        # splits it into at most 5 items long
        for role_names in zip_longest(*([iter(available_roles)] * 5)):
            # we append one row at a time
            components.append(ActionRow(
                *[Button(
                    style = ButtonStyle.blurple,
                    label = self.padding(role_name),
                    custom_id = f"change_colour_role:{available_roles[role_name][0]}",
                    emoji = available_roles[role_name][1]
                    )
                for role_name in role_names if role_name is not None]
            ))

        await inter.create_response("Which roles do you want to add/remove?", components = components, ephemeral = True)
    
    @commands.Cog.listener("on_button_click")
    async def change_colour_roles(self, inter: MessageInteraction):
        if not inter.component.custom_id.startswith("change_colour_role"):
            return
        
        role_id = int(inter.component.custom_id[19:])

        if inter.author._roles.has(role_id):
            await inter.author.remove_roles(discord.Object(role_id))
            return await inter.create_response(f"Removed <@&{role_id}>!", ephemeral = True)
    
        # does not have the role
        await inter.author.add_roles(discord.Object(role_id))
        await inter.create_response(f"Added <@&{role_id}>!", ephemeral = True)

def setup(bot):
    bot.add_cog(SelfRoles(bot))
