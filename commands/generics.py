import discord
import config
import time

from utils import helpers, owner
from discord.ext import commands


class Generics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        '''Basically the bot's "Hello, World!"'''
        await ctx.send('Greetings mortal...')

    @commands.command()
    async def ping(self, ctx):
        '''Ping the bot for response time'''
        before = time.perf_counter()
        # received = (time.perf_counter() - before)
        embed = discord.Embed(title = 'Pong!', description='', colour=0x1f0000)
        message = await ctx.send(embed = embed)
        sent = (time.perf_counter() - before)
        await message.edit(embed=discord.Embed(title = 'Pong!', description='Time taken: `{}` seconds'.format(sent), colour=0x1f0000))

    @commands.command()
    async def embed(self, ctx, *, message):
        '''Embed a message'''
        delete_target = ctx.message
        await delete_target.delete()
        embed = discord.Embed(title='Notice from: {}'.format(ctx.message.author), description=message, colour=0x1f0000)
        await ctx.send(embed=embed)

    @commands.command()
    async def image(self, ctx, message: str):
        '''Embed an image'''
        delete_target = ctx.message
        await delete_target.delete()
        embed=discord.Embed(title='Requested by: {}'.format(ctx.message.author), description='', colour=0x1f0000)
        embed.set_image(url=message)
        await ctx.send(embed=embed)

    @commands.command()
    async def update(self, ctx):
        '''View the update file'''
        data = helpers.open_file(config.bot['update_details'])
        embed = discord.Embed(title=None, description=data, colour=0x1f0000)
        await ctx.send(embed=embed)

    @commands.command()
    async def release(self, ctx):
        '''Release info'''
        online_time = config.bot['online_time']
        last_pstart = config.bot['pstart_time']
        current_time = time.time()
        data = helpers.open_file(config.bot['release_details'])
        embed = discord.Embed(title=None, description=data.format(helpers.date(current_time),
                                                                  last_pstart,
                                                                  config.bot['update_name'],
                                                                  helpers.convert_time(current_time - online_time),
                                                                  config.bot['version']), colour=0x1f0000)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(owner.is_owner)
    async def invite(self, ctx):
        '''Get the invite link'''
        dm = ctx.message.author
        member = ctx.message.author.id
        invite = config.bot['invite_url']
        await dm.send(invite)
        await ctx.send('Check your direct messages <@{}>. I have sent you an invite link.'.format(member))

    @commands.command()
    async def github(self, ctx):
        '''Link to github'''
        await ctx.send(config.bot['github'])

    @commands.command()
    async def help(self, ctx, helpfile='all'):
        '''Help with commands'''
        try:
            data = helpers.open_file('./data/help/{}.txt'.format(helpfile.casefold()))
            embed = discord.Embed(title=None, description=data, colour=0x1f0000)
            await ctx.send(embed=embed)
        except:
            await ctx.send('An error has occured. The help file either doesn\'t nor will exist or hasn\'t been implemented yet.')


def setup(bot):
    bot.add_cog(Generics(bot))