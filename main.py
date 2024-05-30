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
      

    async def on_chat(self, user: User, message: str) -> None :
        print(f"{user.username} said: {message}")
        response = await self.generate_response(message)
        await self.highrise.chat(response)

    async def generate_response(self, user_input):
        if user_input in self.cache:
            return self.cache[user_input]

        # Check if the rate limit has been exceeded
        if self.rate_limit_reset_time is None or datetime.now() < self.rate_limit_reset_time:
            # Wait until the rate limit resets
            wait_time = (self.rate_limit_reset_time - datetime.now()).total_seconds()
            await asyncio.sleep(wait_time)

        # Define the prompt for the OpenAI API
        prompt = f"{user_input}\n\nAI:"

        # Send a request to the OpenAI API
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Cache the response
        self.cache[user_input] = response.choices[0].text

        # Update the rate limit reset time
        self.rate_limit_reset_time = datetime.now() + timedelta(seconds=60)  # Set the rate limit to 1 request per minute

        # Return the generated response
        return self.cache[user_input]
    
    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)
    
    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)

keep_alive()
if __name__ == "__main__":
   arun(Bot().run("65973a6c5ae45c9ac1b5b7ed", "d4f4d0097df559e6e4a02a27f7567db9f77e83b8f4b212acaef06ac9cdcb67b9"))
