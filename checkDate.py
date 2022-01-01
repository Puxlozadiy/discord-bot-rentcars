# coding=utf-8
from time import daylight
import discord
from discord import channel
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, date, time, timedelta
from access import access_list


async def checkDate(bot):
    for user in access_list:
        channel = bot.get_channel(user[0][2])
        async for messages in channel.history(limit=2):
            if messages.author.id == 916504100470947890:
                await checkDateProcess(messages, user[0][2], user[0][3], bot, user[0][4])
                break


async def checkDateProcess(messages, channel_id, member, bot, name):
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
                    await sendMoney(member, channel, name)
            elif now.month > dt.month:
                await sendMoney(member, channel, name)
        elif now.year > dt.year:
            await sendMoney(member, channel, name)
    except:
        print('Что-то пошло не так при провкерке даты checkDate()')

async def sendMoney(member, channel, name):
    now = datetime.now()
    if member == 0:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - {name} заработал $0")
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - Hurick заработал $0")
    elif member == 1:
        None
    else:
        await channel.send(content=f"{now.day}.{now.month}.{now.year} - {name} заработал $0")