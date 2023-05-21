## Gophersat
####  Pour une case : 
- Rien : ==M==
- Mur : ==W==
- Rien ou Mur : ==MV==
- Costume : ==Cos==
- Corde : ==Cor==
- Garde : ==G== :
- Invité : ==I==
- Personne : ==P==
- Safe : ==S== 

#### Règles initiales :
- Unique de Cor et Cos dans la MAP
- nb_garde parmis ensemble MAP
- nb_invité parmis ensemble MAP
- nb_personne = nb_garde + nb_invité ensemble MAP
- MV $<=>$ Rien ou mur par case
- Safe <=>  Rien, Invité, Corde, Costume

#### Règle déduite :
- trouvé costume ➡ il n'est plus ailleurs
- trouvé corde ➡ elle n'est plus ailleurs
- vu nb_garde ➡ toutes les personnes déduites restantes ou à déduire seront des invités
- vu nb_invité ➡ toutes les personnes déduites restantes ou à déduire seront des gardes
- vu nb_personnes ➡tout ce qui restera sera un costume ou une corde ou ==MV==

<mark style="background: #FF5582A6;">- Comment distinguer mur de rien ?</mark>

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