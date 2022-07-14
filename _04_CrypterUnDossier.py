'''importation des modules natifs usuels'''
import os
import sys
import time

'''modules personnels'''
from _02_Choix import ChoixDossier
from _02_KeyFile import Key
from _03_ChargerUneClef_V2 import ChargerUneClef
from _02_Directory import Directory
from _02_Classes import *
from _01_AlgoG import AlgoG


class CrypterUnDossier:
    '''La particularité de cette classe est l'instanciation de ChoixDossier et de Directory pour
    la sélection du dossier source ainsi que l'appel à la classe File pour la manipulation de tous les fichiers.
    l'algorithme d'arborescence de tree_list() associé à la méthode mkTreeList joue un rôle essentiel.
    Une autre clé est le jeu sur les appels à la fonction os.chdir(). Très discrets, ils jouent un rôle majeurs.
    ATTENTION: Bien lire les commentaires associés à ces fonctions avant d'entreprendre toutes modifications '''
    def __init__(self):
        #variable générale:
        self.app_path = Path(os.path.dirname(os.path.abspath("__00__IA.py")))
        # variables de base; à partir du choix d'un dossier on tirera un nom de dossier et un chemin
        self.choixDossier = None
        self.name = ""
        self.path = ""
        # on aura besoin d'une clé pour encrypter, cette variable correspondra à une instanciation de la classe Key()
        self.key = None

        #variables essentielles associées au choix du dossier
        self.srcDir = None       # instance de Directory() pour le dossier source
        self.parent = ""
        self.treeFileList = []
        self.treeSubDirList = []
        self.nameList = []

        self.algo = None
        # variables en attente, pas d'utilité pour le moment
        self.content = None
        self.newname = ""
        self.decryptedDirectory = None
        self.cryptedDirectory = None  # instance de Directory() pour un dossier target éventuel

        # initialisation des variables
        self.initVariables()
        # self.file = File # on n'a pas forcément besoin d'instancier le fichier à decrypter avec notre classe si les
        # manipulations sur les chemins de fichier suffisent mais peut-être le faudra-t-il si on implémente File
        # dans les fonctions de cryptage de _01_AlgoG

    def initVariables(self):
        '''(re)initialisation des variables de la Classe et lancement de initFichier()
        NB: il est nécessaire de découpler initFichier de initCryptage car on veut pouvoir
        réinitialiser les variables à chaque fois avant de commencer l'opération, autrement les variables restent
        en mémoire et interfèrent avec l'opération de cryptage suivante'''
        # (ré)instanciation et paramètrage de la classe ChoixDossier
        self.choixDossier = ChoixDossier()
        self.choixDossier.question = 'Choisissez un dossier à crypter:'
        # réinitialisation des variables de la classes
        self.path = ""
        self.name = ""
        self.newname = ""
        self.srcDir = None
        self.content = None
        self.parent = ""
        # (ré)instanciation des autres classes
        #self.key = Key()
        self.cryptedDirectory = Directory
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
        '''initialisation du dossier à crypter: commence par une boucle de choix pour la sélection du fichier puis
        fixe les valeurs des variables de la class qui serviront en argument de la fonction crypter(). Il faut
        lancer initFichier avant chaque opération de cryptage si la classe n'est pas réinstancié entre deux
        utilisation de crypter()'''
        choixUtilisateur = self.choixDossier.validerExistence()
        if choixUtilisateur:

            self.path = self.choixDossier.pathDossier()
            self.srcDir = Directory(self.path)
            self.treeFileList = self.srcDir.treeFileList
            self.treeSubdirList = self.srcDir.treeSubdirList
            self.name = self.path.name

            print(self.treeFileList)
            return True
        else:
            return False

    def setTempDir(self):
        '''pourra être utile dans une version ultérieure, pas d'emploi pour le moment'''
        tempPath = Path.mkdir(self.srcDir.path/'TemporaryFiles')
        os.chdir(tempPath)
        return tempPath


    def initcryptage(self):
        '''pour optimiser le lancement des deux fonction initVariables() et initDirectory() en une seule.
         Quand l'utilisateur lance une session crypto il peut vouloir effectuer plusieurs opérations de cryptage
        d'un dossier. Ce sont donc deux fonctions qui doivent nécessairement précéder tout lancement d'un cryptage.
        Cela évite de réinstancier cette classe entre chaque nouveau cryptage.
        Celle-ci est instanciée une fois pour toute au début du programme, mais au cours d'une même
        session les variables doivent être constamment mises à jour pour ne pas que l'application reste bloqué sur
        les mêmes paramètres utilisateurs donnés à la première opération de cryptage.'''
        self.initVariables()  # après le chargement de la clé on initialise toute la séquence de sélection du fichier
        # à crypter
        self.initDirectory()  # attention il faut initialiser le fichier à rcypter ici, autrement la fonction suivante
        # prend en argument les variables d'un fichier crypté précédemment
        # car la class où nous sommes est instanciée une première fois dans le module _00_IA().py et reste active
        # après chaque opération de cryptage.
        #self.setTempDir()

    def crypterDossier(self,init_KEY=True):
        '''C'est la méthode principale qui fait le boulot de cryptage. On initialise une clé de cryptage, toutes les
        variables doivent aussi être (ré)initialisées par inicryptage() et on lance notre algo de cryptage d'un dossier.
        Attention: la liste treeFileList est constituée d'objets de la classe File mais elle est générée automatiquement
        à l'instanciation de la classe Directory qui a lieu dans initcryptage() par initDirectory()
        '''
        if init_KEY:  # on n'a pas toujours besoin de demander une clé si celle-ci à déjà été chargée une fois
            self.initKey()
        self.initcryptage()
        self.algo.cryptDirectoryOperation(self.treeFileList,self.key.key)
        print("Cryptage du dossier réussi!\nRetour au Menu Principal")
        # la ligne suivante est absolument essentiel si l'on veut pouvoir utiliser d'autre fonction de cryptage
        # dans une même session. On veut revenir dans le dossier de l'appli ou se trouve le fichier clé par défaut.
        os.chdir(self.app_path)
        print(f"retour au dossier d'origine: {self.key.path.parent}")
        time.sleep(1)  # pour permettre de lire le message et de réaliser à quel point on est très fort.
        return 'Menu'

if __name__ == "__main__":
    test = CrypterUnDossier()
