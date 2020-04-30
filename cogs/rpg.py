import asyncio
import json
import random

import aiohttp
import discord
from discord.ext import commands
from numpy.random import choice

from utils import default


class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        #self.bot.loop.create_task(RPG.spawn_task(self))
        #self.bg_task = self.bot.loop.create_task(RPG.spawn_task(self))

    lobby_players = []
    lobby_slots = 3
    currentBattle = []
    activemob = 0
    activebattle = 0
#############################################################################################################################################################################################################
#
#   FONCTIONS
#
#############################################################################################################################################################################################################
    dabug = True

#############################################################################################################################################################################################################
#
#   GESTION DE L'EXP
#
#############################################################################################################################################################################################################

    def comparelvl(lvlplayer, lvlmonster):
        color = "None"
        if lvlplayer == lvlmonster:
            color = "Green"
        if lvlmonster <= (lvlplayer-3):
            color = "Grey"
        if (lvlmonster > (lvlplayer)) and (lvlmonster <= lvlplayer+3):
            color = "Orange"
        if (lvlmonster < (lvlplayer)) and (lvlmonster >= lvlplayer-3):
            color = "Green"
        if (lvlmonster > (lvlplayer+3)):
            color = "Red"
        return color

    def xpgainedbylvl(lvlplayer, lvlmonster, result):
        if result == "victoire":
            colorstatus = RPG.comparelvl(lvlplayer, lvlmonster)
            if colorstatus == "Green":
                xpgained = int((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)
            if colorstatus == "Grey":
                xpgained = int(((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)/10)
            if colorstatus == "Orange":
                xpgained = int(((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)*(1 + 0.01 * (int(lvlmonster)-int(lvlplayer))))
            if colorstatus == "Red":
                xpgained = int(((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)*(1 + 0.05 * (int(lvlmonster)-int(lvlplayer))))
            if colorstatus == "None":
                xpgained = 0
            return xpgained
        else:
            #desactivation de la perte d'exp
            #colorstatus = RPG.comparelvl(lvlplayer, lvlmonster)
            #if colorstatus == "Green":
            #    xpgained = int((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)
            #if colorstatus == "Grey":
            #    xpgained = int(((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)/10)
            #if colorstatus == "Orange":
            #    xpgained = int(((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)*(1 + 0.01 * (int(lvlmonster)-int(lvlplayer)))/100)
            #if colorstatus == "Red":
            #    xpgained = int(((5*(int(lvlmonster)**2)+50*int(lvlmonster)+100)*(31.404/100)**1.05)*(1 + 0.05 * (int(lvlmonster)-int(lvlplayer)))/100)
            #if colorstatus == "None":
            #    xpgained = 0
            xpgained = 0
            return xpgained

    @staticmethod
    async def topxp(self):
        """ top xp """
        try:
            url = 'https://dev.knl.im/konobot/api/index.php?call=exptop'
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(url)
                response = await raw_response.text()
                #print(response)
                response = json.loads(response)
                baltop_formatted=''
                count=1
                for f in response:
                    account = f['discord_id']
                    account = account.strip('<')
                    account = account.strip('>')
                    account = account.strip('@')
                    account = account.strip('!')
                    user = await self.bot.get_user_info(account)
                    lvls = RPG._get_level_from_xp(f['exp'])
                    baltop_formatted=baltop_formatted+'#'+str(count)+'. '+str(user)+': '+f['exp']+' xp / Level : '+ str(lvls) +' \n'
                    count=count+1
            return baltop_formatted
        except Exception as e:
            print (e)

    def xpmobs(level):
        """ DEBUG """
        xpraw = (5*(int(level)**2)+50*int(level)+100)*(31.404/100)**1.05
        xpdecim = int(xpraw)
        return xpdecim

    @staticmethod
    async def addxp(self, username, charid, xpcount):
        playerxpurl = 'http://dev.knl.im/konobot/api/index.php?call=getExp&id='+str(charid)
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(playerxpurl)
            response = await raw_response.text()
            response = json.loads(response)
            try:
                playerxp=response[0]['exp']
            except Exception as e:
                playerxp = 0

        if playerxp is None:
            playerxp = 0
        else:
            playerxp = int(playerxp)

        lvl = RPG._get_level_from_xp(playerxp)
        url = 'http://dev.knl.im/konobot/api/index.php?call=modExp&id='+str(charid)+'&ammount='+str(xpcount)
        print('Given $'+str(xpcount)+' exp to '+str(charid))
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)

        newxp = int(playerxp) + int(xpcount)
        newlvl = RPG._get_level_from_xp(newxp)
        if newlvl != lvl:
            destchannel = self.bot.get_channel(549533466350452756)
            await destchannel.send('gg '+str(username)+' ! Tu passes level '+str(newlvl))
            #await destchannel.send('gg '' ! Tu passes level '+str(newlvl))


    def monsterattack(player, monster):
        return winner

#############################################################################################################################################################################################################
#
#   GESTION DES STATS
#
#############################################################################################################################################################################################################

    def get_dmg_from_class(charid):
        x = 0
        return x

    def get_hp_from_class(charid):
        x = 100
        return x

    def get_dmg_from_items(charid):
        x = 0
        return x

    def get_hp_from_items(charid):
        x = 100
        return x


#############################################################################################################################################################################################################
#
#   GESTION DU SPAWN DES LOOTS ET DES MOBS
#
#############################################################################################################################################################################################################
    @staticmethod
    async def spawn_mobs(self):
        """ DEBUG """
        try:
            channel = self.get_channel(543398038220177429)
            #print (RPG.activebattle)
            if RPG.activebattle == 1:
                await channel.send(f"Mob is gone, new mob is coming !.")
            RPG.lobby_slots = 3
            RPG.activebattle = 0
            RPG.lobby_players = []
            drop = await RPG.mobgen()
            RPG.activemob = 1         
            mobapi = 'https://dev.knl.im/konobot/api/index.php?call=getMob&id='+str(drop[0])
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(mobapi)
                response = await raw_response.text()
                response = json.loads(response)
                randommob = random.choice(response)
                RPG.currentBattle = randommob
                print(RPG.currentBattle)
                mobrarity = randommob['rarity']
                if mobrarity == '1' or mobrarity == '2' or mobrarity == '3' or mobrarity == '4':
                    icolor=discord.Color.from_rgb(255,255,255)
                elif mobrarity == '5' or mobrarity == '6' or mobrarity == '7':
                    icolor=discord.Color.from_rgb(0,112,221)
                elif mobrarity == '8' or mobrarity == '9':
                    icolor=discord.Color.from_rgb(163,53,238)
                elif mobrarity == '10':
                    icolor=discord.Color.from_rgb(255,128,0)
                xpbase = str(RPG.xpmobs(randommob['level']))
                embed = discord.Embed(colour=icolor)
                embed.set_thumbnail(url='http://dev.knl.im/konobot/api/data/'+str(randommob['id'])+'.jpg')
                embed.add_field(name="Nom:", value=randommob['name'], inline=True)
                embed.add_field(name="Niveau:", value=randommob['level'], inline=True)
                embed.add_field(name="XP:", value=xpbase, inline=True)
                embed.add_field(name="HP:", value=randommob['hp'], inline=True)
                embed.add_field(name="Dégats:", value=randommob['damage'], inline=True)
                embed.add_field(name="Rareté:", value=randommob['rarity'], inline=True)
                embed.add_field(name="Description:", value=randommob['description'], inline=True)
                await channel.send(content=f"Un **{randommob['name']}** sauvage apparait !", embed=embed)
        except Exception as e:
            print (e)

    @staticmethod
    async def lootgen():
        try:
            ra1= await RPG.lootdb(1)
            ra2= await RPG.lootdb(2)
            ra3= await RPG.lootdb(3)
            ra4= await RPG.lootdb(4)
            ra5= await RPG.lootdb(5)
            items = {"blanc":ra1,"vert":ra2,"rare":ra3,"epique":ra4,"legendaire":ra5}
            probabilities = {"blanc":0.40,"epique":0.1,"legendaire":0.05,"vert":0.25,"rare":0.20}
            #item = choice(items[choice(probabilities.keys(),p=probabilities.values())])
            temp_prob = list(probabilities.keys())
            temp_values = list(probabilities.values())
            itemtemps = choice(temp_prob,p=temp_values)
            item = choice(items[itemtemps])
            return item, itemtemps
        except Exception as e:
            print(e)


    @staticmethod
    async def mobgen():
        try:
            ra1= await RPG.mobdb(1)
            ra2= await RPG.mobdb(2)
            ra3= await RPG.mobdb(3)
            ra4= await RPG.mobdb(4)
            ra5= await RPG.mobdb(5)
            ra6= await RPG.mobdb(6)
            ra7= await RPG.mobdb(7)
            ra8= await RPG.mobdb(8)
            ra9= await RPG.mobdb(9)
            ra10= await RPG.mobdb(10)
            items2 = {"commun":ra1[0]+ra2[0]+ra3[0]+ra4[0],"rare":ra5[0]+ra6[0]+ra7[0],"elite":ra8[0]+ra9[0],"boss":ra10[0]}
            probabilities2 = {"commun":0.45,"rare":0.40,"elite":0.10,"boss":0.05}
            #item = choice(items[choice(probabilities.keys(),p=probabilities.values())])
            temp_prob2 = list(probabilities2.keys())
            temp_values2 = list(probabilities2.values())
            itemtemps2 = choice(temp_prob2,p=temp_values2)
            item2 = choice(items2[itemtemps2])
            return item2, itemtemps2
        except Exception as e:
            print(e)

    @staticmethod
    async def lootdb(rarity:int):
            itemurl = 'http://dev.knl.im/konobot/api/index.php?call=getItemByQ&q='+str(rarity)
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(itemurl)
                response = await raw_response.text()
                response = json.loads(response)
                lootz=[]
                for f in response:
                    lootz.append(f['item_name'])
                return lootz

    @staticmethod
    async def get_char_info(charid):
            itemurl = 'https://dev.knl.im/konobot/api/index.php?call=getChar&id='+str(charid)
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(itemurl)
                response = await raw_response.text()
                response = json.loads(response)
                return response[0]

    @staticmethod
    async def get_tot_char_info(charid):
            playChar = 'https://dev.knl.im/konobot/api/index.php?call=getChar&id='+str(charid)
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(playChar)
                response = await raw_response.text()
                response = json.loads(response)
                username = str(response[0]['username'])
                classe = str(response[0]['class'])
                char_hp = str(response[0]['hp'])
                char_hpmax = str(int(response[0]['hp_max']) + int(RPG.get_hp_from_class(charid)) + int(RPG.get_hp_from_items(charid)))
                char_exp = str(response[0]['exp'])
                char_dmg = str(int(response[0]['dmg']) + int(RPG.get_dmg_from_class(charid)) + int(RPG.get_dmg_from_items(charid)))
                nb_wins = str(response[0]['fight_wins'])
                nb_loses = str(response[0]['fight_loses'])
                summary = [str(charid),username,classe,char_hp,char_hpmax,char_exp,char_dmg,nb_wins,nb_loses]
                return summary

    @staticmethod
    async def mobdb(rarity:int):
            moburl = 'https://dev.knl.im/konobot/api/index.php?call=getMobsByQ&q='+str(rarity)
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(moburl)
                response = await raw_response.text()
                response = json.loads(response)
                mobz=[]
                mobzname=[]
                for f in response:
                    mobz.append(f['id'])
                    mobzname.append(f['name'])
                return mobz,mobzname

    @commands.group()
    async def rpg(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @staticmethod
    def _get_level_xp(n):
        return 5*(n**2)+50*n+100

    @staticmethod
    def _get_level_from_xp(xp):
        remaining_xp = int(xp)
        level = 0
        while remaining_xp >= RPG._get_level_xp(level):
            remaining_xp -= RPG._get_level_xp(level)
            level += 1
        return level




#############################################################################################################################################################################################################
#
#     LOOP
#
#############################################################################################################################################################################################################
    @staticmethod
    async def spawn_task(self):
        chan = self.bot.get_channel(543398038220177429)
        print ("yolo")
        counter = "stupid"
        await chan.send(counter)
        await asyncio.sleep(10)
            #await channel.send(counter)
            #await asyncio.sleep(60)




#############################################################################################################################################################################################################
#
#     COMMANDS
#
#############################################################################################################################################################################################################

    @rpg.command()
    @commands.guild_only()
    #@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def testloop(self, ctx):
        """ DEBUG """
        try:
            if RPG.dabug:
                loop = await RPG.spawn_task(self)
                return loop
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def topxps(self, ctx):
        """ best xp of the server """
        try:
            if RPG.dabug:
                loop = await RPG.topxp(self)
                return await ctx.send(f"```\n{loop}```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    #@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def xpforlevel(self, ctx, level):
        """ DEBUG """
        try:
            _value = 5*(int(level)**2)+50*int(level)+100
            return await ctx.send(f"```\n{_value}```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def xpmonster(self, ctx, level):
        """ xptestmonster """
        try:
            xpraw = (5*(int(level)**2)+50*int(level)+100)*(31.404/100)**1.05
            xpdecim = ("%.2f" % round(xpraw,2))
            return await ctx.send(f"```\n{xpdecim}```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def xpbattle(self, ctx, lvlp:int, lvlm:int, result):
        """ xpforthebattle """
        try:
            resultnum = RPG.xpgainedbylvl(lvlp, lvlm, result)
            return await ctx.send(f"```\n{resultnum} xp```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def loot(self, ctx):
        """ gimmeloot plz """
        try:
            drop = await RPG.lootgen()
            print(drop)
            return await ctx.send(f"```\n Vous avez trouvé un(e) {drop[0]} un équipement {drop[1]} !!```")
        except Exception as e:
            print(e)
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def spawn(self, ctx):
        """ spawn a random mob biatch plz """
        try:
            drop = await RPG.mobgen()
            mobapi = 'https://dev.knl.im/konobot/api/index.php?call=getMob&id='+str(drop[0])
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(mobapi)
                response = await raw_response.text()
                response = json.loads(response)
                randommob = random.choice(response)
                nameid = randommob['name']
            return await ctx.send(f"```\n un {nameid} (ID : {drop[0]}) apparaît, une créature {drop[1]} !!```")
        except Exception as e:
            print(e)
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def listeloot(self, ctx, rarity):
        """ list of loot by rarity plz """
        try:
            listemoi = await RPG.lootdb(rarity)
            return await ctx.send(f"```\n {listemoi} !!```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    #@rpg.command()
    #@commands.guild_only()
    #async def oldme(self, ctx):
    #    """ gimmeloot plz """
    #    try:
    #        charinfos = await RPG.get_char_info(ctx.message.author.id)
    #        print(charinfos)
    #        embed = discord.Embed()
    #        embed.set_thumbnail(url=ctx.message.author.avatar_url)
    #        embed.add_field(name="ID:", value=charinfos['discord_id'], inline=True)
    #        charlvl = RPG._get_level_from_xp(charinfos['exp'])
    #        embed.add_field(name="Niveau:", value=str(charlvl), inline=True)
    #        expstring = str(charinfos['exp'])+'/'+str(RPG._get_level_xp(charlvl))
    #        embed.add_field(name="XP:", value=charinfos['exp'], inline=True)
    #        hpstring = charinfos['hp']+'/'+charinfos['hp_max']
    #        embed.add_field(name="HP:", value=str(hpstring), inline=True)
    #        embed.add_field(name="Dégats:", value=charinfos['dmg'], inline=True)
    #        fightstring = charinfos['fight_wins']+' wins / '+charinfos['fight_loses']+' loses'
    #        embed.add_field(name="Nombre de Combats:", value=str(fightstring), inline=True)
    #        #embed.add_field(name="Description:", value=charinfos['description'], inline=True)
    #        await ctx.send(content=f" **Character Stats** !", embed=embed)
    #    except Exception as e:
    #        return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def me(self, ctx):
        """ show me what i got plz """
        try:
            charinfos = await RPG.get_tot_char_info(ctx.message.author.id)
            #summary = [str(charid),username,classe,char_hp,char_hpmax,char_exp,char_dmg,nb_wins,nb_loses]
            embed = discord.Embed()
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.add_field(name="ID:", value=charinfos[0], inline=True)
            charlvl = RPG._get_level_from_xp(charinfos[5])
            embed.add_field(name="Niveau:", value=str(charlvl), inline=True)
            expstring = str(charinfos[5])+'/'+str(RPG._get_level_xp(charlvl))
            embed.add_field(name="XP:", value=charinfos[5], inline=True)
            hpstring = charinfos[3]+'/'+charinfos[4]
            embed.add_field(name="HP:", value=str(hpstring), inline=True)
            embed.add_field(name="Dégats:", value=charinfos[6], inline=True)
            fightstring = charinfos[7]+' wins / '+charinfos[8]+' loses'
            embed.add_field(name="Nombre de Combats:", value=str(fightstring), inline=True)
            await ctx.send(content=f" **Character Stats** !", embed=embed)
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def listemob(self, ctx, rarity):
        """ list of mobs by rarity plz """
        try:
            listemobz = await RPG.mobdb(rarity)
            return await ctx.send(f"```\n {listemobz} !!```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def oldfight(self, ctx):
        """ gimmeloot plz """
        try:
            if RPG.currentBattle == []:
                await ctx.send(f"No battle in progress.")
                return
            curbattle = RPG.currentBattle
            oldHP = curbattle['hp']
            dmg_s = await RPG.get_tot_char_info(ctx.message.author.id)
            dmg = int(dmg_s[6])
            newHP = int(oldHP) - dmg
            if newHP < 0:
                RPG.currentBattle = [] #boss is dead, reset the array
                await ctx.send(f"Yay gratz you killed that motherfucker !")
                #todo loots
                return
            RPG.currentBattle['hp'] = newHP
            return await ctx.send(f"You hit {curbattle['name']} for {dmg}, this fucker only have {newHP} left !")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @staticmethod
    async def fightingfc(self, charid, charhp, i):
        channel = self.bot.get_channel(543398038220177429)
        curbattle = RPG.currentBattle
        mobHP = int(curbattle['hp'])
        #print(mobHP)
        #print (RPG.activebattle)
        dmg_s = await RPG.get_tot_char_info(charid)
        player1 = await self.bot.get_user_info(charid)
        player2 = str(player1)
        playername = player2[:-5]
        dmg = int(dmg_s[6])
        dmg_mob = int(curbattle['damage'])
        charlvl = RPG._get_level_from_xp(dmg_s[5])
        nbfighters = len(RPG.lobby_players)
        await channel.send(f"{nbfighters} fighter(s)  --  {playername} turn")
        mobHP = mobHP - dmg
        playerHP = charhp - dmg_mob
        #print (playerHP)
        result = "none"
        await channel.send(f"{playername} hits {curbattle['name']} for {dmg}, this fucker only have {mobHP} left !")
        await channel.send(f"{curbattle['name']} hits {playername} for {dmg_mob}, {playername} only has {playerHP} left !")
        RPG.currentBattle['hp'] = int(mobHP)
        RPG.lobby_players[i][2] = playerHP
        #print (RPG.lobby_players)
        #print(RPG.currentBattle['hp'])
        #print (RPG.lobby_players[i][2])
        await asyncio.sleep(1)
        if (mobHP < 0) and (playerHP < 0):
            result = "draw"
            resultnum = RPG.xpgainedbylvl(int(charlvl), int(curbattle['level']), result)
            await channel.send(f"Stupid, you're both dead !")
            await channel.send(f"```\n{resultnum} xp lost```")
        elif (mobHP < 0):
            result = "victoire"
            resultnum = RPG.xpgainedbylvl(int(charlvl), int(curbattle['level']), result)
            await channel.send(f"{curbattle['name']} is dead motherfucker !")
            await channel.send(f"```\n{resultnum} xp gain```")
            #await RPG.addxp(self, ctx.message.author, charid, int(resultnum))
            RPG.activemob = 0
            RPG.currentBattle = []
            RPG.activebattle = 0
            RPG.lobby_players = []
            RPG.lobby_slots = 3
        elif (playerHP<0):
            result = "defaite"
            resultnum = RPG.xpgainedbylvl(int(charlvl), int(curbattle['level']), result)
            await channel.send(f"{playername} is dead motherfucker !")
            await channel.send(f"```\n{resultnum} xp lost```")
            #todo loots
        return result

    @rpg.command()
    @commands.guild_only()
    async def fighting(self, ctx):
        """ Ready ? Fight bitches """
        try:
            RPG.activebattle = 1
            #hppositifs = 0
            if RPG.currentBattle == []:
                await ctx.send(f"No battle in progress.")
                return
            if  RPG.lobby_slots == 3:
                await ctx.send(f"```You must join the lobby```")
                return
            else:
                i = 0
                for i in range(len(RPG.lobby_players)):
                    go = await RPG.fightingfc(self, str(RPG.lobby_players[i][1]), int(RPG.lobby_players[i][2]), int(i))
                    print(go)
                    if go == "defaite" or go == "draw":
                        del RPG.lobby_players[i]
                        RPG.lobby_slots += 1
                        if RPG.lobby_players == []:
                            await ctx.send(f"```Game over```")
                            RPG.activemob = 0
                            RPG.currentBattle = []
                            RPG.activebattle = 0
                            RPG.lobby_players = []
                    await asyncio.sleep(1)

                    #if RPG.lobby_players != []:
                    #    hppositifs += int(RPG.lobby_players[i][2])
            #if hppositifs < 0:
            #    RPG.activemob = 0
            #    RPG.currentBattle = []
            #    RPG.lobby_slots = 3
            #    RPG.lobby_players = []
            #    RPG.activebattle = 0
            #    await ctx.send(f"```Game over```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    #@rpg.command()
    #@commands.guild_only()
    #async def fight(self, ctx):
    #    """ Ready ? Fight bitches """
    #    try:
    #        if RPG.currentBattle == []:
    #            await ctx.send(f"No battle in progress.")
    #            return
    #        if  RPG.lobby_slots == 3:
    #            await ctx.send(f"```You must join the lobby```")
    ##            return
     #       curbattle = RPG.currentBattle
     #       mobHP = int(curbattle['hp'])
     #       dmg_s = await RPG.get_tot_char_info(ctx.message.author.id)
     #       player1 = await self.bot.get_user_info(ctx.message.author.id)
     #       player2 = str(player1)
     #       playername = player2[:-5]
     #       dmg = int(dmg_s[6])
     ##       playerHP = int(dmg_s[4])
      #      dmg_mob = int(curbattle['damage'])
      #      charlvl = RPG._get_level_from_xp(dmg_s[5])
      #      nbfighters = 3-(RPG.lobby_slots)
      #      await ctx.send(f"{nbfighters} fighter(s)")
      #      while ((mobHP > dmg) and (playerHP > dmg_mob)) and RPG.dabug:
      #          mobHP = mobHP - dmg
       ##         #RPG.currentBattle['hp'] = mobHP
         #       playerHP = playerHP - dmg_mob
         #       await ctx.send(f"{playername} hits {curbattle['name']} for {dmg}, this fucker only have {mobHP} left !")
         ##       await ctx.send(f"{curbattle['name']} hits {playername} for {dmg_mob}, {playername} only has {playerHP} left !")
          #      await asyncio.sleep(1)
          #  if (mobHP < dmg) and (playerHP < dmg_mob):
          #      result = "defaite"
           #     resultnum = RPG.xpgainedbylvl(int(charlvl), int(curbattle['level']), result)
           #     await ctx.send(f"Stupid, you're both dead !")
           #     await ctx.send(f"```\n{resultnum} xp lost```")
           ## else:
            #    if (mobHP < dmg):
           #         result = "victoire"
           #         resultnum = RPG.xpgainedbylvl(int(charlvl), int(curbattle['level']), result)
           #         await ctx.send(f"{curbattle['name']} is dead motherfucker !")
           #         await ctx.send(f"```\n{resultnum} xp gain```")
           #         await RPG.addxp(self, ctx.message.author, ctx.message.author.id, int(resultnum))
           #         RPG.activemob = 0
           #         RPG.currentBattle = []
           #     else:
           #         result = "defaite"
           #         resultnum = RPG.xpgainedbylvl(int(charlvl), int(curbattle['level']), result)
           #         await ctx.send(f"{playername} is dead motherfucker !")
           #         await ctx.send(f"```\n{resultnum} xp lost```")
           # #todo loots
           # return
        #except Exception as e:
        #    return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def encounter(self, ctx):
        """ DEBUG """
        try:
            if RPG.currentBattle != []:
                await ctx.send(f"Battle already in progress.")
                return
            drop = await RPG.mobgen()
            mobapi = 'https://dev.knl.im/konobot/api/index.php?call=getMob&id='+str(drop[0])
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(mobapi)
                response = await raw_response.text()
                response = json.loads(response)
                username = await self.bot.get_user_info(ctx.message.author.id)
                randommob = random.choice(response)
                RPG.currentBattle = randommob
                RPG.activemob = 1
                #print(randommob)
                xpbase = str(RPG.xpmobs(randommob['level']))
                embed = discord.Embed()
                embed.set_thumbnail(url='http://dev.knl.im/konobot/api/data/'+str(randommob['id'])+'.jpg')
                embed.add_field(name="Nom:", value=randommob['name'], inline=True)
                embed.add_field(name="Niveau:", value=randommob['level'], inline=True)
                embed.add_field(name="XP:", value=xpbase, inline=True)
                embed.add_field(name="HP:", value=randommob['hp'], inline=True)
                embed.add_field(name="Dégats:", value=randommob['damage'], inline=True)
                embed.add_field(name="Rareté:", value=randommob['rarity'], inline=True)
                embed.add_field(name="Description:", value=randommob['description'], inline=True)
                await ctx.send(content=f"Un **{randommob['name']}** sauvage apparait !", embed=embed)
        except Exception as e:
            return await ctx.send(f"```\n{e}```")#

    @rpg.command()
    @commands.guild_only()
    async def iteminfo(self, ctx, itemid):
        """ Get informations about an item """
        try:
            itemurl = 'http://dev.knl.im/konobot/api/index.php?call=getItem&id='+itemid
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(itemurl)
                response = await raw_response.text()
                response = json.loads(response)
                embed = discord.Embed()
                iconurl='http://dev.knl.im/konobot/api/data/icons/'+response[0]['item_icon']
                print(iconurl)
                iquality = response[0]['item_quality']
                print(iquality)
                if iquality == '1':
                    icolor=discord.Color.from_rgb(157,157,157)
                elif iquality == '2':
                    icolor=discord.Color.from_rgb(255,255,255)
                elif iquality == '3':
                    icolor=discord.Color.from_rgb(0,112,221)
                elif iquality == '4':
                    icolor=discord.Color.from_rgb(163,53,238)
                elif iquality == '5':
                    icolor=discord.Color.from_rgb(255,128,0)

                embed = discord.Embed(colour=icolor)
                embed.set_thumbnail(url=iconurl)
                embed.add_field(name="Nom:", value=response[0]['item_name'], inline=True)
                embed.add_field(name="Description:", value=response[0]['description'], inline=True)
                await ctx.send(content=f"Informations sur l'objet:", embed=embed)
        except Exception as e:
            return await ctx.send(f"```\n{e}```")


    @rpg.command()
    @commands.guild_only()
    async def inventory(self, ctx):
        """ Get user inventory """
        try:
            await ctx.message.add_reaction('⚔')
            itemurl = 'http://dev.knl.im/konobot/api/index.php?call=getUserInventory&account='+str(ctx.message.author.id)
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(itemurl)
                response = await raw_response.text()
                response = json.loads(response)
                await ctx.message.author.send(f"Inventaire: ")
                for f in response:
                    iquality = f['item_quality']
                    string = str(f['item_name'])+' x'+str(f['item_quantity'])
                    if iquality == '1':
                        icolor=discord.Color.from_rgb(157,157,157)
                    elif iquality == '2':
                        icolor=discord.Color.from_rgb(255,255,255)
                    elif iquality == '3':
                        icolor=discord.Color.from_rgb(0,112,221)
                    elif iquality == '4':
                        icolor=discord.Color.from_rgb(163,53,238)
                    elif iquality == '5':
                        icolor=discord.Color.from_rgb(255,128,0)
                    iconurl='http://dev.knl.im/konobot/api/data/icons/'+f['item_icon']
                    embed = discord.Embed(colour=icolor)
                    embed.set_thumbnail(url=iconurl)
                    embed.add_field(name="Nom:", value=f['item_name'], inline=True)
                    embed.add_field(name="Quantité:", value=f['item_quantity'], inline=True)
                    embed.add_field(name="Description:", value=f['description'], inline=True)
                    await ctx.message.author.send(content=f"", embed=embed)

        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def stopit(self, ctx):
        """ kill while"""
        try:
            RPG.dabug = False
        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @rpg.command()
    @commands.guild_only()
    async def joinfight(self, ctx):
        """ join a lobby"""
        try:
            go =  await RPG.joinedfight(self, ctx.message.author.name, ctx.message.author.id)
        except Exception as e:
            return await ctx.send(f"```\n{e}```")


    @staticmethod
    async def joinedfight(self, authorname, authorid):
        channel = self.bot.get_channel(543398038220177429)
        charinfos = await RPG.get_tot_char_info(authorid)
        hp = charinfos[3]
        if RPG.activemob == 0:
            await channel.send(f"No mob currently active")
            return
        if RPG.lobby_slots == 0:
            return await channel.send(f"```\n Fight is full```")
        elif any(authorname in i for i in RPG.lobby_players):
            return await channel.send(f"```\n You're already part of this shit```")
        else:
            couple = [authorname,authorid,hp]
            RPG.lobby_players.append(couple)
            print(RPG.lobby_players)
            await channel.send(f"```\n Members of the fight : {RPG.lobby_players}```")
            RPG.lobby_slots -= 1
            #print(RPG.lobby_slots)
            await channel.send(f"```\n slots remaining : {RPG.lobby_slots}```")


#############################################################################################################################################################################################################
#
#     SETUP
#
#############################################################################################################################################################################################################

def setup(bot):
    bot.add_cog(RPG(bot))
