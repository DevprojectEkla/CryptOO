'''Ce module est la seconde version de _03_ChargerUneClef qu'il annule et remplace'''

'importation des modules natifs usuels'
import os

'modules personnels'
from _00_MenuPrincipal import MenuPrincipal
from _01_general import *
from _02_Classes import *
from _02_Choix import ChoixFichier
from _02_KeyFile import Key
from _01_AlgoG import AlgoG


class ChargerUneClef:
    '''Cette classe initie un choix pour le chargement d'une clé de cryptage. Il y a plusieurs possibiltés selon
   que l'on utilise le fichier par défaut secret.key du dossier courant, que l'on crée une nouvelle clé en écrasant
    le fichier par défaut, ou que l'on souhaite chargér un ficher situé à un autre endroit et/ou sous un autre nom '''

    def __init__(self):
        '''on ne peut pas instancier directement un objet clé Key car il s'agit toujours d'un fichier que l'on souhaite
        soit créer soit charger mais cela dépend justement du choix de l'utilisateur, l'instanciation doit donc 
        se faire par des méthodes et a posteriori, i.e. après le choix du nom de fichier qui permettra d'instancier
        la classe Key(File)'''
        self.app_path = Path(os.path.dirname(os.path.abspath("__00__IA.py")))
        self.menu = MenuPrincipal()
        self.key = Key
        self.choix = Choix(open("ChargeruneClef.txt",'r').read(),"#KeyGen>",['s', 'ovw', 'OF', 'c'],True, False)
        self.choixFichier = ChoixFichier('.key')
        self.algo = AlgoG()

    def choiceKey(self):
        '''boucle principale du module'''

        choix = self.choix.boucleDeChoix()

        if choix == 'ovw':
            key = self.algo.choiceOverWrite()
        elif choix == 'OF':
            key = self.algo.chooseOtherFile()
        elif choix == 'c':
            key = self.algo.creationNouveauFichier()
        elif choix == 's':
            key = self.algo.loadKey('secret.key')
            time.sleep(1)
        elif choix == 'CANCEL': # attention la commande (définie dans Choix()) est en petite case
            self.menu.initChoix()
        if key:
            return (key)
        else:
            self.choiceKey()


if __name__ == "__main__":
    choix = ChargerUneClef()
    choix.choiceKey()
