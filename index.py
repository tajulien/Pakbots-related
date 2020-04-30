import os
#import sys
#sys.path.append('/cogs/')
from datetime import datetime
#from discord.ext.commands import HelpFormatter
from data import Bot
from utils import permissions, default, http

config = default.get("config.json")
description = ("""
The Pakbot !
""")


# class HelpFormat(HelpFormatter):
#     async def format_help_for(self, context, command_or_bot):
#         if permissions.can_react(context):
#             await context.message.add_reaction(chr(0x2709))
#
#         return await super().format_help_for(context, command_or_bot)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time is", current_time)
print("Connecting to Discord...")


help_attrs = dict(hidden=True)
bot = Bot(command_prefix=config.prefix, prefix=config.prefix, pm_help=True, help_attrs=help_attrs)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

#bot.loop.create_task(Myclient.dostuff())

bot.run(config.token)
