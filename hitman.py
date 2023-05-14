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
    
    return dict_position_element[str(li) + str(col) + val]

def variable_to_cell(var : int) -> Tuple[int, int, str]:
    """
    Fonction qui pour une variable donnée renvoie la cellule correspondante (ligne, colonne, valeur)
    """
    
    if var >= len(tab_position_element):
        raise ValueError("Variable trop grande")
    if var < 0:
        raise ValueError("Variable négative")
    
    return (int(tab_position_element[var][0]), int(tab_position_element[var][1]), tab_position_element[var][2])

def ecoute(ligne : int, col : int, num : int) -> List[int]:
    """
    Renvoie toutes les clauses où les num personnes peuvent-être.
    """
    Possibilites = []
    
    for orientation in personnes:
        Possibilites.append(cell_to_variable(ligne+1, col, orientation))
        Possibilites.append(cell_to_variable(ligne-1, col, orientation))
        Possibilites.append(cell_to_variable(ligne, col+1, orientation))
        Possibilites.append(cell_to_variable(ligne, col-1, orientation))
        Possibilites.append(cell_to_variable(ligne+1, col+1, orientation))
        Possibilites.append(cell_to_variable(ligne+1, col-1, orientation))
        Possibilites.append(cell_to_variable(ligne-1, col+1, orientation))
        Possibilites.append(cell_to_variable(ligne-1, col-1, orientation))
        
    return Possibilites


    
if __name__ == "__main__":
    main()