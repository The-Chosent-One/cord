import asyncio
import datetime
import pathlib

from pathlib import Path
from core import checks
from core.models import PermissionLevel
from discord.ext import commands

first = True

def clear_logs():
	this_file_directory = Path(__file__).parent.resolve()
	other_file = this_file_directory / "logs.txt"
	with open(other_file ,"r+") as file: 
		file.write('# logs.txt file\n# Used to log errors & dev messages\n\nCurrent Date     | Current Time   | Log message\n\n')


def log(text):
	global first

	dt = datetime.datetime.now()
	dt_string = dt.strftime("Date: %d/%m/%Y | Time: %H:%M:%S")
	
	this_file_directory = Path(__file__).parent.resolve()
	other_file = this_file_directory / "logs.txt"
	with open(other_file ,"r+") as file: 
		c_text = file.read()
		file.close()

	with open(other_file ,"r+") as file:

		if not first:
			file.write(c_text + f'{dt_string} | {text}\n')
		else:
			clear_logs()
			first = False

		file.close()

class ChL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.ignored = []

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def enablelock(self, ctx):
        if not self.enabled:
            self.enabled = True
            return await ctx.send('Enabled :thumbsup:')

        return await ctx.send('It is already enabled smh stop wasting my time')

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def disablelock(self, ctx):
        if self.enabled:
            self.enabled = False
            return await ctx.send('Disabled :thumbsup:')

        return await ctx.send('It is already disabled smh stop wasting my time')

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.position == after.position or before.category.id in self.ignored:  # Don't trigger unnecessarily
            return
        
        if not self.enabled:
            log('Ignoring channel move since lock is disabled')
            return

        log(f'{before.category.id} {before.id}')

        self.ignored.append(before.category.id)

        await after.edit(position=before.position, reason="Channel moved when lock was enabled")
        await asyncio.sleep(15)

        _ignored = []

        for x in self.ignored:
            if x != before.category.id:
                _ignored.append(x)

        self.ignored = _ignored

    @commands.Cog.listener('on_guild_channel_update')
    async def on_guild_channel_update_category(self, before, after):
        if before.category.id == after.category.id or before.category.id in self.ignored:  # Don't trigger unnecessarily
            return

        if not self.enabled:
            log('Ignoring channel move since lock is disabled')
            return
        
        log(f'{before.category.id} {before.id}')

        self.ignored.append(before.category.id)

        await after.edit(category=before.category, reason="Channel moved when lock was enabled")
        await asyncio.sleep(15)

        _ignored = []

        for x in self.ignored:
            if x != before.category.id:
                _ignored.append(x)

        self.ignored = _ignored

#setup bot
def setup(bot):
    bot.add_cog(ChL(bot))
