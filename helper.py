from discord.ext import commands

class helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.helpMessage = """

```

General commands:

!help - Displays all the available commands.
!p <keywords> - Finds the song on youtube and plays it in your current channel.
!q - Displays the current music queue.
!skip - Skips the current song being played.
!empty - Stops the music and clears the queue.
!leave - Disconnects the bot from the voice channel.
!pause - Pauses the current song being played or resumes if already paused.
!resume - Resumes playing the current song.
!ask <keywords> - Asks google a question and returns the top 5 answers.

```
"""

        self.textChannelList = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.textChannelList.append(channel)
        await self.sendToAll(self.helpMessage)

    async def sendToAll(self, message):
        for textChannel in self.textChannelList:
            await textChannel.send(message)

    @commands.command(name="help", aliases=["h"], description="Displays all the available commands.")
    async def help(self, ctx):
        await ctx.send(self.helpMessage)