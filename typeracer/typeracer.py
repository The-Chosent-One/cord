import asyncio
import inspect
import textwrap
from pathlib import Path
from difflib import SequenceMatcher
from functools import partial
from io import BytesIO
from typing import Optional, Tuple

import aiohttp
import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from core import checks
from core.models import PermissionLevel


bundled_path = Path(__file__).parent.resolve() / "data"

class TypeRacer(commands.Cog):
    """
    Race to see who can type the fastest!
    Credits to Cats3153.
    """

    FONT_SIZE = 30

    def __init__(self, bot) -> None:
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self._font = None
        self.coll = bot.plugin_db.get_partition(self)

    def cog_unload(self) -> None:
        asyncio.create_task(self.session.close())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        pre_processed = super().format_help_for_context(ctx)
        n = "\n" if "\n\n" not in pre_processed else ""
        return f"{pre_processed}{n}\nCog Version: {self.__version__}"

    async def get_quote(self) -> Tuple[str, str]:
        async with self.session.get("https://api.quotable.io/random") as resp:
            data = await resp.json()
        return data["content"], data["author"]
        # back up api in case above goes down
        # async with self.session.get("https://zenquotes.io/api/random") as resp:
        #    data = await resp.json(content_type=None)[0]
        # return data["q"], data["a"]

    @property
    def font(self) -> ImageFont:
        if self._font is None:
            self._font = ImageFont.truetype(
                f"{bundled_path}/Menlo.ttf", self.FONT_SIZE, encoding="unic"
            )
        return self._font

    def generate_image(self, text: str, color: discord.Color) -> discord.File:
        margin = 40
        newline = self.FONT_SIZE // 5

        wrapped = textwrap.wrap(text, width=35)
        text = "\n".join(line.strip() for line in wrapped)

        img_width = self.font.getsize(max(wrapped, key=len))[0] + 2 * margin
        img_height = self.FONT_SIZE * len(wrapped) + (len(wrapped) - 1) * newline + 2 * margin

        with Image.new("RGBA", (img_width, img_height)) as im:
            draw = ImageDraw.Draw(im)
            draw.multiline_text(
                (margin, margin), text, spacing=newline, font=self.font, fill=color.to_rgb()
            )

            buffer = BytesIO()
            im.save(buffer, "PNG")
            buffer.seek(0)

        return buffer

    async def render_typerace(self, text: str, color: discord.Color) -> discord.File:
        func = partial(self.generate_image, text, color)
        task = self.bot.loop.run_in_executor(None, func)
        try:
            return await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            raise commands.UserFeedbackCheckFailure(
                "An error occurred while generating this image. Try again later."
            )
    
    @commands.group(invoke_without_command=True)
    async def typeracer(self, ctx):
        if ctx.invoked_subcommand is None:
            role1 = ctx.guild.get_role(658770981816500234)
            role2 = ctx.guild.get_role(663162896158556212)
            role3 = ctx.guild.get_role(658770586540965911)
            role4 = (role1 , role2 , role3)
            if any(role in ctx.author.roles for role in role4):
                await ctx.send("You are probably looking for `??typeracer config` or maybe `??typerace` for a challenge?")
            else:
                await ctx.send("You are probably looking for `??typerace`")
    
    @typeracer.group()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def config(self,ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Config options", description="Whitelist / Unwhitelist - Allow the command to be used in certain channels \n Whitelisted - Show the currently whitelisted channels", color=0x42f587)
            await ctx.send(embed=embed) 
            
    @config.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def whitelist(self,ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        check = await self.coll.find_one({"channel" : channel.id})
        if check:
            return await ctx.send("This channel is already whitelisted")
        whitelist = {"channel" : channel.id}
        await self.coll.insert_one(whitelist)
        await ctx.send(f" Whitelisted <#{channel.id}> for typeracer")
    
    @config.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def unwhitelist(self,ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        unwhitelist = await self.coll.find_one({"channel" : channel.id})
        if not unwhitelist:
            return await ctx.send("This channel is not whitelisted")
        await self.coll.delete_one(unwhitelist)
        await ctx.send(f" Unwhitelisted <#{channel.id}> for typeracer")
        
    @config.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def whitelisted(self,ctx):
        s = ""
        fetchall = self.coll.find({})
        async for x in fetchall:
            whitelist = x['channel']
            whitelisted = self.bot.get_channel(int(whitelist))
            s += f"{whitelisted} \n"

        embed=discord.Embed(title="Whitelisted channels", description=s, color=0x42f587)
        await ctx.send(embed=embed)    

        
    @commands.command(aliases=["tr"])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def typerace(self, ctx, member: discord.Member = None):
        check = await self.coll.find_one({"channel": ctx.channel.id})
        if not check:
            return await ctx.reply("You are not allowed to use that here", delete_after=4)
        if member == ctx.author:
            return await ctx.send("Imagine trying to challenege youself lmao") 
        if member != None:
            await ctx.send(f"{member.mention}, {ctx.author.mention} challenges you to a battle of speed typing, do you accept? (yes/no)")
            try:
                msg = await self.bot.wait_for("message", timeout=60.0, check=lambda m: m.author == member and m.channel.id == ctx.channel.id)
                if msg.content.lower() in ("y", "yes"):
                    await ctx.send(f"{member.mention} vs {ctx.author.mention}")
                else:
                    return await ctx.send("Looks like someone is scared huh?")
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    color=discord.Color.blurple(),
                    description=f"Looks like {member} is not here, try again later.",
                )
                return await ctx.send(embed=embed)    
        try:
            quote, author = await self.get_quote()
        except KeyError:
            raise commands.UserFeedbackCheckFailure(
                "Could not fetch quote. Please try again later."
            )

        color = discord.Color.random()
        img = await self.render_typerace(quote, color)
        embed = discord.Embed(color=color)
        embed.set_image(url="attachment://typerace.png")
        if author:
            embed.set_footer(text=f"~ {author}")

        msg = await ctx.send(file=discord.File(img, "typerace.png"), embed=embed)
        acc: Optional[float] = None

        def check(m: discord.Message) -> bool:
            if m.channel != ctx.channel or m.author.bot or not m.content:
                return False  # if satisfied, skip accuracy check and return
            if member != None:
                if m.author != member and m.author != ctx.author:
                    return False
            content = " ".join(m.content.split())  # remove duplicate spaces
            accuracy = SequenceMatcher(None, quote, content).ratio()

            if accuracy >= 0.98:
                nonlocal acc
                acc = accuracy * 100
                return True
            return False

        ref = msg.to_reference(fail_if_not_exists=False)
        try:
            winner = await ctx.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                color=discord.Color.blurple(),
                description=f"No one typed the [sentence]({msg.jump_url}) in time.",
            )
            return await ctx.send(embed=embed, reference=ref)

        seconds = (winner.created_at - msg.created_at).total_seconds()
        winner_ref = winner.to_reference(fail_if_not_exists=False)
        wpm = (len(quote) / 5) / (seconds / 60) * (acc / 100)
        description = (
            f"{winner.author.mention} typed the [sentence]({msg.jump_url}) in `{seconds:.2f}s` "
            f"with **{acc:.2f}%** accuracy. (**{wpm:.1f} WPM**)"
        )
        embed = discord.Embed(color=winner.author.color, description=description)
        await ctx.send(embed=embed, reference=winner_ref)
        
def setup(bot):
    bot.add_cog(TypeRacer(bot))
