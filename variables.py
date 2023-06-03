
from typing import List, Tuple, Dict, Set

# Variables globales
dim_global = [-1, -1]
liste_clauses_global = []
dict_pers = {}
dict_pers_inverse = {}

# Types Gophersat
LC = List[List[int]] # Liste de clauses
LL = List[int] # Liste de littéraux
PS = Tuple[int, int] # Position
LP = List[PS] # Liste de positions
DT = Dict[PS, str] # Dictionnaire de tuiles

ELEMENTS_TUILE = ["P", "G", "I"] # P = Personnage, G = Garde, I = Invite
NB_ELEMENTS_TUILE = ELEMENTS_TUILE.__len__()

# Constantes
FILENAME = "hitman_test.cnf"
BROUHAHA = 5
MAX_VOISINS = 25
MAX_OUIE = 2
MAX_VISION_GARDE = 2

# Variables pour les matrices
empty = " "
wall = "\u2588" + "\u2588" + "\u2588" + "\u2588"
# wall = "W"
Costume = "Cos"
Corde = "Cor"
Garde = "G"
Invite = "I"
Personne = "P"
Safe = "OK"
Target = "T"
MV = "MV"

GardeNord = "G" + "\u2191"
GardeSud = "G" + "\u2193"
GardeEst = "G" + "\u2192"
GardeOuest = "G" + "\u2190"
InviteNord = "I" + "\u2191"
InviteSud = "I" + "\u2193"
InviteEst = "I" + "\u2192"
InviteOuest = "I" + "\u2190"
Visited = "V"
