from typing import List
from itertools import combinations

Clause = List[int]

#retourne l'ensemble de clause traitant la contrainte : "au moins n variables vraies dans la liste"
def at_least_n(n: int, vars: List[int]) -> List[Clause]:
	clauses = []
	for c in combinations(vars, len(vars) -(n-1)):
		clauses.append(list(c))
	return clauses

#retourne l'ensemble de clause traitant la contrainte : "au plus n variables vraies dans la liste"
def at_most_n(n: int, vars: List[int]) -> List[Clause]:
	clauses = []
	varsNeg = [i * -1 for i in vars]
	for c in combinations(varsNeg, n+1):
		clauses.append(list(c))
	return clauses

#retourne l'ensemble de clause traitant la contrainte : "exactement n variables vraies dans la liste"
def exactly_n(n: int, vars: List[int]) -> List[Clause]:
	if vars == []:
		return []
	if n==0:
		return at_most_n(0, vars)
	if n==len(vars):
		return at_least_n(n, vars)
	clauses = at_most_n(n, vars)
	clauses += at_least_n(n, vars)
	return clauses
