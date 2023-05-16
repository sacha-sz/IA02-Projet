# IMPORTS
from typing import List, Tuple, Dict, Set, Optional


"""
Map : List[List[str]]
    "r" : rien
    "c" : costume
    "k" : corde
    "t" : cible/target 
    "m" : mur
    "g" : garde
    "p" : personne
    "ci" : civil


"""
tableau_element = []

rien = "r"
tableau_element.append(rien)

costume = "c"
tableau_element.append(costume)

corde = "k"
tableau_element.append(corde)

cible = "t"
tableau_element.append(cible)

mur = "m"
tableau_element.append(mur)

garde = "g"
tableau_element.append(garde)

civil = "ci"

personne = "p" #p <==> g ou ci

nb_lignes = 5
nb_colonnes = 8


# Tableau contenant toutes les combinaisons possibles de position et d'éléments
tab_position_element =[str(i) + str(j) + element for i in range(nb_lignes) for j in range(nb_colonnes) for element in tableau_element]

# Dictionnaire qui pour toutes les combinaisons possibles donne un numéro
dict_position_element = {tab_position_element[i]:i for i in range(len(tab_position_element))}

def cell_to_variable(li : int, col : int, val : str) -> int:
    """
    Fonction qui pour une cellule donnée (ligne, colonne, valeur) renvoie le numéro de la variable correspondante
    """
    if li >= nb_lignes or col >= nb_colonnes:
        raise ValueError("Ligne ou colonne trop grande")
    if val not in tableau_element:
        raise ValueError("Valeur non valide")
    if li < 0 or col < 0:
        raise ValueError("Ligne ou colonne négative")
    
    
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
        