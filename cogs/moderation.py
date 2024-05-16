import discord
import os
import asyncio
import datetime
import sqlite3
import random
from discord import client, member
from discord.app_commands.commands import describe
from discord.ext import commands
from discord import ui, ButtonStyle
from typing import Optional
from key_generator.key_generator import generate
from wonderwords import RandomSentence

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()

class Moderation(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot



  @commands.command(name="ban", description="Usage: -ban <mention> <reason>")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason = None):
        await member.send(f"You were banned from {ctx.guild} for {reason} by {ctx.author}")
        await member.ban(reason = reason)
        embedVar = discord.Embed(title="Banned User", description=f"{member} was banned by {ctx.author} for {reason}", color=00000)
        await ctx.send(embed=embedVar)
  @commands.command(name='unban', description="Usage: -unban <user id> <reason>")
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, id: int, *, reason = None):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user, reason = reason)
        embedVar = discord.Embed(title="Unbanned User", description=f"{user} was unbanned by {ctx.author} for {reason}", color=0x00ff00)
        await ctx.send(embed=embedVar)

  
  @commands.command(name="mute", description="Usage: -mute <mention> <reason>")
  @commands.has_permissions(manage_roles=True)
    async def mute(ctx, member: discord.Member, reason = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming you have a role named "Muted"

        if not role:
        # The "Muted" role does not exist, so create it
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
            # Disallow the "Muted" role to send messages in all channels
                await channel.set_permissions(role, send_messages=False)

        await member.add_roles(role)
        embedVar = discord.Embed(title="User Muted", description=f"{member} was muted by {ctx.author} for {reason}", color=0x00ff00)
        await ctx.send(embed=embedVar)



    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a member to mute.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            await ctx.send("An error occurred while executing this command.")


    @commands.command(name="unmute", description="Usage: -unmute <mention>")
    @commands.has_permissions(manage_roles=True)
    async def unmute(ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming you have a role named "muted"

        if role in member.roles:
            await member.remove_roles(role)
            embedVar = discord.Embed(title="User Unmuted", description=f"{member} was unmuted by {ctx.author}", color=0x00ff00)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(f"{member.mention} is not muted.")




    @unmute.error
    async def unmute_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a member to unmute.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            await ctx.send("An error occurred while executing this command.")



    @commands.command(name="warn")
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, id: int, reason="No reason Specified"):
        moderator = str(ctx.author.name)
        member = await self.bot.fetch_user(id)
        print(member)
        key = generate()
        warnid = key.get_key()
        print(warnid)
        cursor.execute("INSERT INTO warningsdb VALUES (?, ?, ?, ?)",(id, reason, moderator, warnid))
        connection.commit()
        embedVar = discord.Embed(
            title="User Warned",
            description=f"{member} has been warned by {moderator} for {reason}", color=0x2ecc71)
        await ctx.send(embed=embedVar)
        channel = await member.create_dm()
        embedDM = discord.Embed(
            title="Warning",
            description=f"You have been warned by {moderator} for {reason}",
            color=0xe74c3c)
        await channel.send(embed=embedDM)



    @commands.command(name="warnings")
    @commands.has_permissions(manage_roles=True)
    async def warnings(ctx, id: int):
        member = ctx.guild.get_member(id)
        cursor.execute("SELECT * FROM warningsdb WHERE user_id = ?", (id, ))
        result = cursor.fetchall()

        if result:
            embedVar = discord.Embed(title=f"Warnings for {member}",description="Warnings",color=0x2ecc71)
            for row in result:
                moduser = row[2]  # Extract moderator from each row
                warningNumber = row[3]  # Extract warning number from each row
                embedVar.add_field(name=f"Reason: {row[1]}",value=f"Moderator: {moduser}, Warning Number: {warningNumber}",inline=False)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send("No warnings found for the member.")


    @commands.command(name="delwarn")
    @commands.has_permissions(manage_roles=True)
    async def delwarn(ctx, id: int, warnNumb: str):
        member = ctx.guild.get_member(id)

        if member:
            cursor.execute("select warn_id FROM warningsdb WHERE user_id = ?", (id, ))
            warnings = cursor.fetchall()
            print("warnings:", warnings)  # add this line for debugging
            found = False
            for warning in warnings:
                print("warning id:", warning)  # add this line for debugging
                if warnNumb == warning[0]:
                    cursor.execute(f"DELETE FROM warningsdb WHERE warn_id = ?", (warnNumb, ))
                    connection.commit()
                    embed_var = discord.Embed(title="Warning Deleted",description=f"Warning #{warnNumb} was deleted by {ctx.author}", color=0x2ecc71)
                await ctx.send(embed=embed_var)
                found = True
                break
            if not found:
                await ctx.send("Warning number not found.")
            else:
                await ctx.send("Member not found.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot)) #Adding this cog to the main bot.

  
