from typing import List
from itertools import combinations

# Type alias pour les listes de clauses
LC = List[List[int]]

# Type alias pour les listes de litteraux
LL = List[int]

# Fonctions de base
def transform_to_negatif(liste: LL) -> LL:
	return [-x for x in liste]

def transform_to_positif(liste: LL) -> LL:
	return [abs(x) for x in liste]

# Fonctions combinant les litteraux
def exactly_n(n: int, liste: LL) -> LC:
	if n > len(liste):
		raise ValueError("n doit etre inferieur ou egal a la taille de la liste")

	if n == len(liste):
		return [liste]	
	elif n == 0:
		return [[-x] for x in liste]

	litteraux_negatifs = []
	litteraux_positifs = []
	clauses = []

	for comb in combinations(liste, n):
		litteraux_positifs.append(list(comb))
		litteraux_negatifs.append([-x for x in liste if x not in list(comb)])

	for i in range(len(litteraux_negatifs)):
		neg = transform_to_negatif(litteraux_positifs[i])
		for litteral in litteraux_negatifs[i]:
			cl = neg + [litteral]
			cl.sort()	
			if cl not in clauses:
				clauses.append(cl)

	for i in range(len(litteraux_positifs)):
		pos = transform_to_positif(litteraux_negatifs[i]) 
		for litteral in litteraux_positifs[i]:
			cl = pos + [litteral]
			cl.sort()
			if cl not in clauses:
				clauses.append(cl)

	return clauses
