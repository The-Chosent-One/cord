import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

from core import checks
from core.models import PermissionLevel


class Donators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)
        self.check_expiry.start()

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def donatoradd(self, ctx, member: discord.Member, amount: int):
        """
        Adds the donated value to the member.
        """
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            balance = check["balance"]
            total = balance + amount
            await self.coll.update_one({"user_id": member.id}, {"$set": {"balance": total}})
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            embed = discord.Embed(title="**Amount added**",
                                  description=f"{member.mention} has had ${amount} added to their balance.",
                                  color=0x10ea64)
            embed.add_field(name="Total Balance:", value=f"{total}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=f"{expiry}", inline=True)
            await ctx.send(embed=embed)
        else:
            new = await self.coll.insert_one(
                {"user_id": member.id, "balance": amount, "perk_name": "None", "Expiry": "None"})
            perk_level = new["perk_name"]
            expiry = new["Expiry"]
            embed = discord.Embed(title="**Amount added**",
                                  description=f"{member.mention} has had ${amount} added to their balance.",
                                  color=0x10ea64)
            embed.add_field(name="Total Balance:", value=f"{total}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=f"{expiry}", inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def donatorremove(self, ctx, member: discord.Member, amount: int):
        """
        Removes the donated value from the member.
        """
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            balance = check["balance"]
            if balance < amount:
                await ctx.send("How do you plan to remove more than they have?")
            total = balance - amount
            await self.coll.update_one({"user_id": member.id}, {"$set": {"balance": total}})
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            embed = discord.Embed(title="**Amount added**",
                                  description=f"{member.mention} has had ${amount} added to their balance.",
                                  color=0xfb0404)
            embed.add_field(name="Total Balance:", value=f"{total}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=f"{expiry}", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} is not a donator yet and has no balance.")

    @commands.command()
    async def donatorbalance(self, ctx, member: discord.Member):
        """
        Shows the balance of the member.
        """
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            balance = check["balance"]
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            embed = discord.Embed(title="**Balance**",
                                  color=0x10ea64)
            embed.add_field(name="Total Balance:", value=f"{balance}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=f"{expiry}", inline=True)
            await ctx.send(embed=embed)
            await ctx.send(f"{member.mention} has ${balance}")
        else:
            await ctx.send(f"{member.mention} is not a donator yet and has no balance.")

    async def confirm(self, member: discord.Member, balance, perk_value, perk_level):
        expiry = datetime.utcnow() + timedelta(days=30)
        total = balance - perk_value
        await ctx.send(
            f"{member.mention}, Are you sure you want to redeem the `{perk_level}` perk for 30 days? (yes/no)")
        try:
            msg = await self.bot.wait_for('message', check=lambda m: m.author == member,
                                          timeout=30.0 and m.channel.id == ctx.channel.id)
            if msg.content.lower() == "yes":
                await self.coll.update_one({"user_id": member.id},
                                           {"$set": {"balance": total, "perk_name": perk_level, "expiry": expiry}})
                embed = discord.Embed(title="**Perk Redeemed**",
                                      description=f"{member.mention} has redeemed the {perk_level} perk.",
                                      color=0x10ea64)
                embed.add_field(name="Total Balance:", value=f"{total}", inline=True)
                embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
                embed.add_field(name="Expiry", value=f"{expiry}", inline=True)
            else:
                await ctx.send(f"{member.mention} has cancelled the perk redemption.")
        except asyncio.TimeoutError:
            await ctx.send(f"{member.mention} has cancelled the perk redemption.")

    @commands.command()
    async def redeem(self, ctx, perk_level=None):
        """
        Redeem perks from balance
        """
        check = await self.coll.find_one({"user_id": ctx.author.id})
        if check:
            balance = check["balance"]
            perkname = check["perk_name"]
            if perk_level is None:
                await ctx.send("Please specify a perk level. `$5`, `$10`, `$20`, `$30`")
            if perkname != "None":
                await ctx.send("You have already redeemed a perk. Please wait for it to expire.")
            elif perk_level == "$5":
                if balance >= 5:
                    await self.confirm(ctx.author, balance, 5, perk_level)
                    donator5 = ctx.guild.get_role(794300647137738762)
                    await ctx.author.add_roles(donator5)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            elif perk_level == "$10":
                if balance >= 10:
                    await self.confirm(ctx.author, balance, 10, perk_level)
                    donator10 = ctx.guild.get_role(794301192359378954)
                    await ctx.author.add_roles(donator10)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            elif perk_level == "$20":
                if balance >= 20:
                    await self.confirm(ctx.author, balance, 20, perk_level)
                    donator20 = ctx.guild.get_role(794301389769015316)
                    await ctx.author.add_roles(donator20)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            elif perk_level == "$30":
                if balance >= 30:
                    await self.confirm(ctx.author, balance, 30, perk_level)
                    donator30 = ctx.guild.get_role(794302939371929622)
                    serverboss = ctx.guild.get_role(820294120621867049)
                    await ctx.author.add_roles(serverboss)
                    await ctx.author.add_roles(donator30)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            else:
                await ctx.send("Please specify a perk level. `$5`, `$10`, `$20`, `$30`")
        else:
            await ctx.send("You are not a donator yet and have no balance.")

    @tasks.loop(hours=12)
    async def check_expiry(self):
        """
        Checks if the expiry time > current time.
        """
        try:
            fetchall = await self.coll.find().sort("expiry", 1).to_list(10)  # Top 10
            current_time = datetime.utcnow()
            for x in fetchall:
                if current_time >= x["expiry"]:
                    perk_level = x["perk_name"]
                    user = x["user_id"]
                    member = discord.Object(id=user)
                    guild = self.bot.get_guild(645753561329696785)
                    if perk_level == "$5":
                        donator5 = guild.get_role(794300647137738762)
                        await member.remove_roles(donator5)
                    elif perk_level == "$10":
                        donator10 = guild.get_role(794301192359378954)
                        await member.remove_roles(donator10)
                    elif perk_level == "$20":
                        donator20 = guild.get_role(794301389769015316)
                        await member.remove_roles(donator20)
                    elif perk_level == "$30":
                        donator30 = guild.get_role(794302939371929622)
                        await member.remove_roles(donator30)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Donators(bot))
