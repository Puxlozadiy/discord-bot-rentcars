# coding=utf-8
from time import daylight
import discord
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, date, time, timedelta

bot = commands.Bot("!")
target_channel_id = 916341503331291148


@bot.event
async def on_message(message):  # ждёт команды, обрабатывает и удаляет лишние сообщения
    if message.author.id != 916504100470947890:
        if message.channel.id == target_channel_id:
            await messageHandling(message, '!777', 921679140430680084, "Mercedes-G63 6x6 (777)", 29, 3, 916341503331291148)
            await messageHandling(message, '!666', 921679148538290186, "Lamborghini Urus (666)", 25, 2, 916341503331291148)
            await message.delete()
            channel = bot.get_channel(916341503331291148)
            async for messages in channel.history(limit=20):
                if messages.author.id != 916504100470947890:
                    await messages.delete()
        if message.channel.id == 916344696773681153:
            await messageHandling(message, '!605', 921012517575217152, "Mercedes-G63 6x6 (605)", 29, 3, 916344696773681153)
            await messageHandling(message, '!394', 921012526672646174, "Mercedes-G63 6x6 (394)", 29, 3, 916344696773681153)
            await message.delete()
            channel = bot.get_channel(916344696773681153)
            async for messages in channel.history(limit=20):
                if messages.author.id != 916504100470947890:
                    await messages.delete()


async def messageHandling(content, command, message_id, string, position, chooseCar, channel_id):  # принимает команды
    if (content.content.startswith(command)):
        owner = 0
        if channel_id == 916341503331291148:
            owner = 0
        elif channel_id == 916344696773681153:
            owner = 1
        argument = content.content.split()[1]
        argument2 = 0
        argument3 = 'Не известно'
        try:
            argument2 = content.content.split()[2]
        except:
            argument2 = 0

        if content.content.split()[1] == 'рестарт' or content.content.split()[1] == 'продлили':
            try:
                argument3 = content.content.split()[2]
            except:
                None
        else:
            try:
                argument3 = content.content.split()[2]
            except:
                None

        if (argument == 'вернули'):
            try:
                channel = bot.get_channel(channel_id)
                command_arg = command[1] + command[2] + command[3]
                message_arg = ''
                msg_to_delete = 0
                async for messages in channel.history(limit=4):
                    try:
                        tempText = messages.content.split()[3]
                        message_arg = tempText[1] + tempText[2] + tempText[3]
                        if messages.content.split()[5] == 'Ожидается':
                            if command_arg == message_arg:
                                msg_to_delete = messages.id
                                message = channel.get_partial_message(
                                    msg_to_delete)
                                await message.delete()
                    except:
                        None
                message = channel.get_partial_message(message_id)
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
                print(time)
                print(date)
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
                dt = datetime(year=1, month=int(months), day=int(days), hour=int(
                    hours), minute=int(minutes))  # время из сообщения

                if (argument3.find('.') > 0):  # получение времени из аргумента
                    hours = ''
                    minutes = ''
                    bool = 0
                    for symbol in argument3:
                        if bool == 0 and symbol.isdigit():
                            hours += symbol
                        elif bool == 0 and symbol == '.':
                            bool = 1
                        elif bool == 1:
                            minutes += symbol
                    dt = dt + timedelta(hours=int(hours), minutes=int(minutes))
                    await noteMoney(owner, hours, minutes, chooseCar, argument2)
                    channel = bot.get_channel(channel_id)
                    message = channel.get_partial_message(message_id)
                    # продление формата hours.minutes
                    await message.edit(content=f'```{string} - Занят до {dt.hour}:{dt.minute} {dt.day}.{dt.month} ```')
                    channel = bot.get_channel(917122080129032213)
                    await channel.send(f'{string} - Продлили на {hours}:{minutes}. Новое время: {dt.hour}:{dt.minute}.')
                else:
                    dt = dt + timedelta(hours=int(argument2))
                    await noteMoney(owner, argument, 0, chooseCar, argument2)
                    channel = bot.get_channel(channel_id)
                    message = channel.get_partial_message(message_id)
                    # продление формата hours
                    await message.edit(content=f'```{string} - {dt.hour}:{dt.minute} {dt.day}.{dt.month} ```')
                    channel = bot.get_channel(917122080129032213)
                    await channel.send(f'```{string} - Продлили на {argument2} час(ов). Новое время: {dt.hour}:{dt.minute}. ```')
            except:
                print('Что-то пошло не так при обработке запроса: продлить')

        elif (argument != 'рестарт'):
            try:
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
                    await noteMoney(owner, hours, minutes, chooseCar, 0)
                else:
                    dt = datetime.now() + timedelta(hours=(int(argument) + gmtdiff))
                    time = dt.strftime("%H:%M")
                    await noteMoney(owner, argument, 0, chooseCar, 0)
                date = datetime.now()
                if dt.time() < datetime.now().time():
                    date = date + timedelta(days=1)
                channel = bot.get_channel(channel_id)
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Занят до {time} {date.day}.{date.month} ```")
                channel = bot.get_channel(917122080129032213)
                # отправка лога
                await channel.send(f"```{string} - Взяли до {time}. Взял: {argument3} ```")
            except:
                print('Что-то пошло не так при обработке запроса: время')
        elif argument == 'рестарт':
            try:
                channel = bot.get_channel(channel_id)
                message = channel.get_partial_message(message_id)
                if (datetime.now().hour <= 24 and datetime.now().hour > 7):
                    await message.edit(content=f"```{string} - Занят до рестарта {datetime.now().date().day + 1}.{datetime.now().date().month} ```")
                    channel = bot.get_channel(917122080129032213)  # канал #логи
                    # отправка лога
                    await channel.send(f"```{string} - Взяли до рестарта {datetime.now().date().day + 1}.{datetime.now().date().month}. Цена: {argument2} ```")
                elif (datetime.now().hour < 7 and datetime.now().hour > 0):
                    await message.edit(content=f"```{string} - Занят до рестарта {datetime.now().date().day}.{datetime.now().date().month} ```")
                    channel = bot.get_channel(917122080129032213)  # канал #логи
                    # отправка лога
                    await channel.send(f"```{string} - Взяли до рестарта {datetime.now().date().day}.{datetime.now().date().month}. Цена: {argument2} ```")
                await noteMoney(owner, 0, 0, chooseCar, int(argument2))
            except:
                print('Что-то пошло не так при обработке запроса: рестарт')


# в зависимости от канала добавляет деньги мне или Хурику
async def noteMoney(chooseOwner, hours, minutes, chooseCar, customSumm):
    channel = bot.get_channel(916563929612820512)
    # await channel.send(content="04.12.2020 - Rico заработал $100.000")
    async for messages in channel.history(limit=2):
        result = process(chooseCar, messages, hours, minutes, customSumm)
        if chooseOwner == 0:
            if messages.content.find('Rico') > 0:
                await messages.edit(content=f"{result[0]} {result[1]}")
        elif chooseOwner == 1:
            if messages.content.find('Hurick') > 0:
                await messages.edit(content=f"{result[0]} {result[1]}")


def process(chooseCar, messages, hours, minutes, customSumm):  # для noteMoney()
    bool = 0
    thousands = ''
    money = messages.content.split()[4]
    for symbol in money:
        if bool == 0 and symbol.isdigit():
            thousands += symbol
        elif bool == 0 and symbol == '.':
            bool = 1
    thousands = int(thousands)
    hours = int(hours)
    minutes = int(minutes)
    customSumm = int(customSumm)
    if customSumm > 0:
        customSumm = int(customSumm/1000)
        thousands += customSumm
    elif chooseCar == 1:
        thousands += hours*3
        if minutes == 30:
            thousands += 2
        elif minutes == 15:
            thousands += 1
    elif chooseCar == 2:
        None
    elif chooseCar == 3:
        thousands += hours*6
        if hours == 2:
            thousands -= 1
        if hours == 3:
            thousands -= 2
        if minutes == 30:
            thousands += 2
        elif minutes == 15:
            thousands += 1
    text = messages.content
    tempText = ''
    counter = 0
    for str in text.split():
        if counter < 4:
            counter += 1
            tempText += ' '
            tempText += str
    money_string = '$'
    money_string += f'{thousands}'
    money_string += '.'
    money_string += '000'
    return [tempText, money_string]


@tasks.loop(seconds=20)
async def handleTime():
    await eachCar(921679140430680084, 29, "Mercedes-G63 6x6 (777)", 284218293601042433, 916341503331291148, 777)
    await eachCar(921679148538290186, 29, "Lamborghini Urus (666)", 284218293601042433, 916341503331291148, 666)

    await eachCar(921012517575217152, 29, "Mercedes-G63 6x6 (605)", 471247102438277131, 916344696773681153, 605)
    await eachCar(921012526672646174, 29, "Mercedes-G63 6x6 (394)", 471247102438277131, 916344696773681153, 394)
    await checkDate()
    channel = bot.get_channel(916341503331291148)
    # await channel.send("**Статус автомобилей Rico:**")
    # await channel.send("```Mercedes-G63 6x6 (777) - Свободен ```", file=discord.File(fp="6x6-r.png"))
    # await channel.send("```Lamborghini Urus (666) - Свободен ```", file=discord.File(fp="urus.png"))


async def checkDate():
    channel = bot.get_channel(916563929612820512)
    async for messages in channel.history(limit=1):
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
                    await channel.send(content=f"{now.day}.{now.month}.{now.year} - Rico заработал $0")
                    await channel.send(content=f"{now.day}.{now.month}.{now.year} - Hurick заработал $0")
            elif now.month > dt.month:
                await channel.send(content=f"{now.day}.{now.month}.{now.year} - Rico заработал $0")
                await channel.send(content=f"{now.day}.{now.month}.{now.year} - Hurick заработал $0")
        elif now.year > dt.year:
            await channel.send(content=f"{now.day}.{now.month}.{now.year} - Rico заработал $0")
            await channel.send(content=f"{now.day}.{now.month}.{now.year} - Hurick заработал $0")


async def eachCar(message_id, position, string, user_id, channel_id, argument):
    count = 0
    status = ''
    channel = bot.get_channel(channel_id)
    message = channel.get_partial_message(message_id)
    message = await message.fetch()
    text = message.content
    for simbols in message.content:
        count += 1
        if (count >= position):
            status += simbols
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
                        await message.edit(content=f"```{string} - Свободен ```")
            elif (now.month > dt1.month):
                channel = bot.get_channel(channel_id)
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Свободен ```")

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
                    await message.edit(content=f"```{string} - Ожидается освобождение ```")
                    await channel.send(f"{myid}\n```{string} - Ожидается освобождение ```")
            if datetime.now().day > dt.day and datetime.now().month == dt.month:
                myid = f'<@{user_id}>'
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Ожидается освобождение ```")
                await channel.send(f"{myid}\n```{string} - Ожидается освобождение ```")
            elif datetime.now().month > dt.month:
                myid = f'<@{user_id}>'
                message = channel.get_partial_message(message_id)
                await message.edit(content=f"```{string} - Ожидается освобождение ```")
                await channel.send(f"{myid}\n```{string} - Ожидается освобождение ```")

            # except:
            #print('Что-то пошло не так при проверке времени!')
    # elif text.split()[4] == 'Ожидается':
    #     notification_appears = 0
    #     async for messages in channel.history(limit=4):
    #         try:
    #             temptext = messages.content.split()[3]
    #             message_arg = temptext[1] + temptext[2] + temptext[3]
    #             if message_arg == argument:
    #                 notification_appears = 1
    #         except:
    #             None


@handleTime.before_loop
async def before():
    await bot.wait_until_ready()

handleTime.start()


bot.run("OTE2NTA0MTAwNDcwOTQ3ODkw.YarG9Q.Rx4-iGSapWJel-_TsYrU0pCnyp0")
print('Бот готов к работе!')
