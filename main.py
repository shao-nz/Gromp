import discord
import os
from dotenv import load_dotenv
load_dotenv()
RIOT_KEY = os.getenv("RIOT_API_DEV")

class Gromp(discord.Client):
  async def on_ready(self):
    print(f"Logged on as {self.user}!")

intents = discord.Intents.default()

gromp = Gromp(intents=intents)
gromp.run('TOKEN')