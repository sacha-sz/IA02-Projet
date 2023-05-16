<<<<<<< HEAD
class Hitman:
    def __init__(self, n_lignes, n_colonnes, pos_ligne, pos_colonnes, son_nom="GROS ZIZI"):
        self.max_L = n_lignes - 1
        self.max_C = n_colonnes - 1
        self.x = pos_ligne
        self.y = pos_colonnes
        self.name = son_nom
        self.mat_connue = [["X" for i in range(self.max_C)] for j in range(self.max_L)]
        self.mat_regard = [[0 for i in range(self.max_C)] for j in range(self.max_L)]
        
    def __str__(self):
        chaine = "-------------------\n"
        chaine += "Je suis \"" + self.name + "\"\n"
        chaine += "Je suis en (" + str(self.x) + ", " + str(self.y) + ")\n"
        chaine += "Je connais la matrice suivante : \n"
        for i in range(self.max_L):
            for j in range(self.max_C):
                chaine += str(self.mat_connue[i][j]) + " "
            chaine += "\n"
        chaine += "-------------------\n"
        return chaines
    
    def ajout_info_mat(self, ligne, colonne, info):
        if  1 <= ligne and ligne <= self.max_L and 1 <= colonne and colonne <= self.max_C:
            self.mat_connue[ligne][colonne] = info
        else:
            print("Erreur : les coordonnées sont hors de la matrice")
            print("Aucune information n'a été ajoutée")
    
    def get_vision_garde(self, ligne, colonne):
        if  1 <= ligne and ligne <= self.max_L and 1 <= colonne and colonne <= self.max_C:
            if self.mat_connue[ligne][colonne].endswith("N"):
                for i in range(1, 3):
                    if ligne - i <= self.max_L:
                        self.mat_regard[ligne + i][colonne] += 1
            elif self.mat_connue[
    
        
def main():
    Hitman1 = Hitman(10, 10, 5, 5)
    print(Hitman1)

if __name__ == "__main__":
    main()
        