import discord
from discord.ext import commands

from helper import helper
from musicManager import musicManager
from responseManager import responseManager
from googleSearch import googleSearch

TOKEN_FILE_NAME = str("token.txt")
COMMAND_PREFIX = str("!")
STARTING_INDEX = int(0)

async def sendMessage(message):
    try:
        response = responseManager(message)
        await message.channel.send(response.handleResponse())
    except Exception as e:
        print(e)

def getToken():
    file = open(TOKEN_FILE_NAME)
    token = file.read()
    file.close()
    return token

def runDiscordBot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.dm_messages = True
    intents.guilds = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        bot.remove_command("help")
        await bot.add_cog(helper(bot))
        await bot.add_cog(musicManager(bot))
        await bot.add_cog(googleSearch(bot))

    @bot.event
    async def on_message(message):
        if message.content[STARTING_INDEX] == COMMAND_PREFIX:
            await bot.process_commands(message)
            return
        if message.author == bot.user:
            return
        await sendMessage(message)

    bot.run(getToken())