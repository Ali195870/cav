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

import openai


openai.api_key = os.environ["OPENAI_API_KEY"]

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

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

    def __init__(self):
        super().__init__()
        self.maze_players = {}
        self.user_points = {}  # Dictionary to store user points
        self.rasa_executor = ActionExecutor()

    async def on_chat(self, user: User, message: str) -> None :
        print(f"{user.username} said: {message}")
        if user.username!= self.bot.username:
            response = await self.generate_response(message)
            await self.highrise.chat(response)

    async def generate_response(self, user_input):
        # Define the prompt for the OpenAI API
        prompt = f"
