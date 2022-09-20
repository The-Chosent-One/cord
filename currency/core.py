import asyncio
import aiohttp
import discord
from discord.ext import commands

BASE_URL = "https://unbelievaboat.com/api/v1"
AUTHORIZATION_TOKEN = "TOKEN"

RequestResponse = [str, int | str]

class UnbelivaboatClient:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.session: aiohttp.ClientSession = self.bot.session
        self.headers = {"Authorization": AUTHORIZATION_TOKEN}
    
    async def get(self, url: str) -> dict:
        async with self.session.get(url, headers=self.headers) as req:
            response = await req.json()

            if req.status != 429:
                return response

            print(f"Waiting for {response['retry_after']} miliseconds")
            await asyncio.sleep(response["retry_after"]/1000)
            return await self.get(url)
    
    async def request(self, method: str, url: str, payload: dict) -> dict:
        async with self.session.request(method, url, headers=self.headers, json=payload) as req:
            response = await req.json()

            if req.status != 429:
                return response

            print(f"Waiting for {response['retry_after']} miliseconds")
            await asyncio.sleep(response["retry_after"]/1000)
            return await self.request(method, url, payload)

    async def update_cash(self, target: discord.Member, cash: int) -> RequestResponse:
        return await self.request("PATCH", f"{BASE_URL}/guilds/852534243962650665/users/{target.id}", {"cash": cash})
    
    async def set_cash(self, target: discord.Member, cash: int) -> RequestResponse:
        return await self.request("PUT", f"{BASE_URL}/guilds/852534243962650665/users/{target.id}", {"cash": cash})
        
    async def get_cash(self, target: discord.Member) -> RequestResponse:
        return await self.get(f"{BASE_URL}/guilds/852534243962650665/users/{target.id}")
