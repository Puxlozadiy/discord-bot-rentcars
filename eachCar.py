# coding=utf-8
from time import daylight
import discord
from discord import channel
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, date, time, timedelta

async def eachCar(bot, message_id, string, user_id, channel_id, view):
    channel = bot.get_channel(channel_id)
    message = channel.get_partial_message(message_id)
    message = await message.fetch()
    text = message.content
    if (text.split()[4] == 'Занят'):
        if (text.split()[6] == 'рестарта'):
            now = datetime.now()
            dt = datetime(1, 1, 1, 7, 0, 0).time()
            rsdt = text.split()[7]
            day = ''
            month = ''
            bool = 0
            for symbol in rsdt:
                if bool == 0 and symbol.isdigit():
                    day += symbol
                elif bool == 0 and symbol == '.':
                    bool = 1
                elif bool == 1:
                    month += symbol
            dt1 = datetime(1, int(month), int(day), 7, 0, 0)
            if (now.month == dt1.month):
                if (now.day >= dt1.day):
                    if now.time() > dt:
                        channel = bot.get_channel(channel_id)
                        message = channel.get_partial_message(message_id)
                        await message.edit(content=f"```{string} - Свободен ```", view=view[0])
            elif (now.month > dt1.month):
                channel = bot.get_channel(channel_id)
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Свободен ```", view=view[0])

        else:
            time = text.split()[6]
            date = text.split()[7]
            days = ''
            months = ''
            hours = ''
            minutes = ''
            bool = 0
            for symbol in time:
                if bool == 0 and symbol.isdigit():
                    hours += symbol
                elif bool == 0 and symbol == ':':
                    bool = 1
                elif bool == 1:
                    minutes += symbol
            bool = 0
            for symbol in date:
                if bool == 0 and symbol.isdigit():
                    days += symbol
                elif bool == 0 and symbol == '.':
                    bool = 1
                elif bool == 1:
                    months += symbol
            dt = datetime(year=1, month=int(months), day=int(
                days), hour=(int(hours)), minute=int(minutes))
            dt = dt - timedelta(hours=1)
            if datetime.now().day == dt.day and datetime.now().month == dt.month:
                if datetime.now().time() > dt.time():
                    myid = f'<@{user_id}>'
                    message = channel.get_partial_message(message_id)
                    await message.edit(content=f"```{string} - Ожидается освобождение ```", view=view[1])
                    await channel.send(f"{myid}\n```{string} - Ожидается освобождение ```")
            if datetime.now().day > dt.day and datetime.now().month == dt.month:
                myid = f'<@{user_id}>'
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Ожидается освобождение ```", view=view[1])
                await channel.send(f"{myid}\n```{string} - Ожидается освобождение ```")
            elif datetime.now().month > dt.month:
                myid = f'<@{user_id}>'
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Ожидается освобождение ```", view=view[1])
                await channel.send(f"{myid}\n```{string} - Ожидается освобождение ```")