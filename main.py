import discord
from discord.ext import tasks
from datetime import datetime, time
from pytz import timezone
import asyncio

client = discord.Client()

Token = "ODUzNDMyNTI0ODIxNzU3OTUy.YMVS-Q.skol-rpObJvols05OxomwPPLtxU"

# global dream_modes
client.dream_modes = ['Rush', 'Ultimate', 'Castle', 'Voidless', 'Armed', 'Lucky Blocks']

# global current_mode
client.current_mode = 3

scheduled_time = time(22, 5)
print(scheduled_time)


@client.event
async def on_ready():
    print("Checking Mode")


async def update_mode():
    await client.wait_until_ready()

    print(client.dream_modes[client.current_mode])
    client.current_mode = (client.current_mode + 1) % len(client.dream_modes)
    print(client.dream_modes[client.current_mode])
    await client.get_channel(863184063884296192).send(
        f"BedWars Dream mode has changed to {client.dream_modes[client.current_mode]}")

    await asyncio.sleep(20)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '-current':
        print('current')
        await message.channel.send(f"Current game mode is {client.dream_modes[client.current_mode]}")

    if message.content == '-next':
        print('next')
        if client.current_mode + 1 == 6:
            next_adj_mode = 0
            await message.channel.send(f"Next game mode is {client.dream_modes[next_adj_mode]}")
        else:
            await message.channel.send(f"Next game mode is {client.dream_modes[client.current_mode + 1]}")

    if message.content == "-previous":
        print('previous')
        if client.current_mode - 1 == -1:
            prev_adj_mode = 5
            await message.channel.send(f"Previous game mode was {client.dream_modes[prev_adj_mode]}")
        else:
            await message.channel.send(f"Previous game mode was {client.dream_modes[client.current_mode - 1]}")


# time_loop.start()

@tasks.loop(seconds=1)
async def time_loop():
    CDT = timezone('CST6CDT')
    now = datetime.now(CDT)
    if now.weekday() == 3:
        if now.hour == 23:
            if now.minute == 00:
                if now.second == 00:
                    await update_mode()
                    await asyncio.sleep(30)


time_loop.start()
client.run(Token)
