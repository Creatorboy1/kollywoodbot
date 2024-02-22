import discord
from discord.ext import commands
import config
from imdb import Cinemagoer
import asyncio

bot = commands.Bot(command_prefix = '.', intents = discord.Intents.all())

@bot.command()
async def owner(ctx):
  await ctx.send('My owner is <@724606248158232646> and this was done by github')

@bot.command()
async def shutdown(ctx):
  await ctx.send('This bot is shutting down')
  await bot.close()
@bot.command()
async def userinfo(ctx, member:discord.Member=None):
  if member == None:
    member = ctx.message.author
  roles = [role for role in member.roles]
  embed = discord.Embed(title='User info', description = f'A detailed info about the user {member.name}', colour=discord.Color.green(),timestamp=ctx.message.created_at)
  embed.set_thumbnail(url=member.avatar)
  embed.add_field(name='ID',value=member.id)
  embed.add_field(name='Name',value=member.name)
  embed.add_field(name='Nickname',value=member.nick)
  embed.add_field(name='Join At',value=member.joined_at.strftime('%a, %B %d, %Y, %I:%M %p'))
  embed.add_field(name='Status',value=member.status)
  embed.add_field(name='Account Created',value=member.created_at.strftime('%a, %B %d, %Y, %I:%M %p'))
  embed.add_field(name=f'Roles ({len(roles)})',value=' '.join([role.mention for role in roles]))
  embed.add_field(name='Top Role', value=member.top_role)
  embed.add_field(name='Bot?',value=member.bot)
  await ctx.send(embed=embed)

@bot.command()
async def searchmovie(ctx, movie=None):
  if movie == None:
    await ctx.send('Please search with a movie name!')


  def searcher(movie):
    im = Cinemagoer()
    movies = im.search_movie(movie)
    count = 0
    embed1 = discord.Embed(title='Top Search Results', description = 'Please search return with a number', colour=discord.Color.green(),timestamp=ctx.message.created_at)
    countlist = []
    idlist = []
    for i in range(len(movies)):
      try:
        id = movies[i].getID()
        idlist.append(id)
        movie = im.get_movie(id)
        moviesyear = movie['year']
        moviestitle = movie['title']
        moviesdirectors = ' '.join(map(str,movie['directors']))
      except:
        continue
      if i >= 4:
        break
      countlist.append(str(count))
      count += 1
      embed1.add_field(name=str(count),value=f'{moviestitle} {moviesyear} by {moviesdirectors}')

    return embed1, countlist, idlist
  
  loop = asyncio.get_running_loop()
  embed1, countlist, idlist = await loop.run_in_executor(None, searcher, movie)
  await ctx.send(embed=embed1)



  def check(m):
    return m.content in countlist and m.channel == ctx.message.channel
  
  def detailedmovie(idfinal):
    im = Cinemagoer()
    finalmovie = im.get_movie(idfinal)
    moviestitle = finalmovie['title']
    moviesyear = finalmovie['year']
    moviesdirector = ' '.join(map(str, finalmovie['directors']))
    moviesrating = finalmovie['rating']
    try:
      finalplot = finalmovie['synopsis'][0]
    except:
      finalplot = 'N/A'
    embed2 = discord.Embed(title=moviestitle, description='A summary of your chosen movie!', colour=discord.Color.green(),timestamp=ctx.message.created_at)
    embed2.add_field(name='Year of Release', value=str(moviesyear))
    embed2.add_field(name='Director Of Movie', value = moviesdirector)
    embed2.add_field(name='Rating (Out of 10)', value = str(moviesrating))

    try:
      moviescast = ', '.join(map(str,finalmovie['cast']))
      embed2.add_field(name='Cast', value = str(moviescast))
    except:
      pass
    try:
      genres = ', '.join(map(str,finalmovie['genres']))
      embed2.add_field(name='Genres', value = str(genres))
    except:
      pass
    try:
      awards = ', '.join(map(str,finalmovie['awards']))
      embed2.add_field(name='Awards', value = str(awards))
    except:
      pass
    try:
      video = ', '.join(map(str,finalmovie['video clips']))
      embed2.add_field(name='Video Clips', value = str(video))
    except:
      pass
    return embed2


  
  msg = await bot.wait_for('message', check=check)
  for i in range(len(idlist)):
    if int(msg.content)-1 == i:
      idfinal = idlist[i]
  embed2 = await loop.run_in_executor(None, detailedmovie, idfinal)
  await ctx.send(embed=embed2)

bot.run(config.token)