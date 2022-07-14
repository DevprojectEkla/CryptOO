import threading
import time
from _02_Choix import ChoixFichier, ChoixDossier
from _03_ChargerUneClef_V2 import ChargerUneClef
from _02_File import File
from _02_KeyFile import Key
from _02_Classes import *
from _01_AlgoG import AlgoG


class CrypterUnFichier:
    """Cette classe permet d'initier une boucle permettant le chargement d'une clé de cryptage via un sous module suivi
     du choix d'un fichier à crypter et de l'opération de cryptage proprement dite. Instancier cette classe c'est donc
     instancier surtout ChoixFichier et une méthode particulière de cryptage sur le résultat du choix, mais cette
     méthode demande aussi l'instanciation de la classe File pour la création du fichier crypté.
    TODO: essayer de découpler le choix du fichier et le chargement de la clé de l'instanciation de cette classe
    Idée: Crypter un fichier requiert toujours la donnée de trois fichiers: la clé, un fichier existant,
    un fichier à créer. Les deux premier proviennent de deux choix utilisateur distinct le dernier est instancié par
    cette classe mais à l'aide du nom du second fichier.
    La Classe pourrait donc être instancier de cette manière: CrypterUnFichier(path, clé) avec pour seule méthode
    dynamique l'opération de cryptage mais le problème est que cela revient à devoir passer des arguments provenant
    de deux choix successifs"""

    def __init__(self):
        self.app_path = ""
        self.choixFichier = None
        self.key = None  # Attention self.key ne sera finalement jamais un objet de la classe Key. voir initKey()
        self.cryptfile = None
        self.name = ""
        self.path = ""
        self.algo = None
        self.initVariables()
        # self.file = File # on n'a pas forcément besoin d'instancier le fichier à crypter avec notre classe si les
        # manipulations sur les chemins de fichier suffisent mais peut-être le faudra-t-il si on implémente File
        # dans les fonctions de cryptage de _01_AlgoG
        # implémentation GUI:

    def initVariables(self):
        """(re)initialisation des variables de la Classe et lancement d'initFichier()
        NB : il est nécessaire de découpler initFichier d'initCryptage car on veut pouvoir
        réinitialiser les variables à chaque fois avant de commencer l'opération, autrement les variables restent
        en mémoire et interfèrent avec l'opération de cryptage suivante"""
        self.app_path = Path(os.path.dirname(os.path.abspath("__00__IA.py")))
        self.choixFichier = ChoixFichier()
        self.choixFichier.question = 'Choisissez un fichier à crypter:'
        self.name = ""
        self.path = ""

        # implémentation GUI:
        # initObjet = InitObjetsGraphiques()
        #       # self.crypterGUI = CrypterGUI(initObjet.l_objetsG)

        # à supprimer:
        # self.cryptfile = File(f'crypt_{self.name}') # 6n n'utilise plus ce procéder pour changer le nom du fichier
        # (peut-être à tort?). L'opération de changement de nom de fichier se fait par une méthode de AlgoG
        # self.cryptfile.overwrite = True
        # self.key = Key() on ne doit pas instancier self.key ici sous peine de se voir bloqué avec la clé secret.key
        # self.key est initialisé par initKey

        # Instanciation de notre classe d'algo.
        self.algo = AlgoG()

    def initKey(self):
        """Ici on appelle inévitablement un sous-module qui permet de charger la clé de cryptage
        Attention : on ne veut pas initialiser cette variable en même temps que l'instanciation de la classe, mais
        seulement au moment où l'on appelle la méthode crypter sur un objet de la classe."""
        getkey = ChargerUneClef().choiceKey()  # cette méthode permet de charger une clé, elle renvoit un objet Key()
        self.key = getkey  # temporairement on associe l'objet Key à cette variable
        self.key.__setattr__('key', getkey.key)  # ici on fixe la valeur de l'attribut self.key de l'objet Key.
        return getkey

    def initFichier(self):
        """Initialisation du fichier à crypter : commence par une boucle de choix"""
        choixUtilisateur = self.choixFichier.validerExistence()
        if choixUtilisateur:
            # path = self.choixFichier.pathFichier() # uncomment cette ligne pour revenir à la console
            # GUI :
            self.path = Path(choixUtilisateur)
            self.name = self.path.name
            return True
        else:
            return False

    def initcryptage(self):
        """Pour optimiser le lancement de ces deux opérations en une seule. Quand l'utilisateur lance une session, il
         peut avoir à effectuer plusieurs fois l'opération de decryptage d'un dossier.
        Ce sont donc deux opérations qui doivent nécessairement précéder tout lancement d'un cryptage.
        Cela évite de réinstancier cette classe entre chaque nouveau cryptage.
        Celle-ci est instanciée une fois pour toute au début du programme, mais au cours d'une même
        session les variables doivent être constamment mises à jour pour que l'application ne reste pas bloqué sur
        les mêmes paramètres utilisateurs donnés à la première opération de cryptage."""
        self.initVariables()  # après le chargement de la clé on initialise toute la séquence de sélection du fichier
        # à crypter
        self.initFichier()  # attention il faut initialiser le fichier à crypter ici, autrement la fonction suivante
        # Prend en argument les variables d'un fichier crypté précédemment,
        # car la class où nous sommes est instanciée une première fois dans le module _00_IA().py et reste active
        # après chaque opération de cryptage.
        # self.setTempDir()

    def crypter(self, init_KEY=True):
        """Cryptage proprement dit et fin de la boucle du module
        la variable init_KEY permet au besoin d'effectuer plusieurs cryptages de fichier à la suite avec la même clé,
        ce sera utile lorsque l'on voudra crypter un dossier en passant par CryptFichier"""

        if init_KEY:  # on n'a pas toujours besoin de demander une clé si celle-ci à déjà été chargée une fois
            self.initKey()
        self.initcryptage()  # après le chargement de la clé on appelle initie toute la séquence de sélection du fichier
        # à crypter
        print(self.key.key, self.name, self.path.parent)
        os.system('COLOR 02')
        args = [f"{self.app_path}\\audio\\cryptage_fichier.wav"]
        playsound = threading.Thread(target=self.algo.play_sound, args=args)
        playsound.start()
        self.algo.cryptOneFileAndRemove(self.name, self.path.parent, self.key.key)
        # le changement de dossier qui suit est capitale dès lors que l'on cherche à crypter des fichiers qui ne se
        # trouvent pas dans le dossier où l'application est lancée.
        os.chdir(self.app_path)
        print(f"retour au dossier d'origine: {self.key.path.parent}")
        print("cryptage réussi!\nRetour au Menu Principal")
        time.sleep(1)  # pour permettre de lire le message et de réaliser à quel point on est très fort.
        os.system('COLOR 07')
        return 'Menu'
