#!/python

# 
#    ,-,--.    _,.---._                ,---.                   .=-.-.  ,-,--.  
#  ,-.'-  _\ ,-.' , -  `.    _.-.    .--.'  \      .-.,.---.  /==/_ /,-.'-  _\ 
# /==/_ ,_.'/==/_,  ,  - \ .-,.'|    \==\-/\ \    /==/  `   \|==|, |/==/_ ,_.' 
# \==\  \  |==|   .=.     |==|, |    /==/-|_\ |  |==|-, .=., |==|  |\==\  \    
#  \==\ -\ |==|_ : ;=:  - |==|- |    \==\,   - \ |==|   '='  /==|- | \==\ -\   
#  _\==\ ,\|==| , '='     |==|, |    /==/ -   ,| |==|- ,   .'|==| ,| _\==\ ,\  
# /==/\/ _ |\==\ -    ,_ /|==|- `-._/==/-  /\ - \|==|_  . ,'.|==|- |/==/\/ _ | 
# \==\ - , / '.='. -   .' /==/ - , ,|==\ _.\=\.-'/==/  /\ ,  )==/. /\==\ - , / 
#  `--`---'    `--`--''   `--`-----' `--`        `--`-`--`--'`--`-`  `--`---'  
#

# THIS IS DISCONTINUED UNTIL FURTHER NOTICE!


import discord, json, asyncio, datetime, requests, httpx, pytube, sys, subprocess
from discord.ext import commands
from pytube import YouTube

##################################### TERMINAL #######

bash_script_path = './term.sh'
subprocess.run(['bash', bash_script_path], check=True)

##################################### ARGUMENTS ######

botPrefix = sys.argv[1]
botToken = sys.argv[2]
urban_dictionary = "https://api.urbandictionary.com/v0/define"

client = commands.Bot(command_prefix=botPrefix, self_bot=True)

gifs = {}
servers = {}

##################################### FUNCTIONS ######

async def yes(message):
  await message.add_reaction("✅")

async def no(message):
  await message.add_reaction("❌")

async def delete(message):
  await message.delete()

################################# SELFBOT CODE #######

@client.command()
async def ping(ctx):
  await ctx.send(f"🏓 Pong!")

@client.command()
async def nickname(ctx, *, newname: str = ""):
    if newname == "":
        try:
            await ctx.author.edit(nick=None)
            await yes(ctx.message)
        except discord.Forbidden:
            await no(ctx.message)
    else:
        try:
            await ctx.author.edit(nick=newname)
            await yes(ctx.message)
        except (discord.Forbidden, discord.NotFound, discord.HTTPException, discord.ClientException) as e:
            await no(ctx.message)

@client.command()
async def mod(ctx, type: str, user: discord.Member):
    if ctx.channel is not None:
        modtype = type.lower()
    
        if modtype == "ban":
            await user.ban()
    
        if modtype == "kick":
            await user.kick()

        if modtype == "unban":
            await user.unban()
    else:
        await no(ctx.message)

@client.command()
async def purge(ctx, delete_amount: int):
    deleted_count = 0
    async for message in ctx.channel.history(limit=None):
        if deleted_count >= delete_amount:
            break

        if message.author.id == ctx.author.id:
            await message.delete()
            deleted_count += 1
            await asyncio.sleep(1)

@client.command()
async def addgif(ctx, name, link):
    gifs[name] = link
    await yes(ctx.message)

@client.command()
async def gif(ctx, name):
    if name in gifs:
        await ctx.send(gifs[name])
        await ctx.message.delete()
    else:
        await no(ctx.message)

@client.command()
async def addserver(ctx, name, link):
    servers[name] = link
    await yes(ctx.message)

@client.command()
async def server(ctx, name):
    if name in servers:
        await yes(ctx.message)
        await ctx.send(servers[name])
    else:
        await no(ctx.message) 

@client.command()
async def dm(ctx, id: int, *, message: str):
   try:
      user = await client.fetch_user(id)
      await user.send(message)
      await yes(ctx.message)
   except discord.Forbidden:
      await no(ctx.message)

@client.command()
async def dictionary(ctx, *, word: str):
    params = {"term": word}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(urban_dictionary, params=params)
            response.raise_for_status()
            data = response.json()
            definitions = data.get("list", [])
            if definitions:
                first_definition = definitions[0]
                definition = first_definition.get("definition", "No definition found.")
                example = first_definition.get("example", "No example found.")
                await ctx.send(f"**{word.capitalize()}**\nDefinition: {definition}\nExample: {example}")
            else:
                await ctx.send(f"No definitions found for {word}.")
        except httpx.HTTPError:
            await ctx.send("Failed to fetch word definition from Urban Dictionary API.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

@client.command()
async def youtube(ctx, url):
    if not url:
        await ctx.send("Please provide a YouTube video URL.")
        return
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        file_path = 'downloads/downloaded_video.mp4'

        video_stream.download(output_path='downloads', filename='downloaded_video.mp4')

        await ctx.send(file=discord.File(file_path))
    except Exception as e:
        await no()

@client.command()
async def message(ctx, num: int, *, msg: str):
    await ctx.message.delete()
    for i in range(num):
        try:
            await ctx.send(msg)
            await asyncio.sleep(.75)
        except discord.Forbidden:
            pass

@client.command()
async def leave(ctx):
    await ctx.guild.leave()

@client.command()
async def membercount(ctx):
    guild = ctx.guild
    memberCount = guild.member_count
    await ctx.send(f"{memberCount} members")
    await yes(ctx.message)

@client.command()
async def leavegroup(ctx):
    if isinstance(ctx.channel, discord.GroupChannel):
        try:
            await ctx.channel.leave()
        except discord.Forbidden:
            await no(ctx.message)

@client.command()
async def leavegroups(ctx):
    for channel in client.private_channels:
        if isinstance(channel, discord.GroupChannel):
            await channel.leave()

@client.command()
async def kickgroup(ctx):
    if isinstance(ctx.message.channel, discord.GroupChannel):
        for recipient in ctx.message.channel.recipients:
            try:
                await ctx.message.channel.remove_recipients(recipient)
            except discord.Forbidden:
                pass

@client.command()
async def walloftext(ctx, count: int):
    def wall(lines):
        if lines <= 0:
            return ""
    
        pattern = "** **\n" * lines
        return pattern
    
    await ctx.message.delete()
    await ctx.send(wall(count))

@client.command()
async def fetchpfp(ctx, userid: int):
    if userid == None:
        await no(ctx.message)
    await yes(ctx.message)
    member = await client.fetch_user(userid)
    pfp = member.avatar_url
    await ctx.send(pfp)

@client.command()
async def channelid(ctx):
    try:
        await ctx.send(ctx.channel.id)
        await yes(ctx.message)
    except discord.Forbidden:
        await no(ctx.message)

@client.command()
async def userid(ctx, user: discord.Member):
    try:
        await ctx.send(user.id)
        await yes(ctx.message)
    except discord.Forbidden:
        await no(ctx.message)

@client.command()
async def serverinfo(ctx):
    server = ctx.guild
    roles = server.roles
    bot_count = len([member for member in server.members if member.bot])
    server_icon_link = str(server.icon_url)
    server_banner_link = str(server.banner_url) if server.banner_url else "None"
    server_boosts = server.premium_subscription_count

    contents = f"""
## Info for {server.name}
{ctx.author.name} / {ctx.author.id}
```    
MEMBERS
{server.member_count}
    
ROLES
{len(roles)}
    
BOTS
{bot_count}
    
SERVER ICON LINK
{server_icon_link}
    
SERVER BANNER LINK
{server_banner_link}
    
SERVER BOOSTS
{server_boosts}
```
    """
    await ctx.send(contents)



####################################### LOGIN ########
client.run(botToken, bot=False)
