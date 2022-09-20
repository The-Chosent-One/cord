import discord
from discord.ext import commands
from motor import motor_asyncio

class CurrencyHandler:
    def __init__(self, bot: commands.Bot, collection: motor_asyncio.AsyncIOMotorCollection) -> None:
        self.bot = bot
        self.collection: motor_asyncio.AsyncIOMotorCollection = collection
        
    async def get_cash(self, target: discord.Member) -> int:
        res = await self.collection.find_one({"user_id": target.id})
        if res is None:
            return 0
        
        return res["cash"]
    
    async def update_cash(self, target: discord.Member, cash: int) -> int:
        res = await self.collection.find_one_and_update({"user_id": target.id}, {"$inc": {"cash": cash}}, upsert=True, return_document=True)

        return res["cash"]
    
    async def set_cash(self, target: discord.Member, cash: int) -> int:
        res = await self.collection.find_one_and_update({"user_id": target.id}, {"$set": {"cash": cash}}, upsert=True, return_document=True)

        return res["cash"]
