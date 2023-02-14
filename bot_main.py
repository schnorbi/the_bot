import requests
import discord
import datetime
import asyncio
import aiohttp
import bot_func as func

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='>help'))

    while True:
        now = datetime.datetime.now()
        if now.hour == 0:
            response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={func.configreader("nasa")}', verify=False)

            embed_nasa = discord.Embed(
                title='NASA picture of today',
                description=f'This is the NASA picture of {response.json().get("date")}\n\n{response.json().get("explanation")}',
                color=discord.Color.blue()
            )
            embed_nasa.set_image(url=response.json().get("url"))

            channels = func.configreader('nasa_pod_channels').split(',')
            for channel_id in channels:
                channel = client.get_channel(int(channel_id))
                await channel.send(embed=embed_nasa)

        await asyncio.sleep(3600)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('>shutdown') and message.author == func.configreader('owner'):
        await message.channel.send('Shuting down...')
        quit()

    if message.content.startswith('>ping'):
        start_time = asyncio.get_running_loop().time()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discordapp.com/api/v6/ping') as resp:
                await resp.text()
        ping_time = (asyncio.get_running_loop().time() - start_time) * 1000

        embed_ping = discord.Embed(
            title='Ping Test',
            description=f'Time: {ping_time:.2f} seconds',
            color=discord.Color.dark_red()
        )
        await message.channel.send(embed=embed_ping)

    if message.content.startswith('>help'):
        pass

    if message.content.startswith('>about'):
        pass

client.run(func.configreader('discord'))