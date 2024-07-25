import discord
from discord.ext import commands
from imdb import Cinemagoer
from colorama import Back,Fore,Style
import config
import asyncio
import time
import platform

bot = commands.Bot(command_prefix = '.', intents = discord.Intents.all())
prfx = (Back.BLACK + Fore.GREEN + time.strftime(("%H:%M:%S UTC"), time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Friends'))

    print(prfx + ' Connected to bot: ' + Fore.CYAN + bot.user.name)
    print(prfx + ' Bot ID: ' + Fore.CYAN + str(bot.user.id))
    print(prfx + ' Discord Version: '+ Fore.CYAN + discord.__version__)
    print(prfx + ' Python Version: '+ Fore.CYAN + str(platform.python_version()))
    
@bot.command()
async def owner(ctx):
  await ctx.send('My owner is <@724606248158232646> and this was done by github')
  print(prfx + 'Owner command sent by: ' + Fore.CYAN + ctx.message.author.name)

@bot.command()
async def updatestatus(ctx,message1=None):
    print(prfx + 'Updating Status Command Started')
    def check(m):
      return m.author == ctx.message.author and m.channel == ctx.message.channel
    if message1 == None:
      await ctx.send('Please provide a status!')
      print(prfx + 'Update Status Command Unsuccessful by user error of: '+ Fore.CYAN + ctx.message.author.name)
    elif message1.lower() == 'watching':
      await ctx.send('Please provide what to watch!')
      msg1 = await bot.wait_for('message', check=check)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=msg1.content))
      await ctx.send(f'Updated to watching {msg1.content}!')
      print(prfx + 'Update Status Command Successful by: ' + Fore.CYAN + ctx.message.author.name)
    elif message1.lower() == 'playing':
      await ctx.send('Please provide what to play!')
      msg1 = await bot.wait_for('message', check=check)
      await bot.change_presence(activity=discord.Game(msg1.content))
      await ctx.send(f'Updated to playing {msg1.content}!')
      print(prfx + 'Update Status Command Successful by: ' + Fore.CYAN + ctx.message.author.name)
    elif message1.lower() == 'listening':
      await ctx.send('Please provide what to listen!')
      msg1 = await bot.wait_for('message', check=check)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=msg1.content))
      await ctx.send(f'Updated to listening to {msg1.content}!')
      print(prfx + 'Update Status Command Successful by: ' + Fore.CYAN + ctx.message.author.name)
    elif message1.lower() == 'streaming':
      await ctx.send('Please provide what to stream')
      msg1 = await bot.wait_for('message', check=check)
      await ctx.send('Please provide URL!')
      msg2 = await bot.wait_for('message', check=check)
      await bot.change_presence(activity=discord.Streaming(name=msg1.content, url=msg2.content))
      await ctx.send(f'Updated to streaming {msg1.content} on {msg2.content}!')
      print(prfx + 'Update Status Command Successful by: ' + Fore.CYAN + ctx.message.author.name)
    else:
      await ctx.send('Did not percieve your status! [choose either watching, playing, listening or streaming!]')
      print(prfx + 'Update Status Command unsuccessful due to user error by: '  + Fore.CYAN + ctx.message.author.name)

@bot.command()
@commands.has_role('Administrator')
async def shutdown(ctx):
  await ctx.send('This bot is shutting down')
  print(prfx + 'Bot to shutdown command initiated')
  await bot.close()
@bot.command()
async def userinfo(ctx, member:discord.Member=None):
  print(prfx + 'UserInfo Command By: ' + Fore.CYAN + ctx.message.author.name)
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
      finalplot = finalmovie['plot outline']
    except:
      finalplot = 'N/A'
    try:
      coverpg = finalmovie['cover url']
    except:
      coverpg = 'https://upload.wikimedia.org/wikipedia/commons/5/5a/Black_question_mark.png'
    embed2 = discord.Embed(title=moviestitle, description=finalplot, colour=discord.Color.green(),timestamp=ctx.message.created_at)
    embed2.set_thumbnail(url=coverpg)
    embed2.add_field(name='Year of Release', value=str(moviesyear))
    embed2.add_field(name='Director Of Movie', value = moviesdirector)
    embed2.add_field(name='⭐ Rating (Out of 10)', value = str(moviesrating))

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
    try:
      embed2.add_field(name='IMBd Link', value = URL)
    except:
      pass
    return embed2


  
  msg = await bot.wait_for('message', check=check)
  for i in range(len(idlist)):
    if int(msg.content)-1 == i:
      idfinal = idlist[i]
  embed2 = await loop.run_in_executor(None, detailedmovie, idfinal)
  await ctx.send(embed=embed2)
  await print(prfx + 'Movie Command By: ' + Fore.CYAN + ctx.message.author.name)

@bot.command()
@commands.has_role('Administrator')
async def sendmessage(ctx, message=None):
  def check(m):
      return m.author == ctx.message.author and m.channel == ctx.message.channel
  if message == None:
    ctx.send('Please provide a channel ID to send into!')
  channel = bot.get_channel(int(message))
  await ctx.send('Please provide content for the message')
  msg3 = await bot.wait_for('message', check=check)
  await channel.send(msg3.content)
  await ctx.send('Done!')
  await print(prfx + 'Channel Message Command By: ' + Fore.CYAN + ctx.message.author.name + 'to ' + str(channel) + 'with the content of '+ msg3.content)

@bot.command()
@commands.has_role('Administrator')
async def dm(ctx, message=None):
  def check(m):
      return m.author == ctx.message.author and m.channel == ctx.message.channel
  if message == None:
    ctx.send('Please provide a userID to DM into!')
  user = bot.get_user(int(message))
  await ctx.send('Please provide content for the dm')
  msg4 = await bot.wait_for('message', check=check)
  await user.send(msg4.content)
  await ctx.send('Done!')
  await print(prfx + 'Direct Message Command By: ' + Fore.CYAN + ctx.message.author.name + 'to '+ str(user) + 'with the content of '+ msg4.content)

@bot.command()
async def playaudio(ctx, message2 =None):
  if message2 == None:
    ctx.send('Please provide a numeral for audio')
  user=ctx.message.author
  voicech = ctx.author.voice.channel
  if voicech != None:
      vc = await voicech.connect()
  else:
      await client.say('User is not in a channel.')

@bot.event()
async def on_member_join(member):
    joined_at = member.joined_at.strftime("%b %d, %Y, %T")
    welcomeembed = discord.Embed(title="New Member!",description=f"Please welcome our new member, {member.mention}! Nesamani is excited to have you here! :hug_pepe:", colour=discord.Color.green(),timestamp=joined_at)
    welcomeebed.set_thumbnail(url=member.avatar.url)
    channel = 1145809051888922694
    user = member.id
    await channel.send(embed=welcomeembed)
    await user.send("Welcome to the server da! Hope you have a great time, make sure to check out the welcome screen and get your roles and channels and say hello!")
    await print(prfx + ' New Member Joined: ' + Fore.CYAN + member.name)


bot.run(config.token)
