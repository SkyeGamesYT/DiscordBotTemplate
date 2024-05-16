import discord
from discord import ui, ButtonStyle
import os
import asyncio
import datetime
from discord import client
from discord import member
from discord.app_commands.commands import describe
from discord.ext import commands


class Misc(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot



  @commands.command(name="Slap")
  async def slap(self, ctx, member: discord.User):
    if member:
      await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}! Owch!")


  @commands.command(name="Echo")
  async def echo(self, ctx, *, message):
    if message:
      ctx.send(message)


  @commands.command(name="Ping")
  async def ping(self, ctx):
    ctx.reply("Pong!")

async def setup(bot: commands.Bot):
  await bot.add_cog(Misc(bot))
