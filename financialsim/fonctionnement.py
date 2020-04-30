import json
import os
from financialsim import matrices_vierges
from financialsim import func_glob

class Fonctionnement:
    attri_global, attri_temps = [], []

    def __init__(self):
        #func_glob.liste_update_vierge_fonct()
        Fonctionnement.read_json()
        Fonctionnement.calculs()
        self.attri_used = Fonctionnement.attri_used()

    @staticmethod
    def calculs():
        Fonctionnement.calcul_prixht()
        Fonctionnement.calcul_tva()
        Fonctionnement.total_tva()

    @staticmethod
    def calcul_prixht():
        for elt in Fonctionnement.attri_global:
            if elt[0] == '100' and any('Notaire' in sublist for sublist in Fonctionnement.attri_global):
                Fonctionnement.prixttcDC = elt[5]
            if elt[1] == 'Notaire':
                elt[3] = int(Fonctionnement.prixttcDC * elt[2])

    @staticmethod
    def total_tva():
        for elt in Fonctionnement.attri_global:
            elt[5] = elt[4] + elt[3]

    @staticmethod
    def calcul_tva():
        for elt in Fonctionnement.attri_global:
            if elt[1] == 'Notaire':
                elt[4] = int(elt[3] * 0.2 * 0.85)
            elif elt[0] == '135' or elt[0] == '115':
                elt[4] = 0
            else:
                elt[4] = int(elt[3] * 0.2)

    @staticmethod
    def attri_used():
        return [elt for elt in Fonctionnement.attri_global if (elt[6] == 1)]

    @staticmethod
    def read_json():
        with open(os.getcwd() + "\\datas\\datas.json", 'r') as json_file:
            datas_cons = json.load(json_file)
            for p in datas_cons['financialsim']['fonctionnement']['attribs']:
                for elt, value in datas_cons['financialsim']['fonctionnement']['attribs'][p].items():
                    Fonctionnement.attri_temps.append(value)
                Fonctionnement.attri_global.append(Fonctionnement.attri_temps)
                Fonctionnement.attri_temps = []
        json_file.close()

    @staticmethod
    def update_json(env, entry):
        with open(os.getcwd() + "\\datas\\datas.json", 'r+') as json_file:
            yet = json.load(json_file)
            yet['financialsim']['fonctionnement'][entry] = env
            with open(os.getcwd() + "\\datas\\datas.json", 'w+') as json_file:
                json.dump(yet, json_file)

    @staticmethod
    def liste_update(liste, entry):
        i = 0
        env = {}
        for elt in liste:
            if entry == 'attribs':
                env[i] = {"id": elt[0], "name": elt[1],
                          "coeff": elt[2], "prixht": elt[3],
                          "tva": elt[4], "prixttc": elt[5], "used": elt[6]}
            if entry == 'summary':
                env[i] = {"subtotal_ht": elt[0], "subtotal_tva": elt[1],
                          "subtotal_ttc": elt[2]}
            i += 1
        Fonctionnement.update_json(env, entry)
        Fonctionnement.attri_global = []


def main():
    Fonctionnement()
    #print(Fonctionnement.attri_global[0])


if __name__ == "__main__":
    main()