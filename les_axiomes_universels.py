# Import
from typing import List, Tuple, Dict, Set
from itertools import combinations
import les_contraintes_clausales_en_cavales as cc

# Variables globales
dim_global = [-1, -1]
liste_clauses_global = []
dict_pers = {}
dict_pers_inverse = {}


# Constantes
FILENAME = "hitman.cnf"
BROUHAHA = 6
MAX_VOISINS = 9

# Types alias
LC = List[List[int]]
LL = List[int]


def initialisation_fichier(N_lignes: int, N_colonnes: int, Nom_fichier: str = FILENAME) -> None:
    dim_global[0] = N_lignes
    dim_global[1] = N_colonnes

    # On ajoute les axiomes universels
    index = 1
    for i in range(N_lignes):
        for j in range(N_colonnes):
            dict_pers[str(i)+str(j)] = index
            dict_pers_inverse[index] = str(i)+str(j)
            index += 1

    with open(Nom_fichier, 'w') as f:
        f.write("c \n")
        f.write("c \n")
        f.write(
            "c Ce fichier a ete genere automatiquement par le programme les_axiomes_universels.py\n")
        f.write("c Il contient les axiomes universels pour le jeu Hitman\n")
        f.write("c Il contient egalement les deductions ajoutees a chaque tour\n")
        f.write("c Il correspond a un plateau de taille " +
                str(N_lignes)+"x"+str(N_colonnes)+"\n")
        f.write("c \n")
        f.write("c \n")
        f.write("p cnf "+str(N_lignes*N_colonnes)+" 0\n")

    return None


def generate_neighboors(Indice_ligne: int, Indice_colonne: int) -> LC:
    """
    Fonction qui genere les voisins d'une case donnee
    """
    liste_voisins = []

    for change_ligne in [-1, 0, 1]:
        for change_col in [-1, 0, 1]:
            if Indice_ligne + change_ligne < 0 or Indice_ligne + change_ligne >= dim_global[0]:
                continue
            if Indice_colonne + change_col < 0 or Indice_colonne + change_col >= dim_global[1]:
                continue
            liste_voisins.append(
                [Indice_ligne + change_ligne, Indice_colonne + change_col])

    return liste_voisins


def entendre_voisins(Indice_ligne: int, Indice_colonne: int, Nb_voisins: int, Nom_fichier: str = FILENAME) -> None:
    liste_voisins = generate_neighboors(Indice_ligne, Indice_colonne)
    liste_clauses = []
    
    for i in range(len(liste_voisins)):
        liste_voisins[i] = dict_pers[str(liste_voisins[i][0]) + str(liste_voisins[i][1])]

    # Génération des combinaisons de taille Nb_voisins parmi les voisins
    if Nb_voisins <= 5:
        liste_clauses = cc.exactly_n(Nb_voisins, liste_voisins)
    else:
        liste_clauses_temp = []
        liste_clauses_temp = cc.at_least(BROUHAHA, liste_voisins)
        liste_clauses_temp = cc.at_most(MAX_VOISINS, liste_voisins)
        
        liste_clauses = [x for x in liste_clauses_temp if x != [] and x not in liste_clauses] 
        
    return liste_clauses


def modify_nb_clauses(new_nb : int, Nom_fichier: str = FILENAME) -> None:
    with open(Nom_fichier, 'r') as f:
        lines = f.readlines()
        
    with open(Nom_fichier, 'w') as f:
        for line in lines:
            if line.startswith("p cnf"):
                line = "p cnf " + str(dim_global[0]*dim_global[1]) + " " + str(new_nb) + "\n"
            f.write(line)


def add_to_file(append_liste_clauses: LC, Nom_fichier: str = FILENAME) -> None:
    # Ajoute les clauses à la liste globale des clauses et les écrit dans le fichier
    modify_nb_clauses(len(liste_clauses_global) + len(append_liste_clauses), Nom_fichier)

    for clause in append_liste_clauses:
        if clause not in liste_clauses_global:
            liste_clauses_global.append(clause)

    with open(Nom_fichier, 'a') as f:
        for clause in append_liste_clauses:
            for literal in clause:
                if literal > 0:
                    f.write(str(literal) + " ")
                else:
                    f.write("-" + str(-literal) + " ")
            f.write("0\n")
    
    return None


def main():
    initialisation_fichier(3, 3)
    vois = entendre_voisins(0, 0, 1)
    add_to_file(vois)
    vois = entendre_voisins(1, 0, 1)
    add_to_file(vois)
    vois = entendre_voisins(1, 1, 2)
    add_to_file(vois)
    vois = entendre_voisins(2, 1, 1)
    add_to_file(vois)
    
    return None


if __name__ == "__main__":
    print("Debut du programme")
    main()
    print("Fin du programme")
