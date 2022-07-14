import os
import sys
import time

from _02_Choix import ChoixFichier, ChoixDossier
from _03_ChargerUneClef_V2 import ChargerUneClef
from _02_File import File
from _02_KeyFile import Key
from _02_Classes import *
from _01_AlgoG import AlgoG


class DecrypterUnFichier:
    '''cette classe permet de charger une clé de cryptage pour effectuer le décryptage d'un fichier.
    NB: Il faut que le fichier ait été crypté après avoir été ouvert et lu en mode 'rb' et que l'ouverture au moment
    du décryptage se fasse également en mode 'rb'. Tout cela est géré au niveau de la classe File() mais des erreurs
    Fernet peuvent se produire inexplicablement si ces étapes là ne sont pas bien suivies. '''

    def __init__(self):
        self.app_path = ""
        self.choixFichier = None
        self.key = None
        self.decryptedFile = None
        self.name = ""
        self.newname = ""
        self.path = ""
        self.algo = None
        self.initVariables()
        # self.file = File # on n'a pas forcément besoin d'instancier le fichier à decrypter avec notre classe si les
        # manipulations sur les chemins de fichier suffisent mais peut-être le faudra-t-il si on implémente File
        # dans les fonctions de cryptage de _01_AlgoG

    def initVariables(self):
        '''(re)initialisation des variables de la Classe et instanciation de ChoixFichier()
        NB: il est nécessaire de découpler initFichier de initCryptage car on veut pouvoir
        réinitialiser les variables à chaque fois avant de commencer l'opération, autrement les variables restent
        en mémoire et interfèrent avec l'opération de cryptage suivante'''
        self.app_path = Path(os.path.dirname(os.path.abspath("__00__IA.py")))
        self.choixFichier = ChoixFichier()
        self.choixFichier.question = 'Choisissez un fichier à décrypter:'
        self.decryptedFile = File
        self.name = ""
        self.newname = ""
        self.path = ""
        self.algo = AlgoG()

    def initKey(self):
        """Ici on appelle inévitablement un sous-module qui permet de charger la clé de cryptage
        Attention : on ne veut pas initialiser cette variable en même temps que l'instanciation de la classe, mais
        seulement au moment ou l'on appelle la méthode crypter sur un objet de la classe."""
        getkey = ChargerUneClef().choiceKey()
        self.key = getkey
        self.key.__setattr__('key', getkey.key)
        return getkey

    def initFichier(self):
        """Initialisation du fichier à décrypter : commence par une boucle de choix pour la sélection du fichier puis
        fixe les valeurs des variables de la class qui serviront en argument de la fonction decrypter(). Il faut
        lancer initFichier avant chaque opération de décryptage si la classe n'est pas réinstancié entre deux
        utilisation de decrypter()"""
        choixUtilisateur = self.choixFichier.validerExistence()
        if choixUtilisateur:
            path = self.choixFichier.pathFichier()
            name = path.name
            self.__setattr__('path', path)
            self.__setattr__('name', name)
            # file = File(self.path) # cf. commentaire de l'attribut self.file pour l'instant on n'en a pas besoin
            # self.__setattr__('file',file)
            return True
        else:
            return False

    def initDecryptage(self):
        """Pour optimiser le lancement de ces deux opérations en une seule. Quand l'utilisateur lance une session il
         peut avoir à effectuer plusieurs fois l'opération de decryptage d'un fichier.
        Ce sont donc deux opérations qui doivent nécessairement précéder tout lancement d'un décryptage.
        Cela évite de réinstancier la classe entre chaque nouveau décryptage.
        Celle-ci est instanciée une fois pour toute au début du programme, mais au cours d'une même
        session les variables doivent être constamment mises à jour pour que l'application ne reste pas bloquer sur
        les mêmes paramètres utilisateurs donnés à la première opération de décryptage."""
        self.initVariables()  # après le chargement de la clé on initialise toute la séquence de sélection du fichier
        # à décrypter
        self.initFichier()  # attention il faut initialiser le fichier à dércypter ici, autrement la fonction suivante
        # prend en argument les variables d'un fichier décrypté précédemment,
        # car la class où nous sommes est instanciée une première fois dans le module _00_IA().py et reste active
        # après chaque opération de décryptage.

    def renameDecryptedFiles(self,prefix="crypt_"):
        self.newname = self.algo.renameDecryptFiles(self.name, prefix)
        return self.newname

    def decrypter(self,init_KEY=True):
        """Décryptage proprement dit et fin de la boucle du module
        la variable init_KEY permet au besoin d'effectuer plusieurs cryptages de fichier à la suite avec la même clé,
        ce sera utile lorsque l'on voudra crypter un dossier en passant par CryptFichier"""
        if init_KEY:  # on n'a pas toujours besoin de demander une clé si celle-ci à déjà été chargée une fois
            self.initKey()
        self.initDecryptage()
        print(self.key.key, self.name, self.path.parent)
        input("enter si c'est la bonne clé")
        self.algo.decryptOneFileAndRemove(self.name, self.path.parent, self.key.key)
        os.chdir(self.app_path)
        print(f"retour au dossier d'origine: {self.key.path.parent}")
        print("Décryptage réussi!\nRetour au Menu Principal")
        time.sleep(1)  # pour permettre de lire le message et de réaliser à quel point on est très fort.
        return 'Menu'


if __name__ == "__main__":
    key = Key()
    print(key.key.encode())
    k = Fernet.generate_key()
    f = Fernet(key.key)
    c = f.encrypt('test'.encode())

    #c = file.getContent()
    #file.closeFile()
    print(c)
    d = f.decrypt(c)
    print(d)