from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, date
import json
import os
import random

NEWSL = []
data = {'newsbourse': []}
file = open(os.getcwd()+"/cogs/newsdata/newsdata.json", "w")
# print(os.getcwd())
# print(file)
file.close()


def check_if_exist_and_add(newstitle, newsurl, timing_news_formatted):
    if any(newstitle in sublist for sublist in NEWSL):
        print(f'News {newstitle} already exist')
        return False
    d = date.today()
    d = d.strftime("%d/%m/%y")
    data['newsbourse'].append({"date": d, "time": timing_news_formatted, "title": newstitle, "url": newsurl})
    NEWSL.append([newstitle, newsurl])
    print(f'{timing_news_formatted} - News {newstitle} - {newsurl} added')
    return data



def notify_chan():
    home = get_parsed_page("https://www.boursorama.com/bourse/actualites/")
    pos, pos2 = -1, -1
    t = 0
    while True:
        timing_news = str(home.find_all(class_="c-list-news__date"))
        day = home.find_all(class_="c-list-news__content")
        day = str(day)
        pos = day.find('href=', pos + 1)
        pos2 = timing_news.find("date", pos2 + 1)
        if pos == -1 or t == 20:
            break
        t += 1
        timing_news = str(home.find_all(class_="c-list-news__date"))
        timing_news_formatted = timing_news[timing_news.find("date", pos2):]
        timing_news_formatted = timing_news_formatted[:timing_news_formatted.find("<")]
        timing_news_formatted = timing_news_formatted[6:]
        url = day[day.find("href=", pos):]
        url = url[:url.find("title")]
        title = day[day.find("title", pos):]
        title = title[:title.find(">")]
        result = check_if_exist_and_add(title[7:-1], "https://www.boursorama.com"+url[6:-2], timing_news_formatted)
    with open(os.getcwd()+"/cogs/newsdata/newsdata.json", 'w+') as json_file:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time + " data printed")
        json.dump(data, json_file)
    json_file.close()
    ## reset data json ?


def get_parsed_page(url):
    headers = {
        "referer": "https://www.boursorama.com/bourse/actualites/",
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")


while True:
    notify_chan()
    time.sleep(random.randint(600,800))
