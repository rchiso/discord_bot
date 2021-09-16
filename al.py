import json
import requests
import discord
from replit import db

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def al(q, author, M_flag):
    if M_flag == 0:
        query = '''
        query ($search: String) {
          Media(search: $search, type: ANIME) {
            id
            title {
              romaji
            }
            type
            format
            chapters
            volumes
            episodes
            status
            genres
            studios(isMain: true) {
              edges {
                node {
                  name 
                }
              }
            }
            description
            coverImage {
              medium
            }
            siteUrl
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
          }
        }
        '''
    else:
        query = '''
        query ($search: String) {
          Media(search: $search, type: MANGA) {
            id
            title {
              romaji
            }
            type
            format
            chapters
            volumes
            episodes
            status
            genres
            staff{
              edges {
                node {
                  name { 
                    full
                  } 
                }
                role
              }
            }
            description
            coverImage {
              medium
            }
            siteUrl
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
          }
        }
        '''
    
    variables = {
        'search': q
    }
    url = 'https://graphql.anilist.co'
    
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = json.loads(response.text)
    dic = {"id": 0, "type":"Unknown", "format": "Unknown", "status":"Unknown", "genres":"Unknown", "description":"Unknown", "siteUrl": "Unknown", "startDate":"Unknown", "endDate": "Unknown"}
    if "errors" in data.keys():
        error = discord.Embed(
            title="Title not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
    for element in dic.keys():
        try:
          if type(data["data"]["Media"][element]) != None:
              dic[element] = data["data"]["Media"][element]
              
        except KeyError:
          continue
    try:
      chapters = "Unknown"
      if (data["data"]["Media"]["chapters"]) != None:
        chapters = str(data["data"]["Media"]["chapters"]) 
      volumes = "Unknown"
      if (data["data"]["Media"]["volumes"]) != None:
        volumes = str(data["data"]["Media"]["volumes"])  
      episodes = "Unknown" 
      if (data["data"]["Media"]["episodes"]) != None:
        episodes = str(data["data"]["Media"]["episodes"])      
      title = data["data"]["Media"]["title"]["romaji"]
      coverImage = data["data"]["Media"]["coverImage"]["medium"]
      genrelst = dic["genres"]
      genres=", "
      genlist = []
      for element in genrelst:
          genlist.append(element)
      genres = genres.join(genlist)
      slist=[]
      for element in dic["startDate"].keys():
        if dic["startDate"][element]!= None:
          slist.append(str(dic["startDate"][element]))
      elist=[]
      for element in dic["endDate"].keys():
        if dic["endDate"][element]!= None:
          elist.append(str(dic["endDate"][element]))
      sdate="/"
      edate="/"
      sdate=sdate.join(slist)
      edate=edate.join(elist)        
      if M_flag == 0:
        studiolst = data["data"]["Media"]["studios"]["edges"]
        stdlist=[]
        studios=", "
        for element in studiolst:
            stdlist.append(element["node"]["name"])
        studios = studios.join(stdlist)  
      else:
        stafflst = data["data"]["Media"]["staff"]["edges"]
        stflist=[]
        staff=", "
        for element in stafflst:
            if(element["role"].find("Story") !=-1 or element["role"].find("Art") != -1):
              stflist.append(element["node"]["name"]["full"])
        staff = staff.join(stflist)  
      content = "\n" + remove_html_tags(dic["description"]) + "\n\n"
      if M_flag == 0:
          stats = "Type: " + dic["type"] + "\nFormat: " + dic["format"] + "\nStatus: " + dic["status"] + "\nStudios: " + studios + "\nEpisodes: " + episodes +  "\nGenres: " + genres + "\nAired: " + sdate + " to " + edate
      else:
          stats = "Type: " + dic["type"] + "\nFormat: " + dic["format"] + "\nChapters: " + chapters + "\nVolumes: " + volumes + "\nStaff: " + staff + "\nStatus: " + dic["status"] + "\nPublished: " + sdate + " to " + edate + "\nGenres: " + genres
    except:
      error = discord.Embed(
            title="Title not found"
        )
      error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
      return error
      
    try:
      if str(author.id) in db.keys():
        query='''
        query ($userName: String, $mediaId: Int) { 
          MediaList(mediaId: $mediaId, userName: $userName){
            status
            progress
            progressVolumes
            repeat
            score(format: POINT_10_DECIMAL)
          }
          }

        '''

        variables = {
          "userName": db[str(author.id)][0], 
          "mediaId": int(dic["id"])
        }
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = json.loads(response.text)
        user_header = db[str(author.id)][0] + "'s Stats: "
        if data["data"]["MediaList"] == None:
          user_stats = db[str(author.id)][0] + " does not have this item in their list"
        else:
          status = data["data"]["MediaList"]["status"]
          progress = data["data"]["MediaList"]["progress"]
          if(data["data"]["MediaList"]["progressVolumes"]!=None):
            vols = data["data"]["MediaList"]["progressVolumes"]
          repeat = data["data"]["MediaList"]["repeat"]
          score = data["data"]["MediaList"]["score"]
          if M_flag == 0:
            user_stats = "Status: " + status + "\nEpisodes Watched: " + str(progress) + "\nRewatches: " + str(repeat) + "\nScore: " + str(score) 
          else:
            user_stats = "Status: " + status + "\nChapters Read: " + str(progress) + "\nVolumes Read: " + str(vols) + "\nRereads: " + str(repeat) + "\nScore: " + str(score)
      else:
        user_header = str(author.name) + " has not registered their account"
        user_stats = "Unavailable"

      embed = discord.Embed(
          title=title,
          url=dic["siteUrl"],
          description = content,
          color = discord.Colour.red()
      )
      embed.add_field(name="Information", value = stats, inline = False)
      embed.add_field(name=user_header, value = user_stats, inline = False)
      embed.set_thumbnail(url=coverImage)
      embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
      return embed 
    except:
      error = discord.Embed(
            title="Error while fetching user stats"
        )
      error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
      return error


def profile(auth):
  #[discord_id] = [al_username, animedays, animescore, animecount, mangadays, mangascore, mangacount, profilepic_url]
  if str(auth.id) in db.keys():
    query = '''
    query ($search: String) { 
    User(name: $search){
      avatar{
        medium
      }
      statistics{
        anime{
          meanScore
          minutesWatched
          count
        }
        manga{
          meanScore
          chaptersRead
          volumesRead
          count
        }
      }
      
      
    }
    }
    '''
    variables = {
        "search": db[str(auth.id)][0]
      }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = json.loads(response.text)
    avatar_url = data["data"]["User"]["avatar"]["medium"]
    anime_score = data["data"]["User"]["statistics"]["anime"]["meanScore"]
    anime_count = data["data"]["User"]["statistics"]["anime"]["count"]
    anime_days = data["data"]["User"]["statistics"]["anime"]["minutesWatched"]
    anime_days = round(anime_days/1440, 1)

    manga_score = data["data"]["User"]["statistics"]["manga"]["meanScore"]
    manga_count = data["data"]["User"]["statistics"]["manga"]["count"]
    manga_chaps = data["data"]["User"]["statistics"]["manga"]["chaptersRead"]
    manga_vols = data["data"]["User"]["statistics"]["manga"]["volumesRead"]
    x = round((manga_chaps*8)/1440, 1)
    y = round((manga_vols*1.2)/24, 1)
    manga_days = max(x, y)

    #[discord_id] = [al_username, animedays, animescore, animecount, mangadays, mangascore, mangacount, profilepic_url]
    db[str(auth.id)] = [db[str(auth.id)][0], anime_days, anime_score, anime_count, manga_days, manga_score, manga_count, avatar_url]
    l = db[str(auth.id)]
    embed = discord.Embed(
      title = l[0] + "'s Profile",
      url = "https://anilist.co/user/" + l[0]
    )
    embed.add_field(name="Anime:", value="Total Anime: " + str(l[3]) + "\nMean Score: " + str(l[2]) + "\nTotal Days: " + str(l[1]), inline=False)
    embed.add_field(name="Manga:", value="Total Manga: " + str(l[6]) + "\nMean Score: " + str(l[5]) + "\nTotal Days: " + str(l[4]), inline=False)
    embed.set_thumbnail(url=l[-1])
    embed.set_footer(icon_url=auth.avatar_url, text=f"Requested by {auth.name}")
    return embed
  else:
    error = discord.Embed(
            title="Error"
        )
    error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
    return error  


def register(q, author):
  
  query = '''
  query ($search: String) { 
  User(name: $search){
    avatar{
      medium
    }
    statistics{
      anime{
        meanScore
        minutesWatched
        count
      }
      manga{
        meanScore
        chaptersRead
        volumesRead
        count
      }
    }
    
    
  }
  }
  '''
  variables = {
      "search": q
    }

  url = 'https://graphql.anilist.co'
  response = requests.post(url, json={'query': query, 'variables': variables})
  data = json.loads(response.text)
  if "errors" in data.keys():
      error = discord.Embed(
              title="Registration Failed"
          )
      return error  

  avatar_url = data["data"]["User"]["avatar"]["medium"]

  anime_score = data["data"]["User"]["statistics"]["anime"]["meanScore"]
  anime_count = data["data"]["User"]["statistics"]["anime"]["count"]
  anime_days = data["data"]["User"]["statistics"]["anime"]["minutesWatched"]
  anime_days = round(anime_days/1440, 1)

  manga_score = data["data"]["User"]["statistics"]["manga"]["meanScore"]
  manga_count = data["data"]["User"]["statistics"]["manga"]["count"]
  manga_chaps = data["data"]["User"]["statistics"]["manga"]["chaptersRead"]
  manga_vols = data["data"]["User"]["statistics"]["manga"]["volumesRead"]
  x = round((manga_chaps*8)/1440, 1)
  y = round((manga_vols*1.2)/24, 1)
  manga_days = max(x, y)

  #[discord_id] = [al_username, animedays, animescore, animecount, mangadays, mangascore, mangacount, profilepic_url]
  db[str(author.id)] = [q, anime_days, anime_score, anime_count, manga_days, manga_score, manga_count, avatar_url]

  embed = discord.Embed(
              title="Registration Successful"
          )
  return embed


