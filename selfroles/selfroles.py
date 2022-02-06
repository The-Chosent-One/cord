import discord
from discord.ext import commands
from dislash import slash_commands, ActionRow, Button, ButtonStyle, MessageInteraction
from itertools import zip_longest
import traceback
import sys
from core import checks
from core.models import PermissionLevel

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

        self.access_roles: dict[int, str] = {
            "├── Dank Access──┤": (680115778967699517, "<:dankmemeraccess:939734546147078144>"),
            "├──Pokémon Access─┤": (680115782645973003,"<:pokemonaccess:939738001083347005>"),
            "├── Anime Access──┤": (791439539854901248, "<:animeaccess:939738555364827156>"),
        }

        self.ping_roles: dict[int, str] = {
            "● Nitro Giveaway ●": (800660323203022868,"<a:giveaway_blob:939746793225343068>")
            "● • Giveawayss • ●": (672889430171713538,"<a:giveaway_blob:830768052156104705>")
            "● • Livestreams • ●": (864637855245795330,"<:status_streaming:939746824187682826>")
            "● • Event Time! • ●":  (684552219344764934,"<:hypesquad_events:939746866294313002>")
            "● • Mafia Time! • ●": (713898461606707273,"<:mafia:939746925400457307>")
            "● • Song Contest • ●": (710184003684270231,"<a:2musicvibe:939746897671880794>")
            "● • Partnership • ●": (793454145897758742,"<a:PartnerShine:939746957918875660>")
            "● • Farm Medic • ●": (722634660068327474,"<:DeadChat:939746982866608208>")
            "● • • Lottery • • ●": (732949595633614938,"<:winninglotteryticket:939747030560047104>")
            "● Friendly Heist ●": (750908803704160268,"💰")
            "● Daily Question ●": (872546624461738035,"❓")
            "● Heist Hipphoes ●": (684987530118299678,"<a:fh_pepeheist:939747192451772486>")
            "● Hype My Stream! ●": (865796857887981579,"<:streaming:939747138030669834>")
        }

        if not hasattr(self.bot, "inter_client"):
            slash_commands.InteractionClient(self.bot)

    def padding(self, string: str) -> str:
        # pads a string to the right with hair spaces

        # The number of hair spaces each character is (approximately)
        offset = {"a": 6, "b": 7, "c": 6, "d": 7, "e": 6, "f": 3, "g": 6, "h": 7, "i": 3, "j": 3, "k": 6, "l": 3,
                  "m": 11, "n": 7, "o": 7, "p": 7, "q": 7, "r": 4, "s": 5, "t": 4, "u": 7, "v": 6, "w": 9, "x": 6,
                  "y": 6, "z": 5, "A": 9, "B": 7, "C": 8, "D": 9, "E": 7, "F": 6, "G": 9, "H": 9, "I": 3, "J": 5,
                  "K": 8, "L": 6, "M": 12, "N": 9, "O": 9, "P": 7, "Q": 9, "R": 7, "S": 7, "T": 7, "U": 9, "V": 9,
                  "W": 13, "X": 8, "Y": 8, "Z": 7, " ": 3}

        hair_spaces = sum(offset[c] for c in string)

        # 51 is the widest role name (Opossum)
        # yes, this is bad if additional roles are added, but that's another problem for future me
        padding = "\u200a" * (51 - hair_spaces)
        return string + padding

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def send_colour_embed(self, ctx: commands.Context):
        row = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Click me!",
                custom_id="colour_roles"
            )
        )

        colour_embed = discord.Embed(title="Get your colour roles here!", description="Click the button below to choose colour roles", color=0x90ee90)

        await ctx.send(embed=colour_embed, components=[row])

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def send_access_embed(self, ctx: commands.Context):
        row = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Click me!",
                custom_id="access_roles"
            )
        )

        colour_embed = discord.Embed(title="Get your access roles here!", description="Click the button below to choose access roles", color=0x90ee90)

        await ctx.send(embed=colour_embed, components=[row])

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def send_pingroles_embed(self, ctx: commands.Context):
        row = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Click me!",
                custom_id="ping_roles"
            )
        )

        colour_embed = discord.Embed(title="Get your ping roles here!", description="Click the button below to choose ping roles", color=0x90ee90)

        await ctx.send(embed=colour_embed, components=[row])

    @send_colour_embed.error
    async def not_allowed(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            return await ctx.send("Wait, that's illegal >:(")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener("on_button_click")
    async def get_roles(self, inter: MessageInteraction):
        if inter.component.custom_id == "colour_roles":

            available_roles = self.regular_colour_roles.copy()

            if bool(set(inter.author._roles) & {867366006635364363}):  # Farmer
                available_roles.update(self.premium_colour_roles)

            components = []

            # splits it into at most 5 items long
            for role_names in zip_longest(*([iter(available_roles)] * 5)):
                # we append one row at a time
                components.append(ActionRow(
                    *[Button(
                        style=ButtonStyle.blurple,
                        label=self.padding(role_name),
                        custom_id=f"change_colour_role:{available_roles[role_name][0]}",
                        emoji=available_roles[role_name][1]
                    )
                        for role_name in role_names if role_name is not None]
                ))

            await inter.create_response("Which roles do you want to add/remove?", components=components, ephemeral=True)

        elif inter.component.custom_id == "access_roles":

            available_roles = self.access_roles.copy()

            components = []

            for role_names in zip_longest(*([iter(available_roles)] * 5)):
                components.append(ActionRow(
                    *[Button(
                        style=ButtonStyle.blurple,
                        label=self.padding(role_name),
                        custom_id=f"change_access_role:{available_roles[role_name][0]}",
                        emoji=available_roles[role_name][1]
                    )
                        for role_name in role_names if role_name is not None]
                ))

            await inter.create_response("Which roles do you want to add/remove?", components=components, ephemeral=True)

        elif inter.component.custom_id == "ping_roles":

            available_roles = self.ping_roles.copy()

            components = []

            for role_names in zip_longest(*([iter(available_roles)] * 5)):
                components.append(ActionRow(
                    *[Button(
                        style=ButtonStyle.blurple,
                        label=self.padding(role_name),
                        custom_id=f"change_ping_role:{available_roles[role_name][0]}",
                        emoji=available_roles[role_name][1]
                    )
                        for role_name in role_names if role_name is not None]
                ))

            await inter.create_response("Which roles do you want to add/remove?", components=components, ephemeral=True)

    @commands.Cog.listener("on_button_click")
    async def change_roles(self, inter: MessageInteraction):
        if inter.component.custom_id.startswith("change_colour_role"):
            role_id = int(inter.component.custom_id[19:])
    
            if inter.author._roles.has(role_id):
                await inter.author.remove_roles(discord.Object(role_id))
                return await inter.create_response(f"Removed <@&{role_id}>!", ephemeral=True)
    
            # does not have the role
            await inter.author.add_roles(discord.Object(role_id))
            await inter.create_response(f"Added <@&{role_id}>!", ephemeral=True)
        
        if inter.component.custom_id.startswith("change_access_role"):
            role_id = int(inter.component.custom_id[19:])
            
            if inter.author._roles.has(role_id):
                await inter.author.remove_roles(discord.Object(role_id))
                return await inter.create_response(f"Removed <@&{role_id}>!", ephemeral=True)
            
            # does not have the role
            await inter.author.add_roles(discord.Object(role_id))
            await inter.create_response(f"Added <@&{role_id}>!", ephemeral=True)
            
        if inter.component.custom_id.startswith("change_ping_role"):
            role_id = int(inter.component.custom_id[19:])
            
            if inter.author._roles.has(role_id):
                await inter.author.remove_roles(discord.Object(role_id))
                return await inter.create_response(f"Removed <@&{role_id}>!", ephemeral=True)
            
            # does not have the role
            await inter.author.add_roles(discord.Object(role_id))
            await inter.create_response(f"Added <@&{role_id}>!", ephemeral=True)
            
def setup(bot):
    bot.add_cog(SelfRoles(bot))
