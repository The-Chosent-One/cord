from discord.ext import commands
import discord

class ForumChannels(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener(name="on_raw_thread_update")
    async def forum_channel_archived(self, payload: discord.RawThreadUpdateEvent):
        data = payload.data
        if payload.parent_id != 1019806662766379160:
            return
        
        if payload.data["thread_metadata"]["archived"] is False:
            return
        
        farm = self.bot.get_guild(645753561329696785)
        thread = payload.thread or await farm.fetch_channel(payload.thread_id)
        owner_id = int(data["owner_id"])

        async for entry in farm.audit_logs(limit=10, action=discord.AuditLogAction.thread_update):
            if entry.target.id != thread.id:
                continue

            if entry.user.id == owner_id:
                return await thread.send(
                    f"<@{owner_id}> You cannot archive your own thread. It has been unarchived and will be automatically archived after 1 hour of inactivity."
                )
            
            # farmmail
            if entry.user.id == 855270214656065556:
                return
        
        # archiving was done by someone else other than the owner of the thread
        await thread.send(
            f"Thread has been archived and locked due to inactivity. Please create a new thread if you wish to continue using the bot"
        )
        await thread.edit(locked=True, archived=True, reason="Archived due to inactivity")

async def setup(bot: commands.Bot):
    await bot.add_cog(ForumChannels(bot))
