import discord
import asyncio
import config
import os
import sys

from discord.ext import commands
from utils import owner, helpers, log


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(owner.is_owner)
    async def pstart(self, ctx, request = 'hard'):
        '''Reboot bot'''
        if(request.lower() == 'hard'):
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            await ctx.send('Initiating Hard pstart...')
            os.system(config.bot['pstart'])
            await self.bot.logout()
            await asyncio.sleep(1)
            sys.exit()
        else:
            await ctx.send('Initiating Soft pstart...')
            await self.bot.change_presence(activity = discord.Game(name = config.bot['game']))

    @commands.command()
    @commands.check(owner.is_owner)
    async def sleep(self, ctx):
        '''Close program and send bot to sleep'''
        await ctx.send('Going back to sleep...')
        await self.bot.logout()
        await asyncio.sleep(1)
        sys.exit()

    @commands.command()
    @commands.check(owner.is_owner)
    async def cmd(self, ctx, *, message):
        '''Write to the console'''
        embed = discord.Embed(title = None, description = 'Command sent: `{}`'.format(message), colour = 0x1f0000)
        await ctx.send(embed = embed)
        os.system(message)

    @commands.command()
    @commands.check(owner.is_owner)
    async def fromcmd(self, ctx, *, message):
        '''Write to the console and get the result back'''
        output = os.popen(message).read()
        str_collection = ['**Terminal Input**','```bash', '{}```'.format(message), '**Terminal Output**', '```bash', '{}```'.format(output)]
        str_build = helpers.StringManipulator(None, 2000)
        str_build.build_array(str_collection, "\n")
        await ctx.send(str_build)

    @commands.command()
    @commands.check(owner.is_owner)
    async def status(self, ctx, *, message: str):
        '''Change the bots presence'''
        await self.bot.change_presence(activity = discord.Game(name = message))
        await ctx.send('Status updated to `{}`'.format(message))

    @commands.command()
    @commands.check(owner.is_owner)
    async def logs(self, ctx):
        '''Get the log files'''
        direct_message = ctx.message.author
        await direct_message.send(file=discord.File('./data/logs/debug.log'))
        await direct_message.send(file=discord.File('./data/logs/error.log'))
        log.clearlogs()


def setup(bot):
    bot.add_cog(Admin(bot))