import sys,random,discord,time
import os
import stonks
from discord.ext import commands 
from datetime import date
import datetime
from datetime import datetime
from dotenv import load_dotenv
import youtube_dl
import hashlib
import asyncio
#from geizhals import Geizhals
os.system("pip install discord.py[voice]")

load_dotenv()

prefix_command="!!"

def hash_text(text):
  hashed_text=hashlib.sha256(str(text).encode()).hexdigest()
  return hashed_text

#log 
def log(user,server,user_command):
  log_time=datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
  f=open("log/bot_user_log.txt","a")
  f.write(str(user)+" | "+str(server)+" | "+str(user_command)+" | "+str(log_time)+"\n")
  f.close()
  f=open("log/bot_command_log.txt","a")
  f.write(server+" | "+str(user_command)+" | "+str(log_time)+"\n")
  f.close
  with open("log/hash_bot_user_log.txt","a") as f:
    f.write(str(hash_text(user))+" | "+str(hash_text(server))+" | "+str(user_command)+" | "+str(log_time)+"\n")
  with open("log/hash_bot_command_log.txt","a") as f:
    f.write(str(hash_text(server))+" | "+str(user_command)+" | "+str(log_time))

client=commands.Bot(command_prefix=prefix_command)
client.remove_command('help')

#login and set activity
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    activity=discord.Game(name=prefix_command+"help")
    await client.change_presence(status=discord.Status.online, activity=activity)

#ping to server
@client.command(pass_context=True)
async def ping(ctx):
  log(ctx.message.author,ctx.message.guild.name,ctx.command)
  await ctx.send(f"Ping: {client.latency}")

#pre_stock data
@client.command(pass_context=True)
async def pre_stock(ctx,*,stock_date):
  log(ctx.message.author,ctx.message.guild.name,ctx.command)
  send=True
  stock_date=stock_date.replace(" ","")
  stock_date=stock_date.split("-")
  if int(stock_date[1])>12 or int(stock_date[2])>31:send=False
  if int(stock_date[0])>date.today().year:send=False
  if int(stock_date[1])>date.today().month and int(stock_date[0])==date.today().year:send=False
  if int(stock_date[2])>date.today().day and int(stock_date[1])==date.today().month and int(stock_date[0])==date.today():send=False
  if send:
    picture_path=stonks.predefinded_stocks(stock_date[0]+"-"+stock_date[1]+"-"+stock_date[2])
    await ctx.send(file=discord.File(picture_path))
    os.remove(picture_path)
  else:
    await ctx.send("Error! Use '"+prefix_command+"help'")

#stock data
@client.command(pass_context=True)
async def stock(ctx,*,user_message):
  log(ctx.message.author,ctx.message.guild.name,ctx.command)
  send=True
  user_message=user_message.split(" ")
  stock=user_message[0]
  period=user_message[1]
  period_list=["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y"]
  if period not in period_list:send=False
  if send:
    picture_path=stonks.custom_stock(stock,period)
    await ctx.send(file=discord.File(picture_path))
    os.remove(picture_path)
  else:
    await ctx.send("error") 

#shoot russian roulette
@client.command(pass_context=True)
async def shoot(ctx):
  log(ctx.message.author,ctx.message.guild.name,ctx.command)
  gun=random.choice(["click","peng"])
  if gun=="peng":
    user=ctx.message.author
    print(user)
    await ctx.send(gun+"\nYou are dead, like Winnie the pooh")
    await user.kick(reason=None)
  else:
    await ctx.send(gun+"\nYou are lucky bro")

#ping_spam
@client.command(pass_context=True)
async def ping_spam(ctx,*,member:discord.Member):
  pass

#say=tts
@client.command()
async def say(ctx,*,user_message):
  await ctx.send(user_message,tts=True)

#join voice channel
@client.command(pass_context=True)
async def join(ctx):
  if ctx.author.voice:
    channel=ctx.message.author.voice.channel
    await channel.connect()
  else:
    await ctx.send("You are not in a voice channel")

#leave voice channel
@client.command(pass_context=True)
async def leave(ctx):
  if ctx.voice_client:
    await ctx.guild.voice_client.disconnect()
    await ctx.send("i left")
  else:
    await ctx.send("I am not in a voice channel")

#musik
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
  def __init__(self,source,*,data,volume=0.5):
    super().__init__(source, volume)
    self.data=data
    self.title=data.get('title')
    self.url=data.get('url')

  @classmethod
  async def from_url(cls,url,*,loop=None,stream=False):
    loop=loop or asyncio.get_event_loop()
    data=await loop.run_in_executor(None,lambda: ytdl.extract_info(url,download=not stream))
    if 'entries' in data:
      # take first item from a playlist
      data=data['entries'][0]
    filename=data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

song_queue=[]

#add song to queue
@client.command()
async def queue(ctx,url):
  global song_queue
  song_queue.append(url)
  await ctx.send(f'`{url}` added to queue!')

#remove from queue
@client.command()
async def remove(ctx,number):
  global song_queue
  try:
    del(song_queue[int(number)])
    await ctx.send(f'Your queue is now `{song_queue}!`') 
  except:
    await ctx.send('Your queue is either **empty** or the index is **out of range**')

#play first song from queue      
@client.command()
async def play(ctx):
  global song_queue
  server=ctx.message.guild
  voice_channel=server.voice_client
  async with ctx.typing():
    player=await YTDLSource.from_url(song_queue[0], loop=client.loop)
    voice_channel.play(player,after=lambda e: print('Player error: %s' % e) if e else None)
  await ctx.send('**Now playing:** {}'.format(player.title))
  del(song_queue[0])

#pause song
@client.command()
async def pause(ctx):
  server=ctx.message.guild
  voice_channel=server.voice_client
  voice_channel.pause()

#resum song
@client.command()
async def resume(ctx):
  server=ctx.message.guild
  voice_channel=server.voice_client
  voice_channel.resume()

#view queue
@client.command()
async def view(ctx):
  await ctx.send(f'Your queue is now `{song_queue}!`')

#stop playing
@client.command()
async def stop(ctx):
  server=ctx.message.guild
  voice_channel=server.voice_client
  voice_channel.stop()

#help
@client.command(pass_context=True)
async def help(ctx):
  log(ctx.message.author,ctx.message.guild.name,ctx.command)
  embed=discord.Embed(colour=discord.Colour.orange())
  embed.set_author(name='Help')
  embed.add_field(name=prefix_command+'ping',value='Returns ping',inline=False)
  embed.add_field(name=prefix_command+'pre_stock',value='Needs a date(yyyy-mm-dd)',inline=False)
  embed.add_field(name=prefix_command+'stock',value='Needs a stock("gme") and period("1d,5d,1mo,3mo,6mo,1y,2y,5y,10y")',inline=False)
  embed.add_field(name=prefix_command+"shoot",value="Russain Roulette",inline=False)
  embed.add_field(name=prefix_command+"say",value="tts",inline=False)
  embed.add_field(name=prefix_command+"join",value="joins your voice channel",inline=False)
  embed.add_field(name=prefix_command+"leave",value="leaves your voice channel",inline=False)
  embed.add_field(name=prefix_command+"queue <url>",value="add a song to the queue",inline=False)
  embed.add_field(name=prefix_command+"remove <index>",value="removes a song on index",inline=False)
  embed.add_field(name=prefix_command+"play",value="plays the queue",inline=False)
  embed.add_field(name=prefix_command+"pause",value="pauses current song",inline=False)
  embed.add_field(name=prefix_command+"resume",value="resumes paused song",inline=False)
  embed.add_field(name=prefix_command+"view",value="shows queue",inline=False)
  embed.add_field(name=prefix_command+"stop",value="stop current song",inline=False)
  await ctx.send(embed=embed)

"""
base_url="https://geizhals.de/"
products=[]
prices=[]
for i in products:
  obj=Geizhals(base_url+i+".hmtl",'DE')
  device=obj.parse()
  prices.add(device)
print(prices)  
"""

client.run(os.getenv("DISCORD_TOKEN"))


#credits for the music part: https://github.com/RK-Coding/Videos/blob/master/rkcodingmusic.py