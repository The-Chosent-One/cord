from discord.ext import commands, tasks
import discord
import time


class ForumChannels(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.archive_and_lock_threads.start()

    @commands.Cog.listener(name="on_raw_thread_update")
    async def forum_channel_archived(self, payload: discord.RawThreadUpdateEvent):
        data = payload.data
        if payload.parent_id != 1023436140759482419:
            return

        if payload.data["thread_metadata"]["archived"] is False:
            return

        farm = self.bot.get_guild(645753561329696785)
        thread = payload.thread or await farm.fetch_channel(payload.thread_id)
        owner_id = int(data["owner_id"])

        async for entry in farm.audit_logs(
            limit=10, action=discord.AuditLogAction.thread_update
        ):
            if entry.target.id != thread.id:
                continue

            if entry.user.id == owner_id:
                return await thread.send(
                    f"<@{owner_id}> You cannot archive your own thread. It has been unarchived and will be automatically archived after 1 hour of inactivity."
                )

            # farmmail
            if entry.user.id == 855270214656065556:
                return

    @tasks.loop(minutes=30)
    async def archive_and_lock_threads(self):
        forum = self.bot.get_channel(
            1023274993045471272
        ) or await self.bot.fetch_channel(1023274993045471272)

        for thread in reversed(forum.threads):
            timestamp = ((thread.last_message_id >> 22) + 1420070400000) / 1000
            print(timestamp)
            if time.time() - timestamp >= 3600:
                await thread.send(
                    "Thread has been archived and locked due to inactivity. Please create a new thread if you wish to continue using the bot"
                )
                await thread.edit(
                    locked=True, archived=True, reason="Archived due to inactivity"
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(ForumChannels(bot))
