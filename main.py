import os
import discord
from discord import AllowedMentions
from al import al, profile, register, leaderboard
from mal import mal
from others import mov, book
import json

def hel(author, server_id):
    embed = discord.Embed(
        title="Help Page",
        description = "List of available commands"
    )
    embed.add_field(name="Anime", value="r!anime <query>", inline=False)
    embed.add_field(name="Manga", value="r!manga <query>", inline=False)
    embed.add_field(name="TV Show", value="r!tv <query>", inline=False)
    embed.add_field(name="Movie", value="r!movie <query>", inline=False)
    embed.add_field(name="Book", value="r!book <query>", inline=False)
    #embed.add_field(name="Trace", value="r!trace <image url>", inline=False)
    if server_id == 582854818243018752 or server_id == 681089524226457620: 
      embed.add_field(name="Register", value="r!register <your AL username>\nRegister your Anlist account, for example 'r!register Qfu10'", inline=False)
      embed.add_field(name="Profile", value="r!profile\nCheck your AL stats(you need to be registered for this)", inline=False)
      embed.add_field(name="Leaderboard", value="r!leaderboard or r!lb\nCheck the leaderboard for where you stand in the server, also you can check other some page x by 'r!lb x', for example 'r!lb 2' gets the 2nd page of the leaderboard", inline=False)
      embed.add_field(name="Delete", value="r!delete\nDelete your AL account in the bot's database", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed
client = discord.Client(allowed_mentions = AllowedMentions().none())

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="r!help"))
    ch = client.get_channel(819858607537389578)
    await ch.send("**hi**")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content    
    if msg.startswith('r!help'):
        await message.channel.send(embed = hel(message.author, message.guild.id))
    lst = msg.split()
    if len(lst) == 0:
      return
    prefix=lst.pop(0)
    q = ' '.join(lst)        
    if message.guild.id == 582854818243018752 or message.guild.id == 681089524226457620:  
      if prefix == "r!anime":
          await message.channel.send(embed = al(q, message.author, 0))
      elif prefix == "r!manga":
          await message.channel.send(embed = al(q, message.author, 1))
      elif prefix == "r!register":
        await message.channel.send(embed = register(q, message.author))
      elif prefix == "r!profile":
          await message.channel.send(embed = profile(q, message.author))
      elif prefix == "r!delete":
          f = open('db.json')
          db = json.load(f)
          del db[str(message.author.id)] 
          with open('db.json', 'w') as fp:
            json.dump(db, fp)
          embed = discord.Embed(
                title="Account Deleted"
            )
          await message.channel.send(embed = embed) 
      elif prefix == "r!leaderboard" or prefix == "r!lb":
          await message.channel.send(embed = leaderboard(q, message.author))     
    else:
      if prefix == "r!anime":
          await message.channel.send(embed = mal(q, message.author, 0))
      elif prefix == "r!manga":
          await message.channel.send(embed = mal(q, message.author, 1))
    if prefix == "r!movie":
        await message.channel.send(embed = mov(q, message.author,0))
    elif prefix == "r!tv":
        await message.channel.send(embed = mov(q, message.author,1))
    elif prefix == "r!book" or prefix == "r!books":
        await message.channel.send(embed = book(q, message.author))
    #elif prefix == "r!trace" or prefix == "r!search":
    #    await message.channel.send(embed = trace(q, message.author))
       

        


f = open('secrets.json')
secrets = json.load(f)
client.run(secrets['TOKEN'])
