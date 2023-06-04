
from typing import List, Tuple, Dict


# Types Gophersat
LC = List[List[int]] # Liste de clauses
LL = List[int] # Liste de littéraux
PS = Tuple[int, int] # Position
LP = List[PS] # Liste de positions
PST = Tuple[int, int, str] # Position et son type
LPS = List[PST] # Liste de positions et de leurs types
DT = Dict[PS, str] # Dictionnaire de tuiles

ELEMENTS_TUILE = ["P", "G", "I"] # P = Personnage, G = Garde, I = Invite
NB_ELEMENTS_TUILE = ELEMENTS_TUILE.__len__()

# Constantes
FILENAME = "hitman.cnf"
BROUHAHA = 5
MAX_VOISINS = 25
MAX_OUIE = 2
MAX_VISION_GARDE = 2

# Variables pour les matrices
empty = " " # "E"
wall = "\u2588" + "\u2588" + "\u2588" + "\u2588" # "W"
Costume = "C"
Corde = "R"
Target = "T"

Personne = "P"

Garde = "G"
GardeNord = "G" + "\u2191"
GardeSud = "G" + "\u2193"
GardeEst = "G" + "\u2192"
GardeOuest = "G" + "\u2190"

Invite = "I"
InviteNord = "I" + "\u2191"
InviteSud = "I" + "\u2193"
InviteEst = "I" + "\u2192"
InviteOuest = "I" + "\u2190"
