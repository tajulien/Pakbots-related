import asyncio
import re
import pyppeteer

from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
from utils import default


class Looped(commands.Cog):
    LIST = []
    LIST_DESIRED_PRICE = [
        ['Greater Arcane Elixir', '6g 00s 00c']
    ]

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

#   FONCTIONS

    def index_2d(my_List, v):
        for i, x in enumerate(my_List):
            if v in x:
                return (i, x.index(v))

    def check_if_desired(itemtitle_short):
        return any(itemtitle_short in sublist for sublist in Looped.LIST_DESIRED_PRICE)

    def fix_desired_price(itemtitle_short):
        if Looped.check_if_desired(itemtitle_short):
            ind = Looped.index_2d(Looped.LIST_DESIRED_PRICE, itemtitle_short)
            return Looped.LIST_DESIRED_PRICE[ind[0]][1]
        else:
            return "No price fixed"

    def check_if_exist(itemtitle, result, fix_desired_price, icon_url):
        if any(itemtitle in sublist for sublist in Looped.LIST):
            ind = Looped.index_2d(Looped.LIST, itemtitle)
            if Looped.LIST[ind[0]][1] != result:
                Looped.LIST[ind[0]][1] = result
                print(f'Price of {itemtitle} Updated')
                print(Looped.LIST)
                return
            return
        Looped.LIST.append([itemtitle, result, fix_desired_price, icon_url])
        print(f'Item {itemtitle} added at {result}')
        print(Looped.LIST)

    def get_buyout_formated(buyoutprice):
        if "g" in buyoutprice:
            gold = buyoutprice.lstrip()
            gold = gold[:gold.find('g')]
        else:
            gold = "00"
        if "s" in buyoutprice:
            if "g" in buyoutprice:
                silver = buyoutprice[buyoutprice.find('g'):]
                silver = silver[2:silver.find('s')]
                if int(silver) < 10:
                    silver = '0' + silver
            else:
                silver = buyoutprice[2:buyoutprice.find('s')]
                if int(silver) < 10:
                    silver = '0' + silver
        else:
            silver = "00"
        if "c" in buyoutprice:
            copper = buyoutprice[:buyoutprice.find('c')]
            copper = copper[-2:]
            copper = copper.lstrip()
            if int(copper) < 10:
                copper = '0' + copper
        else:
            copper = "00"
        sum_compare = gold + silver + copper
        formatted = f'{gold}g {silver}s {copper}c'
        return gold, silver, copper, sum_compare, formatted

    def find_icon(itemid):
        html = urlopen('https://classic.wowhead.com/item='+str(itemid))
        bs = BeautifulSoup(html, 'html.parser')
        bs = str(bs)
        icon_url = bs[bs[bs.find('script'):].find('meta content="https://wow.zamimg.com/images/wow/icons/large'):]
        icon_url2 = icon_url[icon_url.find('meta content'):]
        icon_url3 = icon_url2[icon_url2.find("https://wow.zamimg.com/images/wow/icons"):]
        icon_url4 = icon_url3[:icon_url3.index("property")]
        return icon_url4[:-2]

    @staticmethod
    async def compare_price_get_notified(self, itemtitle_short, pricenow, pricetarget):
        ret2 = re.sub('[gsc]', '', pricetarget)
        pricetarget = re.sub(r"\s+", '', ret2)
        ret3 = re.sub('[gsc]', '', pricenow)
        pricenow = re.sub(r"\s+", '', ret3)
        if pricenow <= pricetarget:
            pricenow_formatted = f'{pricenow[:-4]}g {pricenow[-4:-2]}s {pricenow[-2:]}c'
            pricetarget_formatted = f'{pricetarget[:-4]}g {pricetarget[-4:-2]}s {pricetarget[-2:]}c'
            await Looped.notify(self, itemtitle_short, pricenow_formatted, pricetarget_formatted)
        else:
            print("Price is still higher than expected")

    @staticmethod
    async def notify(self, itemtitle_short, pricenow_formatted, pricetarget_formatted):
        channel = self.get_channel(543398038220177429)
        await channel.send(f'The price for {itemtitle_short} is now at {pricenow_formatted} target : {pricetarget_formatted}')


    @staticmethod
    async def get_price(self, itemid):
        try:
            browser = await pyppeteer.launch(headless=True, executablePath='/usr/bin/chromium-browser', args=['--no-sandbox'])
            page = await browser.newPage()
            await page.goto('https://nexushub.co/wow-classic/items/sulfuron-horde/'+str(itemid))
            await asyncio.sleep(15)
            title = await page.title()
            itemtitle = str(title)[:-11]
            itemtitle_short = str(itemtitle)[:-20]
            fix_desired_price = Looped.fix_desired_price(itemtitle_short)
            result = await page.evaluate('document.body.textContent', force_expr=True)
            result = result[result.find('Minimum Buyout'):]
            result = result[24:37]
            if result == '':
                result = ["", "", "", "", "No buyout available"]
            else:
                result = Looped.get_buyout_formated(result)
                if fix_desired_price != "No price fixed":
                    await Looped.compare_price_get_notified(self, itemtitle_short, result[4], fix_desired_price)
            icon_url = Looped.find_icon(itemid)
            Looped.check_if_exist(itemtitle, result[4], fix_desired_price, icon_url)
            #print(base.Discord_Info.sendtime(self))
        except Exception as e:
            print(e)
        finally:
            await browser.close()

    @staticmethod
    async def fletch(self):
        """ DEBUG """
        try:
            await Looped.get_price(13454)
            channel = self.get_channel(543398038220177429)
            await channel.send("Fletching some datas")
        except Exception as e:
            print(e)

#     SETUP


def setup(bot):
    bot.add_cog(Looped(bot))
