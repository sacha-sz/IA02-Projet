import subprocess
from variables import *


class Gophersat:
    def __init__(self, nb_ligne: int, nb_colonnes: int):
        self.nLitteraux = nb_colonnes * nb_ligne * len(ELEMENTS_TUILE)
        self.nClauses = 0
        self.clauses: set[tuple[int] | tuple[int, int, int] | tuple[int, int] | int] = set()
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

        # Initialisation des clauses pour qu’il y ait au moins un personnage par case et d’un seul type
        for i in range(nb_ligne):
            for j in range(nb_colonnes):
                self.clauses.add((-self.dVar[(i, j, "P")], self.dVar[(i, j, "G")], self.dVar[(i, j, "I")]))
                self.clauses.add((self.dVar[(i, j, "P")], -self.dVar[(i, j, "G")]))
                self.clauses.add((self.dVar[(i, j, "P")], -self.dVar[(i, j, "I")]))
                self.nClauses += 3

        self.write_file()

    def write_file(self, file_name: str = FILENAME, test: bool = False) -> None:
        with open(file_name, "w") as f:
            f.write(f"p cnf {self.nLitteraux} {self.nClauses + int(test)}\n")
            for clause in self.clauses:
                if type(clause) == int:
                    f.write(str(clause) + " 0\n")
                elif type(clause) == tuple:
                    f.write(" ".join(str(litteral) for litteral in clause) + " 0\n")

    def ajout_clauses_entendre(self, lp: List[Tuple[int, int]], nb_ouie: int) -> None:
        """
        À partir des positions environnantes, on ajoute les clauses pour que le nombre de personnages entendus soit
        égal à nb_ouie
        """

        if nb_ouie < 0 or nb_ouie > len(lp):
            return

        elif nb_ouie == 0:
            for t in lp:
                for elt in ELEMENTS_TUILE:
                    self.clauses.add((-self.dVar[(t[0], t[1], elt)]))
                    self.nClauses += 1

        elif nb_ouie < BROUHAHA:
            # Au moins et au plus nb_ouie personnages
            clause_exactly = exactly_n(nb_ouie, [self.dVar[(t[0], t[1], "P")] for t in lp])
            for clause in clause_exactly:
                self.clauses.add(clause)
            self.nClauses += len(clause_exactly)

        else:
            clauses_at_least = at_least_n(BROUHAHA, [self.dVar[(t[0], t[1], "P")] for t in lp])
            for clause in clauses_at_least:
                self.clauses.add(clause)
            self.nClauses += len(clauses_at_least)

            clauses_at_most = at_most_n(len(lp), [self.dVar[(t[0], t[1], "P")] for t in lp])
            for clause in clauses_at_most:
                self.clauses.add(clause)
            self.nClauses += len(clauses_at_most)

        self.write_file()

    def ajout_clauses_voir(self, res_liste: List[Tuple[int, int, str]]) -> None:
        """
        À partir des positions vues et de leur type, on ajoute les clauses pour que les positions vues soient correctes
        """
        for t in res_liste:
            self.pos_connues.append((t[0], t[1]))
            self.pos_inconnues = [pos for pos in self.pos_inconnues if pos not in self.pos_connues]

            if t[2] == 'G':
                self.clauses.add((self.dVar[(t[0], t[1], "G")]))
                self.clauses.add((self.dVar[(t[0], t[1], "P")]))
                self.clauses.add((-self.dVar[(t[0], t[1], "I")]))

                self.nClauses += 3
            elif t[2] == 'I':
                self.clauses.add((self.dVar[(t[0], t[1], "I")]))
                self.clauses.add((self.dVar[(t[0], t[1], "P")]))
                self.clauses.add((-self.dVar[(t[0], t[1], "G")]))
                self.nClauses += 3
            else:
                for elt in ELEMENTS_TUILE:
                    self.clauses.add((-self.dVar[(t[0], t[1], elt)]))
                    self.nClauses += 1

        self.write_file()

    def invite_max_trouve(self) -> None:
        """
        On a trouvé le nombre maximum d’invités et on ajoute dans les clauses que les autres cases ne le sont pas
        """
        for t in self.pos_inconnues:
            self.clauses.add((-self.dVar[(t[0], t[1], "I")]))
            self.nClauses += 1

        self.write_file()

    def garde_max_trouve(self) -> None:
        """
        On a trouvé le nombre maximum de gardes et on ajoute dans les clauses que les autres cases ne le sont pas
        """
        for t in self.pos_inconnues:
            self.clauses.add((-self.dVar[(t[0], t[1], "G")]))
            self.nClauses += 1

        self.write_file()

    def personne_max_trouve(self) -> None:
        """
        On a trouvé le nombre maximum de personnes et on ajoute dans les clauses que les autres cases ne le sont pas
        """
        for t in self.pos_inconnues:
            self.clauses.add((-self.dVar[(t[0], t[1], "P")]))
            self.clauses.add((-self.dVar[(t[0], t[1], "G")]))
            self.clauses.add((-self.dVar[(t[0], t[1], "I")]))
            self.nClauses += 3

        self.write_file()

    def test_personne(self, pos_test: Tuple[int, int]) -> int:
        """
        On teste si la position est une personne.

        Valeurs de retour :
        0 : inconnu
        1 : personne avec certitude
        -1 : il n’y a personne avec certitude
        """
        ret = 0
        temp_filename = "test.cnf"

        self.write_file(temp_filename, True)
        with open(temp_filename, "a") as f:
            f.write(str(-self.dVar[(pos_test[0], pos_test[1], "P")]) + " 0\n")

        res = subprocess.run(["gophersat", temp_filename], capture_output=True)
        res = res.stdout.decode("utf-8")

        if "UNSATISFIABLE" in res:
            ret = 1
        else:
            self.write_file(temp_filename, True)
            with open(temp_filename, "a") as f:
                f.write(str(self.dVar[(pos_test[0], pos_test[1], "P")]) + " 0\n")

            res = subprocess.run(
                ["gophersat", temp_filename], capture_output=True)
            res = res.stdout.decode("utf-8")

            if "UNSATISFIABLE" in res:
                ret = -1

        return ret

    def test_type(self, pos_test: Tuple[int, int, str]) -> bool:
        """
        On teste si la position est du type donné : G ou I
        On retourne True si c’est du type, False sinon
        """

        temp_filename = "test.cnf"
        self.write_file(temp_filename, True)
        with open(temp_filename, "a") as f:
            f.write(str(-self.dVar[(pos_test[0], pos_test[1], pos_test[2])]) + " 0\n")

        res = subprocess.run(["gophersat", temp_filename], capture_output=True)
        res = res.stdout.decode("utf-8")

        return "UNSATISFIABLE" in res
