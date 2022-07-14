'''importation des modules natifs usuels'''
import os
import sys
import threading
import time
import winsound

'''modules personnels'''
from _02_Choix import ChoixDossier
from _03_ChargerUneClef_V2 import ChargerUneClef
from _02_KeyFile import Key
from _02_Directory import Directory
from _02_Classes import *
from _01_AlgoG import AlgoG


class DecrypterUnDossier:
    '''La particularité de cette classe est l'instanciation de ChoixDossier et de Directory pour
    la sélection du dossier source ainsi que l'appel à la classe File pour la manipulation de tous les fichiers.
    l'algorithme d'arborescence de tree_list() associé à la méthode mkTreeList joue un rôle essentiel.
    Une autre clé est le jeu sur les appels à la fonction os.chdir(). Très discrets, ils jouent un rôle majeurs.
    ATTENTION: Bien lire les commentaires associés à ces fonctions avant d'entreprendre toutes modifications '''

    def __init__(self):
        # variable d'instanciation de la classe ChoixDossier()
        self.app_path = ""
        self.choixDossier = None
        self.key = None
        # variables de base; à partir du choix d'un dossier on tirera un nom de dossier et un chemin
        self.name = ""
        self.path = ""
        # variables essentielles associées au choix du dossier
        self.srcDir = None  # attention: on a besoin d'une instance de Directory() pour un dossier source
        self.decryptedDirectory = None  # et d'une instance de Directory() pour un dossier target.
        self.content = None
        self.parent = ""
        self.treeFileList = []
        self.treeSubDirList = []
        self.treeNameList = []
        # notre instance de AlgoG()
        self.algo = None
        # variable en attente pour la programmation de la création d'un dossier target éventuel.
        self.decryptedDirectory = None
        self.newname = ""

        # initialisation des variables
        self.initVariables()
        # self.file = File # on n'a pas forcément besoin d'instancier le fichier à decrypter avec notre classe si les
        # manipulations sur les chemins de fichier suffisent mais peut-être le faudra-t-il si on implémente File
        # dans les fonctions de cryptage de _01_AlgoG

    def initVariables(self):
        '''(re)initialisation des variables de la Classe et lancement de initFichier()
        NB: il est nécessaire de découpler initVariables de initDirectory car on veut pouvoir
        réinitialiser ces variables à chaque fois avant de recommencer l'opération, autrement les variables restent
        en mémoire et interfèrent avec l'opération de cryptage suivante'''
        # (ré)instanciation et paramètrage de la classe ChoixDossier
        self.choixDossier = ChoixDossier()
        self.choixDossier.question = 'Choisissez un dossier à décrypter:'
        # réinitialisation des variables de la classe
        self.app_path = Path(os.path.dirname(os.path.abspath("__00__IA.py")))
        self.path = ""
        self.name = ""
        self.newname = ""
        self.srcDir = None  # attention: on a besoin d'une instance de Directory() pour un dossier source
        self.decryptedDirectory = None  # et d'une instance de Directory() pour un dossier target.
        self.content = None
        self.parent = ""
        self.treeFileList = []
        self.treeSubDirList = []
        self.treeNameList = []
        # (ré)instanciation des autres classes
        # self.key = Key()
        self.decryptedDirectory = Directory
        self.algo = AlgoG()

    def initKey(self):
        '''ici on appelle inévitablement un sous-module qui permet de charger la clé de cryptage
        Attention: on ne veut pas initialiser cette variable en même temps que l'instanciation de la classe mais
        seulement au moment ou l'on appelle la méthode crypter sur un objet de la classe.'''
        getkey = ChargerUneClef().choiceKey()
        self.key = getkey
        self.key.__setattr__('key', getkey.key)
        return getkey

    def initDirectory(self):
        '''initialisation du fichier à décrypter: commence par une boucle de choix pour la sélection du fichier puis
        fixe les valeurs des variables de la class qui serviront en argument de la fonction decrypter(). Il faut
        lancer initFichier avant chaque opération de décryptage si la classe n'est pas réinstancié entre deux
        utilisation de decrypter()'''
        choixUtilisateur = self.choixDossier.validerExistence()
        if choixUtilisateur:
            self.path = self.choixDossier.pathDossier()
            self.name = self.path.name
            self.srcDir = Directory(self.path)
            self.treeFileList = self.srcDir.treeFileList
            self.treeNameList = self.srcDir.treeNameList
            return True
        else:
            return False

    def setTempDir(self):
        tempPath = Path.mkdir(self.srcDir.path / 'TemporaryFiles')
        os.chdir(tempPath)
        return tempPath

    def initDecryptage(self):
        '''pour optimiser le lancement de ces deux opérations en une seule. Quand l'utilisateur lance une session il
         peut avoir à effectuer plusieurs fois l'opération de decryptage d'un dossier.
        Ce sont donc deux opérations qui doivent nécessairement précéder tout lancement d'un décryptage.
        Cela évite de réinstancier cette classe entre chaque nouveau décryptage.
        Celle-ci est instanciée une fois pour toute au début du programme, mais au cours d'une même
        session les variables doivent être constamment mises à jour pour ne pas que l'application reste bloqué sur
        les mêmes paramètres utilisateurs donnés à la première opération de décryptage.'''
        self.initVariables()  # après le chargement de la clé on initialise toute la séquence de sélection du fichier
        # à décrypter
        self.initDirectory()  # attention il faut initialiser le fichier à dércypter ici, autrement la fonction suivante
        # prend en argument les variables d'un fichier décrypté précédemment
        # car la class où nous sommes est instanciée une première fois dans le module _00_IA().py et reste active
        # après chaque opération de décryptage.
        # self.setTempDir()

    def decrypterDossier(self, init_KEY=True):
        """C'est la méthode principale qui fait le boulot de décryptage. On initialise une clé, toutes les variables
        doivent aussi être (ré)initialisées par initDecryptage() et on lance notre algo de décryptage d'un dossier.
        Attention : la liste treeFileList est constituée d'objets de la classe File, mais elle est générée automatiquement
        à l'instanciation de la classe Directory qui a lieu dans initDecryptage() par initDirectory()"""
        if init_KEY:  # on n'a pas toujours besoin de demander une clé si celle-ci a déjà été chargée une fois
            self.initKey()
        self.initDecryptage()
        os.system('COLOR 02')
        args = [f"{self.app_path}\\audio\\menu.wav"]
        playsound = threading.Thread(target=self.algo.play_sound, args=args)
        playsound.start()
        self.algo.decryptDirectoryOperation(self.treeFileList, self.key.key)
        os.system('COLOR 07')
        print("Décryptage réussi!\n")
        os.chdir(self.app_path)
        print(f"retour au dossier d'origine: {self.app_path}")
        print("\nRetour au Menu Principal")
        time.sleep(1)  # pour permettre de lire le message et de réaliser à quel point on est très fort.
        return 'Menu'


if __name__ == "__main__":
    test = DecrypterUnDossier()
