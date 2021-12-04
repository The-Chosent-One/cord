import discord
from discord.ext import commands
from discord.utils import get
from discord import Embed, Member
from core import checks
from core.models import PermissionLevel

class shortcuts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def dmads(self,ctx, user: discord.User, proof , proof2 = None):
        if proof2 == None:
            await ctx.send(f'```.ban {user.id} DM [Advertisments]({proof}) are against the rules of the server. Appeal this ban at https://discord.gg/appeal ```')
        else:
            await ctx.send(f'```.ban {user.id} DM Advertisments are against the rules of the server. Proof: [1]({proof}), [2]({proof2}). Appeal this ban at https://discord.gg/appeal```')
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def scammer(self,ctx, user: discord.User,user2: discord.User,quantity ,what , proof , proof2 = None):
        if proof2 == None:
            await ctx.send(f'```.ban {user.id} Scammed {quantity} {what} from `{user2.id}` and left the server to evade punishment [here]({proof}) Appeal this ban at https://discord.gg/appeal```')
        else:
            await ctx.send(f'```.ban {user.id} Scammed {quantity} {what} from `{user2.id}` and left the server to evade punishment. Proof: [1]({proof}), [2]([{proof2}) Appeal this ban at https://discord.gg/appeal ```')
 
def setup(bot):
    bot.add_cog(shortcuts(bot))
