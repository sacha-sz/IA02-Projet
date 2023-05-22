
from typing import List, Tuple, Dict, Set

# Variables globales
dim_global = [-1, -1]
liste_clauses_global = []
dict_pers = {}
dict_pers_inverse = {}


# Constantes
FILENAME = "hitman_test.cnf"
BROUHAHA = 6
MAX_VOISINS = 25
MAX_OUIE = 2
MAX_VISION_GARDE = 2

# Variables pour les matrices
empty = "E"
wall = "W"
Costume = "Cos"
Corde = "Cor"
Garde = "G"
Invite = "I"
Personne = "P"
Safe = "OK"
MV = "MV"

GardeNord = "GN"
GardeSud = "GS"
GardeEst = "GE"
GardeOuest = "GO"
InviteNord = "IN"
InviteSud = "IS"
InviteEst = "IE"
InviteOuest = "IO"
Visited = "V"

# Types alias
LC = List[List[int]]
LL = List[int]
