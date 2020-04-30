from bs4 import BeautifulSoup
import requests
import time
import datetime
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import tokened

def get_parsed_page(url):
    headers = {
        "referer": "https://www.abcbourse.com/marches/",
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")


datas = []


def get_result():
    home = get_parsed_page("https://www.abcbourse.com/marches/indice_cac40.aspx")
    # print(home)
    dateparse = str(home.find("div", class_="flm pad5"))
    dateparse = dateparse[dateparse.find(">"):]
    timeparse = dateparse[dateparse.find("-"):]
    timeparse = timeparse[:timeparse.find("<")]
    timeparse = timeparse[2:].rstrip()
    dateparse = dateparse[:dateparse.find(" ")]
    dateparse = dateparse[1:]
    cotations = str(home.find("tbody"))
    pos, pos2 = -1, -1
    t = 0
    while True:
        pos = cotations.find("data-name=", pos + 1)
        pos2 = cotations.find("data-name", pos2 + 1)
        if pos == -1 or t == 20:
            break
        action_abbr = cotations[cotations.find("data-name", pos):]
        action_abbr = action_abbr[:action_abbr.find(">")]
        action_abbr = action_abbr[11:-1]
        action_name = cotations[cotations.find("href", pos):]
        action_name = action_name[action_name.find(">"):]
        action_name = action_name[:action_name.find("<")]
        action_name = action_name[1:]
        action_url = cotations[cotations.find("href", pos):]
        action_url = action_url[:action_url.find(">")]
        action_url = "https://www.abcbourse.com" + action_url[6:-1]
        action_grid = cotations[cotations.find("<td>", pos2):]
        action_open = action_grid[4:].replace(',', '.')
        action_high = action_open[action_open.find("<td>"):]
        action_high = action_high[4:]
        action_low = action_high[action_high.find("<td>"):]
        action_low = action_low[4:]
        action_volume = action_low[action_low.find("<td>"):]
        action_volume = action_volume[4:]
        action_volume = int(action_volume[:action_volume.find("<")])
        action_ystrd = action_low[action_low.find("<td>"):]
        action_ystrd = action_ystrd[4:]
        action_ystrd = action_ystrd[action_ystrd.find("<td>"):]
        action_ystrd = action_ystrd[4:]
        action_value = action_ystrd[action_ystrd.find("bold"):]
        action_value = action_value[:action_value.find("<")]
        action_value = action_value[6:]
        action_var = action_ystrd[action_ystrd.find("quote"):]
        action_var = action_var[action_var.find(">"):]
        action_var = action_var[:action_var.find("<")]
        action_var = action_var[1:]
        action_ystrd = action_ystrd[:action_ystrd.find("<")]
        action_low = action_low[:action_low.find("<")]
        action_low = float(action_low)
        action_high = action_high[:action_high.find("<")]
        action_high = float(action_high)
        action_open = action_open[:action_open.find("<")]
        action_open = float(action_open)
        isin_code = get_ISIN(action_abbr)
        datas.append(
            [dateparse, timeparse, action_abbr, action_name, isin_code[0], action_url, action_open, action_high,
             action_low, action_ystrd, action_value, action_var, action_volume])
    return datas


def get_ISIN(actions):
    result = get_parsed_page("https://www.abcbourse.com/cotation/" + actions)
    result2 = str(result.findAll("span", class_="co_g2"))
    result2 = result2[result2.find("</span>"):]
    result2 = result2[result2.find("-"):]
    result2 = result2[2:]
    result2 = result2[:result2.find("-")]
    result2 = result2.rstrip()
    # print(result2)
    return [result2, actions]


def index_2d(my_List, v):
    for i, x in enumerate(my_List):
        if v in x:
            return (i, x.index(v))


histo = []
line_count = 0
totaladd = 0


def addsql(a, b, c, d, e, f, g, h):
    global totaladd
    try:
        connection = mysql.connector.connect(host=tokened.bddurl,
                                             database='market_datas',
                                             user=tokened.bdduser,
                                             password=tokened.bddpass)
        records_to_insert = [(a, b, c, d, e, f, g, h, a, b, c, d, e, f, g, h)]
        sql_insert_query = """ INSERT INTO market_histo (Prim_key, act_name, act_abbr, act_isin, act_date, act_open, act_close, act_volume) 
	                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Prim_key = %s, act_name=%s, act_abbr=%s, act_isin=%s, act_date=%s, act_open=%s, act_close=%s, act_volume=%s
	                        """""
        # sql_insert_query = """ INSERT INTO getscrap (Dategi, Country, League, ComptID, GameID, ID1, Name1, ID2,
        # Name2, Hda, Probability,  Odd,  MatchPlayed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE
        # KEY UPDATE GameID = %s"""
        cursor = connection.cursor(prepared=True)
        result = cursor.executemany(sql_insert_query, records_to_insert)
        connection.commit()
        totaladd += cursor.rowcount
        print(cursor.rowcount, "Record inserted successfully into market_histo table")
    except mysql.connector.Error as error:
        print("Failed inserting record into market_histo table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("connection is closed")
        print(str(totaladd) + " Record inserted successfully into market_histo table")


def update_everyday():
    if datetime.today().weekday() == 5 or datetime.today().weekday() == 6:
        print("it's weekend we are fucked")
        print(datetime.today())
        return
    yes = get_result()
    update_date = ""
    for element in yes:
        element[0] = str(element[0])[:-2]
        element[0] = element[0][6:] + "-" + element[0][3:5] + "-" + element[0][:2]
        primary_keys = str(element[4]) + str(element[2]) + str(element[0]).replace('-', '')
        addsql(primary_keys, element[3], element[2], element[4], element[0], element[6], element[10], element[12])
        update_date = element[0]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'{update_date} - {current_time} datas updated')


# print(datetime.today().weekday())
while True:
    update_everyday()
    time.sleep(86400)
