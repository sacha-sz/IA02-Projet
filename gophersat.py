import subprocess
from variables import *
from typing import List, Tuple, Dict, Set
from itertools import combinations


class Gophersat:
    def __init__(self, nb_ligne: int, nb_colonnes: int):
        self.nLitteraux = nb_colonnes * nb_ligne * len(ELEMENTS_TUILE)
        self.nClauses = 0
        self.clauses: LC = []
        self.pos_connues: List[Tuple[int, int]] = []
        self.pos_inconnues: List[Tuple[int, int]] = []

        # Initialisation du dictionnaire liant les positions aux variables et vice-versa
        self.dVar: Dict[Tuple[int, int, str], int] = {}
        self.dVarInv: Dict[int, Tuple[int, int, str]] = {}

        # Initialisation des littéraux
        for i in range(nb_ligne):
            for j in range(nb_colonnes):
                self.pos_inconnues.append((i, j))
                for elt in ELEMENTS_TUILE:
                    self.dVar[(i, j, elt)] = len(self.dVar) + 1
                    self.dVarInv[len(self.dVar)] = (i, j, elt)

        # Initialisation des clauses pour qu'il y ait au moins un personnage par case et d'un seul type
        for i in range(nb_ligne):
            for j in range(nb_colonnes):
                self.clauses.append(
                    [-self.dVar[(i, j, "P")], self.dVar[(i, j, "G")], self.dVar[(i, j, "I")]])
                self.clauses.append(
                    [self.dVar[(i, j, "P")], -self.dVar[(i, j, "G")]])
                self.clauses.append(
                    [self.dVar[(i, j, "P")], -self.dVar[(i, j, "I")]])
                self.nClauses += 3
        self.write_file()

    def write_file(self, file_name: str = "test.cnf", test: bool = False) -> None:
        with open(file_name, "w") as f:
            if test:
                f.write("p cnf " + str(self.nLitteraux) +
                        " " + str(self.nClauses + 1) + "\n")
            else:
                f.write("p cnf " + str(self.nLitteraux) +
                        " " + str(self.nClauses) + "\n")
            for clause in self.clauses:
                for litteral in clause:
                    f.write(str(litteral) + " ")
                f.write("0\n")

    def ajout_clauses_entendre(self, lp: List[Tuple[int, int]], nb_ouie: int) -> None:
        """
        A partir des positions environnantes, on ajoute les clauses pour que le nombre de personnages entendus soit égal à nb_ouie
        """
        if nb_ouie < 0 or nb_ouie > len(lp):
            print("Je fais rien car j'entends rien")
        elif nb_ouie == 0:
            print("Je n'entends personne")
            for t in lp:
                self.clauses.append([-self.dVar[(t[0], t[1], "P")]])
                self.nClauses += 1
        elif nb_ouie < BROUHAHA:
            print("Je peux entendre", nb_ouie, "personnes avec certitude")

            # Liste des litteraux correspondant aux triplets (i, j, "P")
            liste_litteraux = []
            for t in lp:
                liste_litteraux.append(self.dVar[(t[0], t[1], "P")])

            # On ajoute les clauses
            for combi in combinations(liste_litteraux, len(lp) - nb_ouie + 1):
                self.clauses.append(list(combi))
                self.nClauses += 1

            liste_neg = [-x for x in liste_litteraux]
            for combi in combinations(liste_neg, nb_ouie + 1):
                self.clauses.append(list(combi))
                self.nClauses += 1
            self.write_file()

        else:
            print("Je peux entendre entre ", nb_ouie,
                    "et", len(lp), "personnes")
            liste_triplet = []  # Liste des triplets au format (i, j, "P")
            for t in lp:
                liste_triplet.append((t[0], t[1], "P"))

            liste_litteraux = []  # Liste des litteraux correspondant aux triplets
            for t in liste_triplet:
                liste_litteraux.append(self.dVar[t])

            # On ajoute les clauses

            # Au moins len(lp) - nb_ouie + 1 personnes
            combi_l = combinations(liste_litteraux, len(lp) - nb_ouie + 1)
            for combi in combi_l:
                self.clauses.append(list(combi))
                self.nClauses += 1

            # Au plus len(lp) personnes
            liste_neg = [-x for x in liste_litteraux]
            combi_l = combinations(liste_neg, len(lp))
            for combi in combi_l:
                self.clauses.append(list(combi))
                self.nClauses += 1
            self.write_file()

    def ajout_clauses_voir(self, res_liste: List[Tuple[int, int, str]]) -> None:
        """
        A partir des positions vues et de leur type, on ajoute les clauses pour que les positions vues soient correctes
        """
        for t in res_liste:
            self.pos_connues.append((t[0], t[1]))
            if t[2] == "G" or t[2] == "I":
                self.clauses.append([self.dVar[t]])
                self.nClauses += 1
            else:
                self.clauses.append([-self.dVar[(t[0], t[1], "P")]])
                self.nClauses += 1
        self.write_file()

    def invite_max_trouve(self) -> None:
        """
        On a trouvé le nombre maximum d'invités et on ajoute dans les clauses que les autres cases ne le sont pas
        """
        for t in self.pos_inconnues:
            self.clauses.append([-self.dVar[(t[0], t[1], "I")]])
            self.nClauses += 1
        self.write_file()

    def garde_max_trouve(self) -> None:
        """
        On a trouvé le nombre maximum de gardes et on ajoute dans les clauses que les autres cases ne le sont pas
        """
        for t in self.pos_inconnues:
            self.clauses.append([-self.dVar[(t[0], t[1], "G")]])
            self.nClauses += 1
        self.write_file()
    
    def personne_max_trouve(self) -> None:
        """
        On a trouvé le nombre maximum de personnes et on ajoute dans les clauses que les autres cases ne le sont pas
        """
        for t in self.pos_inconnues:
            self.clauses.append([-self.dVar[(t[0], t[1], "P")]])
            self.nClauses += 1
        self.write_file()

    def test_personne(self, pos_test: Tuple[int, int]) -> int:
        """
        On teste si la position est une personne
        Valeurs de retour :
        0 : inconnu
        1 : personne avec certitude
        -1 : pas personne avec certitude
        """
        ret = 0
        TEMP_FILENAME = "test_temp.cnf"

        self.write_file(TEMP_FILENAME, True)
        with open(TEMP_FILENAME, "a") as f:
            f.write(str(-self.dVar[(pos_test[0], pos_test[1], "P")]) + " 0\n")

        res = subprocess.run(["gophersat", TEMP_FILENAME], capture_output=True)
        res = res.stdout.decode("utf-8")

        if "UNSATISFIABLE" in res:
                ret = 1
        else:
            self.write_file(TEMP_FILENAME, True)
            with open(TEMP_FILENAME, "a") as f:
                f.write(
                    str(self.dVar[(pos_test[0], pos_test[1], "P")]) + " 0\n")

            res = subprocess.run(
                ["gophersat", TEMP_FILENAME], capture_output=True)
            res = res.stdout.decode("utf-8")

            if "UNSATISFIABLE" in res:
                ret = -1
                                
        return ret

    def test_type(self, pos_test: Tuple[int, int, str]) -> bool:
        """
        On teste si la position est du type donné : G ou I
        On retourne True si c'est du type, False sinon
        """
        
        TEMP_FILENAME = "test_temp.cnf"
        self.write_file(TEMP_FILENAME, True)
        with open(TEMP_FILENAME, "a") as f:
            f.write(str(-self.dVar[(pos_test[0], pos_test[1], pos_test[2])]) + " 0\n")
            
        res = subprocess.run(["gophersat", TEMP_FILENAME], capture_output=True)
        res = res.stdout.decode("utf-8")
        
        if "UNSATISFIABLE" in res:
            return True
        else:
            return False
    
def main():
    go = Gophersat(3, 3)

    go.ajout_clauses_entendre([(0, 0), (0, 1), (0, 2),
                                (1, 0), (1, 1), (1, 2),
                                (2, 0), (2, 1), (2, 2)], 2)

    go.ajout_clauses_voir([(0, 0, "E"), (1, 0, "E"), (2, 0, "E")])
    go.ajout_clauses_voir([(0, 1, "E"), (1, 1, "E"), (2, 1, "E")])
    go.ajout_clauses_voir([(0, 2, "E")])
    
    ret = go.test_personne((2, 2))
    print(ret)


if __name__ == "__main__":
    main()
