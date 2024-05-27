import os
import json
import requests
import discord 
import time


def mov(q, author,T_flag):
    f = open('secrets.json')
    secrets = json.load(f)
    key = secrets["api_key"]
    temp_list = q.split('(')
    q = temp_list[0]
    if len(temp_list) != 1:  
      year_string = temp_list[-1][:-1]
    else:
      year_string = "awooga"    
    try:
      int(year_string)
      if T_flag == 0:
        url = "http://www.omdbapi.com/?t=" + q + "&y=" + year_string + "&type=movie&apikey=" + key

      else:
        url = "http://www.omdbapi.com/?t=" + q + "&y=" + year_string + "&type=series&apikey=" + key
    except ValueError:  
      if T_flag == 0:
          url = "http://www.omdbapi.com/?t=" + q + "&type=movie&apikey=" + key
      else:
          url = "http://www.omdbapi.com/?t=" + q + "&type=series&apikey=" + key    
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "False":
        error = discord.Embed(
            title="Title not found"
        )
        error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
        return error
    poster = "https://www.messagetech.com/wp-content/themes/ml_mti/images/no-image.jpg"
    title = data["Title"]
    if data["Poster"][0] == "h":
      poster = data["Poster"]
    year = data["Year"]
    genres = data["Genre"]
    director = data["Director"]
    writer = data["Writer"]
    actors = data["Actors"]
    
    para = data["Plot"]
    score = data["imdbRating"]
    type_ = data["Type"]
    id_ = data["imdbID"]
    url_ = "https://www.imdb.com/title/" + id_
    
    if T_flag == 1:
      seasons = data["totalSeasons"]
    stats = "Type: " + type_ + "\nRating: " + str(score) + "\nYear: " + year +''' "\nSeasons: " + str(seasons) + '''"\nDirector: " + director + "\nActors: " + actors + "\nGenres: " + genres      
    content = "\n" + para[:2048] + "\n\n"
    if T_flag == 0:
      stats = "Type: " + type_ + "\nRating: " + str(score) + "\nYear: " + year + "\nDirector: " + director + "\nActors: " + actors + "\nGenres: " + genres
    else: 
      stats = "Type: " + type_ + "\nRating: " + str(score) + "\nYear: " + year +"\nSeasons: " + seasons + "\nWriter: " + writer + "\nActors: " + actors + "\nGenres: " + genres  
    embed = discord.Embed(
        title=title,
        url=url_,
        description = content,
        color = discord.Colour.green()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=poster)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed

def book(q, auth):
  response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + q)
  data = json.loads(response.text)
  if data["totalItems"] == 0:
        error = discord.Embed(
            title="Book not found"
        )
        error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
        return error
  title=""
  if "title" in  data["items"][0]["volumeInfo"].keys():      
    title = data["items"][0]["volumeInfo"]["title"]
  para=""
  if "description" in  data["items"][0]["volumeInfo"].keys(): 
    para = data["items"][0]["volumeInfo"]["description"]
  if len(para) > 750:
      para = para[:750] + "..."
  date_ =""
  if "publishedDate" in  data["items"][0]["volumeInfo"].keys(): 
    date_ = data["items"][0]["volumeInfo"]["publishedDate"]
  authorlst=[]
  if "authors" in  data["items"][0]["volumeInfo"].keys():   
    authorlst = data["items"][0]["volumeInfo"]["authors"]
  author=""
  for element in authorlst:
      author +=element + ", "
  id_ = data["items"][0]["id"]
  cover_image = "https://www.messagetech.com/wp-content/themes/ml_mti/images/no-image.jpg"
  if "imageLinks" in  data["items"][0]["volumeInfo"].keys():
    if "thumbnail" in  data["items"][0]["volumeInfo"]["imageLinks"].keys():
      cover_image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
  url = "http://books.google.com/books?id=" + id_
  categorylst=[]
  if "categories" in  data["items"][0]["volumeInfo"].keys(): 
    categorylst = data["items"][0]["volumeInfo"]["categories"]
  categories=""
  for element in categorylst:
      categories += element + " " 
  content = "\n" + para + "\n\n"
  stats = "Author: " + author + "\nPublishing Date: " + date_ + "\nCategories: " + categories
  embed = discord.Embed(
    title=title,
    url = url,
    description = content
  )
  embed.add_field(name="Information", value = stats, inline = False)
  embed.set_thumbnail(url=cover_image)
  embed.set_footer(icon_url=auth.avatar_url, text=f"Requested by {auth.name}")
  return embed    

def trace(q, author):
    api_url = "https://api.trace.moe/search?url=" + q
    response = requests.get(api_url)
    data_ = json.loads(response.text)
    if data_["error"]:
      error = discord.Embed(
            title="Unable to trace"
        )
      error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
      return error
    id_ = data_["result"][0]["anilist"]
    episode = str(data_["result"][0]["episode"])
    temp = int(data_["result"][0]["from"])
    stamp = time.strftime("%H:%M:%S", time.gmtime(temp))
    content = "Episode: " + episode + "\nTimestamp: " + stamp
    source_url = "https://anilist.co/anime/" + str(id_)
    query = '''
        query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (search)
            title {
              romaji
            }
            coverImage{
                medium
            }

        }
        }
        '''
    variables = {
      'id': id_
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = json.loads(response.text)
    title = data["data"]["Media"]["title"]["romaji"]
    cover_image= data["data"]["Media"]["coverImage"]["medium"]
    embed = discord.Embed(
        title=title,
        url=source_url,
        description = content,
        color = discord.Colour.red()
    )
    embed.set_thumbnail(url=cover_image)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed       
