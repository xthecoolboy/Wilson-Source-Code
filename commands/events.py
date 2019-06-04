import discord
import traceback
import config
import time

from utils import helpers, log
from discord.ext import commands
from discord.ext.commands import errors


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        '''on_ready() runs on boot'''
        config.bot['online_time'] = time.time()
        config.bot['pstart_time'] = helpers.date(time.time())
        print('--------------------')
        print('Discord API Version: V{}'.format(discord.__version__))
        print('--------------------')
        print('Present time: {}'.format(helpers.date(config.bot['online_time'])))
        print('Logged in as:')
        print('Bot: {}, Codenamed: {}'.format(self.bot.user.id, self.bot.user.name))
        print('--------------------')
        log.debug('{} Online'.format(self.bot.user.name))
        await self.bot.change_presence(activity=discord.Game(name=config.bot['game']))
        data = helpers.open_file(config.bot['checkin_details'])
        channel = self.bot.get_channel(int(config.bot['checkin_channel']))
        embed = discord.Embed(title=None, description=data.format(self.bot.user.name, self.bot.user.name,
                                                                  helpers.date(config.bot['online_time']),
                                                                  config.bot['version']), colour=0x1f0000)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        '''on_message() reads incoming messages, checks for mentions, then reacts or passes whether or not it finds mentions respectively'''
        if (message.author.bot):
            return
        user_id = message.author.id
        direct_message = message.author
        if ('<@{}>'.format(config.bot['client_id']) in message.content):
            if (str(user_id) in config.bot['owner']):
                await direct_message.send('Good day Master. <:WilsonHonour:424918644250902529>')
            else:
                await direct_message.send('Greetings, mortal. Now whatever it is you want, I do not have time for a chat. I am busy enough as it is responding to commands and whatnot. If you need me for *anything* it must be commands only, because I am not wasting my time talking to you. Good day. <:WilsonHonour:424918644250902529>')
        elif('@everyone' in message.content or '@here' in message.content):
            await direct_message.send('Tagging everyone is just begging for attention')
        else:
            # Unless you're Google, don't log other user's messages
            pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        '''Logging'''
        try:
            log.debug('{} > {} > {}'.format(ctx.guild.name, ctx.message.author, ctx.message.clean_content))
        except AttributeError:
            log.debug('Direct Message > {} > {}'.format(ctx.message.author, ctx.message.clean_content))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Logging and Handling Errors'''
        if isinstance(error, errors.CommandNotFound):
            log.debug('{} > {} > {} - CommandNotFound'.format(ctx.guild.name, ctx.message.author, ctx.message.clean_content))
            await ctx.send('Command not found')
        elif isinstance(error, errors.MissingRequiredArgument) or isinstance(error, errors.BadArgument):
            log.debug('MissingRequiredArgument or BadArgument')
            await ctx.send('Error, invalid or missing argument(s)')
        elif isinstance(error, errors.CommandInvokeError):
            bot_error_response = helpers.StringManipulator()
            owner = self.bot.get_user(int(config.bot['owner']))
            error = error.original

            _traceback = traceback.format_tb(error.__traceback__)
            _traceback = ''.join(_traceback)
            full_error = '{}{}: Message: {}\nTraceback:\n{}'.format(error, type(error).__name__, ctx.message.content, _traceback)

            log.error(full_error)
            await owner.send(bot_error_response.build_array(['```py', full_error, '```'], '\n'))
            await ctx.send('An error occured while invoking the command')
        elif isinstance(error, errors.MissingPermissions) or isinstance(error, errors.NotOwner):
            log.debug('MissingPermissions or NotOwner')
            await ctx.send('You do not have permission to do that.')
        elif isinstance(error, errors.CommandOnCooldown):
            log.debug('CommandOnCooldown')
            await ctx.send('This command is on cooldown...')
        else:
            log.error(str(error))


def setup(bot):
    bot.add_cog(Events(bot))
