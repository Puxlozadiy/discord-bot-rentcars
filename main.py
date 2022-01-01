# coding=utf-8
from time import daylight
import discord
from discord.ui import Button, View
from discord.ext import commands, tasks
from datetime import datetime, date, time, timedelta
from checkDate import checkDate
from eachCar import eachCar
from noteMoney import noteMoney
from messageHandling import messageHandling
from access import getId, getLogChannel, getAccess, chooseCar, access_list
bot = commands.Bot("!")
target_channel_id = 916341503331291148

car_channels_list = [923248484579160074, 923201869982101566, 923232543472513054,923253620164689941, 924441319697424444, 924802330623365130]
car_channel_list2 = [926189538097889320, 926189491151044731, 926301497069817856, 926301564640043028]
money_channel_list = []
for users in access_list:
    money_channel_list.append(users[0][2])


async def buttonSetup():
    view = View()
    # кнопки при статусе "свободен"
    item = Button(style=discord.ButtonStyle.blurple, label="1.5 часа")
    item1 = Button(style=discord.ButtonStyle.blurple, label="2 часа")
    item2 = Button(style=discord.ButtonStyle.blurple, label="3 часа")
    view.add_item(item=item)
    view.add_item(item=item1)
    view.add_item(item=item2)
    item.callback = buttonCallback_1_5
    item1.callback = buttonCallback_2
    item2.callback = buttonCallback_3
    view.timeout = 9999999999
    # кнопки при статусе "занят" или "ожидается"
    view2 = View()
    item3 = Button(style=discord.ButtonStyle.blurple, label="Вернули")
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
    print(datetime.now())
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
        await messageHandling(bot, f'!{car_number} вернули', interaction.message.id, ad_text, choseCar, interaction.message.channel.id, log_channel, owner, await buttonSetup(), 1)


async def universalButtonCallback(message, interaction, time):
    print(datetime.now())
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
    print(f'Определено имя: {interaction.user.name}')
    print(f'Определён статус доступа: {access}')
    print(f'Определён номер владельца: {owner}')
    print(f'Определён канал лога владельца: {log_channel}')
    print(f'Текст требуемого объявления: {ad_text}')
    print(f'Выбран автомобиль: {choseCar}')
    if access == 1 and owner >= 0:
        await messageHandling(bot, f'!{car_number} вернули', message.id, ad_text, choseCar, message.channel.id, log_channel, owner, await buttonSetup(), 1)
        await messageHandling(bot, f'!{car_number} {time}', message.id, ad_text, choseCar, message.channel.id, log_channel, owner, await buttonSetup(), 1)
    print('=============================================')


@bot.event
async def on_message(message):  # ждёт команды, обрабатывает и удаляет лишние сообщения
    if message.author.id != 916504100470947890:
        await onMessage(message, car_channels_list, 1)
        await onMessage(message, car_channel_list2, 0)

        for user in access_list:
            for channels in money_channel_list:
                if message.channel.id == channels:
                    if message.author.id == user[0][0]:
                        if message.channel.id == user[0][2]:
                            await customNoteMoney(message, '!добавить', user[0][3], 0)
                            await customNoteMoney(message, '!отнять', user[0][3], 1)
                            break

        for channels in car_channels_list:
            if message.channel.id == channels:
                await message.delete()
                break

        for channels in money_channel_list:
            if message.channel.id == channels:
                await message.delete()
                break


async def onMessage(message, channel_list, buttonBool):
    for channels in channel_list:
        if message.channel.id == channels:
            print(datetime.now())
            print(f'Принята команда: {message.content}')
            print(f'Канал команды: {message.channel.id}')
            channel = bot.get_channel(message.channel.id)
            async for messages in channel.history(limit=30):
                if messages.author.id == 916504100470947890:
                    text = messages.content
                    command = message.content
                    car_number = text.split()[2]
                    car_number = car_number[1:4]
                    car_name = text.split()[0] + ' ' + text.split()[1]
                    car_name = car_name[3:]
                    command_number = command[1:4]
                    if car_number == command_number:
                        ad_text = text.split()[
                            0] + ' ' + text.split()[1] + ' ' + text.split()[2]
                        ad_text = ad_text[3:]
                        access = getAccess(message.author.id, car_number)[0]
                        owner = getAccess(message.author.id, car_number)[1]
                        log_channel = getLogChannel(message.author.id)
                        choseCar = chooseCar(car_name)
                        print(f'Отправитель команды: {message.author.name}')
                        print(f'Определён статус доступа: {access}')
                        print(f'Определён номер владельца: {owner}')
                        print(f'Определён канал лога владельца: {log_channel}')
                        print(f'Текст требуемого объявления: {ad_text}')
                        print(f'Выбран автомобиль: {choseCar}')
                        if access == 1:
                            await messageHandling(bot, f'!{car_number} вернули', message.id, ad_text, choseCar, message.channel.id, log_channel, owner, await buttonSetup(), buttonBool)
                            await messageHandling(bot, message.content, messages.id, ad_text, choseCar, message.channel.id, log_channel, owner, await buttonSetup(), buttonBool)
                        print('=============================================')
                        break


async def customNoteMoney(message, command, owner, negative):
    if message.content.startswith(command):
        text = message.content
        summ = text.split()[1]
        summ = int(summ)
        await noteMoney(bot, owner, 0, 0, 0, summ, negative)


@tasks.loop(seconds=20)
async def handleTime():
    await eachCarProcess(car_channels_list, 1)
    await eachCarProcess(car_channel_list2, 0)

    await checkDate(bot)
    channel = bot.get_channel(924802330623365130)
    #messagess = channel.get_partial_message(924835682042671134)
    #await messagess.edit(content='```Ferrari Aperta (658) - Занят до рестарта 31.12 ```')
    # await channel.send("30.12.2021 - Crazy заработал $0")
    # await channel.send("**Статус автомобилей <@775417780421001237>:**")
    # await channel.send("```Lamborghini Urus (101) - Свободен ```", file=discord.File(fp="assets/urus_crystal.png"))
    # await channel.send("```Mercedes-G63 6x6 (605) - Залог $2.000 ```")
    # await channel.send("```Mercedes-G63 6x6 (394) - Залог $2.000 ```")
    # await channel.send("24.12.2021 - Conqueror заработал $0")
    # '<@{user_id}>'
    # await channel.send("**Статус автомобилей <@469858564299816960>:**")
    # await channel.send("```Ford Raptor (344) - Свободен ```", file=discord.File(fp="assets/raptor_slayer.png"))
    # await channel.send("**Статус автомобилей <@790343763637043300>:**")
    # await channel.send("```Ford Raptor (648) - Свободен ```", file=discord.File(fp="assets/raptor_slayer2.png"))
    # await channel.send("**Статус автомобилей <@284218293601042433>:**")
    # await channel.send("```Mercedes-G63 6x6 (777) - Свободен ```", file=discord.File(fp="assets/6x6-r.png"))
    # await channel.send("```Mercedes-G63 6x6 (222) - Свободен ```", file=discord.File(fp="assets/6x6-r.png"))
    # await channel.send("```Mercedes-G63 6x6 (605) - Свободен ```", file=discord.File(fp="assets/6x6.png"))
    # await channel.send("```Mercedes-G63 6x6 (394) - Свободен ```", file=discord.File(fp="assets/6x6.png"))

    await buttonSetup()

async def eachCarProcess(channel_list, buttonBool):
    for channel in channel_list:
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
                    await eachCar(bot, messages.id, ad_text, user_id, messages.channel.id, await buttonSetup(), buttonBool)


@tasks.loop(minutes=10)
async def setupButtons():
    print(f'Кнопки запущены или перезапущены: {datetime.now()}')
    for channels in car_channels_list:
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
