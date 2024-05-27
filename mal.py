import json
import requests
import discord
import os
from requests.structures import CaseInsensitiveDict 

def mal(q, author, M_flag):
    f = open('secrets.json')
    secrets = json.load(f)
    token = secrets["mal_token"]
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer " + token
    if M_flag == 0:
        query_url = "https://api.myanimelist.net/v2/anime?q=" + q + "&nsfw=true"
        resp = requests.get(query_url, headers=headers)
        data_ = json.loads(resp.text)
        id_ = str(data_["data"][0]["node"]["id"])
        url = "https://api.myanimelist.net/v2/anime/" + id_ + "?fields=id,title,main_picture,start_date,synopsis,mean,media_type,status,genres,num_episodes,rating,studios"
        resp = requests.get(url, headers=headers)
        data = json.loads(resp.text)    
        url = "https://myanimelist.net/anime/" + id_
        image_url = data["main_picture"]["large"]
        dic = {"title":"", "media_type":"Unknown", "num_episodes":"Unknown", "status":"Unknown", "start_date":"Unknown", "mean":"Unknown", "rating":"Unknown", "synopsis":"Unknown"} 
        
        for element in dic.keys():
          try:
              if data[element] != None and data[element] != 0:
                  dic[element] = str(data[element])
          except KeyError:
            continue
        try:
          studiolst = data["studios"]
          stdlist=[]
          studios=", "
          for element in studiolst:
              stdlist.append(element["name"])
          studios = studios.join(stdlist)    
          genrelst = data["genres"]
          genres=", "
          genlist = []
          for element in genrelst:
              genlist.append(element["name"])
          genres = genres.join(genlist)
        except: 
          error = discord.Embed(title="Error")
          error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
          return error       
    else:
        query_url = "https://api.myanimelist.net/v2/manga?q=" + q + "&nsfw=true"
        resp = requests.get(query_url, headers=headers)
        data_ = json.loads(resp.text)
        id_ = str(data_["data"][0]["node"]["id"])
        url = "https://api.myanimelist.net/v2/manga/" + id_ + "?fields=id,title,main_picture,start_date,synopsis,mean,media_type,status,genres,num_chapters,num_volumes,authors{first_name,last_name}"
        resp = requests.get(url, headers=headers)
        data = json.loads(resp.text) 
        url = "https://myanimelist.net/manga/" + id_
        image_url = data["main_picture"]["large"]
        dic = {"title":"", "media_type":"Unknown", "num_chapters":"Unknown", "status":"Unknown", "num_volumes":"Unknown", "mean":"Unknown", "synopsis":"Unknown", "start_date":"Unknown"} 
        for element in dic.keys():
            try:
              if data[element] != None and data[element] != 0:
                  dic[element] = str(data[element])
            except KeyError:
              continue
        try:  
          authorlst = data["authors"]
          authlist=[]
          authors=", "
          tempauth = []
          for element in authorlst:
              tempauth.append(element["node"]["first_name"])
              tempauth.append(element["node"]["last_name"])
              temp = " "
              temp = temp.join(tempauth)
              tempauth.clear()
              authlist.append(temp)
          authors = authors.join(authlist)    
          genrelst = data["genres"]
          genres=", "
          genlist = []
          for element in genrelst:
              genlist.append(element["name"])
          genres = genres.join(genlist)
        except: 
          error = discord.Embed(title="Error")
          error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
          return error  
    content = "\n" + dic["synopsis"][:2048] + "\n\n"
    if M_flag == 0:
        stats = "Type: " + dic["media_type"] + "\nStatus: " + dic["status"] + "\nStudios: " + studios + "\nEpisodes: " + dic["num_episodes"] + "\nStart Date: " + dic["start_date"] +"\nScore: " + dic["mean"] + "\nRating: " + dic["rating"] + "\nGenres: " + genres  

    else:
        stats =  "\nType: " + dic["media_type"] + "\nStatus: " + dic["status"] + "\nAuthors: " + authors + "\nChapters: " + dic["num_chapters"] + "\nVolumes: " + dic["num_volumes"] + "\nPublished: " + dic["start_date"] +"\nScore: " + dic["mean"] + "\nGenres: " + genres
            
    embed = discord.Embed(
        title=dic["title"],
        url=url,
        description = content,
        color = discord.Colour.red()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=image_url)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed       

