import json
from discord.ext import commands
from utils import default
import os
from datetime import datetime, date
today = date.today()
import time

class News(commands.Cog):
    datejour1 = today.strftime("%y/%m/%d")
    LISTGIVE = []
    LISTRENDER = []
    firstturn = False

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    def check_list_update(self):
        try:
            #print("3")
            #print(os.getcwd())
            #print(os.getcwd()+"\\newsdata\\newsdata.json")
            #print(os.path.join(os.getcwd(),"/newsdata/newsdata.json"))
            #print(os.path.realpath(__file__))
            #path_to_json = 'newsdata/'
            #os.listdir(path_to_json)
            with open(os.getcwd()+"/cogs/newsdata/newsdata.json") as json_file:
                dataz = json.load(json_file)
                if News.LISTGIVE == []:
                    News.firstturn = True
                else:
                    News.firstturn = False
                for p in dataz['newsbourse']:
                    p_date, p_time = p['date'], p['time']
                    p_title, p_url = p['title'], p['url']
                    if any(p_title in sublist for sublist in News.LISTGIVE):
                        print(f'{News.datejour1} - News {p_title} already exist')
                    else:
                        if not News.firstturn:
                            News.LISTRENDER.append([p_date, p_time, p_title, p_url])
                        News.LISTGIVE.append([p_date, p_time, p_title, p_url])
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f'{News.datejour1} - {current_time} - News {p_title} - {p_url} added')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{News.datejour1} - {current_time} datas updated')
            json_file.close()
            return True
        except Exception as e:
            print(e)

    @staticmethod
    async def notify_chan(self):
        News.LISTRENDER = []
        News.check_list_update(self)
        if News.LISTRENDER:
            for result in reversed(News.LISTRENDER):
                channel = self.get_channel(686901430669672462)
                await channel.send(f'{result[0]} - {result[1]} - News : {result[2]} - {result[3]}')
                time.sleep(10)
            News.LISTRENDER = []


def setup(bot):
    bot.add_cog(News(bot))
