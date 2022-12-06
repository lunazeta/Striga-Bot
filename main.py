import discord
from os import environ
import threading
import datetime
from time import sleep
from typing import Awaitable, TypeVar
import asyncio
import keepalive
import requests

intents = discord.Intents.default()
intents.message_content = True

def looper(loop):
  asyncio.set_event_loop(loop)
  loop.run_forever()

def asyncio_run(coro: Awaitable[T], timeout=30) -> T:
  return asyncio.run_corountine_threadsafe(coro, loop).result(timeout=timeout)


loop = asyncio.new_event_loop()
asyncio.set_event_loop()
t = threading.Thread(target=looper, args=(loop,))
t.start()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

messageChannel = None

MESSAGE1 = '''<@&105472720865202257>  when are we raiding this week?
🇫 riday
🇸 aturday
☀️ Sunday'''
MESSAGE2 = '''KF 🗳️  , VotD ✅ , DSC 👾 , Last Wish ✨ , GoS 😐 , VoG <:poggers:1029848733657071789>'''

GUILD = None
stop = False

keepalive.keepAlive()

def log(s: str):
  time = datetime.datetime.now()
  print(f"{time.strftime('%H:%M:%S')} {s}")


async def sendMessages(client: discord.Client, messageChannel):
  message1 = await messageChannel.send(MESSAGE1)
  message2 = await messageChannel.send(MESSAGE2)
  EMOJI1 = ["🇫", "🇸", "☀️"]
  EMOJI2 = ["🗳️", "✅", "👾", "✨", "😐", "<:poggers:1029848733657071789>"]
  print(EMOJI2)
  for i in EMOJI1:
    await message1.add_reaction(i)
  for i in EMOJI2:
    await message2.add_reaction(i)
  log("TIMED MESSAGE SENT")


def messageTimer(client: discord.Client):
  global messageChannel
  global stop
  global loop
  asyncio.set_event_loop(loop)
  while not stop:
    time = datetime.datetime.now()
    print("yes")
    if time.strftime("%H") == "10" and time.date().weekday() == 0:
      asyncio.run(sendMessages(client, messageChannel))
      print("it done")
    else:
      log(f"Timed message not sent: {time.date().weekday()}")
    sleep(3600)

  return False


async def updateStrigaStatus(client: discord.Client):
  log("doing an update")
  r = requests.request("GET", "https://www.bungie.net/Platform/Destiny2/1/Account/4611686018492829196/Character/0/Stats/UniqueWeapons", headers={"X-API-Key": environ.get("BUNGIETOKEN")})
  if r.ok:
    for i in r.json()["Response"]["weapons"]:
      if i["referenceId"] == 46524085:
          await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"qwhaty's {i['values']['uniqueWeaponKills']['basic']['displayValue']} striga kills"))
          break
  else:
    log("Bungie api request failed")


def statusUpdate(client: discord.Client):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  while True:
    asyncio.run(updateStrigaStatus(client))
    sleep(300)


@tree.command(name="sendhere",
              description="Sets the channel in which to send timed messages",
              guild=GUILD)
async def setMessageLocation(interaction: discord.Interaction):
  global messageChannel
  messageChannel = interaction.channel
  log(f"Message sending bound to {messageChannel.name}")
  await interaction.response.send_message("ok.")


@tree.command(name="start",
              description="Starts sending timed messages",
              guild=GUILD)
async def startMessages(interaction: discord.Interaction):
  global stop
  stop = False
  timerThread = threading.Thread(target=messageTimer, args=(client, ))
  timerThread.start()
  log("Message sending started")
  await interaction.response.send_message("message sending started.")


@tree.command(name="end",
              description="Ends sending timed messages",
              guild=GUILD)
async def endMessages(interaction: discord.Interaction):
  global stop
  stop = True
  log("Message sending ended")
  await interaction.response.send_message("message sending ended.")


@client.event
async def on_ready():
  global GUILD
  GUILD = client.get_guild(1005471883539513384)
  await tree.sync(guild=GUILD)
  statusThread = threading.Thread(target=statusUpdate, args=(client,))
  statusThread.start()
  log(f"{client.user} logged in")


client.run(environ.get("TOKEN"))
