import discord
import os
import asyncio
import datetime
import sqlite3
from typing import Optional
from discord import ui, ButtonStyle, client
from discord.ext import commands


connection = sqlite3.connect("Database.sqlite")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS warnings (discord_id INTEGER, moderator TEXT, warn_id TEXT)")
connection.commit()

help_command = commands.DefaultHelpCommand(
  no_catagory = "Commands"
)

client = commands.Bot(
  command_prefix="!", #Sets the bot's prefix, default is !
  case_insensitive=True, #Makes it so commands can be in any capatalization, !HELP and !help work the same
  intents=discord.Intents.all(), #Make sure to have all of the discord bot's intents ON in the dev portal.
  help_command=help_command,#Sets default help command
  activity=discord.Activity(type=discord.activity.ActivityType.watching, name="you sleep",status=discord.Status.idle), #Sets the bot's activity to "watching you sleep"
)


@client.event #Loading cogs with commands, see cogs API to learn how to use/create cogs
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")
        else:
            print("Unable to load pycache folder.")

@client.event
async def on_ready():
  print(f"Logged in as {client.user}") #So you know the bot is correct, and active

client.run("TOKEN_HERE")
