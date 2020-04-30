from utils import permissions
from discord.ext.commands import AutoShardedBot
import asyncio
from cogs import base
from cogs import infobourse
from cogs import marketindics
from cogs import looped
from datetime import datetime
import random


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

        #self.bg_task = self.loop.create_task(self.dotstuff())
        self.bg_task = self.loop.create_task(self.doubledostuff())

    async def dotstuff(self):
        await self.wait_until_ready()
        while not self.is_closed():
            #await looped.Looped.get_price(self, 13454)
            #await looped.Looped.get_price(self, 13452)
            #await looped.Looped.get_price(self, 13511)
            #await looped.Looped.get_price(self, 13512)
            #await looped.Looped.get_price(self, 13513)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time is", current_time)
            await asyncio.sleep(random.randint(3200, 3800))

    async def doubledostuff(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await marketindics.Indics.notify_chan(self)
            await infobourse.News.notify_chan(self)
            await asyncio.sleep(random.randint(80, 90))

    async def on_message(self, msg):
        if not self.is_ready() or not permissions.can_send(msg):
            return

        await self.process_commands(msg)
