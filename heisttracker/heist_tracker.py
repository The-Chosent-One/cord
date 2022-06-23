import asyncio
import re
import discord
import aiosqlite
from discord.ext import commands

RESULTS_REGEX = re.compile(r"```(?:diff)?\n(?:(?:(?:[+#].*)+⏣ \d{0,3}(?:,\d{3})*.+\n)|- .+ died RIP\n)*\n*```")
LEADER_REGEX = re.compile(r"led.+<@!?(\d{17,19})>", flags=re.I)
SCOUTER_REGEX = re.compile(r"scout.+<@!?(\d{17,19})>", flags=re.I)
AMOUNT_REGEX = re.compile(r"Amazing job everybody,.+⏣ ([1-9]\d{0,2}(?:,\d{3})*).+")
BACKUP_AMOUNT_REGEX = re.compile(r"\+.+⏣ ([1-9]\d{0,2}(?:,\d{3})*)")

class HeistTracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def cog_load(self) -> None:
        # initialise db
        async with aiosqlite.connect("heists.db") as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS heists (
                user_id INTEGER PRIMARY KEY,
                led_maximum INTEGER DEFAULT 0,
                scouted_maximum INTEGER DEFAULT 0,
                led_amount INTEGER DEFAULT 0,
                scouted_amount INTEGER DEFAULT 0,
                led_count INTEGER DEFAULT 0,
                scouted_count INTEGER DEFAULT 0
            )""")
            await db.commit()
    
    def check_valid_results(self, content: str) -> bool:
        return bool(RESULTS_REGEX.search(content))
    
    def get_id(self, person: str, content: str) -> int | None:
        if person == "leader":
            regex = LEADER_REGEX
        if person == "scouter":
            regex = SCOUTER_REGEX

        match = regex.search(content)

        if match is None:
            return None
        
        return int(match.group(1))
    
    def get_amount(self, content: str) -> int:
        match = AMOUNT_REGEX.search(content)

        if match is not None:
            return int(match.group(1).replace(",",""))
        
        # if "Amazing job everyone, ..." isn't placed into the 
        # message, we tally everyone's earnings through the codeblock.
        return content.count("\n+") * int(BACKUP_AMOUNT_REGEX.search(content).group(1).replace(",", ""))

    async def update_db(self, leader_id: int, scouter_id: int, amount: int) -> None:
        # updates database with values
        async with aiosqlite.connect("heists.db") as db:
            await db.execute("INSERT INTO heists (user_id, led_maximum, led_amount, led_count) VALUES (:leader_id, :amount, :amount, 1) ON CONFLICT (user_id) DO UPDATE SET led_maximum = MAX(:amount, led_maximum), led_amount = led_amount + :amount, led_count = led_count + 1", {"amount": amount, "leader_id": leader_id})
            await db.execute("INSERT INTO heists (user_id, scouted_maximum, scouted_amount, scouted_count) VALUES (:scouter_id, :amount, :amount, 1) ON CONFLICT (user_id) DO UPDATE SET scouted_maximum = MAX(:amount, scouted_maximum), scouted_amount = scouted_amount + :amount, scouted_count = scouted_count + 1", {"amount": amount, "scouter_id": scouter_id})
            await db.commit()
    
    async def get_info(self, user_id: int) -> dict[str, int] | None:
        # fetches relevant information
        rows = ["user_id", "led_maximum", "scouted_maximum", "led_amount", "scouted_amount", "led_count", "scouted_count"]

        async with aiosqlite.connect("heists.db") as db:
            cur = await db.execute(f"SELECT {', '.join(rows)} FROM heists WHERE user_id = ?", (user_id,))
            res = await cur.fetchone()
        
        # has not scouted/led any heists
        if res is None:
            return None
        
        return {info: val for info, val in zip(rows, res)}

    @commands.Cog.listener("on_message")
    async def recv_heist_msg(self, message: discord.Message):
        # trophy room
        # if message.channel.id != 669866611313999882:
        #     return
        
        # we do this just in case the bot auto-deletes the heist message
        # if there's sensitive words in the message
        await asyncio.sleep(2)
        try:
            await message.channel.fetch_message(message.id)
        except discord.NotFound:
            # if the message has been deleted, ignore
            return
        
        content = message.content

        if not self.check_valid_results(content):
            return
        
        leader_id = self.get_id("leader", content)
        scouter_id = self.get_id("scouter", content)

        # either one of the ids are missing
        if not all((leader_id, scouter_id)):
            return
        
        amount = self.get_amount(content)

        await self.update_db(leader_id, scouter_id, amount)
    
    @commands.command(aliases=["hs", "heiststatistics", "heiststat"])
    async def heiststats(self, ctx: commands.Context, user: discord.Member = None):
        target = user or ctx.author
        user_id = target.id

        res = await self.get_info(user_id)

        if res is None:
            return await ctx.send(f"{target} does not have any unfriendly heist statistics")

        embed = discord.Embed(title=f"{target}'s unfriendly heist statistics!", colour=0x303135)

        embed.description = (
            f"Number of heists led: **{res['led_count']:,}**\n"
            f"Total amount led: **⏣ {res['led_amount']:,}**\n"
            f"Largest amount led in one heist: **⏣ {res['led_maximum']:,}**\n"
            "\n"
            f"Number of heists scouted: **{res['scouted_count']:,}**\n"
            f"Total amount scouted: **⏣ {res['scouted_amount']:,}**\n"
            f"Largest amount scouted in one heist: **⏣ {res['scouted_maximum']:,}**\n"
        )

        await ctx.send(embed=embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(HeistTracker(bot))
