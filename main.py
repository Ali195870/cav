import os
import random
import time
from highrise import BaseBot, Highrise, Position, AnchorPosition, Reaction
from highrise import __main__
from asyncio import run as arun
import asyncio
from random import choice
import json
from datetime import datetime, timedelta
from highrise.models import SessionMetadata
import re
from highrise.models import SessionMetadata, User, Item, Position, CurrencyItem, Reaction

from webserver import keep_alive
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

class BotDefinition:
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token
        openai.api_key = os.environ["OPENAI_API_KEY"]  

class Counter:
    bot_id = ""
    static_ctr = 0
    usernames = ['Alionadro_']


class Bot(BaseBot):
    cooldowns = {}  # Class-level variable to store cooldown timestamps
    emote_looping = False
    cache = {}
    rate_limit_reset_time = datetime.now()
    def __init__(self):
        super().__init__()
        self.maze_players = {}
        self.user_points = {}  # Dictionary to store user points
      
    async def openai_response(self, message):
      # You will need to replace 'your-openai-api-key' with your actual API key
      openai_api_key = os.environ["OPENAI_API_KEY"]
      openai_model = "gpt-3.5-turbo"

      openai_client = openai.Client(api_key=openai_api_key)

      response = openai_client.completion.create(
        engine=openai_model,
        prompt=message,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
      )

      return response.choices[0].text.strip()
    async def on_chat(self, user: User, message: str) -> None:
        print(f"{user.username} said: {message}")
        if message.lower().startswith("hey"):
         response = await self.openai_response(message)
         await self.highrise.chat(response)
            
    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)


keep_alive()
if __name__ == "__main__":
   arun(Bot().run("65973a6c5ae45c9ac1b5b7ed", "d4f4d0097df559e6e4a02a27f7567db9f77e83b8f4b212acaef06ac9cdcb67b9"))
