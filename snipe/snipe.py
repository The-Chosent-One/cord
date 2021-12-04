import discord
import pathlib
from pathlib import Path

from discord.ext import commands

this_file_directory = Path(__file__).parent.resolve()
other_file = this_file_directory / "nosnipe.txt"
with open(other_file, "r+") as file:
    nosnipe = [nosnipe.strip().lower() for nosnipe in file.readlines()]


class Snipe(commands.Cog):
    sniped = {}
    snipe_list = {}

    esniped = {}
    esnipe_list = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:  # Not needed
            return
        if any(word in message.content.lower() for word in nosnipe):
            return

        em = discord.Embed(description=message.content)
        em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)

        em.set_footer(text='Sent at: ')
        em.timestamp = message.created_at

        self.sniped[str(message.channel.id)] = em

        if str(message.channel.id) not in self.snipe_list:
            self.snipe_list[str(message.channel.id)] = []

        elif len(self.snipe_list[str(message.channel.id)]) > 11:
            self.snipe_list[str(message.channel.id)] = self.snipe_list[str(message.channel.id)][1:]

        self.snipe_list[str(message.channel.id)].append({'author': message.author, 'content': message.content,
                                                         'time': message.created_at})
        
    def check_view_perms(self, channel, member):
        if channel.permissions_for(member).view_channel:
            return True
        else:
            return False
        
    @commands.check_any(
        commands.is_owner(),
        commands.has_role('❋ Booster Rooster ❋'),
        commands.has_role('Satellite Supporter'),
        commands.has_role('⋯ ☆ ⋯ $10 Cash Donator ⋯ ☆ ⋯'),
        commands.has_role('Giveaway Manager'),
        commands.has_role('Heist Leader'),
        commands.has_role('Partner Manager'),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_role(682698693472026749),
        commands.has_role('Farmer - Head Moderator'),
        commands.has_role('Farm Manager - Server Admin'),
        commands.has_role('Level 20'),
    )
    @commands.command()
    async def snipe(self, ctx, *, channel: discord.TextChannel = None):
        ch = channel or ctx.channel
        member = ctx.author

        if (ctx.channel.id == 882758609921015839):
            return

        has_perms = self.check_view_perms(ch, member)
        if has_perms:

            if str(ch.id) not in self.sniped:
                return await ctx.send('There\'s nothing to be sniped!')

            return await ctx.send(embed=self.sniped[str(ch.id)])
        else:
            await ctx.send("You arent supposed to see whats going on here!")

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_role(682698693472026749),
        commands.has_role('Farmer - Head Moderator'),
        commands.has_role('Farm Manager - Server Admin'),
    )
    @commands.command(name='snipe-list')
    async def _snipe_list_(self, ctx, *, channel: discord.TextChannel = None):
        ch = channel or ctx.channel

        if str(ch.id) not in self.snipe_list:
            return await ctx.send('There\'s nothing to be sniped!')

        data = self.snipe_list[str(ch.id)][:5]
        em = discord.Embed(title='Snipe list', description='', colour=discord.Colour.random())

        for x in data:
            em.description += '**Sniped!**\n'
            em.description += f"User: {x['author'].mention}({x['author'].id})\n"
            em.description += f'Content: {x["content"]}\n'
            em.description += f'{x["time"].strftime("%m/%d/%Y, %H:%M:%S")}GMT\n\n'

        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return

        if before.author.bot:
            return

        if any(word in before.content.lower() for word in nosnipe):
            return

        em = discord.Embed(description=f'**Before: ** {before.content}\n**After: ** {after.content}')
        em.set_author(name=before.author.display_name, icon_url=before.author.avatar_url)

        em.set_footer(text='Sent at: ')
        em.timestamp = before.created_at

        self.esniped[str(before.channel.id)] = em

        if str(before.channel.id) not in self.esnipe_list:
            self.esnipe_list[str(before.channel.id)] = []

        elif len(self.esnipe_list[str(before.channel.id)]) > 11:
            self.esnipe_list[str(before.channel.id)] = self.esnipe_list[str(before.channel.id)][1:]

        self.esnipe_list[str(before.channel.id)].append({'author': before.author, 'before': before.content,
                                                         'after': after.content, 'time': after.created_at})

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('❋ Booster Rooster ❋'),
        commands.has_role('Satellite Supporter'),
        commands.has_role('⋯ ☆ ⋯ $10 Cash Donator ⋯ ☆ ⋯'),
        commands.has_role('Giveaway Manager'),
        commands.has_role('Heist Leader'),
        commands.has_role('Partner Manager'),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_role(682698693472026749),
        commands.has_role('Farmer - Head Moderator'),
        commands.has_role('Farm Manager - Server Admin'),
        commands.has_role('Level 20'),
    )
    @commands.command()
    async def esnipe(self, ctx, *, channel: discord.TextChannel = None):
        ch = channel or ctx.channel
        member = ctx.author

        if (ctx.channel.id == 882758609921015839):
            return

        has_perms = self.check_view_perms(ch, member)
        if has_perms:

            if str(ch.id) not in self.esniped:
                return await ctx.send('There\'s nothing to be sniped!')

            return await ctx.send(embed=self.esniped[str(ch.id)])
        else:
            await ctx.send("You arent supposed to see whats going on here!")

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_role(682698693472026749),
        commands.has_role('Farmer - Head Moderator'),
        commands.has_role('Farm Manager - Server Admin'),
    )
    @commands.command(name='esnipe-list')
    async def snipe_list_(self, ctx, *, channel: discord.TextChannel = None):
        ch = channel or ctx.channel

        if str(ch.id) not in self.esnipe_list:
            return await ctx.send('There\'s nothing to be sniped!')

        data = self.esnipe_list[str(ch.id)][:5]
        em = discord.Embed(title='Edit Snipe list', description='', colour=discord.Colour.random())

        for x in data:
            em.description += '**Edited!**\n'
            em.description += f"User: {x['author'].mention}({x['author'].id})\n"
            em.description += f'Before: {x["before"]}\n'
            em.description += f'After: {x["after"]}\n'
            em.description += f'{x["time"].strftime("%m/%d/%Y, %H:%M:%S")} GMT\n\n'

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Snipe(bot))
