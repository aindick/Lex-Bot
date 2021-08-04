import discord
import os
import requests
import json
import random
import joke_api
from replit import db
from KeepAlive import keep_alive
client = discord.Client()
# I made this bot with the help of FreeCodeAcademy!

sad_words = ["sad", "depressed", "unhappy", "depressing", "miserable"]

starter_encouragements = ["Cheer up!", "Life gets better hun!", " You're amazing!", "You're loved!",
                          "You're beautiful!", "Hang in there!", "You got this!"]
if "responding" not in db.keys():
  db["responding"] = True

def get_quotes():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      encouragements.append(encouraging_message)
      db["encouragements"] = encouragements
  else:
      db["encouragements"] = [encouraging_message]


def delete_encouragments(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
      del encouragements[index]
  db["encouragements"] = encouragements


@client.event
# calls when the bot is ready to be used.
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
# triggers each time a message is received.
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('.inspire'):
     quote = get_quotes()
     await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"][:]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('.new'):
    encouraging_message = msg.split(".new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith('.del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split(".del ", 1)[1])
      delete_encouragments(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('.list'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('.responding'):
     value = msg.split(".responding ", 1)[1]

     if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
     else:
        db["responding"] = False
        await message.channel.send("Responding is off.")


    # jokes!
  if message.content.startswith('.joke'):
     joke = joke_api.get_joke()
     if not joke:
         await message.channel.send("Couldn't get joke from API. Try again later.")
     else:
        await message.channel.send(joke['setup'] + '\n' + joke['punchline'])

    # greeting!
  if message.content.startswith('.hello'):
    await message.channel.send("Hi cutie!")

keep_alive()
client.run(os.getenv('TOKEN'))
