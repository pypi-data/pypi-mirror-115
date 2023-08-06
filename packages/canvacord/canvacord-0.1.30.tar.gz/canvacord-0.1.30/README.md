[![Discord](https://discord.com/api/guilds/872291125547921459/embed.png)](https://discord.gg/mPU3HybBs9)
[![PyPi](https://img.shields.io/pypi/v/canvacord.svg)](https://pypi.org/project/canvacord)
[![Python](https://img.shields.io/pypi/pyversions/dislash.py.svg)](https://pypi.python.org/pypi/canvacord)

A copy of [canvacord](https://www.npmjs.com/package/canvacord) made in python!



# Table of contents
1. [Installation](#installation)
2. [Examples](#examples)
3. [Creating Images](#creating-images)
4. [Links](#links)
5. [Downloads](#downloads)

# Installation

Run any of these commands in terminal:

Mac / Linux
```
pip install canvacord
```

Windows
```
python -m pip install canvacord
```

# Examples
💡 This library requires **[discord.py](https://github.com/Rapptz/discord.py)**.


## Creating-Images

```python
import discord
from discord.ext import commands
import canvacord

client = commands.Bot(command_prefix="!")

@client.comand()
async def rankcard(ctx):
    user = ctx.author
    username = ctx.author.name + "#" + ctx.author.discriminator
    currentxp = 1
    lastxp = 0
    nextxp = 2
    current_level = 1
    current_rank = 1
    background = None
    image = await canvacord.rankcard(user=user, username=username, currentxp=currentxp, lastxp=lastxp, nextxp=nextxp, level=current_level, rank=current_rank, background=background)
    file = discord.File(filename="rankcard.png", fp=image)
    await ctx.send(file=file)

@client.comand()
async def triggered(ctx):
    user = ctx.author
    image = await canvacord.trigger(user)
    file = discord.File(filename="triggered.gif", fp=image)
    await ctx.send(file=file)

@client.comand()
async def communism(ctx):
    user = ctx.author
    image = await canvacord.communism(user)
    file = discord.File(filename="communism.gif", fp=image)
    await ctx.send(file=file)

@client.comand()
async def jail(ctx):
    user = ctx.author
    image = await canvacord.jail(user)
    file = discord.File(filename="jail.png", fp=image)
    await ctx.send(file=file)

@client.comand()
async def gay(ctx):
    user = ctx.author
    image = await canvacord.gay(user)
    file = discord.File(filename="gay.png", fp=image)
    await ctx.send(file=file)

@client.comand()
async def hitler(ctx):
    user = ctx.author
    image = await canvacord.hitler(user)
    file = discord.File(filename="hitler.png", fp=image)
    await ctx.send(file=file)

@client.comand()
async def spank(ctx):
    user1 = ctx.author
    user2 = ctx.author
    image = await canvacord.spank(user1, user2)
    file = discord.File(filename="spank.png", fp=image)
    await ctx.send(file=file)
    
client.run("BOT_TOKEN")
```


# Links
[![Discord](https://discord.com/api/guilds/872291125547921459/embed.png)](https://discord.gg/mPU3HybBs9)
[![PyPi](https://img.shields.io/pypi/v/canvacord.svg)](https://pypi.org/project/canvacord)


# Downloads


[![Downloads](https://pepy.tech/badge/canvacord)](https://pepy.tech/project/canvacord)
[![Downloads](https://pepy.tech/badge/canvacord/month)](https://pepy.tech/project/canvacord)
![Downloads](https://pepy.tech/badge/canvacord/week)
