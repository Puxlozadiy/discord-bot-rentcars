# coding=utf-8
from time import daylight
import discord
from discord import channel
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, date, time, timedelta


async def checkDate(bot):
    channel = bot.get_channel(916563929612820512) # бухгалтерия Rico и Hurick
    channel1 = bot.get_channel(923215838675341333) # бухгалтерия Nick
    channel2 = bot.get_channel(923275886697021500) # бухгалтерия Kapsul
    channel3 = bot.get_channel(923882650417115177) # бухгалтерия Conqueror
    channel4 = bot.get_channel(924437573898731600) # бухгалтерия Conqueror
    async for messages in channel.history(limit=2):
        if messages.author.id == 916504100470947890:
            await checkDateProcess(messages, 916563929612820512, 1, bot)
            break
    async for messages in channel1.history(limit=2):
        if messages.author.id == 916504100470947890:
            await checkDateProcess(messages, 923215838675341333, 2, bot)
            break
    async for messages in channel2.history(limit=2):
        if messages.author.id == 916504100470947890:
            await checkDateProcess(messages, 923275886697021500, 3, bot)
            break
    async for messages in channel3.history(limit=2):
        if messages.author.id == 916504100470947890:
            await checkDateProcess(messages, 923882650417115177, 4, bot)
            break
    async for messages in channel4.history(limit=2):
        if messages.author.id == 916504100470947890:
            await checkDateProcess(messages, 924437573898731600, 5, bot)
            break

async def checkDateProcess(messages, channel_id, member, bot):
    try:
        channel = bot.get_channel(channel_id)
        bool = 0
        text = messages.content
        day = ''
        month = ''
        year = ''
        for symbol in text.split()[0]:
            if bool == 0 and symbol.isdigit():
                day += symbol
            elif bool == 0 and symbol == '.':
                bool = 1
            elif bool == 1 and symbol.isdigit():
                month += symbol
            elif bool == 1 and symbol == '.':
                bool = 2
            elif bool == 2 and symbol.isdigit():
                year += symbol
        now = datetime.now()
        dt = datetime(year=int(year), month=int(month), day=int(day))
        if (now.year == dt.year):
            if now.month == dt.month:
                if now.day > dt.day:
                    await sendMoney(member, channel)
            elif now.month > dt.month:
                await sendMoney(member, channel)
        elif now.year > dt.year:
            await sendMoney(member, channel)
    except:
        print('Что-то пошло не так при провкерке даты checkDate()')

async def sendMoney(member, channel):
    now = datetime.now()
    if member == 1:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Rico заработал $0")
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Hurick заработал $0")
    elif member == 2:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Nick заработал $0")
    elif member == 3:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Kapsul заработал $0")
    elif member == 4:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Conqueror заработал $0")
    elif member == 5:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Tovsali заработал $0")