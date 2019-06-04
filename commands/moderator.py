import discord
import asyncio

from discord.ext import commands


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['nick'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, user: discord.Member, *, nickname):
        if(len(nickname) > 32):
            await ctx.message.channel.send('Nickname too long')
            pass
        await user.edit(nick=nickname)
        await ctx.message.channel.send('Nickname changed to **{}**'.format(nickname))


    @commands.command(aliases = ['prune'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def sweep(self, ctx, number: int = 20):
        '''Prune a channel's messages'''
        channel = ctx.message.channel
        try:
            if (number > 100):
                await ctx.send('Too many! Your not even paying me.')
            elif (number < 2):
                await ctx.send('Too few! Do it yourself you lazy human!')
            else:
                await ctx.message.delete()
                await channel.purge(limit=number)
                message = await ctx.send('All done')
                await message.edit(content = 'All done, `{}` messages cleared. <:WilsonEvil:424575223883366431>'.format(number))
                await asyncio.sleep(2)
                await message.delete()
        except:
            await ctx.send('I cannot bulk delete messages older than 14 days.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def dupe(self, ctx, duplicate: int, *, message):
        '''Duplicate a message'''
        await ctx.message.delete()
        for i in range(duplicate):
            await ctx.send(message)
            await asyncio.sleep(1)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason = 'Not Specified'):
        '''Kick a user from a server'''
        author = ctx.message.author
        server = ctx.guild.name
        try:
            await user.send('You have been kicked from **{}**.\n**Reason:** {}'.format(server, reason))
            await user.kick(reason=reason)
            await author.send('**{}** has been kicked from **{}**.\n**Reason:** {}'.format(user, server, reason))
        except:
            await author.send('Could not kick member from the server.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason = 'Not Specified'):
        '''Ban a member from a server'''
        author = ctx.message.author
        try:
            await user.send('You have been banned from **{}**\n**Reason:** {}'.format(ctx.guild, reason))
            await ctx.guild.ban(user, reason=reason)
            await author.send('**{}** has been banned from **{}**\n**Reason:** {}'.format(user, ctx.guild, reason))
        except:
            await author.send('Could not ban member from the server.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        '''Unban a member from a server'''
        author = ctx.message.author
        try:
            await ctx.guild.unban(discord.Object(id=user_id))
            await author.send('<@{}> has been unbanned from **{}**\nBe sure to send them an invite.'.format(user_id, ctx.guild))
        except:
            await author.send('Could not unban member from the server.')


def setup(bot):
    bot.add_cog(Moderator(bot))
