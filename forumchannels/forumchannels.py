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
            channel = await self.bot.fetch_channel(int(payload.data["id"]))
            print(channel)
            print(channel.archiver_id)
            print(channel.archiver)
            print(data["owner_id"])



async def setup(bot):
    await bot.add_cog(ForumChannels(bot))
