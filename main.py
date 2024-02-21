import discord
from discord.ext import commands
import config


bot = commands.Bot(command_prefix = '.', intents = discord.Intents.all())

@bot.command()
async def owner(ctx):
  await ctx.send('My owner is <@724606248158232646> and this was done by github')

@bot.command()
async def shutdown(ctx):
  await ctx.send('This bot is shutting down')
  await bot.close()

bot.run(config.token)