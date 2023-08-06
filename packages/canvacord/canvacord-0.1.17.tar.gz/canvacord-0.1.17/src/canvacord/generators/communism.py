from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor
import asyncio
import aiohttp
from random import randint
from io import BytesIO
import discord
from typing import Union

async def getavatar(user: Union[discord.User, discord.Member]) -> bytes:
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    async with session.get(str(user.avatar_url)) as response:
        avatarbytes = await response.read()
    await session.close()
    return avatarbytes

async def getbackground(background):
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    async with session.get("https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fcommunism.gif?v=1628348497336") as response:
        backgroundbytes = await response.read()
    await session.close()
    return backgroundbytes

async def communism(user):
        avatar = Image.open(BytesIO(await getavatar(user))).resize((300, 300)).convert('RGBA')
        img2 = Image.open(BytesIO(await getbackground()))
        img1.putalpha(96)

        out = []
        for i in range(0, img2.n_frames):
            img2.seek(i)
            f = img2.copy().convert('RGBA').resize((300, 300))
            f.paste(img1, (0, 0), img1)
            out.append(f.resize((256, 256)))

        b = BytesIO()
        out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=40)
        img2.close()
        b.seek(0)
        return b