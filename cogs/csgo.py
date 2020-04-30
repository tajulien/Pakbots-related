import re
import requests

from bs4 import BeautifulSoup
from discord.ext import commands
from utils import default


class csgo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    async def get_parsed_page(self, url):
        headers = {
            "referer": "https://www.hltv.org/stats",
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0)"
        }
        return BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

    @commands.group()
    async def csgo(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @csgo.command()
    async def top5(self, ctx):
        """ WIP """
        try:
            home = await self.get_parsed_page("http://hltv.org/")
            count = 0
            teams = []
            for team in home.find_all("div", {"class": ["col-box rank"], }):
                count += 1
                teamname = team.text[3:]
                teams.append(teamname)
            return await ctx.send(f"```\n{teams}```")

        except Exception as e:
            return await ctx.send(f"```\n{e}```")

    @csgo.command()
    async def matches(self, ctx):
        """ WIP """
        try:
            matches = await self.get_parsed_page("http://www.hltv.org/matches/")
            matches_list = []
            upcomingmatches = matches.find("div", {"class": "upcoming-matches"})

            matches_formatted=''

            matchdays = upcomingmatches.find_all("div", {"class": "match-day"})

            for match in matchdays:
                matchDetails = match.find_all("table", {"class": "table"})

                for getMatch in matchDetails:
                    matchObj = {}

                matchObj['date'] = match.find("span", {"class": "standard-headline"}).text.encode('utf8')
                matchObj['time'] = getMatch.find("td", {"class": "time"}).text.encode('utf8').lstrip().rstrip()

                if (getMatch.find("td", {"class": "placeholder-text-cell"})):
                    matchObj['event'] = getMatch.find("td", {"class": "placeholder-text-cell"}).text.encode('utf8')
                elif (getMatch.find("td", {"class": "event"})):
                    matchObj['event'] = getMatch.find("td", {"class": "event"}).text.encode('utf8')
                else:
                    matchObj['event'] = None

                if (getMatch.find_all("td", {"class": "team-cell"})):
                    matchObj['team1'] = getMatch.find_all("td", {"class": "team-cell"})[0].text.encode('utf8').lstrip().rstrip()
                    matchObj['team2'] = getMatch.find_all("td", {"class": "team-cell"})[1].text.encode('utf8').lstrip().rstrip()
                    regex = r"\/matches\/([\d]+)/"
                    matchstr = match.find("a", {"class": "upcoming-match"})['href']
                    matches = re.search(regex, matchstr)
                    matchObj['matchID'] = matches[1]
                    mtime = matchObj['time'].decode().replace('b\'', '')
                    mdate = matchObj['date'].decode().replace('b\'', '')

                    team1 = matchObj['team1'].decode().replace('b\'', '')
                    team2 = matchObj['team2'].decode().replace('b\'', '')
                    event = matchObj['event'].decode().replace('b\'', '')
                    matches_formatted=matches_formatted+f"{matchObj['matchID']} | {mdate} {mtime} : {team1} VS {team2} Tournoi: {event}\n"
                else:
                    matchObj['team1'] = None
                    matchObj['team2'] = None
                    matchObj['matchID'] = None

                matches_list.append(matchObj)

            return await ctx.send(f"```\n{matches_formatted}```")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")


def setup(bot):
    bot.add_cog(csgo(bot))
