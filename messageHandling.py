# coding=utf-8
from time import daylight
import discord
from discord import channel
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, date, time, timedelta
from noteMoney import noteMoney

async def messageHandling(bot, content, message_id, string, chooseCar, channel_id, log_channel, owner, view, buttonBool):  # принимает команды
    argument = content.split()[1]
    argument2 = 'Не известно'
    argument3 = 0
    try:
        argument2 = content.split()[2]
    except:
        argument2 = 0
    if content.split()[1] == 'продлили':
        try:
            argument3 = content.split()[3]
        except:
            None
    else:
        try:
            argument3 = content.split()[3]
        except:
            None

    if (argument == 'вернули' or argument == 'свободен'):
        try:
            channel = bot.get_channel(channel_id)
            msg_to_delete = 0
            async for messages in channel.history(limit=4):
                try:
                    message_arg = messages.content.splitlines()[1]
                    message_arg = message_arg.split()[2]
                    message_arg = message_arg[1:4]
                    if message_arg == content.split()[0][1:]:
                        if messages.content.split()[5] == 'Ожидается':
                            msg_to_delete = messages.id
                            message = channel.get_partial_message(msg_to_delete)
                            await message.delete()
                            break
                except:
                    None
            message = channel.get_partial_message(message_id)
            if buttonBool == 1:
                await message.edit(content=f"```{string} - Свободен ```", view=view[0])
            else:
                await message.edit(content=f"```{string} - Свободен ```")
        except:
            print('Что-то пошло не так при обработке запроса: вернули')
    elif (argument == 'продлили' or argument == 'продлить'):
        try:
            channel = bot.get_channel(channel_id)
            message = channel.get_partial_message(message_id)
            message = await message.fetch()
            text = message.content
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
            dt = datetime(year=1, month=int(months), day=int(days), hour=int(hours), minute=int(minutes))  # время из сообщения

            if (argument2.find('.') > 0):  # получение времени из аргумента
                hours = ''
                minutes = ''
                bool = 0
                for symbol in argument2:
                    if bool == 0 and symbol.isdigit():
                        hours += symbol
                    elif bool == 0 and symbol == '.':
                        bool = 1
                    elif bool == 1:
                        minutes += symbol
                dt = dt + timedelta(hours=int(hours), minutes=int(minutes))
                await noteMoney(bot, owner, 0, 0, chooseCar, argument3, 0)
                channel = bot.get_channel(channel_id)
                message = channel.get_partial_message(message_id)
                # продление формата hours.minutes
                if buttonBool == 1:
                    await message.edit(content=f'```{string} - Занят до {dt.hour}:{dt.minute} {dt.day}.{dt.month} ```', view=view[1])
                else:
                    await message.edit(content=f'```{string} - Занят до {dt.hour}:{dt.minute} {dt.day}.{dt.month} ```')
                channel = bot.get_channel(log_channel)
                await channel.send(f'```{string} - Продлили на {hours}:{minutes}. Новое время: {dt.hour}:{dt.minute}. ```')
            else:
                dt = dt + timedelta(hours=int(argument2))
                await noteMoney(bot, owner, 0, 0, chooseCar, argument3, 0)
                channel = bot.get_channel(channel_id)
                message = channel.get_partial_message(message_id)
                # продление формата hours
                if buttonBool == 1:
                    await message.edit(content=f'```{string} - Занят до {dt.hour}:{dt.minute} {dt.day}.{dt.month} ```', view=view[1])
                else:
                    await message.edit(content=f'```{string} - Занят до {dt.hour}:{dt.minute} {dt.day}.{dt.month} ```')
                channel = bot.get_channel(log_channel)
                await channel.send(f'```{string} - Продлили на {argument2} час(ов). Новое время: {dt.hour}:{dt.minute}. ```')
        except:
            print('Что-то пошло не так при обработке запроса: продлить')

    elif (argument != 'рестарт'):
        gmtdiff = 1
        if (argument.find('.') > 0):
            hours = ''
            minutes = ''
            bool = 0
            for symbol in argument:
                if bool == 0 and symbol.isdigit():
                    hours += symbol
                elif bool == 0 and symbol == '.':
                    bool = 1
                elif bool == 1:
                    minutes += symbol
            dt = datetime.now() + timedelta(hours=(int(hours) + gmtdiff), minutes=int(minutes))
            time = dt.strftime("%H:%M")
            await noteMoney(bot, owner, hours, minutes, chooseCar, 0, 0)
        else:
            dt = datetime.now() + timedelta(hours=(int(argument) + gmtdiff))
            time = dt.strftime("%H:%M")
            await noteMoney(bot, owner, argument, 0, chooseCar, 0, 0)
        date = datetime.now()
        if dt.time() < datetime.now().time():
            date = date + timedelta(days=1)
        channel = bot.get_channel(channel_id)
        message = channel.get_partial_message(message_id)
        if buttonBool == 1:
            await message.edit(content=f"```{string} - Занят до {time} {date.day}.{date.month} ```", view=view[1])
        else:
            await message.edit(content=f"```{string} - Занят до {time} {date.day}.{date.month} ```")
        channel = bot.get_channel(log_channel)
        # отправка лога
        if argument2 == 0:
            argument2 = 'Не известно'
        await channel.send(f"```{string} - Взяли до {time}. Взял: {argument2} ```")
        #except:
            #print('Что-то пошло не так при обработке запроса: время')
        
    elif argument == 'рестарт':
        try:
            channel = bot.get_channel(channel_id)
            message = channel.get_partial_message(message_id)
            if (datetime.now().hour <= 24 and datetime.now().hour > 7):
                dt = datetime.now() + timedelta(days=1)
                if buttonBool == 1:
                    await message.edit(content=f"```{string} - Занят до рестарта {dt.day}.{dt.month} ```", view=view[1])
                else:
                    await message.edit(content=f"```{string} - Занят до рестарта {dt.day}.{dt.month} ```")
                channel = bot.get_channel(log_channel)  # канал #логи
                # отправка лога
                await channel.send(f"```{string} - Взяли до рестарта {dt.day}.{dt.month}. Цена: {argument2} ```")
            elif (datetime.now().hour < 7 and datetime.now().hour >= 0):
                if buttonBool == 1:
                    await message.edit(content=f"```{string} - Занят до рестарта {datetime.now().date().day}.{datetime.now().date().month} ```", view=view[1])
                else:
                    await message.edit(content=f"```{string} - Занят до рестарта {datetime.now().date().day}.{datetime.now().date().month} ```")
                channel = bot.get_channel(log_channel)  # канал #логи
                # отправка лога
                await channel.send(f"```{string} - Взяли до рестарта {datetime.now().date().day}.{datetime.now().date().month}. Цена: {argument2} ```")
            await noteMoney(bot, owner, 0, 0, chooseCar, int(argument2), 0)
        except:
            print('Что-то пошло не так при обработке запроса: рестарт')