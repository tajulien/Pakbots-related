import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from othersfuncs import aplatliste

testlist = [i for i in range(1,519)]
# print(testlist)
dftest = pd.DataFrame(testlist)
# print(dftest)
testlist2 = testlist*40
dftest2 = pd.DataFrame(testlist2)




def macd(df):

    exp1 = df.ewm(span=12, adjust=False).mean()
    # print(exp1)
    exp2 = df.ewm(span=26, adjust=False).mean()
    macdvalue = exp1 - exp2
    signal = macdvalue.ewm(span=9, adjust=False).mean()
    return macdvalue,signal

result = list((macd(dftest)))
valeursmacd = aplatliste(result[0].values.tolist())
valeurssignal = aplatliste(result[1].values.tolist())
#print(valeursmacd,":\n",valeurssignal)

def macddeparcours(df,numberdata,numberaction):
    return aplatliste([macd(df[0+k*numberdata:(k+1)*numberdata]) for k in range(0,numberaction)])

# result2 = list(macddeparcours(dftest2,20720,40))
# valeurmacdparcour = aplatliste(result2[0].values.tolist())
# print("la fonction renvoie un liste de dimension",len(valeurmacdparcour),":\n et de valeurs :\n",valeurmacdparcour),
