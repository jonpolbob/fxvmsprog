#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  utilistaires lisant les datas sur free-forex,
# a  la difference de clicselenioum, on ne lit que une paire
# pour un mois et on le dezippe dans un sous dossier
# si le fichier existe deja : on ne le relit pas

#donc in fine on renvoie le nom d'un csv qui contient un mois de cette paire.

#penser a mettre chromedriver.exe dans le path

__author__ = 'cagibi'

import selenium
import os
import zipfile
import ReadWebWindows


#############################################################"
#charge un fichier de paires pour un mois et une annee donnee
#si le fichier est deja charge : on ne le recharge pas
#renvoie le nom du fichier csv extrait
#paire mois et an sont  des chaines correctement formatees
#mois et an sont des nombres
#paire est en majuscules
#############################################################"
def loadpairemoisan(paire,mois,an):
    #nom du fichier csv sur tmp
    nomcsv = "%04d%02d%s" %(int(an),int(mois),paire)
    totest = "c:\\tmp\\" + nomcsv + ".csv"
    if os.path.exists(totest):
        return "", totest  #premier argument = vide

    URL = "http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/"+paire+"/"+an+"/"+mois+"/"
    FileName = "HISTDATA_COM_NT_"+paire+"_T_BID_"+an+mois+".zip"
    RealFileName = "HISTDATA_COM_NT_"+paire+"_T_BID"+an+mois+".zip"

    driver.get(URL)

    toclic = driver.find_element_by_link_text(FileName) #le nom de fichier est l'objet clicable
    notseen = True
    while (notseen):
        notseen =False
        try:
           toclic.click()
        except selenium.common.exceptions.ElementNotVisibleException :
            notseen = True
        except selenium.common.exceptions.WebDriverException :
            notseen = True


    pathdownload = "c:\\tmp\\"+RealFileName #attention le nom est different entre le zip et le lien clic

    #ici on attend la fin du telechargement
    notfound = True
    while (notfound):
        if os.path.exists(pathdownload):
            notfound = False

    print("found")
    # on cherche dans le zip un fichier csv
    #on le decompress dans tmp
    #puis on enleve le zip
    notok = True

    while notok:
        try:
            with zipfile.ZipFile(pathdownload, 'r') as zf:
                print (zf.filelist)
                for i in zf.filelist:
                    if i.filename.find(".csv") != -1 :
                        print("extract dans c:\\tmp : ",i.filename)
                        newpath = zf.extract(i,path="c:/tmp")
                        print('new path ',newpath, 'rename to',"c:\\tmp\\"+nomcsv+".csv")
                        os.rename(newpath,totest)
                        notok = False
                    else:
                        print("jump ",i.filename)

            zf.close()

        except PermissionError:
            #zf.close()
            print("perm error")
            if os.path.exists("c:\\tmp\\" + nomcsv + ".csv"):
                os.remove("c:\\tmp\\" + nomcsv + ".csv")
            print('redo')

    print('remmove',pathdownload)
    os.remove(pathdownload)  #provoque une plante
    print ("ok")
    return newpath,"c:\\tmp\\"+nomcsv+".csv"


######################################################"""
#ici le main
######################################################"""

#antidemarrage en librrairie
if __name__ == "__main__":
    # personalisation des options(rep de download et adresse vers chromdriver
    driver = ReadWebWindows.initwebwindows()
    loadpairemoisan("EURUSD","01","2014")
    driver.stop()

