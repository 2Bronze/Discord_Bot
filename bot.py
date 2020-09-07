import os
import random
import requests
import discord
from discord.ext import commands

token = os.getenv('DISCORD_TOKEN')
RIOT_API = 'RGAPI-68d77d95-0c8c-45a3-bee5-679b70474ab6'

bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the authority to execute this command')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('This command does not exist')

@bot.command(name='inspiration', help="Inspires you")
async def Inspiration(ctx):
    quotes = ['The Way Get Started Is To Quit Talking And Begin Doing.',
              'The Pessimist Sees Difficulty In Every Opportunity. The Optimist Sees Opportunity In Every Difficulty',
              'Don’t Let Yesterday Take Up Too Much Of Today',
              'You Learn More From Failure Than From Success. Don’t Let It Stop You. Failure Builds Character',
              'It’s Not Whether You Get Knocked Down, It’s Whether You Get Up',
              f'There is no hope for you {ctx.author}',
              'If You Are Working On Something That You Really Care About, You Don’t Have To Be Pushed. The Vision Pulls You.',
              'We Generate Fears While We Sit. We Overcome Them By Action',
              'What You Lack In Talent Can Be Made Up With Desire, Hustle And Giving 110% All The Time'

    ]
    quote = random.choice(quotes)
    await ctx.send(quote)

@bot.command(name='coin', help = 'Flips a coin')
async def coin_toss(ctx):
        coinflip = random.randint(0,1)
        if coinflip == 0:
            await ctx.send('Heads')
        else:
            await ctx.send('Tails')

@bot.command(name='ct-channel', help ='Creates text channel')
@commands.has_role('Admin')
async def ct_channel(ctx, new_channel):
    server = ctx.guild
    existing_channel = discord.utils.get(server.text_channels, name = new_channel)
    if not existing_channel:
        await server.create_text_channel(new_channel)
    else:
        await ctx.send(f'{new_channel} already exists')

@bot.command(name='dt-channel', help = 'Deletes text channel')
@commands.has_role('Admin')
async def dt_channel(ctx, channel):
    server = ctx.guild
    existing_channel = discord.utils.get(server.text_channels, name = channel)
    if not existing_channel:
        await ctx.send(f'{channel} does not exist')
    else:
        await discord.TextChannel.delete(existing_channel)

@bot.command(name='cv-channel', help='Creates voice channel')
@commands.has_role('Admin')
async def cv_channel(ctx, new_channel):
    server = ctx.guild
    existing_channel = discord.utils.get(server.voice_channels, name=new_channel)
    if not existing_channel:
        await server.create_voice_channel(new_channel)
    else:
        await ctx.send(f'{new_channel} already exists')

@bot.command(name='dv-channel', help = 'Deletes voice channel')
@commands.has_role('Admin')
async def dv_channel(ctx,channel):
    server = ctx.guild
    existing_channel = discord.utils.get(server.voice_channels, name=channel)
    if not existing_channel:
        await ctx.send(f'{channel} does not exist')
    else:
        await discord.VoiceChannel.delete(existing_channel)

@bot.command(name='Freechamps', help = 'Free champ rotation')
async def Freechamps(ctx, region):
    URL = 'https://'+ region + '.api.riotgames.com/lol/platform/v3/champion-rotations' + '?api_key=' + RIOT_API
    response = requests.get(URL)
    JSON = response.json()
    await ctx.send(JSON["freeChampionIds"])

@bot.command(name = 'Summoner', help = 'Get Summoner info')
async def Summonerid(ctx, region, summonername):
    URL1 = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonername + '?api_key=' + RIOT_API
    response1 = requests.get(URL1).json()
    id = response1["id"]
    URL2 = 'https://' + region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + id + '?api_key=' + RIOT_API
    response2 = requests.get(URL2).json()
    wins = response2[0]["wins"]
    losses = response2[0]["losses"]
    total = wins + losses
    winrate = (wins / total) * 100
    await ctx.send(response2[0]["queueType"] + ': ' + response2[0]["tier"] + ' ' + response2[0]["rank"])

bot.run(token)

