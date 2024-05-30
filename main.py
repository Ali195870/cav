
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
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

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
    def respond(self, user_input):
        # Tokenize the user input
        inputs = self.tokenizer.encode_plus(
            user_input,
            add_special_tokens=True,
            max_length=512,
            return_attention_mask=True,
            return_tensors='pt'
        )

        # Generate a response using the GPT model
        outputs = self.model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response
    
    async def on_chat(self, user: User, message: str) -> None :
        print(f"{user.username} said: {message}")
        if user.username!= self.bot.username:
            chatbot = Chatbot(model, tokenizer)
            response = chatbot.respond(message)
            await self.highrise.chat(response)
    


    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem) -> None:
        try:
            print(f"{sender.username} tipped {receiver.username} an amount of {tip.amount}")
                
        except Exception as e:
            print(f"An exception occured: {e}")  

  


    async def on_user_move(self, user: User, pos: Position) -> None:
        try:

            if user.username == "gooshie":
                print(pos)
        
        except Exception as e:
            print(f"An error on_user_move: {e}")

    
  
 

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        Counter.bot_id = session_metadata.user_id
        print("gooshie bot is Booting...")
        pass
        self.highrise.tg.create_task(self.highrise.teleport(session_metadata.user_id, Position(x=4.5, y=0, z=0, facing='FrontLeft')))
        self.load_temporary_vips()
        
       
       

    async def on_user_join(self, user: User, position: Position  | AnchorPosition) -> None: 
     try:
        print(f"{user.username} joined the room standing at {position}")
        await self.highrise.send_whisper(user.id,f"Hey {user.username}")
     except Exception as e:
            print(f"An error on user_on_join: {e}") 

    async def on_user_leave(self, user: User) ->None:
        print(f"{user.username} has left the room")
   
    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)






keep_alive()
if __name__ == "__main__":
    room_id = "65973a6c5ae45c9ac1b5b7ed"
    token = "d4f4d0097df559e6e4a02a27f7567db9f77e83b8f4b212acaef06ac9cdcb67b9"
    arun(Bot().run(room_id, token))

