import discord
from discord.ext import tasks
import dotenv
import datetime
import keepalive
import requests


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


TIME = "14"
WEEKDAY = 3

MESSAGE1 = '''<@&1005472720865202257>  when are we raiding this week?
🇫 riday
🇸 aturday
☀️ Sunday'''
MESSAGE2 = '''KF 🗳️  , VotD ✅ , DSC 👾 , Last Wish ✨ , GoS 😐 , VoG <:poggers:1029848733657071789>'''
EMOJI1 = ["🇫", "🇸", "☀️"]
EMOJI2 = ["🗳️", "✅", "👾", "✨", "😐", "<:poggers:1029848733657071789>"]
TIMETICK = 10

CHANNEL = None
GUILD = None

# Hosts a webpage, which can be pinged to keep the replit up
keepalive.keepAlive()

# Generic utils

def log(s: str):
  time = datetime.datetime.now()
  print(f"{time.strftime('%H:%M:%S')} {s}")

# Status Updates

@tasks.loop(minutes=5.0)
async def updateStrigaStatus():
  log("Doing an update")
  r = requests.request("GET", "https://www.bungie.net/Platform/Destiny2/1/Account/4611686018492829196/Character/0/Stats/UniqueWeapons", headers={"X-API-Key": dotenv.get_key(".env","BUNGIETOKEN")})
  if r.ok:
    for i in r.json()["Response"]["weapons"]:
      if i["referenceId"] == 46524085:
          await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"qwhaty's {i['values']['uniqueWeaponKills']['basic']['displayValue']} striga kills"))
          break
  else:
    log("Bungie api request failed")
    return False

  return True

# Timed messages

@tasks.loop(seconds=10.0)
async def sendMessage() -> bool:
  now = datetime.datetime.now()
  if now.strftime("%H") == TIME and now.date().weekday() == WEEKDAY:
    
    message1 = await CHANNEL.send(MESSAGE1)
    message2 = await CHANNEL.send(MESSAGE2)

    for i in EMOJI1:
      await message1.add_reaction(i)
    for i in EMOJI2:
      await message2.add_reaction(i)

    log("Timed message sent successfully.")
    return True
  else:
    log("It is not time to send a timed message.")
    return False

# On ready stuff

@sendMessage.before_loop
async def sendBefore():
  await client.wait_until_ready()

@updateStrigaStatus.before_loop
async def sendBefore():
  await client.wait_until_ready()

# Start

@client.event
async def on_ready():
  # Setting guild
  global GUILD, CHANNEL
  GUILD = client.get_guild(1005471883539513384)
  CHANNEL = client.get_channel(1046836261958201415)

  updateStrigaStatus.start()
  sendMessage.start()

  log(f"{client.user} logged in")


client.run(dotenv.get_key(".env", "TOKEN"))