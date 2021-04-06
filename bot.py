'''
Author(s): Declan Hollingworth
Title: Python Discord Chat Bot
Date: 2021-04-06
'''
import os
import random
import requests
import discord
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
apikey = os.getenv('TENORKEY')
lmt = 10
search_term = "bingus"
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    monke_quotes = ['Monke pee, Monke poo','Return to monke','bingus bongus', 'Come With Me To Monkey Land', 'Hi Herb', 'Bingus Sus']

    if message.content == '!bingus':
        response = random.choice(monke_quotes)
        await message.channel.send(response)
    if message.content == '!showmebingus':
        r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            gif = json.loads(r.content)
            i = random.randint(3, 9)
            url = gif['results'][i]['media'][0]['gif']['url']
            await message.channel.send(url)
        else:
            gif = None
        
client.run(TOKEN)
