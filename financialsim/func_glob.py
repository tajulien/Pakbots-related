from financialsim import matrices_vierges
from financialsim.chargefon import Chargesfonc
from financialsim.construction import Construction
from financialsim.fonctionnement import Fonctionnement
from financialsim.commercialisation import Commercialisation


def index_2d(my_List, v):
    for i, x in enumerate(my_List):
        if v in x:
            return i, x.index(v)


def liste_update_vierge_chargefonc():
    i = 0
    env = {}
    for elt in matrices_vierges.attri_globalvierge_chargesfon:
        env[i] = {"id": elt[0], "name": elt[1],
                  "coeff": elt[2], "prixht": elt[3],
                  "tva": elt[4], "prixttc": elt[5], "used": elt[6]}
        i += 1
    Chargesfonc.update_json(env, 'attribs')


def liste_update_vierge_const():
    i = 0
    env = {}
    for elt in matrices_vierges.attri_globalvierge_const:
        env[i] = {"id": elt[0], "name": elt[1],
                  "coeff": elt[2], "prixht": elt[3],
                  "tva": elt[4], "prixttc": elt[5], "used": elt[6]}
        i += 1
    Construction.update_json(env, 'attribs')


def liste_update_vierge_fonct():
    i = 0
    env = {}
    for elt in matrices_vierges.attri_globalvierge_fonct:
        env[i] = {"id": elt[0], "name": elt[1],
                  "coeff": elt[2], "prixht": elt[3],
                  "tva": elt[4], "prixttc": elt[5], "used": elt[6]}
        i += 1
    Fonctionnement.update_json(env, 'attribs')


def liste_update_vierge_commerce():
    i = 0
    env = {}
    for elt in matrices_vierges.attri_globalvierge_commerc:
        env[i] = {"id": elt[0], "name": elt[1],
                  "coeff": elt[2], "prixht": elt[3],
                  "tva": elt[4], "prixttc": elt[5], "used": elt[6]}
        i += 1
    Commercialisation.update_json(env, 'attribs')
