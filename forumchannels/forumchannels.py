from discord.ext import commands


class ForumChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

        @commands.Cog.listener(name="on_raw_thread_update")
        async def forum_channel_archived(self, payload):
            print("Updated")
            if (
                payload.data["parent_id"] == 1019806662766379160
                and payload.data["archived"] == True
                and payload.data["archiver_id"] == payload.data["owner_id"]
            ):
                print("Passed check 1")
                channel = self.bot.get_channel(payload.data["id"])
                print("got channel")
                member = self.bot.get_user(payload.data["owner_id"])
                print("got member")
                await channel.edit(archived=False)
                print("edited channel")
                await channel.send(
                    f"{member.mention} \n You cannot archive your own thread. It has been unarchived and will be automatically archived after 1 hour of inactivity."
                )
                print("sent message")
            if (
                payload.data["parent_id"] == 1019806662766379160
                and payload.data["archived"] == True
                and payload.data["archiver_id"] != payload.data["owner_id"]
            ):
                print("Passed check 2")
                channel = self.bot.get_channel(payload.data["id"])
                print("got channel")
                member = self.bot.get_user(payload.data["owner_id"])
                print("got member")
                if member is None:
                    return
                await channel.set_permissions(
                    member.guild.default_role, send_messages=False
                )
                print("set permissions")
                await channel.send(
                    f"Thread has been archived and locked due to inactivity. Please create a new thread if you wish to continue using the bot"
                )
                print("sent message")


async def setup(bot):
    await bot.add_cog(ForumChannels(bot))
