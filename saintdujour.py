import json
import requests
from bs4 import BeautifulSoup
import time
import tokened

def send_notification_via_pushbullet(title, body):
    data_send = {"type": "note", "title": title, "body": body}

    ACCESS_TOKEN = tokened.tok
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')


def saintdujour():
    home = get_parsed_page("https://www.ephemeride.com/free/fete.jsp")
    day = home.find_all(class_="fmb")
    for value in day:
        print(value.text[:-20])
    result = value.text[13:-20]
    # print (result.capitalize())
    #return result
    send_notification_via_pushbullet(str(result.capitalize()), str(result.capitalize()))


def get_parsed_page(url):
    headers = {
        "referer": "https://www.ephemeride.com/",
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")


while True:
    saintdujour()
    time.sleep(86400)
