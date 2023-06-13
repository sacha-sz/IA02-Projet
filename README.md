# IA02-Projet
:robot: IA capable de jouer à Hitman

Ce projet a été réalisé dans le cadre de l'UV IA02 à l'UTC.
Binôme : Lucas, Sacha.
Le projet consiste à permettre à l'agent Hitman de se déplacer dans une map 2D pour tuer une cible.
Au début Hitman ne connait pas la map. Il doit l'explorer.
Nous disposons d'une matrice des regards (attribut ```self.mat_regard```) qui indique dans quelles directions regardent les gardes et civils qu'on a trouvé.
Nous avons aussi une matrice de connaissance (attribut ```self.mat_connue```) qui contient toutes les informations sur la map qu'on a découvert.
L'objectif est réalisé en deux phases : 

### Phase 1 :
L'agent doit se déplacer dans la map pour découvrir toute la map.
On utilise pour cela du SAT.

On explore la map en trouvant l'inconnu le plus proche et l'agent essaye de se rapprocher de cette case pour la voir.
Le chemin est généré en utilisant l'algorithme A*. On prend en compte les regards des gardes si on les connait déjà. On prend bien-sûr en compte le coup des déplacements.

Pour avancer il faut être bien orienté. La case où on veut aller doit être devant nous.
Des rotations peuvent donc être nécessaire. Une methode, ```best_turn```, permet de s'orienter vers la case
en faisant le moins de rotations possibles.



### Phase 2 :
L'agent doit se déplacer dans la map pour tuer la cible.
On utilise pour cela l'algorithme A*. Plusieurs optimisations sont faites.
Tout d'abord on regarde le chemin qui coute le moins pour tuer la cible parmi ces chemins :

* chemin 1 : aller de la case départ puis à la case où se trouve et ensuite aller à la case de la cible pour la tuer et revenir à la case de départ
* chemin 2 : aller de la case départ à la case du costume puis aller à la case de la corde puis aller la case cible pour la tuer et revenir à la case de départ
* chemin 3 : aller de la case départ à la case de la corde puis aller à la case du costume puis aller la case cible pour la tuer et revenir à la case de la corde puis aller à la case de départ


Lorsqu'on a le costume on prend en compte d'essayer de mettre le costume lorsqu'on nous voit pas. 
De plus lorsqu'on a mis le costume on prend en compte qu'on n'est pas vu par un garde lorsqu'on passe devant
son champ de vision.

#### STRIPS :

##### Fluents : 
Orientation(actuelle), Position(Hitman, x, y), Sur_case(cible, x, y), Sur_case(corde_de_piano, x, y), Sur_case(costume, x, y), Sur_case(civil, x, y), Sur_case(garde, x, y), Regarde(vous, garde), Regarde(vous, civil), Regarde(vous, Hitman), Possède(corde_de_piano), Possède(costume), Avance_possible(x, y), Garde_present(Garde, x, y), Civil_present(Civil, x, y)

Init(
    Position(Hitman, 0,0)
)

Goal (
    ¬Sur_case(cible, x, y)
)

##### Actions :

* Action(tourner_horaire, 
PRECOND: Orientation(actuelle) = nord, 
EFFECT: Orientation(est) )

* Action(tourner_horaire, 
PRECOND: Orientation(actuelle) = est, 
EFFECT: Orientation(sud) )

* Action(tourner_horaire, 
PRECOND: Orientation(actuelle) = sud, 
EFFECT: Orientation(ouest) )

* Action(tourner_horaire, 
PRECOND: Orientation(actuelle) = ouest, 
EFFECT: Orientation(nord) )

* Action(tourner_antihoraire, 
PRECOND: Orientation(actuelle) = nord, 
EFFECT: Orientation(ouest) )

* Action(tourner_antihoraire, 
PRECOND: Orientation(actuelle) = ouest, 
EFFECT: Orientation(sud) )

* Action(tourner_antihoraire, 
PRECOND: Orientation(actuelle) = sud, 
EFFECT: Orientation(est) )

* Action(tourner_antihoraire, 
PRECOND: Orientation(actuelle) = est, 
EFFECT: Orientation(nord) )

* Action(avancer(x, y, x+1, y), 
PRECOND: Orientation(actuelle) = nord ∧ Avance_possible(x+1, y), 
EFFECT: Position(Hitman, x+1, y), ¬Position(Hitman, x, y) )

* Action(avancer(x, y, x-1, y), 
PRECOND: Orientation(actuelle) = sud ∧ Avance_possible(x-1, y), 
EFFECT: Position(Hitman, x-1, y), ¬Position(Hitman, x, y) )

* Action(avancer(x, y, x, y+1), 
PRECOND: Orientation(actuelle) = est ∧ Avance_possible(x, y+1), 
EFFECT: Position(Hitman, x, y+1), ¬Position(Hitman, x, y) )

* Action(avancer(x, y, x, y-1), 
PRECOND: Orientation(actuelle) = ouest ∧ Avance_possible(x, y-1), 
EFFECT: Position(Hitman, x, y-1), ¬Position(Hitman, x, y) )

* Action(tuer_cible(Hitman, cible, x,y), 
PRECOND: Position(Hitman, x, y) ∧ Sur_case(cible, x, y) ∧ Possède(corde_de_piano), 
EFFECT: ¬Sur_case(cible, x, y), ¬Position(Hitman, x, y) )

* Action(neutraliser_garde(Hitman, Garde, x, y), 
PRECOND: Position(Hitman, x, y) ∧ Garde_present(Garde, x, y) ∧ ¬Regarde(vous, garde), 
EFFECT: ¬Garde_present(Garde, x, y))

* Action(neutraliser_civil(Hitman, Civil, x, y), 
PRECOND: Position(Hitman, x, y) ∧ Civil_present(Civil, x, y) ∧ ¬Regarde(vous, civil), E
FFECT: ¬Civil_present(Civil, x, y) )

* Action(prendre_corde(Hitman, corde_de_piano, x, y), 
PRECOND: Position(Hitman, x, y) ∧ Sur_case(corde_de_piano, x, y), 
EFFECT: Possède(corde_de_piano) ∧ ¬Sur_case(corde_de_piano, x, y))

* Action(prendre_costume(Hitman, costume, x, y), 
PRECOND: Position(Hitman, x, y) ∧ Sur_case(costume, x, y), 
EFFECT: Possède(costume) ∧ ¬Sur_case(costume, x, y) )

