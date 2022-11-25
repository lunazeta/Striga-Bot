import discord
from os import environ
import threading
import datetime
from time import sleep
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

messageChannel = None

MESSAGE1 = '''<@&10054727230865202257>  when are we raiding this week?
🇫 riday
🇸 aturday
☀️ Sunday'''
MESSAGE2 = '''KF 🗳️  , VotD ✅ , DSC 👾 , Last Wish ✨ , GoS 😐 , VoG <:poggers:1029848733657071789>'''

GUILD = client.get_guild(1005471883539513384)
stop = False

def log(s: str):
    time = datetime.datetime.now()
    print(f"{time.strftime('%H:%M:%S')} {s}")

async def sendMessages(client: discord.Client):
    message1 = await messageChannel.send(MESSAGE1)
    message2 = await messageChannel.send(MESSAGE2)
    EMOJI1 = ["🇫","🇸","☀️"]
    EMOJI2 = ["🗳️","✅","👾","✨","😐","<:poggers:1029848733657071789>"]
    print(EMOJI2)
    for i in EMOJI1:
        await message1.add_reaction(i)
    for i in EMOJI2:
        await message2.add_reaction(i)
    log("TIMED MESSAGE SENT")
    return True

async def messageTimer(client: discord.Client):
    global messageChannel
    global stop
    while not stop:
        time = datetime.datetime.now()
        print("yes")
        if time.strftime("%H") == "4" and time.date().weekday() == 3:
            await asyncio.Task(sendMessages(client))
        else:
            log(f"Timed message not sent: {time.date().weekday()}")
        sleep(3600)

    return False

@tree.command(name="sendhere", description="Sets the channel in which to send timed messages", guild=GUILD)
async def setMessageLocation(interaction: discord.Interaction):
    global messageChannel
    messageChannel = interaction.channel
    log(f"Message sending bound to {messageChannel.name}")
    await interaction.response.send_message("ok.")

@tree.command(name="start", description="Starts sending timed messages", guild=GUILD)
async def startMessages(interaction: discord.Interaction):
    timerThread = threading.Thread(target=asyncio.run, args=(messageTimer(client),))
    timerThread.start()
    log("Message sending started")
    await interaction.response.send_message("message sending started.")

@tree.command(name="end", description="Ends sending timed messages", guild=GUILD)
async def endMessages(interaction: discord.Interaction):
    global stop
    stop = True
    log("Message sending ended")
    await interaction.response.send_message("message sending ended.")

@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    log(f"{client.user} logged in")

client.run(environ.get("TOKEN"))