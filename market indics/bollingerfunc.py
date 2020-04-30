import numpy as np
import pandas as pd
from othersfuncs import aplatliste

def bollinger_bands(coursfermeture,Ndays, num_of_std):

    rolling_mean = coursfermeture.rolling(Ndays).mean()
    rolling_std2  = coursfermeture.rolling(Ndays).std()
    upper_band2 = rolling_mean + (rolling_std2*num_of_std)
    lower_band2 = rolling_mean - (rolling_std2*num_of_std)
    l_lower_band = aplatliste(lower_band2.values.tolist())
    l_upper_band = aplatliste(upper_band2.values.tolist())
    l_rolling_std = aplatliste(rolling_std2.values.tolist())
    return l_rolling_std,l_upper_band, l_lower_band

def upper_bands(coursfermeture,Ndays, num_of_std):

    rolling_mean = coursfermeture.rolling(Ndays).mean()
    rolling_std  = coursfermeture.rolling(Ndays).std()
    upper_band2 = rolling_mean + (rolling_std*num_of_std)
    lower_band2 = rolling_mean - (rolling_std*num_of_std)
    l_upper_band = upper_band2.values.tolist()
    return l_upper_band

def upperbollingerdeparcours(list2, Ndays,num_of_std,numberdata,numberaction):
    return aplatliste([upper_bands(list2[0+k*numberdata:(k+1)*numberdata],Ndays, num_of_std) for k in range(0,numberaction)])

def lower_bands(coursfermeture,Ndays, num_of_std):

    rolling_mean = coursfermeture.rolling(Ndays).mean()
    rolling_std  = coursfermeture.rolling(Ndays).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band2 = rolling_mean - (rolling_std*num_of_std)
    l_lower_band = lower_band2.values.tolist()
    return l_lower_band

def lowerbollingerdeparcours(list2, Ndays,num_of_std,numberdata,numberaction):
    return aplatliste([lower_bands(list2[0+k*numberdata:(k+1)*numberdata],Ndays, num_of_std) for k in range(0,numberaction)])

# testlist = [i for i in range(1,519)]
# datalist = pd.DataFrame(testlist)
# print("la datalist est :\n",datalist)
# print("les bandes de bolli pour :\n",bollinger_bands(datalist,20,2))

# testlist2 = testlist*40
# datalist2 = pd.DataFrame(testlist2)
# print("la datalist complète de test est :\n",datalist2)
# print("sorties du lowerbollinger de parcours :\n",lowerbollingerdeparcours(datalist2,20,2,518,40))
# print("sorties du upperbollinger de parcours :\n",upperbollingerdeparcours(datalist2,20,2,518,40))
