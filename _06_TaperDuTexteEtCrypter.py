import os
import sys
import time
from pathlib import Path

from _01_AlgoG import AlgoG
from _02_Classes import Choix
from _02_File import File
from _02_Choix import ChoixFichier
from _03_ChargerUneClef_V2 import ChargerUneClef


class TaperEtCrypter:
    def __init__(self):
        self.app_path = None
        self.content = None
        self.text = None
        self.tempFile = None
        self.buffer = None
        self.entry = None  # ici mettre notre objet Choix()
        self.key = None
        self.algo = None
        self.ask = None
        self.save = None
        self.file = None

        self.initVariables()

    def initVariables(self):
        self.app_path = Path(os.path.dirname(os.path.abspath("__00__IA.py")))
        self.text = Choix("entrer votre texte", check=False)
        self.tempFile = File('TempFile')
        self.file = File
        self.save = ChoixFichier(ext=".txt")
        self.algo = AlgoG()
        self.content = ""
        self.buffer = ""
        self.ask = Choix("\n\tdo you want to save it in a particular .txt file ?", "#Crypto>", ['y', 'n'])

    def initKey(self):
        '''ici on appelle inévitablement un sous-module qui permet de charger la clé de cryptage
        Attention: on ne veut pas initialiser cette variable en même temps que l'instanciation de la classe mais
        seulement au moment ou l'on appelle la méthode crypter sur un objet de la classe.'''
        getkey = ChargerUneClef().choiceKey()  # cette méthode permet de charger une clé, elle renvoit un objet Key()
        self.key = getkey  # temporairement on associe l'objet Key à cette variable
        self.key.__setattr__('key', getkey.key)  # ici on fixe la valeur de l'attribut self.key de l'objet Key.
        return getkey

    def initCrypt(self):
        self.initVariables()
        self.initKey()

    def taperCrypter(self):
        """Cette fonction permet de taper directement le texte dans l'invite de commande
        avant de l'encrypter. On indique la fin du fichier par le signal chaîne vide "" en appuyant sur 'enter' """
        self.initCrypt()
        self.buffer = self.text.boucleDeChoix()
        self.tempFile.appendMode()
        self.content = self.algo.typeAndRecord(firstLine=self.buffer, file=self.tempFile)
        print(f"this is your message before encryption:{self.content}")
        time.sleep(2)
        self.content = self.algo.encryptAnyContent(self.content, self.key.key)
        print(f"\n\there is your encrypted message: {self.content}")
        self.saveInFile()
        os.chdir(self.app_path)  # on retourne dans le dossier de démarrage de l'application.
        return 'Menu'

    def saveInFile(self):
        """ Supprime le fichier temporaire créé par la fontion taperCrypter() après avoir proposé de l'enregistrer
         sous un nouveau nom."""
        save = self.ask.boucleDeChoix()
        if save:
            self.save.question = "Chosissez un nom de fichier à l'extension .txt"
            filename = self.save.validerCreationFichier()
            self.file = self.file(filename)
            self.file.overwrite = True
            self.file.writeBytes(self.content)
            self.file.closeFile()
        self.tempFile.deleteFile()


if __name__ == "__main__":
    t = TaperEtCrypter()
    t.taperCrypter()
