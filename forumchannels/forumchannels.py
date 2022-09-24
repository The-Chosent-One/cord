from discord.ext import commands


class ForumChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.Cog.listener(name="on_raw_thread_update")
    async def forum_channel_archived(self, payload):
        data = payload.data
        if (
            data["thread_metadata"]["archived"] == True
            and data["parent_id"] == "1019806662766379160"
        ):
            channel = self.bot.get_channel(int(payload.data["id"]))
            if channel.archiver_id == int(data["owner_id"]):
                await channel.edit(archived=False)
                member = self.bot.get_user(int(payload.data["owner_id"]))
                await channel.send(
                    f"{member.mention} \n You cannot archive your own thread. It has been unarchived and will be automatically archived after 1 hour of inactivity."
                )
            if channel.archiver_id != int(data["owner_id"]):
                member = self.bot.get_user(int(payload.data["owner_id"]))
                if member is None:
                    return
                await channel.set_permissions(
                    member.guild.default_role, send_messages=False
                )
                await channel.send(
                    f"Thread has been archived and locked due to inactivity. Please create a new thread if you wish to continue using the bot"
                )


async def setup(bot):
    await bot.add_cog(ForumChannels(bot))
