import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN') 

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_profanity_filter():
    """Load profanity words from external file"""
    try:
        with open('profanity_list.txt', 'r') as file:
            return [line.strip().lower() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Warning: profanity_list.txt not found. Using empty filter.")
        return []

#Stores the profanity word list
banned_words = load_profanity_filter()

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if any(word in message.content.lower() for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are an ape!")
    
    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def reply(ctx):
    await ctx.author.send(f"That's not very nice!")

 
bot.run(token, log_handler=handler, log_level=logging.DEBUG)