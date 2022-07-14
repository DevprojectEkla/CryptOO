"""importation des modules natifs usuels"""
import os
import sys
import threading
import time

'modules personnels'
from _00_MenuPrincipal import MenuPrincipal
from _04_CrypterUnFichier import CrypterUnFichier
from _04_CrypterUnDossier import CrypterUnDossier
from _05_DecrypterUnFichier import DecrypterUnFichier
from _05_DecrypterUnDossier import DecrypterUnDossier
from _06_TaperDuTexteEtCrypter import TaperEtCrypter
from _01_AlgoG import AlgoG
from CryptoMail import CryptoMail


class IA:
    # GUI implementation:
    # pygame.init()

    def __init__(self):
        self.taperCrypter = TaperEtCrypter()
        self.crypter = CrypterUnFichier()
        self.crypterDossier = CrypterUnDossier()
        self.decrypter = DecrypterUnFichier()
        self.decryptDossier = DecrypterUnDossier()
        self.cryptoMail = CryptoMail()
        self.menu = MenuPrincipal()
        self.algo = AlgoG()
        self.app_path = os.path.dirname(os.path.abspath("_00_IA.py"))
        # lancement de la boucle du programme
        self.choixDuModule()

    def choixDuModule(self):
        choix = "Menu"  # module interface utilisateur par défaut
        self.algo.presentation2()
        while True:
            if choix == "Menu":
                choix = self.menu.initChoix()

            elif choix == "CrypterUnFichier":
                choix = self.crypter.crypter()

            elif choix == "DecrypterUnFichier":
                choix = self.decrypter.decrypter()

            elif choix == "LancerCryptoMail":
                choix = self.cryptoMail.initMail()

            elif choix == "TaperEncrypter":
                choix = self.taperCrypter.taperCrypter()

            elif choix == "CrypterUnDossier":
                choix = self.crypterDossier.crypterDossier()

            elif choix == "DecrypterUnDossier":
                choix = self.decryptDossier.decrypterDossier()

            elif choix == "QUITTER":
                print("Fin du programme !")
                AlgoG.goodbye()


if __name__ == "__main__":
    ia = IA()
