from variables import *

import les_contraintes_clausales_en_cavales as cc
class Hitman:
    def __init__(self, n_lignes:int, n_colonnes:int, pos_ligne:int, pos_colonne:int, nb_gardes:int, nb_invites: int, MAX_OUIE : int, BROUHAHA : int,son_nom: str="Hitman, l'agent 47"):
        self.max_L = n_lignes
        self.max_C = n_colonnes 
        self._x = pos_ligne
        self._y = pos_colonne
        self.name = son_nom
        self.MAX_OUIE = MAX_OUIE
        self.BROUHAHA = BROUHAHA
        self.MAX_VOISINS = self.getMAXVOISINS()
        self.costume_trouve = False
        self.corde_trouve = False
        self.nb_gardes = nb_gardes
        self.nb_invites = nb_invites
        self.nb_gardes_trouvees = 0
        self.nb_invites_trouves = 0
        self.unknown = "X"
        self.mat_connue = [[self.unknown for i in range(self.max_C)] for j in range(self.max_L)]
        self.mat_regard = [[0 for i in range(self.max_C)] for j in range(self.max_L)]

    def getMAXVOISINS(self) -> int:
        return (self.MAX_OUIE * 2 + 1) ** 2
    

    def voit(self, info: dict) -> None:
        """
        Reçoit l'info de l'oracle. A déterminer comment l'info
        sera transmise.
        Hypothèse : dictionnaire avec les clés qui sont un Tuple désignant une position.
        La valeur associée est ce qu'il y a à cette position (exemple : un garde, civil, un mur, vide, etc.)
        """

        for pos in info.keys():
            self.ajout_info_mat(pos[0], pos[1], info[pos])



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
            if info.startswith("G"):
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
            if self.mat_connue[ligne][colonne].endswith("S"):
                for i in range(1, 3):
                    if ligne + i < self.max_L:
                        self.mat_regard[ligne + i][colonne] += 1
            elif self.mat_connue[ligne][colonne].endswith("N"):
                for i in range(1, 3):
                    if ligne - i >= 0:
                        self.mat_regard[ligne - i][colonne] += 1
            elif self.mat_connue[ligne][colonne].endswith("E"):
                for i in range(1, 3):
                    if colonne + i < self.max_C:
                        self.mat_regard[ligne][colonne + i] += 1
            elif self.mat_connue[ligne][colonne].endswith("O"):
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

        for i in range(self.max_L):
            for j in range(self.max_C):
                if self.mat_connue[i][j].startswith("G"):
                    vision_bloque = False
                    if self.mat_connue[i][j].endswith("S"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i + v < self.max_L:
                                
                                if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != "X":
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i + v][j] = 0
                                     
                        
                    elif self.mat_connue[i][j].endswith("N"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i - v >= 0:
                                
                                if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != "X":
                                    vision_bloque = True
                                    

                                if vision_bloque:
                                    self.mat_regard[i - v][j] = 0
                        
                    elif self.mat_connue[i][j].endswith("E"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if j + v < self.max_C:
                                
                                if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != "X":
                                    vision_bloque = True
                                    

                                if vision_bloque:
                                    self.mat_regard[i][j + v] = 0
                        
                    elif self.mat_connue[i][j].endswith("O"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            
                            if j - v >= 0:
                                #print(i, j-v,self.mat_connue[i][j - v])
                                
                                if self.mat_connue[i][j - v] != empty and self.mat_connue[i][j - v] != "X":
                                    vision_bloque = True
                                    

                                if vision_bloque:
                                    self.mat_regard[i][j - v] = 0
                        
                    else:
                        print("Erreur : le garde en (" + str(i) + ", " + str(j) + ") n'a pas de direction")
        
def main():
    Hitman1 = Hitman(3, 3, 0, 0)
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
        