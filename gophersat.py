from variables import *
from typing import List, Tuple, Dict, Set
from itertools import combinations


class Gophersat:
    def __init__(self, max_invites: int, max_gardes: int, nb_ligne: int, nb_colonnes: int):
        self.maxInv = max_invites
        self.maxGar = max_gardes
        self.nLig = nb_ligne
        self.nCol = nb_colonnes
        self.maxPers = max_invites + max_gardes
        self.nLitteraux = nb_colonnes * nb_ligne 
        self.nClauses = 0
        self.clauses: LC = []
        # Dictionnaire des variables et de leur numéro
        self.dVar: Dict[str, int] = {}
        self.litGarde: List[int] = []  # Liste des littéraux des gardes
        self.litInvite: List[int] = []  # Liste des littéraux des invités
        self.litPers: List[int] = []  # Liste des littéraux des personnages

        # Initialisation des littéraux
        for i in range(nb_ligne):
            for j in range(nb_colonnes):
                self.dVar[str(i) + str(j) + "P"] = self.dVar.__len__() + 1
                """
                for elt in ELEMENTS_TUILE:
                    self.dVar[str(i) + str(j) + elt] = self.dVar.__len__() + 1
                    if elt == "G":
                        self.litGarde.append(self.dVar[str(i) + str(j) + elt])
                    elif elt == "I":
                        self.litInvite.append(self.dVar[str(i) + str(j) + elt])
                    else:
                        self.litPers.append(self.dVar[str(i) + str(j) + elt])

        # Exactement max_gardes parmis l'ensemble des positions
        if max_gardes == 0:
            self.clauses.append([[-x] for x in self.litGarde])
            self.nClauses += len(self.litGarde)
        elif max_gardes == len(self.litGarde):
            self.clauses.append([x] for x in self.litGarde)
            self.nClauses += len(self.litGarde)
        else:
            for c in combinations(self.litGarde, len(self.litGarde) - (max_gardes - 1)):
                self.clauses.append(list(c))
                self.nClauses += 1

            varsNeg = [-i for i in self.litGarde]
            for c in combinations(varsNeg, max_gardes+1):
                self.clauses.append(list(c))
                self.nClauses += 1
            

        # Exactement max_invites parmis l'ensemble des positions
        if max_invites == 0:
            self.clauses.append([[-x] for x in self.litInvite])
            self.nClauses += len(self.litInvite)
        elif max_invites == len(self.litInvite):
            self.clauses.append([x] for x in self.litInvite)
            self.nClauses += len(self.litInvite)
        else:
            for c in combinations(self.litInvite, len(self.litInvite) - (max_invites - 1)):
                self.clauses.append(list(c))
                self.nClauses += 1

            varsNeg = [-i for i in self.litInvite]
            for c in combinations(varsNeg, max_invites+1):
                self.clauses.append(list(c))
                self.nClauses += 1

        # Ajouter pour chaque case l'équivalence  :
        # P <=> (G ou I)
        for i in range(nb_ligne):
            for j in range(nb_colonnes):
                self.clauses.append([-self.dVar[str(i) + str(j) + "P"], self.dVar[str(
                    i) + str(j) + "G"], self.dVar[str(i) + str(j) + "I"]])
                self.clauses.append(
                    [self.dVar[str(i) + str(j) + "P"], -self.dVar[str(i) + str(j) + "G"]])
                self.clauses.append(
                    [self.dVar[str(i) + str(j) + "P"], -self.dVar[str(i) + str(j) + "I"]])
        """
        
        print(self.dVar)
        self.write_file("test.cnf")

    def write_file(self, file_name: str):
        with open(file_name, "w") as f:
            f.write("p cnf " + str(self.nLitteraux) +
                    " " + str(self.nClauses) + "\n")
            for clause in self.clauses:
                for litteral in clause:
                    f.write(str(litteral) + " ")
                f.write("0\n")

def main():
    gophersat = Gophersat(3, 3, 9, 9)


if __name__ == "__main__":
    main()
