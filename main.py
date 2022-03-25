from typing import *
import os, dotenv
import threading, asyncio

import disnake
from disnake.ext import commands

if os.name != "nt":
    import uvloop
    uvloop.install()

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

from music import *
INF = int(1e18)

@bot.event
async def on_ready():
    print('On ready')

class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.player = Player()

    @commands.command(name='join')
    async def join(self, ctx: commands.Context):
        await self.player.join(ctx.author.voice.channel)
        await ctx.send('Join successfully')

    @commands.command(name='leave')
    async def leave(self, ctx: commands.Context):
        await self.player.leave()
        await ctx.send('Leave successfully')

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx: commands.Context, url):
        await self.join(ctx)
        self.player.search(url)
        await ctx.send('Search successfully')
        self.player.voice_client = ctx.guild.voice_client
        self.bot.loop.create_task(self._mainloop(ctx))

    async def _mainloop(self, ctx: commands.Context):
        if (self.player.in_mainloop):
            return
        self.player.in_mainloop = True
        await ctx.send('It is playing music now')
        while (len(self.player.playlist)):
            await ctx.send(f'Now is playing {self.player.playlist[0].title}')
            self.player.play()
            await self.player.wait()
            self.player.playlist.rule()
        self.player.in_mainloop = False
        await ctx.send('The playlist is empty now')

    @commands.command(name='pause')
    async def pause(self, ctx: commands.Context):
        self.player.pause()
        await ctx.send('Pause successfully')

    @commands.command(name='resume')
    async def resume(self, ctx: commands.Context):
        self.player.resume()
        await ctx.send('Resume successfully')

    @commands.command(name='skip')
    async def skip(self, ctx: commands.Context):
        self.player.skip()
        await ctx.send('Skip successfully')

    @commands.command(name='stop')
    async def stop(self, ctx: commands.Context):
        self.player.stop()
        await ctx.send('Stop successfully')

    @commands.command(name='seek')
    async def seek(self, ctx: commands.Context, timestamp: Union[float, str]):
        if not isinstance(timestamp, float):
            return await ctx.send('Fail to seek. Maybe you request an invalid timestamp')
        self.player.seek(timestamp)
        await ctx.send('Seek successfully')

    @commands.command(name='restart', aliases=['replay'])
    async def restart(self, ctx: commands.Context):
        self.player.seek(0)
        await ctx.send('Restart sucessfully')

    @commands.command(name='loop', aliases=['songloop'])
    async def single_loop(self, ctx: commands.Context, times: Union[int, str]=INF):
        print(times)
        print(type(times))
        if not isinstance(times, int):
            return await ctx.send('Fail to loop. Maybe you request an invalid times')
        self.player.playlist.single_loop(times)
        await ctx.send('Enable single song loop sucessfully')

    @commands.command(name='wholeloop', aliases=['queueloop', 'qloop'])
    async def whole_loop(self, ctx: commands.Context):
        self.player.playlist.whole_loop()
        await ctx.send('Enable whole queue loop successfully')

    @commands.command(name='show', aliases=['queuelist', 'queue'])
    async def show(self, ctx: commands.Context):
        pass

    @commands.command(name='remove', aliases=['queuedel'])
    async def remove(self, ctx: commands.Context, idx: Union[int, str]):
        try:
            self.player.playlist.pop(idx)
            await ctx.send('Remove successfully')
        except (IndexError, TypeError):
            await ctx.send('Fail to remove. Maybe you request an invalid index')
    
    @commands.command(name='swap')
    async def swap(self, ctx: commands.Context, idx1: Union[int, str], idx2: Union[int, str]):
        try:
            self.player.playlist.swap(idx1, idx2)
            await ctx.send('Swap successfully')
        except (IndexError, TypeError):
            await ctx.send('Fail to swap. Maybe you request an invalid index')

    @commands.command(name='move_to', aliases=['insert_to'])
    async def move_to(self, ctx: commands.Context, origin: Union[int, str], new: Union[int, str]):
        try:
            self.player.playlist.move_to(origin, new)
            await ctx.send('Move successfully')
        except (IndexError, TypeError):
            await ctx.send('Fail to move. Maybe you request an invalid index')

bot.add_cog(MusicBot(bot))

bot.run(TOKEN)