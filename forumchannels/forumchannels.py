import discord
from discord.ext import command


class ForumChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.Cog.listener(name="on_raw_thread_update")
    async def forum_channel_archived(self, payload):
        if (
            payload.data["parent_id"] == 1019806662766379160
            and payload.data["archived"] == True
            and payload.data["archiver_id"] == payload.data["owner_id"]
        ):
            channel = self.bot.get_channel(payload.data["id"])
            member = self.bot.get_user(payload.data["owner_id"])
            await channel.edit(archived=False)
            await channel.send(
                f"{member.mention} \n You cannot archive your own thread. It has been unarchived and will be automatically archived after 1 hour of inactivity."
            )
        if (
            payload.data["parent_id"] == 1019806662766379160
            and payload.data["archived"] == True
            and payload.data["archiver_id"] != payload.data["owner_id"]
        ):
            channel = self.bot.get_channel(payload.data["id"])
            member = self.bot.get_user(payload.data["owner_id"])
            if member is None:
                return
            await channel.set_permissions(
                member.guild.default_role, send_messages=False
            )
            await channel.send(
                f"Thread has been archived and locked due to inactivity. Please create a new thread if you wish to continue using the bot"
            )


async def setup(bot):
    bot.add_cog(ForumChannels(bot))
