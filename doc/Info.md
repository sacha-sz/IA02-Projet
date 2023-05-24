## Gophersat
####  Pour une case : 
- Garde : ==G== :
- Invité : ==I==
- Personne : ==P==

#### Règles initiales :
- nb_garde parmis ensemble MAP
- nb_invité parmis ensemble MAP
- nb_personne = nb_garde + nb_invité ensemble MAP

#### Règle déduite :
- vu nb_garde ➡ toutes les personnes déduites restantes ou à déduire seront des invités
- vu nb_invité ➡ toutes les personnes déduites restantes ou à déduire seront des gardes
- vu nb_personnes ➡tout ce qui restera sera un costume ou une corde ou ==MV==

#### Utilisation :



### Python

#### Matrice

Pour une case : 
- Rien : ==E==
- Mur : ==W==
- Costume : ==Cos==
- Corde : ==Cor==
- Garde : ==G== :
	- ==GN==
	- ==GS==
	- ==GE==
	- ==GO==
- Invité : ==I==
	- ==IN==
	- ==IS==
	- ==IO==
	- ==IE==
- Personne : ==P==
- Safe : ==OK==
- Cout : 
	- ==C5==
	- ==C10==
	- ==C15==
	- ==C20==
- Visited : ==V==


- Impossible :
	- <mark style="background: #ADCCFFA6;">Phase 1</mark> :
		- G + ses directions
		- Mur
		- C20
	- <mark style="background: #ADCCFFA6;">Phase 2 </mark> :
		- Mur