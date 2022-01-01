# coding=utf-8
from time import daylight
import discord
from discord import channel
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, date, time, timedelta
from eachCar import eachCar
from access import access_list

# в зависимости от канала добавляет деньги владельцам в канал "бухгалтерия"
async def noteMoney(bot, chooseOwner, hours, minutes, chooseCar, customSumm, negative):
    for user in access_list:
        if user[0][3] == chooseOwner:
            await changeMoney(user[0][2], bot, user[0][4], chooseCar, hours, minutes, customSumm, negative)
            break

async def changeMoney(channel_id, bot, string, chooseCar, hours, minutes, customSumm, negative):
    channel = bot.get_channel(channel_id)
    async for messages in channel.history(limit=3):
        if messages.content.find(f'{string}') > 0:
            result = process(chooseCar, messages, hours, minutes, customSumm, negative)
            await messages.edit(content=f"{result[0]} {result[1]}")
            break

def getPrice(car, hours, minutes):
    price_list = [
        [1, [3, 0], [4, 5], [5, 5], [8, 0]], # Ford Raptor
        [2, [0, 0], [0, 0], [0, 0], [0, 0]], # Lamborghini Urus
        [3, [6, 0], [8, 0], [11, 0], [15, 0]], # Mercedes G63 6x6
        [4, [3, 0], [5, 0], [6, 0], [8, 0]], # Infinity FX50s
        [5, [5, 0], [7, 5], [9, 0], [13, 0]], # Rolls Royce Cullinan
        [6, [4, 5], [7, 0], [8, 5], [12, 0]], # Rolls Royce Ghost
        [7, [6, 0], [8, 0], [10, 0], [14, 0]], # Buggati Chiron
        [8, [5, 0], [7, 5], [9, 0], [13, 5]], # McLaren Senna
        [9, [5, 0], [7, 5], [9, 0], [13, 5]], # McLaren 720s
        [10, [5, 0], [7, 5], [9, 0], [13, 5]], # Ferrari Aperta
        [11, [6, 0], [7, 5], [9, 0], [13, 5]], # Pagani Huayra
        [12, [3, 0], [4, 5], [5, 5], [8, 0]],
        [13, [3, 0], [4, 5], [5, 5], [8, 0]],
    ]
    for prices in price_list:
        if prices[0] == car:
            if hours == 1 and minutes == 30:
                return prices[2]
            if hours == 1:
                return prices[1]
            if hours == 2:
                return prices[3]
            if hours == 3:
                return prices[4]
            else:
                return [0, 0]

def process(chooseCar, messages, hours, minutes, customSumm, negative):  # для noteMoney()
    #try:
    bool = 0
    thousands = ''
    hundreds = ''
    money = messages.content.split()[4]
    for symbol in money:
        if bool == 0 and symbol.isdigit():
            thousands += symbol
        elif bool == 0 and symbol == '.':
            bool = 1
        elif bool == 1 and symbol.isdigit():
            hundreds += symbol
            break
    if hundreds == '':
        hundreds = 0
    thousands = int(thousands)
    hundreds = int(hundreds)
    hours = int(hours)
    minutes = int(minutes)
    customSumm = int(customSumm)
    if customSumm != 0:
        if negative == 1:
            temp_thousands = customSumm // 1000
            customSumm -= temp_thousands * 1000
            temp_hundreds = customSumm // 100
            thousands -= temp_thousands
            hundreds -= temp_hundreds
            if hundreds < 0:
                temp_hundreds = 10
                hundreds = temp_hundreds + hundreds
                thousands -= 1
        else:
            tempint = int(int(customSumm)//100)
            tempint2 = tempint//10
            if tempint2 == 0:
                hundreds += tempint
            else:
                thousands += tempint2
                tempint = tempint - (tempint2 * 10)
                hundreds += tempint
    else:
        price = getPrice(chooseCar, hours, minutes)
        thousands+=price[0]
        hundreds+=price[1]
        print(f'Денег прибавлено: {price[0]}.{price[1]}к')
    if hundreds >= 10:
        thousands+=1
        hundreds-=10
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
    money_string += f'{hundreds}'
    money_string += '00'
    return [tempText, money_string]
    #except:
        #print('Что-то пошло не так при изменении в бухгалтерии')