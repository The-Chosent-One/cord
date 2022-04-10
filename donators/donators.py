import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime, timedelta
import asyncio

from core import checks
from core.models import PermissionLevel


class Donators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)
        self.check_expiry.start()

    async def confirm(self, ctx, member: discord.Member, balance, perk_value, perk_level, validity, totdonated, url):
        expiry = datetime.utcnow() + timedelta(days=validity)
        if expiry != "None":
            timestamp = round(datetime.timestamp(expiry))
            exp = f"<t:{timestamp}:f>"
        else:
            exp = "None"
        total = balance - perk_value
        await ctx.send(
            f"{member.mention}, Are you sure you want to redeem the `{perk_level}` perk for {validity} days? (yes/no)")
        try:
            msg = await self.bot.wait_for("message", timeout=30,
                                          check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
            if msg.content.lower() == "yes":
                if perk_value in (20, 30):
                    await ctx.send(
                        "You are eligible for a autoreact on ping. Do you want one? (yes/no)")
                    try:
                        msg = await self.bot.wait_for("message", timeout=30, check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
                        if msg.content.lower() == "yes":
                            await ctx.send("Please send ONLY the emoji you want to use. **Must be in this server**")
                            try:
                                msg = await self.bot.wait_for("message", timeout=30, check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
                                ar = {"user_id": member.id, "reaction": msg.content}
                                await self.bot.db.plugins.Autoreact.insert_one(ar)
                                await ctx.send(f"Added reaction {msg.content} for {member.mention}")
                            except asyncio.TimeoutError:
                                return await ctx.send(f"{member.mention} has cancelled the perk redemption.")
                        elif msg.content.lower() == "no":
                            pass
                        else:
                            return await ctx.send(f"{member.mention} has cancelled the perk redemption.")
                    except asyncio.TimeoutError:
                        return await ctx.send(f"{member.mention} has cancelled the perk redemption.")
                await self.coll.update_one({"user_id": member.id},
                                           {"$set": {"balance": total, "perk_name": perk_level, "expiry": expiry},
                                            "$push": {"Donation": {"Value": -abs(perk_value), "Date": datetime.utcnow(),
                                                                   "Proof": url}}})
                embed = discord.Embed(title="**Perk Redeemed**",
                                      description=f"{member.mention} has redeemed the {perk_level} perk.",
                                      color=0x10ea64)
                embed.add_field(name="Total Donated:", value=f"${totdonated}", inline=True)
                embed.add_field(name="Balance:", value=f"${total}", inline=True)
                embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
                embed.add_field(name="Expiry", value=exp, inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{member.mention} has cancelled the perk redemption.")
        except asyncio.TimeoutError:
            await ctx.send(f"{member.mention} has cancelled the perk redemption.")

    @commands.group(invoke_without_command=True)
    async def donator(self, ctx):
        """
        Donator commands.
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Donator Commands",
                                  color=0x10ea64)
            embed.add_field(name="`donator add`", value="Adds a donation value to a member", inline=False)
            embed.add_field(name="`donator remove`", value="Removes a donation value from a member", inline=False)
            embed.add_field(name="`donator balance`", value="Shows the balance of the member.", inline=False)
            embed.add_field(name="`donator details`", value="Shows the details of a members donations.", inline=False)
            embed.add_field(name="`donator redeem`", value="Redeems the requested perk", inline=False)
            embed.add_field(name="`donator leaderboard`", value="Shows the donation leaderboard", inline=False)

            await ctx.send(embed=embed)

    @donator.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def add(self, ctx, member: discord.Member, amount: int, proof):
        """
        Adds the donated value to the member.
        """
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            balance = check["balance"]
            totdonated = check["total_donated"]
            total = balance + amount
            await self.coll.update_one({"user_id": member.id},
                                       {"$set": {"balance": total, "total_donated": totdonated + amount}, "$push": {
                                           "Donation": {"Value": amount, "Date": datetime.utcnow(), "Proof": proof}}})
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            if expiry != "None":
                timestamp = round(datetime.timestamp(expiry))
                exp = f"<t:{timestamp}:f>"
            else:
                exp = "None"
            embed = discord.Embed(title="**Amount added**",
                                  description=f"{member.mention} has had ${amount} added to their balance.",
                                  color=0x10ea64)
            embed.add_field(name="Total Donated:", value=f"${totdonated + amount}", inline=True)
            embed.add_field(name="Balance:", value=f"${total}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=exp, inline=True)
            await ctx.send(embed=embed)
        else:
            await self.coll.insert_one({"user_id": member.id, "balance": amount, "total_donated": amount,
                                        "perk_name": "None", "expiry": "None",
                                        "Donation": [{"Value": amount, "Date": datetime.utcnow(), "Proof": proof}]})
            check = await self.coll.find_one({"user_id": member.id})
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            if expiry != "None":
                timestamp = round(datetime.timestamp(expiry))
                exp = f"<t:{timestamp}:f>"
            else:
                exp = "None"
            totdonated = check["total_donated"]
            embed = discord.Embed(title="**Amount added**",
                                  description=f"{member.mention} has had ${amount} added to their balance.",
                                  color=0x10ea64)
            embed.add_field(name="Total Donated:", value=f"${totdonated}", inline=True)
            embed.add_field(name="Balance:", value=f"${amount}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=exp, inline=True)
            await ctx.send(embed=embed)

    @donator.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def remove(self, ctx, member: discord.Member, amount: int):
        """
        Removes the donated value from the member.
        """
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            balance = check["balance"]
            totdonated = check["total_donated"]
            if balance < amount:
                return await ctx.send("How do you plan to remove more than they have?")
            total = balance - amount
            url = ctx.message.jump_url
            await self.coll.update_one({"user_id": member.id},
                                       {"$set": {"balance": total, "total_donated": totdonated - amount}, "$push": {
                                           "Donation": {"Value": -abs(amount), "Date": datetime.utcnow(),
                                                        "Proof": url}}})
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            if expiry != "None":
                timestamp = round(datetime.timestamp(expiry))
                exp = f"<t:{timestamp}:f>"
            else:
                exp = "None"
            embed = discord.Embed(title="**Amount removed**",
                                  description=f"{member.mention} has had ${amount} removed from their balance.",
                                  color=0xfb0404)
            embed.add_field(name="Total Donated:", value=f"${totdonated - amount}", inline=True)
            embed.add_field(name="Balance:", value=f"${total}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=exp, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} is not a donator yet and has no balance.")

    @donator.command(name="balance")
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def _balance(self, ctx, member: discord.Member):
        """
        Shows the balance of the member.
        """
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            totdonated = check["total_donated"]
            balance = check["balance"]
            perk_level = check["perk_name"]
            expiry = check["expiry"]
            if expiry != "None":
                timestamp = round(datetime.timestamp(expiry))
                exp = f"<t:{timestamp}:f>"
            else:
                exp = "None"
            embed = discord.Embed(title="**Balance**",
                                  description=f"If you are looking for details, use `??donator details {member.id}`.",
                                  color=0x10ea64)
            embed.add_field(name="Total Donated:", value=f"${totdonated}", inline=True)
            embed.add_field(name="Balance:", value=f"${balance}", inline=True)
            embed.add_field(name="Perks Redeemed", value=f"{perk_level}", inline=True)
            embed.add_field(name="Expiry", value=exp, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} is not a donator yet and has no balance.")

    @donator.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def details(self, ctx, member: discord.Member):
        """
        Shows details of each donation
        """
        s = ""
        check = await self.coll.find_one({"user_id": member.id})
        if check:
            for i in check['Donation']:
                date = i['Date']
                timestamp = round(datetime.timestamp(date))
                s += f"<t:{timestamp}:f> - [${i['Value']}]({i['Proof']})\n"
            embed = discord.Embed(title=f"**{member.name} Detailed Donations**", description=s, color=0x10ea64)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} is not a donator yet and has no balance.")

    @donator.command()
    async def redeem(self, ctx, perk_level=None):
        """
        Redeem perks from balance
        """
        check = await self.coll.find_one({"user_id": ctx.author.id})
        if check:
            balance = check["balance"]
            perkname = check["perk_name"]
            totdonated = check["total_donated"]
            if perk_level is None:
                return await ctx.send("Please specify a perk level. `$5`, `$10`, `$20`, `$30`")
            if perkname != "None":
                await ctx.send("You have already redeemed a perk. Please wait for it to expire.")
            elif perk_level == "$5":
                if balance >= 5:
                    await self.confirm(ctx, ctx.author, balance, 5, perk_level, 15, totdonated, ctx.message.jump_url)
                    donator5 = ctx.guild.get_role(794300647137738762)
                    await ctx.author.add_roles(donator5)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            elif perk_level == "$10":
                if balance >= 10:
                    await self.confirm(ctx, ctx.author, balance, 10, perk_level, 30, totdonated, ctx.message.jump_url)
                    donator10 = ctx.guild.get_role(794301192359378954)
                    await ctx.author.add_roles(donator10)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            elif perk_level == "$20":
                if balance >= 20:
                    await self.confirm(ctx, ctx.author, balance, 20, perk_level, 60, totdonated, ctx.message.jump_url)
                    donator20 = ctx.guild.get_role(794301389769015316)
                    await ctx.author.add_roles(donator20)
                else:
                    await ctx.send("You do not have enough balance to redeem this perk.")
            elif perk_level == "$30":
                if balance >= 30:
                    await self.confirm(ctx, ctx.author, balance, 30, perk_level, 90, totdonated, ctx.message.jump_url)
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

    @donator.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def leaderboard(self, ctx):
        """
        Shows the top 10 donators
        """
        if ctx.invoked_subcommand is None:
            return await ctx.send(
                "Are you looking for `??donator leaderboard total` or `??donator leaderboard balance`?")

    @commands.Cog.listener("on_raw_reaction_add")
    @commands.Cog.listener("on_raw_reaction_remove")
    async def leaderboard_pagination(self, payload: discord.RawReactionActionEvent) -> None:
        if str(payload.emoji) not in ("\U000025c0", "\U000025b6"):
            return

        if payload.member and payload.member.bot:
            return

        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        if message.embeds == []:
            return

        if message.embeds[0].title in ("**Top Donators**", "**Top Balance**"):
            return self.bot.dispatch("update_leaderboard", message, payload)

    @commands.Cog.listener("on_update_leaderboard")
    async def update_leaderboard(self, message: discord.Message, payload: discord.RawReactionActionEvent) -> None:
        embed = message.embeds[0]
        _, page_number = embed.footer.text.split()
        page_number = int(page_number)
        page_add = str(payload.emoji) == "\U000025b6"
        leaderboard_type = "total_donated" if embed.title == "**Top Donators**" else "balance"

        if page_number == 1 and not page_add:
            return

        offset = (page_number - 2) * 10
        if page_add:
            offset = page_number * 10

        top = await self.coll.find().sort(leaderboard_type, -1).skip(offset).limit(10).to_list(length=10)

        if not top:
            return

        embed.description = ""

        for pos, donation_information in enumerate(top, start=1 + offset):
            user_id, total = donation_information["user_id"], donation_information[leaderboard_type]

            embed.description += f"{pos}. <@{user_id}> ➜ ${total}\n"

        embed.set_footer(text=f"Page: {page_number + (-1) ** (page_add + 1)}")
        await message.edit(embed=embed)

    @leaderboard.command()
    async def total(self, ctx: commands.Context):
        top = await self.coll.find().sort("total_donated", -1).limit(10).to_list(length=10)

        embed = discord.Embed(title="**Top Donators**", description="", colour=0x10ea64)
        for pos, donation_information in enumerate(top, start=1):
            user_id, total = donation_information["user_id"], donation_information["total_donated"]

            embed.description += f"{pos}. <@{user_id}> ➜ ${total}\n"

        embed.set_footer(text="Page: 1")
        message = await ctx.send(embed=embed)
        await message.add_reaction("\U000025c0")
        await message.add_reaction("\U000025b6")

    @leaderboard.command()
    async def balance(self, ctx: commands.Context):
        top = await self.coll.find().sort("balance", -1).limit(10).to_list(length=10)

        embed = discord.Embed(title="**Top Balance**", description="", colour=0x10ea64)
        for pos, donation_information in enumerate(top, start=1):
            user_id, total = donation_information["user_id"], donation_information["balance"]

            embed.description += f"{pos}. <@{user_id}> ➜ ${total}\n"

        embed.set_footer(text="Page: 1")
        message = await ctx.send(embed=embed)
        await message.add_reaction("\U000025c0")
        await message.add_reaction("\U000025b6")

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
                    guild = self.bot.get_guild(645753561329696785)
                    member = guild.get_member(user)
                    if perk_level == "$5":
                        donator5 = guild.get_role(794300647137738762)
                        await member.remove_roles(donator5)
                        await self.coll.update_one({"user_id": user},
                                                   {"$set": {"perk_name": "None", "expiry": "None"}})
                        await member.send("You cash donator perks have expired in `The Farm`. gg/dank")
                    elif perk_level == "$10":
                        donator10 = guild.get_role(794301192359378954)
                        await member.remove_roles(donator10)
                        await self.coll.update_one({"user_id": user},
                                                   {"$set": {"perk_name": "None", "expiry": "None"}})
                        await member.send("You cash donator perks have expired in `The Farm`. gg/dank")
                    elif perk_level == "$20":
                        donator20 = guild.get_role(794301389769015316)
                        await member.remove_roles(donator20)
                        await self.coll.update_one({"user_id": user},
                                                   {"$set": {"perk_name": "None", "expiry": "None"}})
                        ar = await self.bot.db.plugins.Autoreact.find_one({"user_id": user})
                        if ar:
                            await self.bot.db.plugins.Autoreact.delete_one({"user_id": user})
                        await member.send("You cash donator perks have expired in `The Farm`. gg/dank")
                    elif perk_level == "$30":
                        donator30 = guild.get_role(794302939371929622)
                        await member.remove_roles(donator30)
                        await self.coll.update_one({"user_id": user},
                                                   {"$set": {"perk_name": "None", "expiry": "None"}})
                        ar = await self.bot.db.plugins.Autoreact.find_one({"user_id": user})
                        if ar:
                            await self.bot.db.plugins.Autoreact.delete_one({"user_id": user})
                        await member.send("You cash donator perks have expired in `The Farm`. gg/dank")
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Donators(bot))
