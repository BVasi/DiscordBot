import discord
from discord.ext import commands
from youtubesearchpython import *
from pytube import YouTube
import yt_dlp

QUERY_LIMIT = int(1)
FIRST_IN_QUEUE = int(0)
FIRST_RESULT = int(0)
URL = str("url")
TITLE = str("title")
LINK = str("link")

def hasFoundResult(resultsDictionary) -> bool:
    if len(resultsDictionary) > 0:
        return True
    return False

class musicManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.musicQueue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def isQueueEmpty(self) -> bool:
        if len(self.musicQueue) > 0:
            return False
        return True

    def convertYoutubeUrlToOnlyAudioUrl(self):
        youtubeURL = self.musicQueue[FIRST_IN_QUEUE][URL]
        self.musicQueue.pop(FIRST_IN_QUEUE)
        # youtube = YouTube(youtubeURL)
        # audioStream = youtube.streams.filter(only_audio=True, file_extension="mp4").first()
        # return audioStream.url
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtubeURL, download=False)
            audio_url = info_dict[URL]
            return audio_url

    def playAudio(self):
        audioSource = discord.FFmpegPCMAudio(source=self.convertYoutubeUrlToOnlyAudioUrl(), **self.FFMPEG_OPTIONS)
        if audioSource is not None:
            self.vc.play(audioSource, after=lambda e: self.playNextSong())

    def playNextSong(self):
        if not self.isQueueEmpty():
            self.playAudio()

    async def connectToCallersChannel(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Connect to a voice channel if you want me to play music dumbo!")
            return
        else:
            voiceChannel = ctx.author.voice.channel
            voiceClient = ctx.voice_client

            if voiceClient is not None:
                await voiceClient.move_to(voiceChannel)
            else:
                vc = await voiceChannel.connect()
                self.vc = vc

    async def addSongToQueue(self, ctx, resultsDictionary):
        self.musicQueue.append({URL : resultsDictionary[FIRST_RESULT][LINK], TITLE : resultsDictionary[FIRST_RESULT][TITLE]})
        await ctx.send(f"Song `{resultsDictionary[FIRST_RESULT][TITLE]}` added to the queue!")

    async def searchSong(self, ctx, query):
        song = VideosSearch(query, limit = QUERY_LIMIT)
        resultsDictionary = song.result()['result']
        if not hasFoundResult(resultsDictionary):
            await ctx.send("An error has occured in finding the song. Try again! (or you could try a new song)")
        else:
            await self.addSongToQueue(ctx, resultsDictionary)

    @commands.command(name="play", aliases=["p"], description="Plays the selected song from youtube.")
    async def play(self, ctx, *args):
        query = " ".join(args)
        await self.connectToCallersChannel(ctx)
        await self.searchSong(ctx, query)
        if self.vc.is_playing() == False:
            self.playNextSong()

    @commands.command(name="pause", aliases=["ps"], description="Pauses the current song being played.")
    async def pause(self, ctx):
        if self.vc.is_playing():
            self.vc.pause()
        elif self.vc.is_paused():
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], description="Resumes playing the current song.")
    async def resume(self, ctx):
        if not self.vc.is_paused():
            return
        self.vc.resume()

    @commands.command(name="skip", aliases=["s"], description="Skips the currently played song.")
    async def skip(self, ctx):
        if self.vc is not None and self.vc.is_playing():
            self.vc.stop()
        self.playNextSong()

    def getFirstFiveSongsInQueue(self):
        songsInQueue = ""
        i = 0
        for song in self.musicQueue:
            songsInQueue += song['title'] + '\n'
            i += 1
            if i > 5: break
        return songsInQueue

    @commands.command(name="queue", aliases=["q"], description="Displays all the songs currently in the queue.")
    async def displayQueue(self, ctx):
        songsInQueue = self.getFirstFiveSongsInQueue()
        if songsInQueue != "":
            await ctx.send(songsInQueue)
        else:
            await ctx.send("Queue is empty!")

    @commands.command(name="empty", aliases=["clear", "c", "bin"], description="Stops the current song and clears the queue.")
    async def clear(self, ctx):
        if self.vc is not None and self.vc.is_playing():
            self.vc.stop()
        self.musicQueue = []
        await ctx.send("Music queue cleared!")

    @commands.command(name="leave", aliases=["l", "disconnect", "d"], description="Kick the bot from the voice channel.")
    async def leave(self, ctx):
        self.musicQueue = []
        await self.vc.disconnect()