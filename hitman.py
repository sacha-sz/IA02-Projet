from variables import *


class Hitman:
    def __init__(self, n_lignes, n_colonnes, pos_ligne, pos_colonnes, son_nom="Hitman, l'agent 47"):
        self.max_L = n_lignes
        self.max_C = n_colonnes 
        self._x = pos_ligne
        self._y = pos_colonnes
        self.name = son_nom
        self.mat_connue = [["X" for i in range(self.max_C)] for j in range(self.max_L)]
        self.mat_regard = [[0 for i in range(self.max_C)] for j in range(self.max_L)]

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, new_x):
        if 0 <= new_x and new_x < self.max_L:
            self._x = new_x
        else:
            print("Erreur : la coordonnée en x est hors de la matrice")
            print("La coordonnée n'a pas été modifiée")

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, new_y):
        if 0 <= new_y and new_y < self.max_C:
            self._y = new_y
        else:
            print("Erreur : la coordonnée en y est hors de la matrice")
            print("La coordonnée n'a pas été modifiée")
        
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
            
            if not info.startswith("E"):
                self.mat_regard[ligne][colonne] = 0
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
        