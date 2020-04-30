import mysql.connector
import pandas as pd
import sys, os
import time
from datetime import datetime, date
import math

from othersfuncs import aplatliste
from Mmafunc import mmadeparcours,mmanod
from bollingerfunc import upperbollingerdeparcours, lowerbollingerdeparcours,upper_bands,lower_bands
from macdfunc import macddeparcours,macd
import tokened


sys.path.append(os.getcwd()+'/homefinancialtools/')
totaladd = 0
today = date.today()


def addsql(a, b, c, d, e, f, g, h , i , j , k , l , m):
    global totaladd
    try:
        connection = mysql.connector.connect(host=tokened.bddurl,
                                             database='market_datas',
                                             user=tokened.bdduser,
                                             password=tokened.bddpass)
        records_to_insert = [(a, b, c, d, e, f, g, h , i , j , k , l , m ,a, b, c, d, e, f, g, h , i , j , k , l , m)]
        sql_insert_query = """ INSERT INTO market_indics (Prim_key, act_name, act_isin, date, mma10, mma20, mma50, mma100, mma200, macd, bollinger_inf, bollinger_sup, signaleuh) 
	                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Prim_key = %s, act_name=%s, act_isin=%s, date=%s, mma10=%s, mma20=%s, mma50=%s, mma100=%s,mma200=%s, macd=%s, bollinger_inf=%s, bollinger_sup=%s, signaleuh=%s
	                        """""
        cursor = connection.cursor(prepared=True)
        result = cursor.executemany(sql_insert_query, records_to_insert)
        connection.commit()
        totaladd += cursor.rowcount
        print(cursor.rowcount, "Record inserted successfully into market_indics table")
    except mysql.connector.Error as error:
        print("Failed inserting record into market_indics table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("connection is closed")
        print(str(totaladd) + " Record inserted successfully into market_indics table")

def starting():
    datejour = today.strftime("%y/%m/%d")
    datejour = datejour.replace('/', '-')
    print(datejour)
    connection = mysql.connector.connect(host=tokened.bddurl,
                                         database='market_datas',
                                         user=tokened.bdduser,
                                         password=tokened.bddpass)

    # on récupère la table qui contient les données sources
    sql_select_Query = "SELECT * FROM `market_histo`" # WHERE `act_date` ='%s'" % datejour
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    #print(records)
    if records == []:
        print('Nothing today')
    else:
        # on crée la dataframe correspondante
        dfi = pd.DataFrame(records,columns =["Prim_key","Nom_Action","Code_ABBR","Code_ISIN","Date","Ouverture","Fermeture","Volume"])
        nombredeligne = dfi.shape[0]
        Prim_key = dfi["Prim_key"].tolist()
        act_name= dfi["Nom_Action"].tolist()
        act_isin = dfi["Code_ISIN"].tolist()
        date = dfi["Date"].tolist()

        # on récupère la liste des actions concernées par l'analyse
        Actionlist = dfi["Nom_Action"].unique().tolist()
        print(len(Actionlist)," actions récupérées, ce sont \n",Actionlist)
        numberaction = len(Actionlist)
        numberdataperaction = int(int(nombredeligne) / int(numberaction))
        print("le nombre de cotation pris en compte par action est de :",numberdataperaction)

        closings = dfi["Fermeture"]
        mma10, mma20, mma50, mma100, mma200, macd, signal, sup_bollinger, inf_bollinger = [], [], [], [], [], [], [], [], []

        mma10 = aplatliste(mmadeparcours(closings,10,numberdataperaction,numberaction))
        mma20 = aplatliste(mmadeparcours(closings,20,numberdataperaction,numberaction))
        mma50 = aplatliste(mmadeparcours(closings,50,numberdataperaction,numberaction))
        mma100 = aplatliste(mmadeparcours(closings,100,numberdataperaction,numberaction))
        mma200 = aplatliste(mmadeparcours(closings,200,numberdataperaction,numberaction))
        sup_bollinger = upperbollingerdeparcours(closings,20,2,numberdataperaction,numberaction)
        inf_bollinger = lowerbollingerdeparcours(closings,20,2,numberdataperaction,numberaction)
        fonctionmacd = macddeparcours(closings,nombredeligne,numberaction)
        macd = aplatliste(fonctionmacd[0])
        signal = aplatliste(fonctionmacd[1])
        # print("macd", ":\n",len(macd))
        # print("signal", ":\n",len(signal))

        #print(inf_bollinger[0])

        sup_bollinger = [0 if math.isnan(x) else x for x in sup_bollinger]
        inf_bollinger = [0 if math.isnan(x) else x for x in inf_bollinger]
        for i in range(0, nombredeligne-1):
            if sup_bollinger[i] != "None":
                sup_bollinger[i] = round(sup_bollinger[i], 3)
            if inf_bollinger[i] != "None":
                inf_bollinger[i] = round(inf_bollinger[i], 3)
            addsql(Prim_key[i], act_name[i], act_isin[i], date[i], round(mma10[i], 3), round(mma20[i], 3),
                   round(mma50[i], 3), round(mma100[i], 3), round(mma200[i], 3), round(macd[i], 3),
                   inf_bollinger[i], sup_bollinger[i], round(signal[i], 3))
            print((i + 1), " de fait")
        print(str(totaladd) + " Records inserted successfully into market_indics table")

while True:
    starting()
    time.sleep(86400)
