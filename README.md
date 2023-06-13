# IA02-Projet
:robot: IA capable de jouer à Hitman

Ce projet a été réalisé dans le cadre de l'UV IA02 à l'UTC.
Binôme : Lucas, Sacha.
Le projet consiste à permettre à l'agent Hitman de se déplacer dans une map 2D pour tuer une cible.
Au début Hitman ne connait même pas la map. Il doit l'explorer.
Nous disposons d'une matrice des regards qui indique dans quelles directions regardent les gardes et civils 
qu'on a trouvé.
Nous avons aussi une matrice de connaissance qui contient toutes les informations sur la map qu'on a découvert.
L'objectif est réalisé en deux phases : 

### Phase 1 :
L'agent doit se déplacer dans la map pour découvrir toute la map.
On utilise pour cela du SAT.

On explore la map en trouvant l'inconnu le plus proche et l'agent essaye de se rapprocher de cette case
en utilisant l'algorithme A*.



### Phase 2 :
L'agent doit se déplacer dans la map pour tuer la cible.
On utilise pour cela l'algorithme A*. Plusieurs optimisations sont faites.
Tout d'abord on regarde le chemin qui coute le moins pour tuer la cible parmi ces chemins :
-chemin 1 : aller de la case départ puis à la case où se trouve et ensuite aller à la case de la cible pour la tuer et revenir à la case de départ
-chemin 2 : aller de la case départ à la case du costume puis aller à la case de la corde puis aller la case cible pour la tuer et revenir à la case de départ
-chemin 3 : aller de la case départ à la case de la corde puis aller à la case du costume puis aller la case cible pour la tuer et revenir à la case de la corde puis aller à la case de départ

Lorsqu'on a le costume on prend en compte d'essayer de mettre le costume lorsqu'on nous voit pas. 
De plus lorsqu'on a mis le costume on prend en compte qu'on n'est pas vu par un garde lorsqu'on passe devant
son champ de vision.

#### STRIPS :
##### Fluents :

* Orientation(actuelle) : représente l'orientation actuelle (par exemple, nord, sud, est, ouest).
* Position(Hitman, x, y) : représente la position actuelle du personnage avec les coordonnées (x, y) dans l'environnement.
* Avance_possible(x, y) : indique si l'avancée depuis la position (x, y) dans la direction actuelle est possible.
* Possède(corde_de_piano) : indique si le personnage possède la corde de piano.
* Sur_case(cible, x, y) : indique si le personnage se trouve sur la même case que la cible avec les coordonnées (x, y).
* Regarde(garde) : indique si le personnage regarde le garde.
* Regarde(vous, garde) : indique si le garde vous regarde.
* Regarde(civil) : indique si le personnage regarde le civil.
* Regarde(vous, civil) : indique si le civil vous regarde.
* Costume_détenu : représente le costume que le personnage possède.
* Possède(arme) : indique si le personnage possède une arme (corde de piano)
* Case_vide(x,y)
* Civil_present(Civil, x,y)
* Garde_present(Garde, x,y)






Init(Orientation(nord) ∧ Position(x, y) ∧ Avance_possible ∧ ¬Possède(corde_de_piano) ∧ ¬Sur_case(cible) ∧ Costume_détenu(aucun) ∧ ¬Possède(arme))


Goal : tuer la cible et revenir à la case départ
Goal(
¬Sur_case(cible, x, y) ∧ Position(Hitman, 0, 0)
)

##### Actions 
* Actions (manque les actions pour le costume et l'arme) : 
    Action(tourner_horaire,
    PRECOND: Orientation(actuelle) = nord,
    EFFECT: Orientation(est)
    )
* Action(tourner_horaire,
PRECOND: Orientation(actuelle) = est,
EFFECT: Orientation(sud)
)
* Action(tourner_horaire,
PRECOND: Orientation(actuelle) = sud,
EFFECT: Orientation(ouest)
)

* Action(tourner_horaire,
PRECOND: Orientation(actuelle) = ouest,
EFFECT: Orientation(nord)
)

* Action(tourner_antihoraire,
PRECOND: Orientation(actuelle) = nord,
EFFECT: Orientation(ouest)
)

* Action(tourner_antihoraire,
PRECOND: Orientation(actuelle) = ouest,
EFFECT: Orientation(sud)
)

* Action(tourner_antihoraire,
PRECOND: Orientation(actuelle) = sud,
EFFECT: Orientation(est)
)

* Action(tourner_antihoraire,
PRECOND: Orientation(actuelle) = est,
EFFECT: Orientation(nord)
)

* Action(avancer(x, y, x+1, y),
PRECOND: Orientation(actuelle) = nord ∧ Avance_possible(x+1, y),
EFFECT: Position(Hitman, x+1, y)
)

* Action(avancer(x, y, x-1, y),
PRECOND: Orientation(actuelle) = sud ∧ Avance_possible(x-1, y),
EFFECT: Position(Hitman, x-1, y)
)

* Action(avancer(x, y, x, y+1),
PRECOND: Orientation(actuelle) = est ∧ Avance_possible(x, y+1),
EFFECT: Position(Hitman, x, y+1)
)

* Action(avancer(x, y, x, y-1),
PRECOND: Orientation(actuelle) = ouest ∧ Avance_possible(x, y-1),
EFFECT: Position(Hitman, x, y-1)
)

* Action(tuer_cible,
PRECOND: Position(Hitman, x, y) ∧ Sur_case(cible, x, y) ∧ Possède(corde_de_piano),
EFFECT: ¬Sur_case(cible, x, y)
)

* Action(neutraliser_garde,
PRECOND: Position(Hitman, x, y) ∧ Garde_present(Garde, x, y) ∧ ¬Regarde(vous, garde) ∧ Case_vide(x, y+1),
EFFECT: ¬Garde_present(Garde, x, y) ∧ Case_vide(x, y+1)
)

* Action(neutraliser_civil,
PRECOND: Position(Hitman, x, y) ∧ Civil_present(Civil, x, y) ∧ ¬Regarde(vous, civil) ∧ Case_vide(x, y+1),
EFFECT: ¬Civil_present(Civil, x, y) ∧ Case_vide(x, y+1)
)
