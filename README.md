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
