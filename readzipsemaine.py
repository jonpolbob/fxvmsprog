#!/usr/bin/env python
# -*- coding: utf-8 -*-

# readsemcsv
# utilisatires pour lire une semain dans les csv de mois

# le fichier zip doit s'appeler BIDAAABBBmmyy

# la fonction presentzip(paire,mois,year) dit si le zip est dispo
# la fonction creenomzip(paire mois year) renvoie la liste des zip correspondant a la semaine


import zipfile
import datesemainutils

# renvoie la liste des zip a utiliser pour pouvoir charger cette semaine
# accompagnée de la date (jour, mois annee du premier jour alire dans ce fichier
#le nom du zip est yyymmpaire
def creenomzip(paire, semaine, annee):
    listemois = datesemainutils.getlistemois(semaine,annee)
    listezips = []
    for mois in listemois:
        zipname = "%04d%02d%s.zip" % (mois[1],mois[2],paire)
        jourdumois = mois[0]
        listezips.append([jourdumois,mois[1],mois[2],zipname])
    return listezips

# import zipfile

# rep ou sont les donnees
datarep = "c:\\tmp"


################## readlines ####################
# : lecture de qq jous dans un fichier mois
# lit nbjours dans un fichier csv contenant le mois pour une paire
# a partir du jour du mois =  jour
# ligne par ligne
# renvoie le nb de minutes entre la ligne et datedeb
# yield la date et la valeur
# renvoie le nb de jours lus quand le balayage est fini (None, nbjourslus)
# charge dans le tableau le nombre de jourd nbjours a partir du jour jour
def readlines(datedeb, nbjours, jour, nomzip, paire):
    # on lit le zip sur le disque
    fh1 = open(nomzip, 'rb')
    z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
    nbjourslus = 0
    lstday = -1
    with z1.open(paire + ".csv", mode='r') as read1:
        for laligne in read1:
            numsample, date, begin = datesemainutils.decodelinemois(laligne)  # lecture de la ligne
            if (date.month != datedeb.month):  # bug : parfois le 1 er jour du mois est ds le mois prec
                continue
            if lstday != date.day:  # la date a changé
                if nbjourslus != 0:  # on a commence a lire des jours
                    nbjourslus = nbjourslus + 1  # un nouveau jour
                else:
                    print("\rjour", date.day, )  # on n'a pas commence a lire des jours : on saute

            lstday = date.day

            if date.day == jour:  # on a atteint le jour recherche
                nbjourslus = 1  # on commence

            if nbjourslus > nbjours:  # on a lu le bon nombre de jours
                break  # fin du for

            if nbjourslus != 0:
                delta = date - datedeb  # delta depuis debut semaine
                yield nbjourslus, date, int(delta.total_seconds() / 60), begin  # date, valeur debut

    fh1.close()

import os.path

#genere un tableau contenant toutes les donnees pour cette paire et cette semaine
def generesemaine(paire,semaine, annee):
    ok=False
    listezip = creenomzip(paire, semaine, annee) #liste jour du mois, mois, annee, nomzip
    #regarde si les zip existent
    for nomfich in listezip:
        nomfich = datarep+"\\"+nomfich[3]
        print(nomfich)
        if os.path.isfile(nomfich):
            ok = True
        else:
            readwebfile(paire,nomfich[1],nomfich[2])






######
#pour test
if __name__=="__main__":
    generesemaine("aaabbb",1,2013)
    #laliste = creenomzip("aaabbb",1,2013)
    #print (laliste)
