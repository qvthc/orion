#     ___     ___     ___     ___    _  _              ___     ___     _        ___    ___     ___    _____  
#    / _ \   | _ \   |_ _|   / _ \  | \| |     o O O  / __|   | __|   | |      | __|  | _ )   / _ \  |_   _| 
#   | (_) |  |   /    | |   | (_) | | .` |    o       \__ \   | _|    | |__    | _|   | _ \  | (_) |   | |   
#    \___/   |_|_\   |___|   \___/  |_|\_|   TS__[O]  |___/   |___|   |____|  _|_|_   |___/   \___/   _|_|_  
#  _|"""""|_|"""""|_|"""""|_|"""""|_|"""""| {======|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""| 
#   `-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 

import discord, json, asyncio, datetime
from discord.ext import commands

client = commands.Bot(command_prefix=">", self_bot=True)

@client.event()
async def on_ready():
  print("Logged into the account!")

@client.command()
async def ping(ctx):
  await ctx.send(f"🏓 Pong! | {ctx.channel.mention} | {ctx.author.mention}")



client.run("")
