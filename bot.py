#
#
#
#                                                                       
#                                                    88           88                                   
#                                ,d                 ""           88                            ,d     
#                                88                              88                            88     
#                                MM88MMM  8b,dPPYba,  88   ,adPPYb,88   ,adPPYba,  8b,dPPYba,  MM88MMM  
#                                88     88P'   "Y8  88  a8"    `Y88  a8P_____88  88P'   `"8a   88     
#                                88     88          88  8b       88  8PP"""""""  88       88   88     
#                                88,    88          88  "8a,   ,d88  "8b,   ,aa  88       88   88,    
#                                "Y888  88          88   `"8bbdP"Y8   `"Ybbd8"'  88       88   "Y888
#
#                                                   </free discord selfbot>
#                                                        by david <3
#
#


#                                                        •           
#                                                        ┓┏┳┓┏┓┏┓┏┓╋┏
#                                                        ┗┛┗┗┣┛┗┛┛ ┗┛
#                                                           ┛       

import discord, json, asyncio, datetime, requests, httpx, pytube, sys, subprocess, pytz
from discord.ext import commands, tasks
from datetime import datetime
from pytube import YouTube

#                                                              •    ┓
#                                                       ╋┏┓┏┓┏┳┓┓┏┓┏┓┃
#                                                       ┗┗ ┛ ┛┗┗┗┛┗┗┻┗

bash_script_path = './cosmetic/term.sh'
subprocess.run(['bash', bash_script_path], check=True)

#                                                      ┏┓┏┓┏┓┓┏┏┳┓┏┓┏┓╋┏
#                                                      ┗┻┛ ┗┫┗┻┛┗┗┗ ┛┗┗┛
#                                                          ┛           

timeZone = "US/Eastern"
botPrefix = sys.argv[1]
botToken = sys.argv[2]
urban_dictionary = "https://api.urbandictionary.com/v0/define"
controlServer = "replace_with_a_webhook_for_logs"
client = commands.Bot(command_prefix=botPrefix, self_bot=True)









###########################################################################################################################################

gifs = {}
servers = {}

def log(msg):
    headers = {'Content-Type': 'application/json'}
    embed = {
        'description': msg,
        'color': 0x262731,
    }

    payload = {'embeds': [embed]}
    response = requests.post(controlServer, headers=headers, data=json.dumps(payload))

async def yes(message):
  await message.add_reaction("✅")

async def no(message):
  await message.add_reaction("❌")

async def delete(message):
  await message.delete()

def get_time():
    timezone = pytz.timezone(timeZone)

    utc_now = datetime.utcnow()

    timez = utc_now.replace(tzinfo=pytz.utc).astimezone(timezone)
    time = timez.strftime('%I:%M %p')

    return time


@client.event
async def on_ready():
    status_strings = [
        "🔱 Trident Client - v16",
        "💻 {guild_count} guilds",
        "🫂 {friend_count} friends"
    ]
    # ^^^^ dont remove it, took me very long :sob:
    current_status_index = 0

    @tasks.loop(seconds=5)
    async def change_status():
        nonlocal current_status_index
        status_text = status_strings[current_status_index].format(
            guild_count=len(client.guilds),
            friend_count=len(client.user.friends)
        )
        content = {
            "custom_status": {"text": status_text}
        }
        requests.patch("https://ptb.discordapp.com/api/v6/users/@me/settings", headers={"authorization": botToken}, json=content)

        current_status_index = (current_status_index + 1) % len(status_strings)

    change_status.start()

    @client.event
    async def on_disconnect():
        change_status.stop()


@client.command()
async def ping(ctx):
  await ctx.reply(f"🏓 Pong!")

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
            log(f"Nickname set to {newname} | **{get_time()}**")
        except (discord.Forbidden, discord.NotFound, discord.HTTPException, discord.ClientException) as e:
            log(f"An error occured while setting a nickname. | **{get_time()}**")
            await no(ctx.message)

@client.command()
async def mod(ctx, type: str, user: discord.Member):
    if ctx.channel is not None:
        modtype = type.lower()
    
        if modtype == "ban":
            await user.ban()
            await yes(ctx.message)
    
        if modtype == "kick":
            await user.kick()
            await yes(ctx.message)

        if modtype == "unban":
            await user.unban()
            await yes(ctx.message)
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
        await yes(ctx.message)
    log(f"Purged {delete_amount} messages in {ctx.channel.mention} | **{get_time()}**")

@client.command()
async def addlink(ctx, name, link=None):
    if ctx.message.reference and ctx.message.reference.cached_message:
        referenced_message = ctx.message.reference.cached_message
        if referenced_message.content.startswith("http"):
            link = referenced_message.content
            name = name.lower()
    else:
        if link is None:
            await no(ctx.message)
            return

    gifs[name] = link
    await yes(ctx.message)

@client.command()
async def link(ctx, name):
    if name in gifs:
        await ctx.send(gifs[name])
        await ctx.message.delete()
    else:
        await no(ctx.message)

@client.command()
async def links(ctx):
    if gifs:
        links_message = "```\n"
        for name, link in gifs.items():
            links_message += f"{name}: {link}\n"
        links_message += "\n```"
        await yes(ctx.message)
        await ctx.send(links_message)
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
                await ctx.reply(f"> {word.capitalize()}\nDefinition: {definition}\nExample: {example}")
            else:
                await no(ctx.message)
        except httpx.HTTPError:
            await no(ctx.message)
        except Exception as e:
            await no(ctx.message)

@client.command()
async def youtube(ctx, url):
    if not url:
        await no(ctx.message)
        return
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        file_path = 'downloads/downloaded_video.mp4'

        video_stream.download(output_path='downloads', filename='downloaded_video.mp4')

        await ctx.reply(file=discord.File(file_path))
        await yes(ctx.message)
        log(f"[YouTube Video]({url}) has been downloaded. | **{get_time()}**")
    except Exception as e:
        await no(ctx.message)


import base64
@client.command()
async def base64_encode(ctx, *, string: str):
    encoded_text = base64.b64encode(string.encode()).decode()
    await ctx.reply(encoded_text, mention_author=False)
    await yes(ctx.message)
    await ctx.message.delete()

@client.command()
async def base64_decode(ctx, *, string: str):
    try:
        encoded_text = base64.b64decode(string.encode()).decode()
        await ctx.reply(encoded_text, mention_author=False)
        try:
            await yes(ctx.message)
        except:
            pass
        await ctx.message.delete()
    except:
        try:
            await no(ctx.message)
        except:
            pass

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
    log(f"The guild **{ctx.guild.name}** has been removed. | **{get_time()}**")
    await ctx.guild.leave()

@client.command()
async def membercount(ctx):
    guild = ctx.guild
    memberCount = guild.member_count
    await ctx.reply(f"{memberCount} members")
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
    await yes(ctx.message)
    log(f"All groups have been left. | **{get_time()}**")


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
    await ctx.reply(pfp)

@client.command()
async def channelid(ctx):
    try:
        await ctx.reply(ctx.channel.id)
        await yes(ctx.message)
    except discord.Forbidden:
        await no(ctx.message)

@client.command()
async def userid(ctx, user: discord.Member):
    try:
        await ctx.reply(user.id)
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
    await ctx.reply(contents)

autoresponder_string = None
sent_messages = {}

@client.command()
async def autoresponder(ctx, *, strings):
    global autoresponder_string, sent_messages
    string = f"""
*Autoresponder - Active since **{get_time()}***

{strings}
"""
    if strings.lower() != "off":
        autoresponder_string = string
    else:
        autoresponder_string = "off"

    sent_messages = {}
    await yes(ctx.message)
    log(f"Autoresponder has been changed/activated. | **{get_time()}**")

@client.event
async def on_message(message):
    await client.process_commands(message)

    global autoresponder_string, sent_messages
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        user_id = message.author.id

        if autoresponder_string and autoresponder_string != "off" and user_id not in sent_messages:
            await message.channel.send(autoresponder_string)
            sent_messages[user_id] = True
            log(f"Autoresponder triggered for {message.author.mention} @ {message.jump_url} | **{get_time()}**")

calories = 0
protein = 0

@client.command()
async def track(ctx, type: str, amount: int = 1):
    global calories
    global protein

    type_of_request = type.lower()
    if type_of_request == "cal" or type_of_request == "calories":
        calories = calories + amount
        await yes(ctx.message)

    if type_of_request == "protein":
        protein = protein + amount
        await yes(ctx.message)

    if type_of_request == "clear" or type_of_request == "wipe" or type_of_request == "new":
        calories = 0
        protein = 0

    if type_of_request == "summary" or type_of_request == "today" or type_of_request == "total" or type_of_request == "list":
        await ctx.reply(f"""
## Diet Tracker
**{calories}** calories | **{protein}**g protein
""")


import os

@client.command()
async def upload(ctx, name):
    if not ctx.message.attachments:
        await no(ctx.message)
        return

    attachment = ctx.message.attachments[0]
    file_path = os.path.join("files", name)

    await attachment.save(file_path)
    await yes(ctx.message)

@client.command()
async def send(ctx, name):
    file_path = os.path.join("files", name)

    if os.path.exists(file_path):
        file = discord.File(file_path)
        await ctx.send(file=file)
    else:
        await no(ctx.message)

@client.command()
async def uploads(ctx):
    files_directory = "files"
    files_list = [f for f in os.listdir(files_directory) if os.path.isfile(os.path.join(files_directory, f))]
    
    files_formatted = "\n".join(files_list)
    response = f"```\n{files_formatted}\n```"

    await ctx.send(response)









####################################### LOGIN ########
client.run(botToken, bot=False)

