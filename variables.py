from hitman import *
from typing import List, Tuple, Dict
from itertools import combinations

# ------------------------------------------#
#              CONSTANTES                   #
# ------------------------------------------#

LC = List[List[int]]  # Liste de clauses
LL = List[int]  # Liste de littéraux
PS = Tuple[int, int]  # Position
LP = List[PS]  # Liste de positions
PST = Tuple[int, int, str]  # Position et son type
LPS = List[PST]  # Liste de positions et de leurs types
DT = Dict[PS, str]  # Dictionnaire de tuiles

ELEMENTS_TUILE = ["P", "G", "I"]  # P = Personnage, G = Garde, I = Invite
NB_ELEMENTS_TUILE = ELEMENTS_TUILE.__len__()

# Constantes
FILENAME = "hitman.cnf"
BROUHAHA = 5
MAX_VOISINS = 25
MAX_OUIE = 2
MAX_VISION_GARDE = 2
MAX_VISION_INVITE = 1

# Variables pour les matrices
empty = " "  # "E"
wall = "\u2588" + "\u2588" + "\u2588" + "\u2588"  # "W"
Costume = "C"
Corde = "R"

Target = "T"
DEAD = "X"

GardeNord = "G" + "\u2191"
GardeSud = "G" + "\u2193"
GardeEst = "G" + "\u2192"
GardeOuest = "G" + "\u2190"

InviteNord = "I" + "\u2191"
InviteSud = "I" + "\u2193"
InviteEst = "I" + "\u2192"
InviteOuest = "I" + "\u2190"

# Variables pour SAT
SAT_GARDE = "G"
SAT_INVITE = "I"
SAT_PERSONNE = "P"
SAT_PROBA_PERSONNE = "P?"
SAT_NP = " "

# ------------------------------------------#
#              UTILITAIRE                   #
#                HITMAN                     #
# ------------------------------------------#
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]


def calculate_heuristic(current, goal):
    # Manhattan distance heuristic
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def convert(var) -> HC:
    if var == empty:
        return HC.EMPTY
    elif var == wall:
        return HC.WALL
    elif var == GardeEst:
        return HC.GUARD_E
    elif var == GardeNord:
        return HC.GUARD_N
    elif var == GardeOuest:
        return HC.GUARD_W
    elif var == GardeSud:
        return HC.GUARD_S
    elif var == InviteEst:
        return HC.CIVIL_E
    elif var == InviteNord:
        return HC.CIVIL_N
    elif var == InviteOuest:
        return HC.CIVIL_W
    elif var == InviteSud:
        return HC.CIVIL_S
    elif var == Costume:
        return HC.SUIT
    elif var == Target:
        return HC.TARGET
    elif var == Corde:
        return HC.PIANO_WIRE
    else:
        raise ValueError("Valeur inconnue : " + str(var))


def case_devant_nous(x: int, y: int, orientation: HC) -> Tuple[int, int]:
    if orientation == HC.E:
        return x, y + 1

    elif orientation == HC.W:
        return x, y - 1

    elif orientation == HC.N:
        return x - 1, y

    elif orientation == HC.S:
        return x + 1, y


# ------------------------------------------#
#              UTILITAIRE                   #
#              Gophersat                    #
# ------------------------------------------#

def at_least_n(n: int, liste_litteraux: List[int]):
    clauses = set()
    for c in combinations(liste_litteraux, len(liste_litteraux) - (n - 1)):
        clauses.add(tuple(c))
    return clauses


def at_most_n(n: int, liste_litteraux: List[int]):
    clauses = set()
    vars_neg = [i * -1 for i in liste_litteraux]
    for c in combinations(vars_neg, n + 1):
        clauses.add(tuple(c))
    return clauses


def exactly_n(n: int, liste_litteraux: List[int]):
    if not liste_litteraux:
        return []
    if n == 0:
        return at_most_n(0, liste_litteraux)
    elif n == len(liste_litteraux):
        return at_least_n(n, liste_litteraux)
    clauses = at_most_n(n, liste_litteraux)
    for cl in at_least_n(n, liste_litteraux):
        clauses.add(cl)
    return clauses
