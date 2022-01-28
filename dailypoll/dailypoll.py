import discord
import asyncio
import pathlib
import re

from pathlib import Path
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

this_file_directory = Path(__file__).parent.resolve()
other_file = this_file_directory / "daily_poll.txt"

with open(other_file, "r+") as file:
    daily_poll = [daily_poll.strip().lower() for daily_poll in file.readlines()]
    daily_poll1 = other_file.read_text()


class DailyPoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll.start()

    @tasks.loop(seconds=5, count=1)
    async def poll(self):
        today = datetime.utcnow().strftime("%Y%m%d")
        for single_line in daily_poll1.splitlines():
            if today in single_line:
                print(single_line)
                pattern = r'[0-9]'
                new_string = re.sub(pattern, '', single_line)
                print(new_string)
                channel = self.bot.get_channel(658776906996514836)
                message = await channel.send(new_string)
                await message.add_reaction("<:farm_1number1:889952572629200946>")
                await message.add_reaction("<:farm_1number2:889952572620820480>")
                file.close()

            else:
                print("Cant find it wot?")


def setup(bot):
    bot.add_cog(DailyPoll(bot))
