from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor
import asyncio
import aiohttp
import datetime
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

def wrap(font, text, line_width):
    words = text.split()

    lines = []
    line = []

    for word in words:
        newline = ' '.join(line + [word])

        w, h = font.getsize(newline)

        if w > line_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)

    if line:
        lines.append(' '.join(line))

    return ('\n'.join(lines)).strip()

def render_text_with_emoji(img, draw, coords:tuple()=(0, 0), text='', font: ImageFont='', fill='black'):
    initial_coords = coords
    emoji_size = font.getsize(text)[1]

    emoji_set = 'twemoji'
    if emoji_set == 'apple':
        emojis = os.listdir('assets/emoji')
        for i in range(0, len(text)):
            char = text[i]
            if char == '\n':
                coords = (initial_coords[0], coords[1] + emoji_size)
            emoji = str(hex(ord(char))).upper().replace('0X', 'u')
            if i + 1 <= len(text) and emoji + '.png' not in emojis and emoji + '.0.png' in emojis:
                emoji = emoji + '.0'
            try:
                u_vs = str(hex(ord(text[i + 1]))).upper().replace('0X', 'u')
                try:
                    u_zws = str(hex(ord(text[i+2]))).upper().replace('0X', 'u')
                    if u_vs == 'uFE0F' and u_zws == 'u200D':
                        emoji = emoji + '_' + str(hex(ord(text[i + 3]))).upper().replace('0X', 'u')
                        try:
                            text = text.replace(text[i + 3], '‍', 1)
                        except IndexError:
                            pass
                except IndexError:
                    pass
                if emoji + '_' + u_vs + '.png' in emojis:
                    emoji = emoji + '_' + u_vs
                    text = text.replace(text[i + 1], '‍', 1)
                if u_vs == 'u1F3FB':
                    emoji = emoji + '.1'
                    text = text.replace(text[i + 1], '‍', 1)
                elif u_vs == 'u1F3FC':
                    emoji = emoji + '.2'
                    text = text.replace(text[i + 1], '‍', 1)
                elif u_vs == 'u1F3FD':
                    emoji = emoji + '.3'
                    text = text.replace(text[i + 1], '‍', 1)
                elif u_vs == 'u1F3FE':
                    emoji = emoji + '.4'
                    text = text.replace(text[i + 1], '‍', 1)
                elif u_vs == 'u1F3FF':
                    emoji = emoji + '.5'
                    text = text.replace(text[i + 1], '‍', 1)
                elif emoji == 'uFE0F' or emoji == 'u200D':
                    continue
            except IndexError:
                pass
            if emoji == 'u200D':
                pass
            elif emoji + '.png' not in emojis:
                size = draw.textsize(char, font=font)
                draw.text(coords, char, font=font, fill=fill)
                coords = (coords[0] + size[0], coords[1])
            else:
                emoji_img = Image.open(f'assets/emoji/{emoji}.png').convert('RGBA').resize((emoji_size, emoji_size), Image.LANCZOS)
                img.paste(emoji_img, (coords[0], coords[1] + 4), emoji_img)
                coords = (coords[0] + emoji_size + 4, coords[1])
    elif emoji_set == 'twemoji':
        emojis = os.listdir('assets/twemoji')
        for i in range(0, len(text)):
            char = text[i]
            if char == '\n':
                coords = (initial_coords[0], coords[1] + emoji_size)
            emoji = str(hex(ord(char))).replace('0x', '')
            if i + 1 <= len(text) and emoji + '.png' not in emojis and emoji + '.0.png' in emojis:
                emoji = emoji + '.0'
            try:
                u_vs = str(hex(ord(text[i + 1]))).replace('0x', '')
                try:
                    u_zws = str(hex(ord(text[i + 2]))).replace('0x', '')
                    if u_vs == 'fe0f' and u_zws == '200d':
                        emoji = emoji + '-' + u_vs + '-' + u_zws + '-' + str(hex(ord(text[i + 3]))).replace('0x', '')
                        try:
                            text = text.replace(text[i + 3], '‍', 1)
                        except IndexError:
                            pass
                except IndexError:
                    pass
                if emoji + '-' + u_vs + '.png' in emojis:
                    emoji = emoji + '-' + u_vs
                    text = text.replace(text[i + 1], '‍', 1)
                elif emoji == 'fe0f' or emoji == '200d':
                    continue
            except IndexError:
                pass
            if emoji == '200d':
                pass
            elif emoji + '.png' not in emojis:
                size = draw.textsize(char, font=font)
                draw.text(coords, char, font=font, fill=fill)
                coords = (coords[0] + size[0], coords[1])
            else:
                emoji_img = Image.open(f'assets/twemoji/{emoji}.png').convert('RGBA').resize((emoji_size, emoji_size),
                                                                                           Image.LANCZOS)
                img.paste(emoji_img, (coords[0], coords[1] + 4), emoji_img)
                coords = (coords[0] + emoji_size + 4, coords[1])


async def getbackground(background):
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    async with session.get("https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Ftrump.bmp?v=1628377870168") as response:
        backgroundbytes = await response.read()
    await session.close()
    return backgroundbytes

async def gettemplate(backtype):
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    if backtype == "font1":
        background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fsegoeuireg.ttf?v=1628378014273"
        async with session.get(str(background)) as response:
            backgroundbytes = await response.read()
    elif backtype == "font2":
        background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Frobotomedium.ttf?v=1628378016419"
        async with session.get(str(background)) as response:
            backgroundbytes = await response.read()
    elif backtype == "font3":
        background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Frobotoregular.ttf?v=1628378020634"
        async with session.get(str(background)) as response:
            backgroundbytes = await response.read()
    await session.close()
    return backgroundbytes

async def tweet(user, text):
        usernames = user.name
        avatar = Image.open(BytesIO(await getavatar(user))).resize((98, 98)).convert('RGBA')
        base = Image.open(BytesIO(await getbackground("tweet")))
        font = ImageFont.FreeTypeFont(BytesIO(await gettemplate("font1")), size=50, )
        font2 = ImageFont.FreeTypeFont(BytesIO(await gettemplate("font2")), size=40)
        font3 = ImageFont.FreeTypeFont(BytesIO(await gettemplate("font3")), size=29)
        font4 = ImageFont.FreeTypeFont(BytesIO(await gettemplate("font3")), size=35)

        circle = Image.new('L', (20, 20), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, 20, 20), fill=255)
        alpha = Image.new('L', avatar.size, 255)
        w, h = avatar.size
        alpha.paste(circle.crop((0, 0, 10, 10)), (0, 0))
        alpha.paste(circle.crop((0, 10, 10, 10 * 2)), (0, h - 10))
        alpha.paste(circle.crop((10, 0, 10 * 2, 10)), (w - 10, 0))
        alpha.paste(circle.crop((10, 10, 10 * 2, 10 * 2)), (w - 10, h - 10))
        avatar.putalpha(alpha)

        base.paste(avatar, (42, 38), avatar)
        canv = ImageDraw.Draw(base)
        text2 = wrap(font2, usernames, 1150)
        tag_raw = str(usernames)
        text3 = wrap(font3, f'@{tag_raw}', 1150)

        time = datetime.datetime.now().strftime('%-I:%M %p - %d %b %Y')
        retweets = "{:,}".format(randint(0, 99999))
        likes = "{:,}".format(randint(0, 99999))
        text4 = wrap(font3, time, 1150)
        text5 = wrap(font4, retweets, 1150)
        text6 = wrap(font4, likes, 1150)
        total_size = (45, 160)
        for i in text.split(' '):
            i += ' '
            if i.startswith(('@', '#')):
                if total_size[0] > 1000:
                    total_size = (45, total_size[1] + 65)
                #render_text_with_emoji(base, canv, total_size, i, font=font, fill='#1b95e0')
                y = canv.textsize(i, font=font)
                total_size = (total_size[0] + y[0], total_size[1])
            else:
                if total_size[0] > 1000:
                    total_size = (45, total_size[1] + 65)
                #render_text_with_emoji(base, canv, total_size, i, font=font, fill='Black')
                y = canv.textsize(i, font=font)
                total_size = (total_size[0] + y[0], total_size[1])
        #render_text_with_emoji(base, canv, (160, 45), text2, font=font2, fill='Black')
        #render_text_with_emoji(base, canv, (160, 95), text3, font=font3, fill='Grey')
        #render_text_with_emoji(base, canv, (40, 570), text4, font=font3, fill='Grey')
        #render_text_with_emoji(base, canv, (40, 486), text5, font=font4, fill='#2C5F63')
        #render_text_with_emoji(base, canv, (205, 486), text6, font=font4, fill='#2C5F63')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return b