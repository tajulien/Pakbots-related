import os
import traceback
from datetime import datetime

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import errors

from utils import default


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    @staticmethod
    def _get_level_xp(n):
        return 5*(n**2)+50*n+100

    @staticmethod
    def _get_level_from_xp(xp):
        remaining_xp = int(xp)
        level = 0
        while remaining_xp >= Events._get_level_xp(level):
            remaining_xp -= Events._get_level_xp(level)
            level += 1
        return level

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot or not message.guild:
    #         return
    #     #exp
    #     playerxpurl = 'http://dev.knl.im/konobot/api/index.php?call=getExp&id='+str(message.author.id)
    #     async with aiohttp.ClientSession() as session:  # Async HTTP request
    #         raw_response = await session.get(playerxpurl)
    #         response = await raw_response.text()
    #         response = json.loads(response)
    #         try:
    #             playerxp=response[0]['exp']
    #         except Exception as e:
    #             playerxp = 0
    #
    #     if playerxp is None:
    #         playerxp = 0
    #     else:
    #         playerxp = int(playerxp)
    #
    #     lvl = self._get_level_from_xp(playerxp)
    #     print(lvl)
    #     rndexp = random.randint(15, 25)
    #     url = 'http://dev.knl.im/konobot/api/index.php?call=modExp&id='+str(message.author.id)+'&ammount='+str(rndexp)
    #     print('Given $'+str(rndexp)+' exp to '+str(message.author))
    #     async with aiohttp.ClientSession() as session:  # Async HTTP request
    #         raw_response = await session.get(url)
    #
    #     newxp = int(playerxp) + int(rndexp)
    #     newlvl = self._get_level_from_xp(newxp)
    #     if newlvl != lvl:
    #         destchannel = self.bot.get_channel(549533466350452756)
    #         await destchannel.send('gg '+str(message.author)+' ! Tu passes level '+str(newlvl))
    #
    #     #money
    #     randomgen = random.randint(1,6)
    #     if (randomgen == 1):
    #         randommoney = random.randint(1,3)
    #         print('Randomly paid $'+str(randommoney)+' to '+str(message.author))
    #         url = 'https://dev.knl.im/konobot/api/index.php?call=payformsg&to='+str(message.author.id)+'&ammount='+str(randommoney)+'&username='+str(message.author.name)
    #         await http.addlog('money',message.author.name,str(randommoney),'randompay','Paid for message')
    #
    #         async with aiohttp.ClientSession() as session:  # Async HTTP request
    #             raw_response = await session.get(url)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #print(payload.emoji)
        emoji_partial = payload.emoji
        message_id = payload.message_id
        channel_id = payload.channel_id
        user_id = payload.user_id

        channel = self.bot.get_channel(channel_id)
        message = await channel.get_message(message_id)
        #await channel.send(f"FUUUUUUUUUUUUUUCK")
        #emoji = reaction.emoji
        #print(dir(message))
        if str(emoji_partial) == '📌':
            destchannel = self.bot.get_channel(545961549106249744)
            await destchannel.send(str(message.author)+': '+str(message.content))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = ('```py\n{2}{0}: {3}\n```').format(type(err).__name__, ctx.message.content, _traceback, err)

            await ctx.send(f"There was an error processing the command ;-;\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.2f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not self.config.join_message:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config.join_message)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            print(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Game(type=0, name=self.config.playing), status=discord.Status.online)


def setup(bot):
    bot.add_cog(Events(bot))
