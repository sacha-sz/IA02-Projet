from variables import *

import les_contraintes_clausales_en_cavales as cc
from hitman import *
from gophersat import *
class Agent_Hitman:
    def __init__(self, MAX_OUIE : int = 2, son_nom: str="Hitman, l'agent 47"):
        self.oracle = HitmanReferee() #On crée l'oracle / arbitre
        self.gophersat = Gophersat() 

        #Taille de la map
        self.max_L = self.oracle.start_phase1()["m"]
        self.max_C = self.oracle.start_phase1()["n"] 

        #Position de départ
        self._x = self.oracle.start_phase1()["position"][0]
        self._y = self.oracle.start_phase1()["position"][1]
        
        self.name = son_nom
        
        #Attributs pour les voisins et l'ouie
        self.MAX_OUIE = MAX_OUIE
        self.BROUHAHA = 5 #Brouhaha si count == 5
        self.MAX_VOISINS = self.getMAXVOISINS()

        
        self.costume_trouve = False
        self.corde_trouve = False
        self.nb_gardes = self.oracle.start_phase1()["guard_count"]
        self.nb_invites = self.oracle.start_phase1()["civil_count"]


        self.unknown = "X"


        self.mat_connue = [[self.unknown for i in range(self.max_C)] for j in range(self.max_L)]
        self.mat_regard = [[0 for i in range(self.max_C)] for j in range(self.max_L)]

        self.loc_gardes = set()
        self.loc_invites = set()

    def entendre(self) -> None:
        """

        Méthode entendre. A partir d'une position,
        on demande si on entend des gens et on génère
        la liste des positions des voisins.
        Si le nombre de gens entendu est inférieur au BROUHAHA,
        on regarde si on a déjà localisé des gens dans cette zone.
        
        """
        self._x = self.oracle["position"][0]
        self._y = self.oracle["position"][1]
        neighbors = self.generate_neighboors(self._x, self._y) #On génère les voisins
        nb_ouie = self.oracle["hear"]
        
        #Si on entend moins de BROUHAHA personnes, on regarde si on a déjà localisé des gens dans cette zone
        if self.oracle["hear"] < self.BROUHAHA:
            pos_neighbors = []
            for pos in neighbors:
                if self.mat_connue[pos[0]][pos[1]] == self.unknown:
                    #self.ajout_info_mat(pos[0], pos[1], empty)
                    pos_neighbors.append(pos)
                elif self.mat_connue[pos[0]][pos[1]] == Personne or self.mat_connue[pos[0]][pos[1]] == Garde or self.mat_connue[pos[0]][pos[1]] == Invite:
                    nb_ouie -= 1
            #On ajoute les clauses
            self.gophersat.ajout_clauses_entendre(pos_neighbors, self.oracle["hear"])
        else:
            self.gophersat.ajout_clauses_entendre(neighbors, self.oracle["hear"])


    def voir(self) -> None:
        """
        
        Méthode voir. A partir d'une position,
        on demande si on voit des gens et on génère
        une liste contenant des certitudes sur les positions.
        
        """

        self._x = self.oracle["position"][0]
        self._y = self.oracle["position"][1]
        vision = self.oracle["vision"]
        certitudes = []
        for v in vision:
            if v[1] == HC.EMPTY:
                certitudes.append((v[0][0], v[0][1], "N"))
            if v[1] in [HC.GUARD_N, HC.GUARD_S, HC.GUARD_E, HC.GUARD_W]:
                certitudes.append((v[0][0], v[0][1], "G"))
                self.loc_gardes.add((v[0][0], v[0][1]))
                self.ajout_info_mat(v[0][0], v[0][1], v[1])
            if v[1] in [HC.CIVILIAN_N, HC.CIVILIAN_S, HC.CIVILIAN_E, HC.CIVILIAN_W]:
                certitudes.append((v[0][0], v[0][1], "I"))
                self.loc_invites.add((v[0][0], v[0][1]))
                self.ajout_info_mat(v[0][0], v[0][1], v[1])

        self.gophersat.ajout_clauses_voir(certitudes)

    def test(self, x : int, y : int, type : str) -> None:
        """

        Demande à gophersat s'il y a la présence d'une personne.

        """
        res = self.gophersat.test_personne((self._x, self._y, "P"))
        if res == 0:
            pass
        elif res == 1:
            self.ajout_info_mat(x, y, type)

        elif res == 2:
            self.ajout_info_mat(x, y, Garde)
            self.loc_gardes.add((x, y))

    def gardesTousTrouves(self):
        return len(self.loc_gardes) == self.nb_gardes
    
    def invitesTousTrouves(self):
        return len(self.loc_invites) == self.nb_invites


    def getMAXVOISINS(self) -> int:
        return (self.MAX_OUIE * 2 + 1) ** 2

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, new_x : int):
        if 0 <= new_x and new_x < self.max_L:
            self._x = new_x
        else:
            print("Erreur : la coordonnée en x est hors de la matrice")
            print("La coordonnée n'a pas été modifiée")

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, new_y):
        if 0 <= new_y and new_y < self.max_C:
            self._y = new_y
        else:
            print("Erreur : la coordonnée en y est hors de la matrice")
            print("La coordonnée n'a pas été modifiée")

    def generate_neighboors(self, Indice_ligne: int, Indice_colonne: int) -> LC:
        """
        Fonction qui genere les voisins d'une case donnee
        """
        liste_voisins = []

        for change_ligne in range(-self.MAX_OUIE, self.MAX_OUIE+1):
            for change_col in range(-self.MAX_OUIE, self.MAX_OUIE+1):
                if Indice_ligne + change_ligne < 0 or Indice_ligne + change_ligne >= self.max_L:
                    continue
                if Indice_colonne + change_col < 0 or Indice_colonne + change_col >= self.max_C:
                    continue

                liste_voisins.append(
                    [Indice_ligne + change_ligne, Indice_colonne + change_col])
        #print(liste_voisins)
        return liste_voisins


    def entendre_voisins(self, Indice_ligne: int, Indice_colonne: int, Nb_voisins: int) -> LC:
        
        liste_voisins = self.generate_neighboors(Indice_ligne, Indice_colonne)
        liste_clauses = []
        liste_voisins_potentiels = []
        
        for index, pos_voisin in enumerate(liste_voisins):

            if self.mat_connue[pos_voisin[0]][pos_voisin[1]] == self.unknown:
                liste_voisins_potentiels.append(dict_pers[str(liste_voisins[index][0]) + str(liste_voisins[index][1])])
            if self.mat_connue[pos_voisin[0]][pos_voisin[1]] == Personne or self.mat_connue[pos_voisin[0]][pos_voisin[1]] == Garde or self.mat_connue[pos_voisin[0]][pos_voisin[1]] == Invite:
                Nb_voisins -= 1

        #liste_clauses += cc.exactly_n(Nb_voisins, liste_voisins)
        if Nb_voisins < self.BROUHAHA:
            return cc.exactly(Nb_voisins, liste_voisins_potentiels)
        
        return cc.at_least(self.BROUHAHA, liste_voisins_potentiels) + cc.at_most(self.MAX_VOISINS, liste_voisins_potentiels)


        
    def __str__(self):
        chaine = "-" * 36 + "-" * max(self.max_C - 32, 0) * 2 + "\n"
        chaine += "Je suis \"" + self.name + "\"\n"
        chaine += "Je suis en (" + str(self._x) + ", " + str(self._y) + ")\n"
        chaine += "\nJe connais la matrice suivante :\n"
        for i in range(self.max_L):
            for j in range(self.max_C):
                chaine += " "* min(3-len(self.mat_connue[i][j]), 2) + self.mat_connue[i][j] 
            chaine += "\n"
            
        chaine += "\nLa matrice des regards est : \n"
        for i in range(self.max_L):
            for j in range(self.max_C):
                chaine += "  " + str(self.mat_regard[i][j])
            chaine += "\n"
        chaine += "-" * 36 + "-" * max(self.max_C - 32, 0) * 2 + "\n"
        return chaine
    
    def check_coord(self, ligne, colonne):
        if  0 <= ligne and ligne < self.max_L and 0 <= colonne and colonne < self.max_C:
            return True
        else:
            return False
    
    def translate_ligne(self, ligne):
        return self.max_L - 1 - ligne
    
    def ajout_info_mat(self, ligne, colonne, info):

        ligne = self.translate_ligne(ligne)
        

        if  self.check_coord(ligne, colonne):
            self.mat_connue[ligne][colonne] = info

            # Si garde on ajoute sa vision
            if info in [HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]:
                self.add_vision_garde(ligne, colonne)
            
            #if info.startswith("E"):
                #self.mat_regard[ligne][colonne] = 0

            if info == Corde:
                self.corde_trouve = True
            elif info == Costume:
                self.costume_trouve = True
        else:
            print("Erreur : les coordonnées sont hors de la matrice")
            print("Aucune information n'a été ajoutée")
    
    def add_vision_garde(self, ligne, colonne):
        if  self.check_coord(ligne, colonne):
            if self.mat_connue[ligne][colonne] == Garde:
                #On ne connait pas sa direction, il peut regarder dans n'importe quelle direction
                pass

            elif self.mat_connue[ligne][colonne] == HC.GUARD_S:
                for i in range(1, 3):
                    if ligne + i < self.max_L:
                        self.mat_regard[ligne + i][colonne] += 1

            elif self.mat_connue[ligne][colonne] == HC.GUARD_N:
                for i in range(1, 3):
                    if ligne - i >= 0:
                        self.mat_regard[ligne - i][colonne] += 1

            elif self.mat_connue[ligne][colonne] == HC.GUARD_E:
                for i in range(1, 3):
                    if colonne + i < self.max_C:
                        self.mat_regard[ligne][colonne + i] += 1

            elif self.mat_connue[ligne][colonne] ==  HC.GUARD_W:
                for i in range(1, 3):
                    if colonne - i >= 0:
                        self.mat_regard[ligne][colonne - i] += 1
            else:
                print("Ce n'est pas un garde qui est en (" + str(ligne) + ", " + str(colonne) + ")")
        else:
            print("Erreur : les coordonnées sont hors de la matrice")
            print("Aucune information n'a été ajoutée")
        self.verif_vision()

    def verif_vision(self):
        """
        Si un garde a un objet/mur/personne devant lui, son champ 
        de vision doit être réduit.
        
        """

        #A MODIFIER

        for i in range(self.max_L):
            for j in range(self.max_C):
                if self.mat_connue[i][j].startswith("G"):
                    vision_bloque = False
                    if self.mat_connue[i][j].endswith("S"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i + v < self.max_L:
                                
                                if self.mat_connue[i + v][j] != HC.EMPTY and self.mat_connue[i + v][j] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i + v][j] = 0
                                     
                        
                    elif self.mat_connue[i][j].endswith("N"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i - v >= 0:
                                
                                if self.mat_connue[i - v][j] != HC.EMPTY and self.mat_connue[i - v][j] != self.unknown:
                                    vision_bloque = True
                                    

                                if vision_bloque:
                                    self.mat_regard[i - v][j] = 0
                        
                    elif self.mat_connue[i][j].endswith("E"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if j + v < self.max_C:
                                
                                if self.mat_connue[i][j + v] != HC.EMPTY and self.mat_connue[i][j + v] != self.unknown:
                                    vision_bloque = True
                                    

                                if vision_bloque:
                                    self.mat_regard[i][j + v] = 0
                        
                    elif self.mat_connue[i][j].endswith("O"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            
                            if j - v >= 0:
                                #print(i, j-v,self.mat_connue[i][j - v])
                                
                                if self.mat_connue[i][j - v] != HC.EMPTY and self.mat_connue[i][j - v] != self.unknown":
                                    vision_bloque = True
                                    

                                if vision_bloque:
                                    self.mat_regard[i][j - v] = 0
                        
                    else:
                        print("Erreur : le garde en (" + str(i) + ", " + str(j) + ") n'a pas de direction")
        
def main():
    Hitman1 = Agent_Hitman(3, 3, 0, 0)
    print(Hitman1)
    Hitman1.ajout_info_mat(1, 1, "GN")
    print(Hitman1)

    Hitman1.ajout_info_mat(2, 0, "GE")
    print(Hitman1)
    Hitman1.ajout_info_mat(2, 1, "GO")
    
    
    print(Hitman1)

    Hitman1.ajout_info_mat(2, 2, "GS")
    print(Hitman1)

if __name__ == "__main__":
    main()
        