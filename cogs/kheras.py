from discord.ext import commands

from utils import default


class kheras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        
    @commands.group()
    async def kheras(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @kheras.command()
    @commands.guild_only()
    async def sayHello(self, ctx):
        """ Test Hellow World """
        try:
            await ctx.send("?rpg spawn")
            return
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

  
def setup(bot):
    bot.add_cog(kheras(bot))
