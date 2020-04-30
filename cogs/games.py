import json
import random

import aiohttp
from discord.ext import commands

from utils import default, http


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.group()
    async def game(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @game.command()
    @commands.guild_only()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def flip(self, ctx, ammount):
        """ Quitte ou double. Face, gagné, Pile, perdu. """
        try:
            if int(ammount) < 1:
                await ctx.send(f"```Mise minimum $1 connard.```")
                return
            playermoneyurl = 'http://dev.knl.im/konobot/api/index.php?call=getbalance&id='+str(ctx.message.author.id)
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(playermoneyurl)
                response = await raw_response.text()
                response = json.loads(response)
                username = await self.bot.get_user_info(ctx.message.author.id)
                playermoney=response[0]['balance']
            if int(playermoney) < int(ammount):
                await ctx.send(f"```T'es trop pauvre, batard.```")
                return
            flip = random.randint(0, 1)
            if (flip == 0):
                payement = int(ammount)*2
                await ctx.send(f'```Face, gagné ${str(payement)}! Solde : ${str(int(ammount)+int(playermoney))} ```')
                await http.addlog('money',ctx.message.author.name,str(ammount),'flip','win')
                url = 'https://dev.knl.im/konobot/api/index.php?call=payformsg&to='+str(ctx.message.author.id)+'&ammount='+str(ammount)
                async with aiohttp.ClientSession() as session:  # Async HTTP request
                    raw_response = await session.get(url)
            else:
                await ctx.send(f'```Pile, perdu ${ammount}. Solde : ${str(int(playermoney)-int(ammount))} ```')
                await http.addlog('money',ctx.message.author.name,'-'+str(ammount),'flip','lose')
                url = 'https://dev.knl.im/konobot/api/index.php?call=payformsg&to='+str(ctx.message.author.id)+'&ammount=-'+str(ammount)
                async with aiohttp.ClientSession() as session:  # Async HTTP request
                    raw_response = await session.get(url)
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @game.command()
    @commands.guild_only()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Machine à sous ! ($5)"""
        try:
            playermoneyurl = 'http://dev.knl.im/konobot/api/index.php?call=getbalance&id='+str(ctx.message.author.id)
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(playermoneyurl)
                response = await raw_response.text()
                response = json.loads(response)
                username = await self.bot.get_user_info(ctx.message.author.id)
                playermoney=response[0]['balance']
            if int(playermoney) < 5:
                await ctx.send(f"```T'es trop pauvre, batard.```")
                return
            to = ctx.message.author.id
            url = 'https://dev.knl.im/konobot/api/index.php?call=payformsg&to='+str(to)+'&ammount=-5'
            await http.addlog('money',ctx.message.author.name,'-'+str(5),'slot','win')
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(url)
            emojis = "🍎🍊🍐🍋🍉🍇🍓🍒🥝"
            a = random.choice(emojis)
            b = random.choice(emojis)
            c = random.choice(emojis)
            slotmachine = f"**[ {a} {b} {c} ]\n{ctx.message.author.name}**,"
            if (a == b == c):
                await ctx.send(f"{slotmachine} 3 à la suite, vous gagnez $50 ! 🎉")
                url = 'https://dev.knl.im/konobot/api/index.php?call=payformsg&to='+str(to)+'&ammount=50'
                await http.addlog('money',ctx.message.author.name,str(50),'slot','win')
                async with aiohttp.ClientSession() as session:  # Async HTTP request
                    raw_response = await session.get(url)
            elif (a == b) or (a == c) or (b == c):
                await ctx.send(f"{slotmachine} 2 à la suite, vous gagnez $10 ! 🎉")
                url = 'https://dev.knl.im/konobot/api/index.php?call=payformsg&to='+str(to)+'&ammount=10'
                await http.addlog('money',ctx.message.author.name,str(10),'slot','win')
                async with aiohttp.ClientSession() as session:  # Async HTTP request
                    raw_response = await session.get(url)
            else:
                await ctx.send(f"{slotmachine} tu as perdu $5 😢")

        except Exception as e:
            return await ctx.send(f"```\n{e}```")


def setup(bot):
    bot.add_cog(Games(bot))
