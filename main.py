import os
import asyncio

import discord
from discord.ext import commands
from discord.utils import escape_markdown

import pytz
from datetime import datetime

#BOT TOKEN
TOKEN = 'TOKEN'

#CHANNEL ID FOR ALERTS ABOUT DELETED MESSAGES
CHANNEL_ID = 'CHANNEL_ID'

#ROLE ID OTHER BOTS
BOT_ROLE_ID = 760474688102727690

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("Bot ready")      

@bot.event
async def on_message_delete(message):

    if message.author.id == bot.user.id:
        return
    
    if message.author.bot:
        return
    
    #SET TIME ZONE
    timezone = pytz.timezone('Europe/Warsaw')
    localized_time = message.created_at.astimezone(timezone)
    formatted_time = localized_time.strftime("%A, %d %B %Y | %H:%M:%S")

    embed = discord.Embed(title='DELETED MESSAGE', color=discord.Color.red())
    embed.add_field(name='Author', value=message.author.mention, inline=True)
    embed.add_field(name='Date', value=formatted_time, inline=True)
    embed.add_field(name='Channel', value=message.channel.mention, inline=True)
    embed.add_field(name='Message', value=message.content, inline=False)
    embed.set_footer(text=f'Message ID: {message.id} | Author ID: {message.author.id}')

    await bot.get_channel(CHANNEL_ID).send(embed=embed)

@bot.event
async def on_message(message):
    
    if message.author.id == bot.user.id:
        return
    
    if message.author.bot:
        return
    
    #RESPONDING ON MESSAGES
    if 'MESSAGE' in message.content.lower():
        await message.channel.send('BOT ANSWER')
        return

bot.run(TOKEN)