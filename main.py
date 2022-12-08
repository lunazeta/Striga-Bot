import discord
import dotenv
import threading
import datetime
from time import sleep
import asyncio
import keepalive
import requests


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


TIME = "13"
WEEKDAY = 3

MESSAGE1 = '''<@&1005472720865202257>  when are we raiding this week?
🇫 riday
🇸 aturday
☀️ Sunday'''
MESSAGE2 = '''KF 🗳️  , VotD ✅ , DSC 👾 , Last Wish ✨ , GoS 😐 , VoG <:poggers:1029848733657071789>'''
EMOJI1 = ["🇫", "🇸", "☀️"]
EMOJI2 = ["🗳️", "✅", "👾", "✨", "😐", "<:poggers:1029848733657071789>"]
GUILD = None
TIMETICK = 10

stop = True
channel = None


# Hosts a webpage, which can be pinged to keep the replit up
keepalive.keepAlive()

# Generic utils

def log(s: str):
  time = datetime.datetime.now()
  print(f"{time.strftime('%H:%M:%S')} {s}")



# Status Updates

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

async def sendMessage() -> bool:
  now = datetime.datetime.now()
  loop = asyncio.get_event_loop()
  if now.strftime("%H") == TIME and now.date().weekday() == WEEKDAY:
    
    message1 = await channel.send(MESSAGE1)
    message2 = await channel.send(MESSAGE2)

    for i in EMOJI1:
      await message1.add_reaction(i)
    for i in EMOJI2:
      await message2.add_reaction(i)

    log("Timed message sent successfully.")
    return True
  else:
    return False



# Commands



# Start sending timed messages

@tree.command(name="start",
              description="Sends timed messages",
              guild=GUILD)
async def start(interaction: discord.Interaction) -> bool:
  global channel
  global stop

  ADMIN = discord.Permissions()
  ADMIN.administrator = True

  if not interaction.permissions >= ADMIN:
    await interaction.response.send_message("insufficient permissions.")
    return False
  else:
    await interaction.response.send_message(f"started messaging in {interaction.channel}")
    channel = interaction.channel
    stop = False
    log(f"Started messaging in {interaction.channel}")
    return True

# Ends timed message sending

@tree.command(name="end",
              description="Stops sending timed messages",
              guild=GUILD)
async def end(interaction: discord.Interaction) -> bool:
  global channel
  global stop

  ADMIN = discord.Permissions()
  ADMIN.administrator = True

  if not interaction.permissions >= ADMIN:
    await interaction.response.send_message("insufficient permissions.")
    return False
  else:
    await interaction.response.send_message(f"stopped messaging in {interaction.channel}.")
    channel = None
    stop = True
    log(f"Stopped messaging in {interaction.channel}.")
    return True


# Main loop

def loopy():

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  # Run commands every so many seconds
  t = 0
  while True:
    if t % 300 == 0:
      asyncio.run(updateStrigaStatus())
    elif t % 10 == 0 and not stop:
      asyncio.run(sendMessage())

    sleep(TIMETICK)
    t = (t + TIMETICK) % 3600



# Start



@client.event
async def on_ready():
  # Setting guild
  global GUILD
  GUILD = client.get_guild(1005471883539513384)
  
  await tree.sync(guild=GUILD)

  # Start main loop
  statusThread = threading.Thread(target=loopy)
  statusThread.start()

  log(f"{client.user} logged in")


client.run(dotenv.get_key(".env", "TOKEN"))