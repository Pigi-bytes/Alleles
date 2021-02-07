import matplotlib.pyplot as plt
import matplotlib
from tkinter import * 
from random import *
import json

class Graphe():
    def __init__(self):
        super().__init__()

    def readDataJson(self):
        with open("data_file.json", "r") as file: # Charger le fichier
            self.Data = json.load(file)
    
    def readDico(self, dico):
        self.Data = dico
        
    def show(self, x):    
        """
        Affiche un graphique 

            Parameters:
                x, "str" : Pourcentage or NbAlleles : Choisi les données a prendre 
        """

        Alleles = self.Data["Parameters"]["Alleles"] #Alleles 
        DataS = self.Data["Simulation"] # Dico avec les simulations 
        pop = self.Data["Parameters"]["GenerationFirst"] # Definie la population

        dicoData = {} 
        gen = []
        for j in range(len(Alleles)): # repeter nombre d'alleles fois 
            ListeA = []
            for i in range(len(DataS)): # Repeter nombre de generation fois 
                if j == 0: 
                    gen.append(str(i)) # permet d'avoir le nombre de generetton
                value = DataS[str(i)]["Stat"][Alleles[j]][x] # Donne la valeur pour l'alleles x a la generation y  
                ListeA.append(value) # stock la valeur dans une liste 
            dicoData[Alleles[j]] = ListeA # Attribue le nom de l'alleles a la liste dans le dico

        
        plt.style.use('ggplot')
        title = """Evolution de {a} alleles pendant {b} generations\ndans une population de {c} individus.""".format(a = len(Alleles), b = len(DataS), c= pop)
        plt.title(title)
        plt.xlabel('Generation')
        if x == "Pourcentage":
            plt.ylabel('Taux Alleles ( en % ) ')
        elif x == "NbAlleles":
            plt.ylabel('Nombre d\'Alleles')

        listeUse = []
        colorDefault = ["b", "g", "r", "c", "m", "y", "k", "w"] # couleur par defaults 
        # b: blue  g: green  r: red  c: cyan  m: magenta  y: yellow  k: black   w: white
        for i in range(len(Alleles)): # repeter par le nombre d'alleles
            if Alleles[i] in colorDefault: # Si c dans les couleurs par defaults 
                plt.plot(gen, dicoData[Alleles[i]], Alleles[i], label='Allele : ' + Alleles[i]) # on le rajoute sur le plot avec sa couleur
            else:
                plt.plot(gen, dicoData[Alleles[i]], label='Allele : ' + Alleles[i]) # sinon on rajoute par default

        plt.legend(loc="upper left") 
        plt.show() # Afficher

class Simulation(Graphe):
    """
    Classe qui s'ocupe de tout se qui est Population
    """

    def __init__(self):
        super().__init__()
        self.Gen = []

    def write_json(self):
        """
        Permet d'ecrire dans le dico
        """
        with open("data_file.json", "w") as write_file:
            json.dump(self.Data, write_file, indent=4)

    def modificationDico(self):
        """
        Fonction qui permet d'ecrire dans un dictionnaire externe
        """
        GenActuel = self.GenActuel  # Savoir a quelle generation on est
        stat = self.returnStat()  # Va chercher les stats

        self.Data["Simulation"][str(self.GenActuel)] = {
            "Stat": stat
        }  # Enregistre dans le dictionnaire
        if self.DataSave == True:
            self.write_json()  # Ecrit le dico dans le .json

    def ReturnString(self, liste):
        """
        Return une string de la generations

            Parameters:
                liste, list : permet de former la string de cette liste
        """
        string = ""
        for i in range(len(liste)):
            for j in range(len(liste[i])):
                string = string + "".join(liste[i][j])
        return string

    def returnStat(self):
        """ "
        Renvoie un dictionnaire avec les stats
        """
        strGen = self.ReturnString(self.Gen)  # La string de la generation
        NbPop = len(strGen)  # Le nombre de personne
        stat = {"NbAlleles": NbPop}

        for i in range(len(self.alleles)):  # Repeter jusqua nombre d'allele
            nbAllelesColor = strGen.count(self.alleles[i])  # Recupere la couleur
            pourcentage = (nbAllelesColor / NbPop) * 100  # Pourcentage
            pourcentage = round(pourcentage, self.Accuracy)  # Arrondis le pourcentage

            stat[self.alleles[i]] = {
                "Pourcentage": pourcentage,
                "NbAlleles": nbAllelesColor,
            }  # Ecriture
        return stat

    def first_generation(self, n):
        """
        Fonction qui genere une population de n taille

            Parameters:
                n, int : La taille de la population
        """
        Population = []
        for i in range(1, n + 1):
            I = [
                choice(self.alleles),
                choice(self.alleles),
            ]  # Choix aleatoire dans les alleles
            Population.append(I)  # Rajout de l'individus
        return Population

    def division_population(self, Population):
        """
        Fonction qui divise la liste en 3, Male, Femelle et Celibataire-

            parameter:
                Population, list : Division de la pop
        """
        NbPop = len(Population)
        PopMale = Population[0 : NbPop // 2]  # premiere moitier
        PopFemelle = Population[NbPop // 2 :]  # deuxiemme moitier
        Celib = []
        if NbPop % 2 == 1:  # si impaire
            Celib = [PopFemelle[-1]]  # ajouter a celib
            del PopFemelle[-1]  # Suppr dernier
        Pop = [PopFemelle, PopMale, Celib]
        return Pop

    def Nouvelle_population(self, oldGen):
        """
        Fonction qui crer une nouvelle populations, en recuperant l'allele d'un pere et d'une mere

            Parameters:
                oldGen, list : Liste permettant de recuperer les alleles
        """
        # Divison de la classe en 3
        popM = oldGen[0]  # Male
        popF = oldGen[1]  # Femelle
        popC = oldGen[2]  # Celibataire
        NewGen = []
        if len(popC) != 0:  # si ya des celibataires ont les rajoutes dans la simulations
            NewGen.append(popC[0])
        for i in range(len(popM)):
            for j in range(self.Children):
                People = [popM[i], popF[i]]
                RandomM = randint(0, i)
                RandomF = randint(0, i)
                PeopleA = [choice(popM[RandomM]), choice(popF[RandomF])]
                # print(People, "=> ", PeopleA)
                NewGen.append(PeopleA)
        return NewGen

    def start(self):
        """
        Fonction pour commencer la simulations
        """

        self.GenActuel = 0

        NewGen = self.first_generation(self.GenerationFirst)  # Creation de la generation Alpha
        self.Gen = self.division_population(NewGen)  # On divise la generation en deux
        self.modificationDico()  # On met a jour les Datas
        
        for i in range(self.NombreGenerations):
            self.GenActuel += 1

            NewGen = self.Nouvelle_population(self.Gen)  # Creation de la generation suivant a partir de la derniere
            self.Gen = self.division_population(NewGen)  # On la divise en deux
            self.modificationDico()  # On met a jour les Datas

        self.GenActuel = str(self.GenActuel)
        self.modificationDico()

    def optionSimulation(self, dico):

        self.alleles = dico["Alleles"]  # Les differents alleles
        self.NombreGenerations = dico["NombreGeneration"]  # Le nombre de generation
        self.GenerationFirst = dico["GenerationFirst"]  # Le nombre d'inidividus a la generation ALPHA
        self.Children = dico["Children"]  # Nombre d'enfant par couple
        self.Accuracy = dico["Accuracy"]  # Nombre de chiffre apres la virgule
        self.DataSave = dico["DataSave"]  # Sauvegarder une copie des donnees apres ? ( .json )
        self.Show = dico["Show"]  # Que montrer sur le graphique ("Pourcentage" or "NbAlleles")
        # self.mortality = 0 # Number of death

        self.Data = {"Parameters": dico, "Simulation": {}}

    def AfficherResultat(self):
        """
        Fonction qui Affiche les resultats
        """
        if self.DataSave == True:
            self.readDataJson()
        else:
            self.readDico(self.Data)
        self.show(self.Show)


# ajouter les legendre avec les parametre
# + mortalité
# + option graphique
# + mode interactif
alleles = Simulation()

# b: blue  g: green  r: red  c: cyan  m: magenta  y: yellow  k: black
option = {
    "Alleles": ["r", "g", "b"],  # Les differents alleles => list
    "NombreGeneration": 30,  # Le nombre de generation => int
    "GenerationFirst": 10,  # Le nombre d'inidividus a la generation ALPHA => int
    "Children": 2,  # Nombre d'enfant par couple => int
    "Accuracy": 1,  # Nombre de chiffre apres la virgule => int 
    "DataSave": True,  # Sauvegarder une copie des donnees apres ? ( .json ) => Booleans 
    "Show": "Pourcentage",  # Que montrer sur le graphique ("Pourcentage" or "NbAlleles") => string
}

alleles.optionSimulation(option)
alleles.start()

alleles.AfficherResultat()
