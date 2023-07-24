import discord
from discord.ext import commands
import random
import os
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents= intents)
from function_calling_sloan import *
disc_api = os.environ.get("DISCORD_API")
@bot.command()
async def hello(ctx):
  await ctx.send("Hello " + ctx.author.display_name)

@bot.command()
async def test_img(ctx):
  sample_test_fn()
  image_file = discord.File('sample_plot.png')
  embed = discord.Embed()
  embed.set_image(url='attachment://sample_plot.png')
  await ctx.send(file=image_file, embed=embed)

  # await ctx.send(xid)
  os.remove('sample_plot.png')
# question = "Retrieve the PhotoObjAll table for the run number 94, rerun number 301, camcol 6, and field 94."
@bot.command()
async def func_call(ctx, * , question:str):
  x = function_call(question)
  await ctx.send(x)
  
bot.run(disc_api)