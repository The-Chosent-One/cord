from discord.ext import commands

class SaleItem(commands.Cog):
    _valid_numbers = [f'{x}%' for x in range(51, 71)]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = 'Flash sale!'
        if (str(message.channel.id)) == str(872709564976472115):  # Id of sale item channel in test server
            for x in self._valid_numbers:
                if '69' not in x:
                    if x in message.embeds[0].description:
                        msg = '<@&724438185601663077>: 50%+ Sale!'
                else:
                    if x in message.embeds[0].description:
                        msg = '<@&724438185601663077>: 69% off, nice!'

            channel = self.bot.get_channel(724437224036499517)  # Id of sale item channel in bot farm

            msg1 = await channel.send(msg, embed=message.embeds[0].set_footer(text='Made by The Farm (discord.gg/dank)'),
                                      delete_after=3600)
            await msg1.publish()


def setup(bot):
    bot.add_cog(SaleItem(bot))
