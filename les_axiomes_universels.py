# Import
from typing import List, Tuple, Dict, Set
from itertools import combinations
import les_contraintes_clausales_en_cavales as cc

# Variables globales
dim_global = [-1, -1]
liste_clauses = []

# Constantes
FILENAME = "hitman.cnf"
BROUHAHA = 6
MAX_VOISINS = 9

# Fonctions


def initialisation_fichier(N_lignes: int, N_colonnes: int, Nom_fichier: str = FILENAME) -> None:
    dim_global[0] = N_lignes
    dim_global[1] = N_colonnes

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


def generate_neighboors(Indice_ligne: int, Indice_colonne: int) -> List[List[int]]:
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
    
    print(liste_voisins)
    for i in range(len(liste_voisins)):
        liste_voisins[i] = str(liste_voisins[i][0]) + str(liste_voisins[i][1])
    
    print(liste_voisins)
    
    liste_clauses = []

    # Génération des combinaisons de taille Nb_voisins parmi les voisins
    if Nb_voisins <= 5:
        liste_clauses = cc.exactly_n(Nb_voisins, liste_voisins)
    else:
        for nbn in range(BROUHAHA, MAX_VOISINS + 1):
            liste_clauses += cc.exactly_n(nbn, liste_voisins)

    return liste_clauses


def main():
    initialisation_fichier(20, 20)
    print(entendre_voisins(1, 1, 0))
    return None


if __name__ == "__main__":
    print("Debut du programme")
    main()
    print("Fin du programme")
