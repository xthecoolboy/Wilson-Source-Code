# Wilson Source Code
This is a repository where I commit a cut down version of my discord bot. Feel free to clone this and use it to write your own! I have removed a lot of the features so you'll need to fill in the gaps yourself. I'd also recommend writing your own commands/ structure, though feel free to use this repo as a reference. Be sure to credit me [@RogueSensei](https://github.com/RogueSensei/) :smile:
## Wilson
Wilson is a Discord Bot using the [discord.py](https://discordpy.readthedocs.io/en/latest/) API. His commands include general chat fun, moderation commands, sniffing out and shunning pings to himself or `@everyone` and generally being an ass.
### Inviting Wilson
Wilson can be invited to a server by typing `|invite` in a server he is in. He will then send a direct message to you with his invite link. A website is due to be constructed to invite him from there.
### Using Wilson
Wilson responds to specific commands with `|` as a prefix. For a list of all his commands, type `|help`. For details on a specific command, type `|help` followed by the name of a command listed when calling help.
Example: `|help hello`
## A Tip of the Hat
- [@AlexFlipnote](https://github.com/AlexFlipnote) - Structure based off of his [discord_bot.py](https://github.com/AlexFlipnote/discord_bot.py) repo, and [nekos.py](https://github.com/Nekos-life/nekos.py) is used. Be sure to check out his work :smile:
- [Imgur/imgurpython](https://github.com/Imgur/imgurpython) is also used
## Authoring your own bot
### Requirements
- `discord.py[voice]`
- `asyncio`
- `pyyaml`
- `bs4`
- `beautifulsoup4`
- `requests`
- `youtube_dl`
- `rule34`

### Installing
If you haven't used github before, you can clone the repository by clicking the `Clone or download` button, or by using the git desktop command `$ git clone https://github.com/RogueSensei/Wilson-Source-Code.git`

Afterwards, `cd` to the project directory e.g. `$ cd C:\Documents\Wilson-Source-Code` and install the dependencies by running `pip install -r requirements.txt`

Finally, you will need to install ffmpeg. On Windows, just download the `zip` folder, then locate to the `bin` folder within it, and put the `ffmpeg.exe` file in the root of the bot folder. On linux, just install it with your package manager, for example on debian-based systems:
```bash
sudo apt-get install ffmpeg
```
### Setting up
Open the file `config.py` in an IDE or text editor of your choice. The code should look like this:
```py
bot = {'owner': '',
       'client_id': '',
       'version': '',
       'prefix': '|',
       'pstart': 'python3 ./main.py',
       'game': '',
       'token': '',
       'invite_url': '',
       'update_name': '',
       'release_details': './data/misc/releaseplaceholder.txt',
       'checkin_details': './data/misc/checkin.txt',
       'checkin_channel': '',
       'update_details': './data/misc/update.txt',
       'startup_time': '',
       'pstart_time': '',
       'imgur_client_id': '',
       'imgur_client_secret': ''}
```
This is your configuration file for you bot. The items you should edit are as follows:
- `owner` - This is your Discord UserId
- `client_id` - This is your bots Discord UserId
- `version` - Version number
- `prefix` - Your bots prefix
- `pstart` - This is used for reboots. Change to `python ./main.py` if you are on Windows
- `game` - The "game" your bot is playing
- `token` - You bots token (Keep this a secret)
- `invite_url` - Url to invite your bot to a server
- `update_name` - Name of your most recent update
- `checkin_channel` - Channel your bot will message when booting up
- `imgur_client_id` and `imgur_client_secret` are API keys for `imgur`

Leave this items as they are (recommended for beginners):
- `release_details`
- `checkin_details`
- `update_details`

Don't touch these at all:
- `startup_time`
- `pstart_time`

### Running
Providing everything is set up correctly, run `main.py` and your bot should come online. Be sure to say `hello` :smile:
### Writing Help Files
You may have noticed in `/data/help` there are some text files named `all.txt` and `hello.txt`. This is the main help file and the help file for the `hello` command respectively. If you do not want to write your own help files, you can use the default `discord.py` help command which uses the comments at the top of each command method. To use the default help command, go to `main.py` and look for the line that reads `bot.remove_command('help')` on line 12 and comment it out. Then go to `generics.py` line 81. You should see the help command which should look something like this:
```py
@commands.command()
async def help(self, ctx, helpfile='all'):
    '''Help with commands'''
    try:
        data = helpers.open_file('./data/help/{}.txt'.format(helpfile.casefold()))
        embed = discord.Embed(title=None, description=data, colour=0x1f0000)
        await ctx.send(embed=embed)
    except:
        await ctx.send('An error has occured. The help file either doesn\'t nor will exist or hasn\'t been implemented yet.')
```
Comment this code out. *You can delete these lines if you wish, but I recommend leaving them in should you decide to write you own help files*
### Imgur API
If you want to make use of the Imgur API, you can register your bot [here](https://api.imgur.com/#registerapp). If you do not wish to use it, you can remove the `imgur_client_id` and `imgur_client_secret` entries in `config.py`. Then, inside `images.py`, comment out/remove:
- line 4: `import config`
- line 9: `from utils.imgurpython import ImgurClient`
- line 16: The `imgur` method:

```py
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
```
You can also remove the `imgurpython` folder in `utils`
### All Set!
Now go fire up a raspberry pi and run your own discord bot!
# Wilson Update History
## Ver. 0.5 The Pi Home Update

Wilson now runs permanently on **RogueSensei's** Raspberry Pi, his new home! With that too, **Wilson** has some nifty new changes.

### New Features
- `release`: Like release details? Yes you do! You can now check Wilson's stats!
- `update`: This very command which you see before you; exciting!
- `flip`: Flip a coin! `V0.5.1`
- `f`: Everyone pay your respects. `V0.5.1`
- `react r m`: New and improved reactions! Type |help react `V0.5.2`
- `invite`: It's about time! `V0.5.2`
- `image`: Embed an image. `V0.5.3`
- `dice i`: Dice roll command `V0.5.4`

### Updated Features
- `sweep`: Due to upcoming Moderation features, sweep is now private.
- `sleep`: Kill is now Sleep again. Hey, I'm the pest bot, may as well play the part.
- `help`: Minor updates to existing help files to match changes.
- `react r`: 5 new reactions! `V0.5.1`
- `help`: Major update to help files to public commands `V0.5.4`

### Removed Features
- Independant reaction commands minus `fight m`. `|dance` is now `|react dance`.

### Fixes
- Wilson now runs slightly smoother and reboots on his own. `V0.5.3`
- The release timer has been rewritten and should be more accurate. `V0.5.5`

## The Core Update

Yay! Version 1.0! Completely re-written, new features, better than ever!

### Behind the Scenes
From a technical perspective, **Wilson's** code base has been completely re-written to be more efficient to improve performance and maintainability. Many of the commands you know and love are back and appear unchanged, however some unused features have also been removed.

### New Features
- `avatar`: See those sweet, sweet avatars close up!
- Moderator commands, at last! *Require user permissions*
- `kick`
- `ban`
*See the help of the moderator commands for more information on permissions of their use*

### Updated Features
- `sweep` is back and better than ever!
- `dupe` is now available for moderators. Use with care before I nerf it...

### Removed Features
- `quickmaffs`: Dead meme
- `evil`: Not really used...
- `invite` has been temporarily moved for stress testing **Wilson**

## Whats Next?
Development on **Wilson** has sped up so you can expect new features soon. **Wilson** will get the `discord.py rewrite` treatment, voice features are impending, some more fun commands are coming soon too!

**Enjoy life, while it lasts... And remember, Don't Starve!**
