# coding=utf-8
from time import daylight
import discord
from discord import channel
from discord import user
from discord.ext import commands, tasks
from discord.ui import view
from discord.utils import get
from datetime import datetime, date, time, timedelta
from checkDate import checkDate
from eachCar import eachCar
from noteMoney import noteMoney
from messageHandling import messageHandling
from access import getId, getLogChannel, getAccess, chooseCar, access_list
bot = commands.Bot("!")
target_channel_id = 916341503331291148

channels_list = [923248484579160074, 923201869982101566, 923232543472513054, 923253620164689941, 924441319697424444, 924802330623365130]

async def buttonSetup():
    view = discord.ui.View()
    # кнопки при статусе "свободен"
    item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="1.5 часа")
    item1 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="2 часа")
    item2 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="3 часа")
    view.add_item(item=item)
    view.add_item(item=item1)
    view.add_item(item=item2)
    item.callback = buttonCallback_1_5
    item1.callback = buttonCallback_2
    item2.callback = buttonCallback_3
    view.timeout = 9999999999
    # кнопки при статусе "занят" или "ожидается"
    view2 = discord.ui.View()
    item3 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Вернули")
    item3.callback = buttonCallback_return
    view2.add_item(item=item3)
    view2.timeout = 9999999999
    view_list = [view, view2]
    return view_list

async def buttonCallback_1_5(interaction):
    await universalButtonCallback(interaction.message, interaction, '1.30')

async def buttonCallback_2(interaction):
    await universalButtonCallback(interaction.message, interaction, '2')

async def buttonCallback_3(interaction):
    await universalButtonCallback(interaction.message, interaction, '3')

async def buttonCallback_return(interaction):
    channel = bot.get_channel(interaction.message.channel.id)
    text = interaction.message.content
    car_number = text.split()[2]
    car_number = car_number[1] + car_number[2] + car_number[3]
    ad_text = text.split()[0] + ' ' + text.split()[1] + ' ' + text.split()[2]
    ad_text = ad_text[3:]
    car_name = text.split()[0] + ' ' + text.split()[1]
    car_name = car_name[3:]
    choseCar = chooseCar(car_name)
    log_channel = getLogChannel(interaction.user.id)
    access = getAccess(interaction.user.id, car_number)[0]
    owner = getAccess(interaction.user.id, car_number)[1]
    if access == 1 and owner >= 0:
        await messageHandling(bot, f'!{car_number} вернули', interaction.message.id, ad_text, choseCar, interaction.message.channel.id, log_channel, owner, await buttonSetup())

async def universalButtonCallback(message, interaction, time):
    channel = bot.get_channel(message.channel.id)
    text = message.content
    messages = channel.get_partial_message(message.id)
    car_number = text.split()[2]
    car_number = car_number[1:4]
    ad_text = text.split()[0] + ' ' + text.split()[1] + ' ' + text.split()[2]
    ad_text = ad_text[3:]
    car_name = text.split()[0] + ' ' + text.split()[1]
    car_name = car_name[3:]
    choseCar = chooseCar(car_name)
    log_channel = getLogChannel(interaction.user.id)
    access = getAccess(interaction.user.id, car_number)[0]
    owner = getAccess(interaction.user.id, car_number)[1]
    #print(access)
    #print(owner)
    #print(choseCar)
    if access == 1 and owner >= 0:
        await messageHandling(bot, f'!{car_number} {time}', message.id, ad_text, choseCar, message.channel.id, log_channel, owner, await buttonSetup())




@bot.event
async def on_message(message):  # ждёт команды, обрабатывает и удаляет лишние сообщения
    print(message.content)
    for channels in channels_list:
        if message.channel.id == channels:
            if message.author.id != 916504100470947890:
                channel = bot.get_channel(message.channel.id)
                async for messages in channel.history(limit=30):
                    if messages.author.id == 916504100470947890:
                        text = messages.content
                        command = message.content
                        car_number = text.split()[2]
                        car_number = car_number[1:4]
                        command_number = command[1:4]
                        if car_number == command_number:
                            ad_text = text.split()[0] + ' ' + text.split()[1] + ' ' + text.split()[2]
                            ad_text = ad_text[3:]
                            access = getAccess(message.author.id, car_number)[0] 
                            owner = getAccess(message.author.id, car_number)[1]
                            log_channel = getLogChannel(message.author.id)
                            if access == 1:
                                await messageHandling(bot, message.content, messages.id, ad_text, 3, message.channel.id, log_channel, owner, await buttonSetup())
                            break
            await message.delete()


    for user in access_list:
        if message.channel.id == user[0][2]:
            if message.author.id == user[0][0]:
                await customNoteMoney(message, '!добавить', user[0][3], 0)
                await customNoteMoney(message, '!отнять', user[0][3], 1)
                await message.delete()
                break
                

async def customNoteMoney(message, command, owner, negative):
    if message.content.startswith(command):
        text = message.content
        summ = text.split()[1]
        summ = int(summ)
        await noteMoney(bot, owner, 0, 0, 0, summ, negative)

@tasks.loop(seconds=20)
async def handleTime():
    for channel in channels_list:
        channel = bot.get_channel(channel)
        async for messages in channel.history(limit=30):
            if messages.author.id == 916504100470947890:
                text = messages.content
                if text.find('Статус') < 0:
                    ad_text = text.split()[0] + ' ' + text.split()[1] + ' ' + text.split()[2]
                    ad_text = ad_text[3:]
                    car_number = text.split()[2]
                    car_number = car_number[1:4]
                    user_id = getId(car_number)
                    await eachCar(bot, messages.id, ad_text, user_id, messages.channel.id, await buttonSetup())
                    break

    await checkDate(bot)
    channel = bot.get_channel(924802330623365130)
    #await channel.send("26.12.2021 - Tovsali заработал $0")
    #await channel.send("```Mercedes-G63 6x6 (222) - Залог $2.000 ```")
    #await channel.send("```Mercedes-G63 6x6 (605) - Залог $2.000 ```")
    #await channel.send("```Mercedes-G63 6x6 (394) - Залог $2.000 ```")
    #await channel.send("24.12.2021 - Conqueror заработал $0")
    #'<@{user_id}>'
    #await channel.send("**Статус автомобилей <@467594732906741763>:**")
    #await channel.send("```Buggati Chiron (457) - Свободен ```", file=discord.File(fp="assets/chiron.png"))
    #await channel.send("```McLaren Senna (347) - Свободен ```", file=discord.File(fp="assets/mclaren.png"))
    #await channel.send("```McLaren 720s (856) - Свободен ```", file=discord.File(fp="assets/mclaren720.png"))
    #await channel.send("```Ferrari Aperta (658) - Свободен ```", file=discord.File(fp="assets/aperta.png"))
    #await channel.send("```Pagani Huayra (327) - Свободен ```", file=discord.File(fp="assets/pagani.png"))

    await buttonSetup()


@tasks.loop(hours=99999)
async def setupButtons():
    for channels in channels_list:
        channel = bot.get_channel(channels)
        async for messages in channel.history(limit=20):               
            if messages.author.id == 916504100470947890:
                text = messages.content
                if text.split()[0].find('Статус') < 0:
                    status = text.split()[4]
                    view = await buttonSetup()
                    if status == 'Свободен':
                        await messages.edit(content=f'{text}', view=view[0])
                    elif status == 'Занят':
                        await messages.edit(content=f'{text}', view=view[1])
                    elif status == 'Ожидается':
                        await messages.edit(content=f'{text}', view=view[1])

        

@handleTime.before_loop
async def before():
    await bot.wait_until_ready()

@setupButtons.before_loop
async def before():
    await bot.wait_until_ready()

handleTime.start()
setupButtons.start()


bot.run("OTE2NTA0MTAwNDcwOTQ3ODkw.YarG9Q.Rx4-iGSapWJel-_TsYrU0pCnyp0")
print('Бот готов к работе!')
