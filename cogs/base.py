import discord
import asyncio
import json
import bs4
import aiohttp
import urllib.request
import time
import psutil
import os

from cogs import looped
from cogs import infobourse
from cogs import marketindics

from utils import lists, permissions, http, default, repo
from discord.ext import commands
from datetime import datetime


class Discord_Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    def sendtime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.LAST_UPDATE_TIME = current_time
        # print(self.LAST_UPDATE_TIME)
        print("Current Time is", current_time)
        return self.LAST_UPDATE_TIME

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        await ctx.send(r[endpoint])

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Random cat """
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def price(self, ctx):
        """ price serv """
        # await ctx.send("Loading items price - Last Update : " + Discord_Info.LAST_UPDATE_TIME)
        for elements in range(len(looped.Looped.LIST)):
            embed = discord.Embed(title=looped.Looped.LIST[elements][0])
            embed.set_thumbnail(url=looped.Looped.LIST[elements][3])
            embed.add_field(name="Current Buyout Price : ", value=looped.Looped.LIST[elements][1], inline=True)
            embed.add_field(name="Wanted Price Fixed : ", value=looped.Looped.LIST[elements][2], inline=True)
            embed.set_footer(text='Pakbot 2020',
                             icon_url='https://img2.freepng.fr/20180531/xxv/kisspng-youtube-t-shirt-film-decal-wingman-top-gun-5b0fc1ba253133.9475205715277592901524.jpg')
            await ctx.send(embed=embed)
            await ctx.message.author.send(embed=embed)
            await asyncio.sleep(1)

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def indics(self, ctx, act_name):
        """ indicators """
        details = marketindics.Indics.check_details(self, act_name)
        if details == "Action non trouvée":
            await ctx.send("Action non trouvée")
        elif details == "Pas d'action aujourd'hui":
            await ctx.send("Action non cotée aujourd'hui")
        else:
            embed = discord.Embed(title=details[1])
            embed.set_thumbnail(url=details[13])
            # embed.set_image(url=details[12])
            embed.add_field(name="mma10 : ", value=details[4], inline=True)
            embed.add_field(name="mma20 : ", value=details[5], inline=True)
            embed.add_field(name="mma50 : ", value=details[6], inline=True)
            embed.add_field(name="mma100 : ", value=details[7], inline=True)
            embed.add_field(name="mma200 : ", value=details[8], inline=True)
            embed.add_field(name="macd : ", value=details[9], inline=True)
            embed.add_field(name="Bollinger inf : ", value=details[10], inline=True)
            embed.add_field(name="Bollinger sup : ", value=details[11], inline=True)
            embed.add_field(name="Signal : ", value=details[12], inline=True)
            embed.set_footer(text='Pakbot 2020',
                             icon_url='https://img2.freepng.fr/20180531/xxv/kisspng-youtube-t-shirt-film-decal-wingman-top-gun-5b0fc1ba253133.9475205715277592901524.jpg')
            await ctx.send(embed=embed)
            # await ctx.message.author.send(embed=embed)
            await asyncio.sleep(1)

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def last(self, ctx):
        """ last news """
        await ctx.send(
            f'News {infobourse.News.LISTGIVE[-1][0]} - {infobourse.News.LISTGIVE[-1][1]} - News : {infobourse.News.LISTGIVE[-1][2]} <{infobourse.News.LISTGIVE[0][3]}>')

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong   |   {int(ping)}ms")

    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx, city):
        """ Weather for somewhere. """
        try:
            weather_icon = ':cloud:';
            url = 'https://www.prevision-meteo.ch/services/json/' + city
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(url)
                response = await raw_response.text()
                response = json.loads(response)

                embed = discord.Embed()
                embed.set_thumbnail(url=response['current_condition']['icon_big'])
                embed.add_field(name="Ville:", value=response['city_info']['name'], inline=True)
                embed.add_field(name="Pays:", value=response['city_info']['country'], inline=True)
                embed.add_field(name="Conditions actuelles:", value=response['current_condition']['condition'],
                                inline=True)
                embed.add_field(name="Pression atmosphérique:", value=response['current_condition']['pressure'],
                                inline=True)
                embed.add_field(name="Humidité:", value=response['current_condition']['humidity'], inline=True)
                embed.add_field(name="Vitesse du vent:", value=response['current_condition']['wnd_spd'], inline=True)
                embed.add_field(name="Température actuelle:", value=response['current_condition']['tmp'], inline=True)
                embed.add_field(name="Température Minimale:", value=response['fcst_day_0']['tmin'], inline=True)
                embed.add_field(name="Température maximale:", value=response['fcst_day_0']['tmax'], inline=True)

                await ctx.send(content=f"ℹ Météo à **{response['city_info']['name']}**", embed=embed)
                # await ctx.send('Meteo à ' + response['city_info']['name'] + '\n Conditions Actuelles: '+weather_icon+' '+response['current_condition']['condition']+'\n Minimales/Maximales: '+str(response['fcst_day_0']['tmin'])+' / '+str(response['fcst_day_0']['tmax']))


        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @commands.command()
    @commands.guild_only()
    async def weekend(self, ctx):
        """ C'est bientôt le weekd ou pas ? """
        try:
            weekend_url = 'http://estcequecestbientotleweekend.fr/'
            with urllib.request.urlopen(weekend_url) as f:
                data = f.read().decode('utf-8')
                soup = bs4.BeautifulSoup(data, 'html.parser')
                result = soup.find(class_='msg').get_text(' ', strip=True)
                await ctx.send('```' + result + '```')

        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @commands.command()
    async def status(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024 ** 2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embed = discord.Embed(colour=ctx.me.top_role.colour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Last boot", value=default.timeago(datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"Developer{'' if len(self.config.owners) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in self.config.owners]),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=True)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)
        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{repo.version}**", embed=embed)

    @commands.group()
    @commands.guild_only()
    async def server(self, ctx):
        if ctx.invoked_subcommand is None:
            findbots = sum(1 for member in ctx.guild.members if member.bot)

            embed = discord.Embed()
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=findbots, inline=True)
            embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            embed.add_field(name="Created", value=default.date(ctx.guild.created_at), inline=True)
            await ctx.send(content=f"ℹ information about **{ctx.guild.name}**", embed=embed)


def setup(bot):
    bot.add_cog(Discord_Info(bot))
