import re

from discord.ext import tasks
from datetime import datetime, timedelta
from discord.ext import commands

time_units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)
        self.reminder_loop.start()

    @staticmethod
    def to_seconds(s):
        return int(timedelta(**{
            time_units.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
            for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', s, flags=re.I)
        }).total_seconds())

    @commands.command(aliases=['rm'])
    async def remind(self, ctx, time, *, message):
        """Reminds you of something in the future."""
        try:
            text = time
            seconds = sum(
                int(num) * {'h': 60 * 60, 'm': 60, 's': 1, ' ': 1}[weight if weight else 's'] for num, weight in
                re.findall(r'(\d+)\s?([msh])?', text))
            if seconds > (86400 * 366):
                await ctx.message.reply('I can\'t remind you after more than a year.')
                return BaseException
            if seconds < 10:
                await ctx.message.reply('I can\'t remind you under 10 seconds. Maybe improve your memory?')
                return BaseException
            check = await self.coll.count_documents({'user_id': ctx.author.id})
            if check >= 10:
                return await ctx.message.reply('You can only have 10 reminders at a time.')
            reminder = {"user_id": ctx.author.id, "message": message,
                        "time": datetime.utcnow() + timedelta(seconds=seconds)}
            await self.coll.insert_one(reminder)
            await ctx.message.reply("Reminder set. You will be dm\'d once it\'s time.")
        except ValueError:
            await ctx.message.reply('Invalid time format. Try `??remind 1h30m Hello!`')

    @commands.command(aliases=['rms'])
    async def reminders(self, ctx):
        """Shows all your reminders."""
        reminders = await self.coll.find({"user_id": ctx.author.id}).to_list(None)
        if not reminders:
            await ctx.send('You have no reminders.')
            return
        reminders = [f'{reminder["time"].strftime("%H:%M:%S")} - {reminder["message"]}' for reminder in reminders]
        final = ('\n'.join(reminders))
        await ctx.message.reply(f'```{final}```')

    @commands.command(aliases=['crm'])
    async def clearreminders(self, ctx):
        """Clears all your reminders."""
        await self.coll.delete_many({"user_id": ctx.author.id})
        await ctx.message.reply('All reminders cleared.')

    @tasks.loop()
    async def reminder_loop(self):
        now = datetime.utcnow()
        reminders = await self.coll.find({"time": {"$lte": now}}).to_list(None)
        if not reminders:
            fetch = await self.coll.find().sort('time', 1).to_list(1)
            if fetch:
                for x in fetch:
                    if x['time'] > now:
                        next_reminder = x['time']
                        return await discord.utils.sleep_until(next_reminder)
            next_reminder = datetime.utcnow() + timedelta(10)
            return await discord.utils.sleep_until(next_reminder)
            
        for reminder in reminders:
            try:
                user = await self.bot.get_user(reminder['user_id'])
                await user.send(f'Reminder: {reminder["message"]}')
                await self.coll.delete_one({"_id": reminder["_id"]})
                fetch = await self.coll.find().sort('time', 1).to_list(1)
                for x in fetch:
                    if x['time'] > now:
                        next_reminder = x['time']
                        return await discord.utils.sleep_until(next_reminder)
            except exception as e:
                print(e)


async def setup(bot):
    await bot.add_cog(Reminders(bot))
