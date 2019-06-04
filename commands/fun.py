import discord
import asyncio
import yaml
import random

from discord.ext import commands


# YAML containing reactions
bot_reactions = yaml.load(open('./data/yaml/reactions.yml'))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def puppet(self, ctx, *, message: str):
        '''Get the bot to speak a message'''
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def message(self, ctx, recipent : discord.Member, *, message):
        '''Direct Message a user'''
        await ctx.message.delete()
        await recipent.send('**Message from {}**\n{}'.format(ctx.message.author, message))

    @commands.command()
    async def send(self, ctx, channel: discord.TextChannel, *, message):
        '''Direct Message a channel'''
        await ctx.message.delete()
        await channel.send('**Message from {}**\n{}'.format(ctx.message.author, message))

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        '''Get a discord user's avatar'''
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(title='Avatar to **{}**'.format(user.name), colour=0x1f0000)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def emoji(self, ctx, emoji :discord.Emoji):
        embed = discord.Embed(colour=0x1f0000)
        embed.set_image(url=emoji.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def lenny(self, ctx):
        '''Get a lenny face ( ͡° ͜ʖ ͡°)'''
        await ctx.message.delete()
        await ctx.send('( ͡° ͜ʖ ͡°)')

    @commands.command()
    async def f(self, ctx):
        '''Pay respects'''
        user = ctx.message.author.id
        await ctx.send('<@{}> paid their respects.'.format(user))

    @commands.command()
    async def flip(self, ctx):
        '''Flip a coin'''
        coin = ['**Heads!**', '**Tails!**']
        await ctx.send(random.choice(coin))

    @commands.command()
    async def dice(self, ctx, message: int = 6):
        '''Roll a dice'''
        dice_faces = message
        if (dice_faces > 0):
            await ctx.send('Rolling D{}'.format(dice_faces))
            # await self.bot.send_typing()
            dice_roll = random.randint(1, dice_faces)
            await asyncio.sleep(0.3)
            await ctx.send('**{}!**'.format(dice_roll))
        else:
            await ctx.send('Invalid dice roll')

    @commands.command()
    async def react(self, ctx, reaction = 'none', *, message = 'none'):
        '''Reaction GIFs'''
        reaction_message = message
        if (message == 'none'):
            reaction_message = bot_reactions['{}'.format(reaction.lower())]['subject']
        if (reaction != 'none'):
            try:
                delete_target = ctx.message
                user = ctx.message.author.id
                embed = discord.Embed(title=None,
                                      description=(bot_reactions[reaction.lower()]['message'].format(user, reaction_message)),
                                      colour=0x1f0000)
                embed.set_image(url=bot_reactions[reaction.lower()]['img'])
                await delete_target.delete()
                await ctx.send(embed=embed)
            except:
                await ctx.send('This reaction does not exist.')


def setup(bot):
    bot.add_cog(Fun(bot))