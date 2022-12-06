import discord
from os import environ
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



MESSAGE1 = '''<@&105472720865202257>  when are we raiding this week?
🇫 riday
🇸 aturday
☀️ Sunday'''
MESSAGE2 = '''KF 🗳️  , VotD ✅ , DSC 👾 , Last Wish ✨ , GoS 😐 , VoG <:poggers:1029848733657071789>'''
EMOJI1 = ["🇫", "🇸", "☀️"]
EMOJI2 = ["🗳️", "✅", "👾", "✨", "😐", "<:poggers:1029848733657071789>"]
GUILD = None


# Hosts a webpage, which can be pinged to keep the replit up
keepalive.keepAlive()

# Generic utils

def log(s: str):
  time = datetime.datetime.now()
  print(f"{time.strftime('%H:%M:%S')} {s}")

# Status Updates

async def updateStrigaStatus(client: discord.Client):
  log("Doing an update")
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



# Commands



@tree.command(name="send",
              description="Sends reaction message",
              guild=GUILD)
async def sendMessages(interaction: discord.Interaction):

  message1 = await interaction.channel.send(MESSAGE1)
  message2 = await interaction.channel.send(MESSAGE2)

  for i in EMOJI1:
    await message1.add_reaction(i)
  for i in EMOJI2:
    await message2.add_reaction(i)

  log("TIMED MESSAGE SENT")
  await interaction.response.send_message("message sent.")



# Start



@client.event
async def on_ready():
  # Setting guild
  global GUILD
  GUILD = client.get_guild(1005471883539513384)
  
  await tree.sync(guild=GUILD)

  # Start status updates
  statusThread = threading.Thread(target=statusUpdate, args=(client,))
  statusThread.start()

  log(f"{client.user} logged in")


client.run(environ.get("TOKEN"))
