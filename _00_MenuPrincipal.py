'''importation des modules natifs usuels'''
import os

'module personnel'
from _02_Classes import Choix
# modules d'implementation d'une GUI
# from GUI._9_initOBJET import InitObjetsGraphiques
# from GUI._1_MenuPrincipal import MenuPrincipalGUI


class MenuPrincipal:
    def __init__(self):

        self.choix = Choix("", "#Crypto>",['M','a','b','c','d','e'], True, False)


    def initChoix(self):

        choix = self.choix.boucleDeChoix()
        self.choix.question = open("Menu.txt", 'r').read()  # à la reprise on ne veut plus la présentation mais juste le menu
        if choix == "a":
            return 'TaperEncrypter'

        elif choix == "b":
            return 'CrypterUnFichier'

        elif choix == "c":
            return 'CrypterUnDossier'

        elif choix == "d":

            return 'DecrypterUnFichier'

        elif choix == "e":
            return 'DecrypterUnDossier'

        elif choix == 'M':
            return "LancerCryptoMail"

        elif not choix == False:
            return 'QUITTER'

        else:
            return "Menu"

