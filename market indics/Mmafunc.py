import numpy as np

def mmanod(list, Ndays) :
    return [ 0*bj for bj in range(0,Ndays)]+[(np.sum(list[(jour-Ndays+1):jour+1]))/len(list[(jour-Ndays+1):jour+1]) for jour in range (Ndays-1, len(list)-1)]
    controle = len(list)
    #print("calul de la MMA sur",len(resu),"jours, [controle :",controle,"]")

def mmadeparcours(list2, Ndays,numberdata,numberaction):
    return [mmanod(list2[0+k*numberdata:(k+1)*numberdata],Ndays) for k in range(0,numberaction)]
