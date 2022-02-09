import discord
from pathlib import Path

from discord.ext import commands

this_file_directory = Path(__file__).parent.resolve()
other_file = this_file_directory / "nosnipe.txt"

with open(other_file, "r+") as file:
    nosnipe = [nosnipe.strip().lower() for nosnipe in file.readlines()]


def check_view_perms(channel, member):
    return channel.permissions_for(member).view_channel


class Snipe(commands.Cog):
    data = {
        'snipe': {},
        'snipe_list': {},
        'esnipe': {},
        'esnipe_list': {}
    }

    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, msg):
        if any(word in msg.content.lower() for word in nosnipe) or msg.author.bot:
            return

        em = discord.Embed(description=msg.content)
        em.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)

        em.set_footer(text='Sent at: ')
        em.timestamp = msg.created_at

        data = {'author': msg.author, 'content': msg.content, 'time': msg.created_at}

        self.data['snipe'][str(msg.channel.id)] = em

        if str(msg.channel.id) not in self.data['snipe_list']:
            self.data['snipe_list'][str(msg.channel.id)] = [em]

        elif len(self.data['snipe_list'][str(msg.channel.id)].keys()) > 6:
            self.data['snipe_list'][str(msg.channel.id)].pop(0)

        self.data['snipe_list'][str(msg.channel.id)].append(data)

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('❋ Booster Rooster ❋'),
        commands.has_role('Satellite Supporter'),
        commands.has_role('⋯ ☆ ⋯ $10 Cash Donator ⋯ ☆ ⋯'),
        commands.has_role('Giveaway Manager'),
        commands.has_role('Heist Leader'),
        commands.has_role('Partner Manager'),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_role(682698693472026749),  # Daughter
        commands.has_role('Farmer - Head Moderator'),
        commands.has_role('Farm Manager - Server Admin'),
        commands.has_role('Level 20'),
        commands.has_role(916271809333166101),  # Secret Supporter
    )
    @commands.command()
    async def snipe(self, ctx, *, channel: discord.TextChannel = None):
        ch = channel or ctx.channel
        member = ctx.author

        if check_view_perms(ch, member):
            if str(ch.id) not in self.data['snipe']:
                return await ctx.send('There\'s nothing to be sniped!')

            return await ctx.send(embed=self.data['snipe'][str(ch.id)])
        else:
            await ctx.message.delete()

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

        if str(ch.id) not in self.data['snipe_list']:
            return await ctx.send('There\'s nothing to be sniped!')

        data = self.data['snipe_list'][str(ch.id)][:5]
        em = discord.Embed(title='Snipe list', description='', colour=discord.Colour.random())

        for x in data:
            em.description += '**Sniped!**\n'
            em.description += f"User: {x['author'].mention}({x['author'].id})\n"
            em.description += f'Content: {x["content"]}\n'
            em.description += f'{x["time"].strftime("%m/%d/%Y, %H:%M:%S")}GMT\n\n'

        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if any(word in before.content.lower() for word in nosnipe) or any(word in after.content.lower() for word in
                                                                          nosnipe) or before.author.bot or before.content == after.content:
            return
        
        msg = before
        
        em = discord.Embed(description=f'**Before: ** {before.content}\n**After: ** {after.content}')
        em.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)

        em.set_footer(text='Sent at: ')
        em.timestamp = msg.created_at

        self.data['esnipe'][str(msg.channel.id)] = em

        if str(msg.channel.id) not in self.data['esnipe_list']:
            self.data['esnipe_list'][str(msg.channel.id)] = [em]

        elif len(self.data['esnipe_list'][str(msg.channel.id)].keys()) > 6:
            self.data['esnipe_list'][str(msg.channel.id)].pop(0)

        self.data['esnipe_list'][str(msg.channel.id)].append({'author': before.author, 'before': before.content,
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
        commands.has_role(682698693472026749),  # Daughter
        commands.has_role('Farmer - Head Moderator'),
        commands.has_role('Farm Manager - Server Admin'),
        commands.has_role('Level 20'),
        commands.has_role(916271809333166101),  # Secret Supporter
    )
    @commands.command()
    async def esnipe(self, ctx, *, channel: discord.TextChannel = None):
        ch = channel or ctx.channel
        member = ctx.author

        if ctx.channel.id == 882758609921015839:
            return

        if check_view_perms(ch, member):
            if str(ch.id) not in self.data['esnipe']:
                return await ctx.send('There\'s nothing to be sniped!')

            return await ctx.send(embed=self.data['esnipe'][str(ch.id)])
        else:
            await ctx.message.delete()

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

        if str(ch.id) not in self.data['esnipe_list']:
            return await ctx.send('There\'s nothing to be sniped!')

        data = self.data['esnipe_list'][str(ch.id)][:5]
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
    
