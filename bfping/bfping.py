import discord
import asyncio
from discord.ext import commands

data = [
    {'gaw': 672889430171713538},
    {'partner': 793454145897758742},
    {'heist': 684987530118299678},
    {'ev': 684552219344764934},
    {'friendly': 750908803704160268},
    {'lot': 732949595633614938},
    {'maf': 713898461606707273},
]


class BFping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.channel.permissions_for(message.author).manage_messages:
            return

        for x in data:
            for key , value in x.items():
                if message.content.startswith("??"+ key):
                    msg = message.content[len("??"+ key)+ 1:] or '^_^'
                    await message.channel.purge(limit=1)
                    await message.channel.send(f'<@&{value}> {msg}')


    @commands.command()
    @commands.has_any_role(682698693472026749, 663162896158556212, 658770981816500234, 855877108055015465)
    async def esponsor(self, ctx, member: discord.Member):
        role = ctx.guild.get_role(787572079573598220)

        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send("The role has been added")
            await asyncio.sleep(300)
            await member.remove_roles(role)

            await ctx.send(f"The Event Sponsor role has has been removed from {member.mention}")

            # allowed_mentions=discord.AllowedMentions.none() will not pass mentions into the message

        else:
            """
            This could be used in a situation where the bot turns off suddenly
            due to an unexpected error and Farm Mail fails to remove the role.

            The same command could be used when Farm Mail is back online to 
            force - remove it.
            """
            await member.remove_roles(role)
            await ctx.send("The role has been removed from them!")


def setup(bot):
    bot.add_cog(BFping(bot))
