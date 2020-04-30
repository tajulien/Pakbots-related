import time
import tokened
import mysql.connector

from datetime import datetime, date
from discord.ext import commands
from utils import default

today = date.today()


class Indics(commands.Cog):
    datejour2 = today.strftime("%y/%m/%d")
    INDICSGIVE = []
    INDICSRENDER = []

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    def check_update(self, datejour):
        try:
            connection = mysql.connector.connect(host=tokened.bddurl,
                                                 database='market_datas',
                                                 user=tokened.bdduser,
                                                 password=tokened.bddpass)
            sql_select_Query = "select * from market_indics"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if any(datejour in sublist for sublist in records):
                for elt in records:
                    elt = list(elt)
                    if datejour in elt:
                        # print(elt[0], elt[1], elt[2], elt[3], elt[4], elt[5], elt[6], elt[7], elt[8], elt[9], elt[10])
                        if any(elt[0] in sublist for sublist in Indics.INDICSGIVE):
                            print(f'{Indics.datejour2} - {current_time}  - Actions already rendered ')
                            return
                        else:
                            Indics.INDICSRENDER.append(
                                [elt[0], elt[1], elt[2], elt[3], elt[4], elt[5], elt[6], elt[7], elt[8], elt[9],
                                 elt[10], elt[11], elt[12]])
                            Indics.INDICSGIVE.append(
                                [elt[0], elt[1], elt[2], elt[3], elt[4], elt[5], elt[6], elt[7], elt[8], elt[9],
                                 elt[10], elt[11], elt[12]])
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            print(f'{Indics.datejour2} - {current_time} - Actions {elt[0]} - {elt[1]} - {elt[3]} added')
            else:
                print(f' {Indics.datejour2} - {current_time} - pas auj')
                return
            # print("indics give :")
            # print(Indics.INDICSGIVE)
            # print("indics render :")
            # print(Indics.INDICSRENDER)
            print(f'{Indics.datejour2} - {current_time} datas updated')
        except Exception as e:
            print(e)

    def check_details(self, act_name):
        try:
            connection = mysql.connector.connect(host=tokened.bddurl,
                                                 database='market_datas',
                                                 user=tokened.bdduser,
                                                 password=tokened.bddpass)
            sql_select_Query = "select * from market_indics"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            now = datetime.now()
            datejour = today.strftime("%y/%m/%d")
            datejour = datejour.replace('/', '-')
            current_time = now.strftime("%H:%M:%S")
            if any(act_name in sublist for sublist in records):
                for elt in records:
                    elt = list(elt)
                    if datejour in elt:
                        if act_name in elt:
                            logos = Indics.getlogo(self, act_name)
                            # print(type(logos))
                            return [elt[0], elt[1], elt[2], elt[3], elt[4], elt[5], elt[6], elt[7], elt[8], elt[9],
                                    elt[10], elt[11], elt[12], logos]
                y = "Pas d'action aujourd'hui"
                return y
            else:
                y = "Action non trouvée"
                return y
        except Exception as e:
            print(e)

    def getlogo(self, act_name):
        try:
            connection = mysql.connector.connect(host=tokened.bddurl,
                                                 database='market_datas',
                                                 user=tokened.bdduser,
                                                 password=tokened.bddpass)
            sql_select_Query = "select * from market_action_details"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            for elt in records:
                elt = list(elt)
                if act_name in elt:
                    return elt[4]
        except Exception as e:
            print(e)

    @staticmethod
    async def notify_chan(self):
        Indics.LISTRENDER = []
        if datetime.today().weekday() == 5 or datetime.today().weekday() == 6:
            print(f' {Indics.datejour2} - it''s weekend we are fucked')
            return
        datejour = today.strftime("%y/%m/%d")
        datejour = datejour.replace('/', '-')
        Indics.check_update(self, datejour)
        if Indics.INDICSRENDER:
            for result in reversed(Indics.INDICSRENDER):
                channel = self.get_channel(691367149041614970)
                await channel.send(
                    f'{Indics.datejour2} - {result[1]} - mma10 : {result[4]} - mma20 : {result[5]} - mma50 : {result[6]} - mma100 : {result[7]} - mma200 : {result[8]} - Macd : {result[9]} - Bolling inf : {result[10]} - Bolling Sup : {result[11]} - Signal : {result[12]} -')
                time.sleep(10)
            Indics.INDICSRENDER = []


def setup(bot):
    bot.add_cog(Indics(bot))
