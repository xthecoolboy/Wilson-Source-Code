import asyncio
import config
import os
import time

from utils import log
from discord.ext import commands


log.debug('Logging in...')
bot = commands.Bot(command_prefix=config.bot['prefix'])
bot.remove_command('help')

loop = asyncio.get_event_loop()

def main():
    try:
        loop.run_until_complete(bot.run(config.bot['token']))
    except Exception as e:
        if not (loop.is_closed()):
            log.error(str(e))
            log.debug('Attempting to reboot in 30 seconds')
            loop.close()
            time.sleep(30)
        if(loop.is_closed()):
            return
        os.system(config.bot['pstart'])


for file in os.listdir('commands'):
    if file.endswith('.py'):
        name = file[:-3]
        bot.load_extension('commands.{}'.format(name))


if __name__ == '__main__':
    main()
