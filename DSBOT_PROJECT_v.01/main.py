import discord
import requests
from bs4 import BeautifulSoup
import pandas as pd
from discord.ext import commands
import pymorphy2
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import random
import asyncio
import time
import os 
from urllib3.util.retry import Retry
import ssl


TOKEN = ''
CHANNEL_ID = # Введите сюда id канала, куда бот будет все отправлять

# Ссылки на сайты с новостями о глобальном потеплении

ria_news = 'https://ria.ru/keyword_globalnoe_poteplenie/'

links = [
  "https://www.youtube.com/watch?v=rD4kvuCVceA",
  "https://www.youtube.com/watch?v=TxOqJNZkAwk",
  "https://www.youtube.com/watch?v=ynqAe4nl-QI",
  "https://www.youtube.com/watch?v=wcVy-0IBpg4",
  "https://www.youtube.com/watch?v=DlKu0MofIjs",

]

# Список ежедневных задач
daily_tasks = [
  "Посадите дерево или цветок",
  "Сделайте уборку в парке или дворе",
  "Откажитесь от использования одноразовых пакетов",
  "Используйте меньше воды при мытье посуды",
  "Перерабатывайте мусор",
  "Сократите потребление электроэнергии",
  "Используйте общественный транспорт вместо личного автомобиля",
  "Купите продукты местного производства",
  "Поделитесь своим экологическим опытом с друзьями",
  "Пожертвуйте деньги в экологическую организацию",
]


path_to_images = os.path.join(os.path.dirname(__file__), "mems")


# Время между отправкой новостей (в секундах)
interval = 3600
interv = 86400

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Список доступных команд:", color=discord.Color.blue())
    bot_commands = [command.name for command in bot.commands]
    embed.add_field(name="Команды", value='\n'.join(bot_commands), inline=False)
    await ctx.send(embed=embed)

async def send_news_ria(ctx):
    while True:
        response = requests.get(ria_news)
        bs = BeautifulSoup(response.text,"lxml")

        articles = bs.find_all('div', 'list-item__content')
        for i, article in enumerate(articles):
            news_title = article.text.strip()
            news_link = article.find('a').get('href')

            await ctx.send(f"**{news_title}**\n{news_link}")
            await asyncio.sleep(interval)

        await asyncio.sleep(interval)

# Функция для отправки случайного слова
async def send_random_word(ctx):
  while True:
    random_word = random.choice(daily_tasks)
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
      print("Канал не найден.")
      return

    await channel.send(f"ЭКОЛОГИЧЕСКОЕ ЗАДАНИЕ НА СЕГОДНЯ: {random_word}")
    await asyncio.sleep(interv)

async def send_random_link(links, interval, ctx):
  while True:
    random_link = random.choice(links)
    await ctx.send(random_link)
    await asyncio.sleep(interval)

async def send_random_mem(links, interval, ctx):
  while True:
    random_link = random.choice(links)
    await ctx.send(random_link)
    await asyncio.sleep(interval)


async def send_random_image(ctx, interval):
    while True:
        images = [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))]

        random_image = random.choice(images)

        image_path = os.path.join(path_to_images, random_image)
        await ctx.send(file=discord.File(image_path))
        await asyncio.sleep(interval)

@bot.command()
async def random_photo(ctx, interval: int = 60):
    await send_random_image(ctx, interval)

@bot.command()
async def random_link(ctx):
  await send_random_link(links, 3600, ctx)

@bot.command()
async def start_news(ctx):
    await send_news_ria(ctx)
  
@bot.command()
async def start_words_command(ctx):
  await send_random_word(ctx)


bot.run(TOKEN)
