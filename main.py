import os
import discord
from keep_alive import keep_alive
from replit import db
from al import al, profile, register
from mal import mal
from others import mov, book, trace

def hel(author):
    embed = discord.Embed(
        title="Help Page",
        description = "List of available commands"
    )
    embed.add_field(name="Anime", value="r!anime <query>", inline=False)
    embed.add_field(name="Manga", value="r!manga <query>", inline=False)
    embed.add_field(name="TV Show", value="r!tv <query>", inline=False)
    embed.add_field(name="Movie", value="r!movie <query>", inline=False)
    embed.add_field(name="Book", value="r!book <query>", inline=False)
    embed.add_field(name="Trace", value="r!trace <image url>", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="r!help"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content    
    if msg.startswith('r!help'):
        await message.channel.send(embed = hel(message.author))
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
          await message.channel.send(embed = profile(message.author))
      elif prefix == "r!delete":
          del db[str(message.author.id)] 
          embed = discord.Embed(
                title="Account Deleted"
            )
          await message.channel.send(embed = embed)  
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
    elif prefix == "r!trace" or prefix == "r!search":
        await message.channel.send(embed = trace(q, message.author))
       

        
    
keep_alive()

client.run(os.environ['TOKEN'])
