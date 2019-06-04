import discord
import asyncio
import os
import youtube_dl
import time

from discord.ext import commands
from queue import Queue
from utils import owner


song_queue = Queue(30)

# Suppress noise about console usage from errors
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
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['connect', 'join'])
    @commands.check(owner.is_owner)
    async def summon(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect(timeout=300, reconnect=True)

    @commands.command()
    @commands.check(owner.is_owner)
    async def play(self, ctx):
        if song_queue.empty():
            await ctx.send('The queue is empty')
        for i in range(song_queue.qsize()):
            song = song_queue.get()
            player = await YTDLSource.from_url(song, loop=self.bot.loop, stream=False)
            ctx.voice_client.play(player, after=lambda e: print('Player error: '.format(e)) if e else None)
            embed = discord.Embed(title='Now playing: {}'.format(player.title), description='**Duration**\n{}'.format(time.strftime('%M:%S', time.gmtime(player.data['duration']))), colour=0x1f0000)
            embed.set_image(url=player.data['thumbnail'])
            await ctx.send(embed=embed)
            await asyncio.sleep(player.data['duration'])
            if ctx.voice_client.is_playing():
                # Breathing room
                await asyncio.sleep(3)
            for file in os.listdir('./'):
                if file.endswith('.webm'):
                    os.remove(file)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not in a voice channel')
        elif ctx.voice_client.is_playing():
            await ctx.voice_client.stop()

    @commands.command()
    @commands.check(owner.is_owner)
    async def stop(self, ctx):
        if ctx.voice_client is not None:
            ctx.voice_client.stop()
        # if ctx.voice_client.is_playing():
        for file in os.listdir('./'):
            if file.endswith('.webm'):
                os.remove(file)

    @commands.command()
    @commands.check(owner.is_owner)
    async def disconnect(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command(aliases=['q'])
    @commands.check(owner.is_owner)
    async def queue(self, ctx, *, url):
        song_queue.put(url)
        await ctx.send('Song queued')


def setup(bot):
    bot.add_cog(Music(bot))