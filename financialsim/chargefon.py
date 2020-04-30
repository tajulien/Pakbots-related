import json
import os
# from financialsim import func_glob


class Chargesfonc:
    attri_global, attri_temps = [], []
    subtotal = []

    def __init__(self):
        # func_glob.liste_update_vierge_chargefonc()
        Chargesfonc.read_json()
        Chargesfonc.calculs()
        self.attri_used = Chargesfonc.attri_used()

    @staticmethod
    def calculs():
        Chargesfonc.calcul_prixht()
        Chargesfonc.calcul_tva()
        Chargesfonc.total_tva()
        Chargesfonc.sub_total()

    @staticmethod
    def calcul_prixht():
        for elt in Chargesfonc.attri_global:
            if elt[0] == '100' and any('Notaire' in sublist for sublist in Chargesfonc.attri_global):
                Chargesfonc.prixttcDC = elt[5]
            if elt[1] == 'Notaire':
                elt[3] = int(Chargesfonc.prixttcDC * elt[2])

    @staticmethod
    def total_tva():
        for elt in Chargesfonc.attri_global:
            elt[5] = elt[4] + elt[3]

    @staticmethod
    def calcul_tva():
        for elt in Chargesfonc.attri_global:
            if elt[1] == 'Notaire':
                elt[4] = int(elt[3] * 0.2 * 0.85)
            elif elt[0] == '135' or elt[0] == '115':
                elt[4] = 0
            else:
                elt[4] = int(elt[3] * 0.2)

    @staticmethod
    def attri_used():
        return [elt for elt in Chargesfonc.attri_global if (elt[6] == 1)]

    @staticmethod
    def read_json():
        with open(os.getcwd() + "\\datas\\datas.json", 'r') as json_file:
            datas_cons = json.load(json_file)
            for p in datas_cons['financialsim']['charges_foncieres']['attribs']:
                for elt, value in datas_cons['financialsim']['charges_foncieres']['attribs'][p].items():
                    Chargesfonc.attri_temps.append(value)
                Chargesfonc.attri_global.append(Chargesfonc.attri_temps)
                Chargesfonc.attri_temps = []
        json_file.close()

    @staticmethod
    def update_json(env, entry):
        with open(os.getcwd() + "\\datas\\datas.json", 'r+') as json_file:
            yet = json.load(json_file)
            yet['financialsim']['charges_foncieres'][entry] = env
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
        Chargesfonc.update_json(env, entry)
        Chargesfonc.attri_global = []

    @staticmethod
    def sub_total():
        subtotal_ht = 0
        subtotal_tva = 0
        subtotal_ttc = 0
        used = Chargesfonc.attri_used()
        for elt in used:
            subtotal_ht += elt[3]
            subtotal_tva += elt[4]
            subtotal_ttc += elt[5]
        Chargesfonc.subtotal = [[subtotal_ht, subtotal_tva, subtotal_ttc]]


def closing_func():
    Chargesfonc.calculs()
    print(Chargesfonc.subtotal)
    Chargesfonc.liste_update(Chargesfonc.attri_global, 'attribs')
    #Chargesfonc.liste_update(Chargesfonc.subtotal, 'summary')


def main():
    Chargesfonc()
    closing_func()

if __name__ == "__main__":
    main()
    closing_func()
