import json
import aiohttp

from discord.ext import commands
from utils import default, http


class Discord_Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.group()
    async def money(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @money.command(name="balance")
    async def balance(self, ctx):
        try:
            playermoneyurl = 'http://dev.knl.im/konobot/api/index.php?call=getbalance&id='+str(ctx.message.author.id)
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(playermoneyurl)
                response = await raw_response.text()
                response = json.loads(response)
                username = await self.bot.get_user_info(ctx.message.author.id)
                playermoney=response[0]['balance']
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"```Money for {username}: ${playermoney}```")

    @money.command(name="top")
    async def top(self, ctx):
        try:
            url = 'https://dev.knl.im/konobot/api/index.php?call=baltop'
            async with aiohttp.ClientSession() as session: # Async HTTP request
                raw_response = await session.get(url)
                response = await raw_response.text()
                #print(response)
                response = json.loads(response)
                baltop_formatted=''
                count=1
                for f in response:
                    account = f['account']
                    account = account.strip('<')
                    account = account.strip('>')
                    account = account.strip('@')
                    account = account.strip('!')
                    user = await self.bot.get_user_info(account)
                    baltop_formatted=baltop_formatted+'#'+str(count)+'. '+str(user)+': $'+f['balance']+'\n'
                    count=count+1
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"```{baltop_formatted}```")

    @money.command(name="pay")
    async def pay(self, ctx, to: str, ammount: str):
        """ Pay money to someone. Usage: ?money pay @user#1234 ammount """
        try:
            if int(ammount) < 0:
                await ctx.send(f"```Azy t'as cru tu vas me niquer comme ça ?```")
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
            payfrom = ctx.message.author.id
            #print(payfrom)
            to = to.strip('<')
            to = to.strip('>')
            to = to.strip('@')
            to = to.strip('!')
            usernametopay = await self.bot.get_user_info(to)
            url = 'https://dev.knl.im/konobot/api/index.php?call=pay&from='+str(payfrom)+'&to='+str(to)+'&ammount='+str(ammount)
            #print(url)
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(url)
                await http.addlog('money',ctx.message.author.name,str(ammount),'pay','payement to '+str(to))
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
            print(e)
        await ctx.send(f"```{ctx.message.author.name} paid {str(ammount)} to {usernametopay}```")

def setup(bot):
    bot.add_cog(Discord_Economy(bot))
