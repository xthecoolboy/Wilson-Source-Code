import discord
import asyncio
import random
import config
import rule34

from discord.ext import commands
from utils import helpers, nekos
from utils.imgurpython import ImgurClient


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def imgur(self, ctx, *, search):
        '''Imgur'''
        client_id = config.bot['imgur_client_id']
        client_secret = config.bot['imgur_client_secret']
        client = ImgurClient(client_id, client_secret)
        search_result = client.gallery_search(search)
        if (len(search_result) == 0):
                await ctx.send('No results found')
                return
        galleries = list(map(lambda x : x.id, filter(lambda y : y.is_album, search_result)))
        album = client.get_album_images(galleries[random.randint(0, len(galleries) - 1)])
        images = list(map(lambda x : x.link, album))
        image = images[random.randint(0, len(images) - 1)]
        embed = discord.Embed(title='Imgur: {}'.format(search), description='',
                              colour=0x1f0000)
        embed.set_image(url=image)
        embed.set_footer(text='Requested by: {}'.format(ctx.message.author))
        await ctx.send(embed=embed)

    @commands.command(aliases = ['r34'])
    async def rule34(self, ctx, *, search):
        '''Rule 34 NSFW'''
        if(ctx.message.channel.is_nsfw()):
            search_tag = helpers.StringManipulator()
            search_tag.build_array(search.lower().split(' '), '_')
            loop = asyncio.get_event_loop()
            r34 = rule34.Rule34(loop=loop)
            images = await r34.getImageURLS(search_tag)
            if(images == None):
                await ctx.send('No results found')
            else:
                image = images[random.randint(0, len(images) - 1)]
                embed = discord.Embed(title='Rule 34: {}'.format(search), description='',
                                  colour=0x1f0000)
                embed.set_image(url=image)
                embed.set_footer(text='Requested by: {}'.format(ctx.message.author))
                await ctx.send(embed=embed)
        else:
            await ctx.send('You need to be in a NSFW channel to do that.')

    @commands.command()
    async def nekos(self, ctx, search):
        if (ctx.message.channel.is_nsfw()):
            image = nekos.img(search)
            if (len(image) == 0):
                await ctx.send('No results found')
            else:
                embed = discord.Embed(title='Nekos: {}'.format(search), description='',
                                      colour=0x1f0000)
                embed.set_image(url=image)
                embed.set_footer(text='Requested by: {}'.format(ctx.message.author))
                await ctx.send(embed=embed)
        else:
            await ctx.send('You need to be in a NSFW channel to do that.')


def setup(bot):
    bot.add_cog(Image(bot))