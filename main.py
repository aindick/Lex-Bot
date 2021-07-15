import discord
import os
import requests
import json
import random
import joke_api
client = discord.Client()
#I made this bot with the help of FreeCodeAcademy!

sad_words = ["sad", "depressed", "unhappy", "depressing", "miserable"]

starter_encouragements = ["Cheer up!", "Life gets better hun!", " You're amazing!", "You're loved!", "You're beautiful!", "Hang in there!", "You got this!"]

def get_quotes():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


  

@client.event
#calls when the bot is ready to be used.
async def on_ready():
 
  print("We have logged in as {0.user}".format(client))

  @client.event
  #triggers each time a message is received.
  
  async def on_message(message):
    if  message.author == client.user:
      return

    msg = message.content
#inspirational quotes!
    if message.content.startswith('.inspire'):
      quote = get_quotes()
      await message.channel.send(quote)
#greeting!
    if message.content.startswith('.hello'):  
      await message.channel.send("Hi cutie!")
#encouragements!
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))
#jokes!
    if message.content.startswith('.joke'):
        joke = joke_api.get_joke()
        if joke == False:
            await message.channel.send("Couldn't get joke from API. Try again later.")
        else:
            await message.channel.send(joke['setup'] + '\n' + joke['punchline'])
    
client.run(os.getenv('TOKEN')) 
