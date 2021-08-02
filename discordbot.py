from discord.ext import tasks, commands
import discord
import json
import os
import asyncio
import time

if not os.path.isfile('settings.json'):
    with open('settings.json', 'w') as f:
        json.dump({
            "servers": {}
        }, f)


def get_settings():
    with open('settings.json', 'r') as f:
        return json.load(f)


def add_user(guild_id, userID):
    settings = get_settings()
    
    if str(guild_id) not in settings:
        settings[str(guild_id)] = []
    
    if str(userID) not in settings['channels'][str(guild_id)]:
        settings['servers'][str(guild_id)].append(str(userID))

        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    return False

def remove_user(guild_id, userID):
    settings = get_settings()
    if str(guild_id) not in settings['channels']:
        settings['servers'][str(guild_id)] = []

    settings['servers'][str(guild_id)].remove(str(userID))

    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)


def getSuccessEmbed(Msg):
    embed = discord.Embed(color=0x00ff00)
    embed.set_author(name='Success')
    embed.description = Msg
    return embed


def getErrorEmbed(errMsg):
    embed = discord.Embed(color=0xFF0000)
    embed.set_author(name='Error')
    embed.description = errMsg
    return embed


"""
=========================================
    Setup
=========================================
"""
command_prefix = '!'
BOT_TOKEN = os.environ['TOKEN']


def run(client):
    client.run(BOT_TOKEN, bot=True)


client = commands.Bot(command_prefix=command_prefix, fetch_offline_members=False)

"""
=========================================
    Events
=========================================
"""


@client.event
async def on_ready():
    print('Discord bot is ready.')
    start = time.time()
    current = start

    while True:
        await asyncio.sleep(1)
        current += 1

        if current - start >= 17959:
            raise KeyboardInterrupt

"""
=========================================
    Commands
=========================================
"""


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')



@client.command(aliases=["rotate"])
async def rotate_toggle(ctx):
    if (add_user(str(ctx.message.channel.guild.id), str(ctx.author.id))):
        await ctx.send(embed=getSuccessEmbed("Successfully added you."))
    else:
        remove_user(str(ctx.message.channel.guild.id), str(ctx.author.id))
        await ctx.send(embed=getSuccessEmbed("Successfully removed you."))

@client.command()
async def exit(ctx):
    raise KeyboardInterrupt

    
"""
=========================================
    Events
=========================================
"""

@tasks.loop(seconds=2)
async def change_nicknames():
    print("task")
    guild = client.get_guild(737724143126052974)
    member = guild.get_member(674710789138939916)
    await member.edit(nick="ezdl sucks")
if __name__ == '__main__':
    run(client)
