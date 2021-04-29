'''
Author(s): Declan Hollingworth
Title: Python Discord Chat Bot
Description: 
  This bot accepts a command "!showme" followed by a search term and returns a random gif from that search term using the Discord and Tenor API's
Last Updated: 2021-04-29
'''
#Imports
import os
import random
import requests
import discord
from dotenv import load_dotenv
import json
from keep_alive import keep_alive

#Linking API's
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
apikey = os.getenv('TENORKEY')
lmt = 50 #Search limit, returns random gif from the top 50 results
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

    if message.content[:7] == '!showme': #Slices string and checks for the command term
        searchKey = message.content[7:] 
        r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (searchKey, apikey, lmt))
        if r.status_code == 200:
            # load the GIFs using the urls
            gif = json.loads(r.content)
            i = random.randint(0, lmt-1)
            url = gif['results'][i]['media'][0]['gif']['url']
            await message.channel.send(url)
        else:
            gif = None    

keep_alive() #Calling keep_alive(), allows another bot to ping the webpage every 5min and keep it online
client.run(TOKEN)
