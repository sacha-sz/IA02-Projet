# IA02-Projet
:gun: :robot: :left_right_arrow: :ninja: IA capable de jouer à Hitman
```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⠤⠤⠤⠤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠶⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣤⣶⡶⣶⢦⠀⠀⠀⠀⠀⠀⠀⡾⠀⠀⠀⢀⣠⠀⠀⠀⠀⠀⠀⠀⠠⢤⣀⠀⠀⠸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠸⡏⠁⣠⡤⠾⣆⠀⠀⠀⠀⠀⢸⡇⢠⠖⣾⣭⣀⡀⠀⠀⠀⠀⠀⠀⣀⣠⣼⡷⢶⡀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢹⣿⠋⠈⣩⢿⡄⠀⠀⠀⠀⣾⠀⣿⠀⠀⠉⠉⠚⠻⠿⠶⠾⠿⠛⢋⠉⠁⠀⠈⡇⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⢯⣉⠟⠛⣲⢷⡀⠀⠀⠀⡿⠀⢻⣄⡀⠀⠀⠀⠀⢀⡴⠂⣀⠴⠃⠀⠀⢀⣰⠇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⡏⢒⡶⠧⢬⣧⠀⠀⠀⡇⠀⢸⡏⠉⣷⣶⣲⠤⢤⣶⣯⡥⠴⣶⣶⣎⠉⢻⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⡷⠶⣤⣏⣙⡆⠀⠀⡇⠀⢸⡆⠀⠑⢆⣩⡿⣖⣀⣰⡶⢯⣁⡴⠃⠀⣸⡄⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢧⠾⢥⣰⣟⣹⡄⠀⣧⠀⣼⠘⢦⣠⠴⠛⠋⠉⠉⠉⠉⠛⠳⢤⣀⡴⢻⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣇⣼⣋⣩⡏⣳⠀⢻⡀⢸⡴⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣼⡇⣶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⣤⢾⣡⣾⣽⣷⢼⡇⢿⡄⠀⠀⠀⠀⠠⣄⡀⢀⡀⠀⠀⠀⠀⠀⢸⠇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣀⣿⠿⣓⣋⡥⣿⠟⢷⠘⣿⣆⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⣰⡿⢀⡏⢳⡦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣯⣁⣠⣿⠁⠀⠀⠻⡄⠀⠀⠸⣎⢧⡀⠀⠀⠀⠀⠀⢰⣿⣷⣀⣼⣫⠃⠀⠀⣸⠇⠀⠀⠙⣦⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⠞⣍⡍⠉⠉⣿⢹⡀⠀⠀⠀⠱⡄⠀⠀⠈⠳⢽⣦⣀⠀⠀⢰⣿⣿⣟⣿⠕⠋⠀⠀⡰⠃⠀⠀⠀⣼⠃⠀⠉⢉⣭⠽⢶⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢨⡷⠋⠙⢷⡀⠹⣾⣧⠀⠀⠀⠀⠈⠦⣄⠀⠀⠀⠀⠈⠉⠉⣿⣾⠁⣼⡇⠀⠀⡠⠞⠁⠀⠀⠀⣸⠏⠀⠀⣠⡞⠉⠻⣾⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⡟⠀⠀⠀⠀⢻⡄⢷⠙⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⡏⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⣴⠏⠀⠀⢠⡟⠀⠀⠀⠘⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣾⡇⠀⠀⠀⠀⠀⢿⡘⣇⠙⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢱⠁⠐⠲⡇⢀⡀⠀⠀⠀⠀⣼⠃⠀⠀⢀⡾⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⠀⠀⠀
⠀⢠⣿⡇⠀⠀⠀⠀⠀⣨⡇⠸⡄⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠘⣀⣀⣀⡟⠉⣿⠀⠀⢠⡞⠁⠀⠀⠀⣸⣃⠀⠀⠀⠀⠀⠘⡏⢧⠀⠀⠀⠀⠀
⠀⣿⠀⢻⡀⠀⣠⠔⠛⠉⠻⣄⠹⡄⠀⠈⠙⠶⢤⣀⡀⠀⠀⢀⣿⣟⡻⣷⠛⠛⠋⢉⣉⣻⡖⠋⠀⠀⠀⠀⡀⡏⢉⠟⠦⣀⠀⠀⠀⢧⠈⣇⠀⠀⠀⠀
⢸⠃⠀⠈⣷⠈⢁⡄⠀⠀⠀⠘⢦⠘⣦⠀⠀⠀⠀⠈⠫⣭⣽⠟⠁⠈⢳⠈⡇⠀⠀⠀⠈⠉⠙⣷⠀⠀⠀⠀⢸⡽⠃⠀⠀⠈⡀⠀⠀⠘⢧⡸⡆⠀⠀⠀
⢸⠀⠀⠀⠁⠀⡞⠀⠀⠀⠀⠀⠘⣇⠈⢳⡀⠀⠀⠀⣠⣾⡌⣆⠀⠀⢸⠀⣧⣀⣹⠤⣶⡀⢀⣿⠀⠀⠀⠀⣾⠁⠀⠀⠀⠀⣇⠀⠀⠀⠈⠈⢹⡀⠀⠀
⢸⠀⡀⠀⠀⢸⠁⠀⢀⣠⡤⠶⠒⠛⠁⠉⠉⠉⠉⠉⠁⠈⣿⠘⢦⢀⡞⢰⣇⡀⢹⡧⣄⣩⡽⠃⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠐⡄⣧⠀⠀
⢸⡀⣇⠀⠀⢸⣦⡞⢻⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⢷⡈⠻⣄⣾⠁⢉⡿⠁⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⢀⣠⡇⠀⠀⠀⠀⠹⣻⠀⠀
⠀⣇⢸⠀⢀⣴⣿⡇⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠞⠁⠀⠈⠛⣦⣿⡿⠒⢯⣀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠀⣀⣤⡴⢿⡉⠙⢶⣄⣀⡀⠀⠹⡄⠀
⠀⠘⣾⡇⢸⠏⠀⣧⠀⢻⡀⠀⠀⠀⣀⣠⠶⠚⠉⠀⠀⠀⠀⠀⣠⡞⠁⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀⠀⠀⢀⡿⠊⠁⠀⠀⠀⢱⡄⠈⣧⠉⠓⢄⠀⢧⠀
⠀⠀⢹⡇⢸⠀⠀⠸⣇⠀⢳⡀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠿⡶⢞⣛⣛⣓⣒⣾⣶⣿⣲⣦⣤⠤⠚⠁⠀⠀⠀⠀⠀⠀⠀⢳⠀⢸⡆⠀⠀⠀⢿⡆
⠀⠀⢸⡇⠀⠀⠀⠀⠙⣷⡀⠙⣆⠀⠀⠀⠀⠀⠀⢀⣠⡾⣋⠁⡾⣱⠋⠁⠀⠀⠀⠈⠙⣮⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄⠘⡇⠀⠀⠀⢸⡇
⠀⠀⠈⢿⡀⠀⠀⠀⠀⠈⢳⣄⠈⠱⣦⡀⣀⡠⠖⠋⡽⠛⢁⣾⡇⡇⠀⠀⠀⠀⠀⠀⠀⢸⡏⣷⠀⠰⠦⠤⢤⣤⣀⣤⠤⠴⠖⠂⡇⠀⡇⠀⠀⢀⡾⠁
⠀⠀⠀⠘⠻⢦⣄⣀⣀⣀⣀⣈⣿⠦⠤⠿⠁⠀⠀⣼⡧⠔⢛⢿⡇⣇⠀⠀⠀⠀⠀⠀⠀⠀⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⡇⠀⣠⠟⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⣿⣠⠴⠋⢀⣧⡸⣦⣀⣀⣀⣀⣀⣠⣼⣇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠇⢰⠗⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⡀⠀⠘⠙⣻⡶⠭⠭⠭⠽⠟⠒⠛⠛⠉⠉⠑⠒⠒⠒⠒⠒⠒⠒⠋⠉⠙⠒⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

Ce projet a été réalisé dans le cadre de l'UV IA02 à l'UTC.
Binôme : Lucas, Sacha.

## Comment exécuter le code 
* Télécharger le rep. Par example via un gitclone :  
```bash
git clone git@github.com:sacha-sz/IA02-Projet.git
```

* Accéder au dossier. Par example, via cd : 
```bash
cd IA02-Projet
```

* Exécuter le fichier ```main.py```
Le programme demandera si on veut la phase 1 avec ou sans SAT. On entre y pour avoir le SAT dans la phase 1.

## Explication du projet
Le projet consiste à permettre à l'agent Hitman de se déplacer dans une map 2D pour tuer une cible.
Au début Hitman ne connait pas la map. Il doit l'explorer.
Nous disposons d'une matrice des regards (attribut ```self.mat_regard```) qui indique dans quelles directions regardent les gardes et civils qu'on a trouvé.
Nous avons aussi une matrice de connaissance (attribut ```self.mat_connue```) qui contient toutes les informations sur la map qu'on a découvert.
L'objectif est réalisé en deux phases : 

### Phase :one: :
L'agent doit se déplacer dans la map pour découvrir toute la map.
On utilise pour cela du SAT.

On explore la map en trouvant l'inconnu le plus proche et l'agent essaye de se rapprocher de cette case pour la voir.
Le chemin est généré en utilisant l'algorithme A*. On prend en compte les regards des gardes si on les connait déjà. On prend bien-sûr en compte le coup des déplacements.

Pour avancer il faut être bien orienté. La case où on veut aller doit être devant nous.
Des rotations peuvent donc être nécessaire. Une methode, ```best_turn```, permet de s'orienter vers la case
en faisant le moins de rotations possibles.

#### Modélisation SAT
Nous avons choisi de modéliser le problème de la manière suivante. 
Une case est représentée par trois variables propositionnelles :
* ```P``` : la case est une personne
* ```I``` : la case est un invité (civil)
* ```G``` : la case est un garde

Nous avons donc la contrainte suivante : 
* ```P ⇔ G ∨ I```  ⇔ ```(¬P ∨ G ∨ I) ∧ (P ∨ ¬G) ∧ (P ∨ ¬I)```


Le fait de **voir** nous ajoute les certitudes suivantes :
- Si on voit un garde alors on sait que la case est un garde
- De même pour un civil
- Si on voit tout autre chose alors on sait que la case n'est pas une personne

Le fait d'**entendre** nous ajoute les certitudes suivantes :
- une valeur fixe d'un nombre de personnes qui sont dans le champ d'écoute,
si ce nombre est compris entre 1 et BROUHAHA.
- une valeur minimum (BROUHAHA) de personnes qui sont dans le champ d'écoute,
si ce nombre est compris entre BROUHAHA et nombre maximum de personnes dans le champ d'écoute.
- la négation des personnes de la zone d'écoute si le nombre de personnes dans le champ d'écoute est 0.


#### Utilisation de cette modélisation
Pour utiliser cette modélisation nous avons d'abord besoin d'ajouter les certitudes que nous avons sur la map (entendre, voir).
Notre méthode pour ne pas faire exploser le nombre de clauses est de ne pas représenter dès le début le nombre maximal de personnes de chaque type sur l'ensemble de la map.
Mais plutôt d'ajouter la négation de ce type lorsque nous avons vu le nombre maximal de personnes de ce type.
Cette méthode nous a permis de passer de plusieurs dizaines de millions de clauses (52 sur une map 9x9) à quelques milliers seulement.
Et ce, sans perdre en précision et en gagnant en rapidité d'exécution (environ **60** secondes pour effectuer toutes les déductions sur une map 6x7).

Ensuite nous utilisons gophersat pour résoudre le problème. 

Mais quel est ce problème ?
Ce problème est de prédire la valeur d'une case non découverte. 
Pour cela nous avons les fonctions ```test_personne``` et ```test_type```.

Vous pouvez modifier la valeur de POIDS_PROBA_PERSONNE dans le fichier ```variables.py```.
Cette modification rendra Hitman plus ou moins frileux à l'idée de parcourir une case inconnue.

### Phase :two: :
L'agent doit se déplacer dans la map pour tuer la cible.
On utilise pour cela l'algorithme A*. Plusieurs optimisations sont faites.
Tout d'abord on regarde le chemin qui coute le moins pour tuer la cible parmi ces chemins :

* chemin 1 : aller de la case départ puis à la case où se trouve et ensuite aller à la case de la cible pour la tuer et revenir à la case de départ
* chemin 2 : aller de la case départ à la case du costume puis aller à la case de la corde puis aller la case cible pour la tuer et revenir à la case de départ
* chemin 3 : aller de la case départ à la case de la corde puis aller à la case du costume puis aller la case cible pour la tuer et revenir à la case de la corde puis aller à la case de départ


Lorsqu'on a le costume on prend en compte d'essayer de mettre le costume lorsqu'on nous voit pas. 
De plus lorsqu'on a mis le costume on prend en compte qu'on n'est pas vu par un garde lorsqu'on passe devant
son champ de vision.

## STRIPS :

##### Fluents : 
Orientation(actuelle), Position(Hitman, x, y), Sur_case(cible, x, y), Sur_case(corde_de_piano, x, y), Sur_case(costume, x, y), Sur_case(civil, x, y), Sur_case(garde, x, y), Regarde(Hitman, garde), Regarde(Hitman, civil),  Regarde(garde, cible), Possède(corde_de_piano), Possède(costume), Avance_possible(x, y), Garde_present(Garde, x, y), Civil_present(Civil, x, y)

Init(
    Position(Hitman, 0,0)
)

Goal (
    ¬Sur_case(cible, x, y)
)

##### Actions :
```
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
EFFECT: Orientation(est))

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

* Action(neutraliser_garde(Hitman, Garde, x, y, x+1, y), 
PRECOND: Position(Hitman, x, y) ∧ Garde_present(Garde, x+1, y) ∧ ¬Regarde(Hitman, garde),
∧ Orientation(actuelle) = nord ∧ regarde(garde, cible),
EFFECT: ¬Garde_present(Garde, x, y), ¬regarde(garde, cible))

* Action(neutraliser_garde(Hitman, Garde, x, y, x-1, y),
PRECOND: Position(Hitman, x, y) ∧ Garde_present(Garde, x-1, y) ∧ ¬Regarde(Hitman, garde)
∧ Orientation(actuelle) = sud, 
EFFECT: ¬Garde_present(Garde, x, y), ¬regarde(garde, cible))

* Action(neutraliser_garde(Hitman, Garde, x, y, x, y+1),
PRECOND: Position(Hitman, x, y) ∧ Garde_present(Garde, x, y+1) ∧ ¬Regarde(Hitman, garde)
∧ Orientation(actuelle) = est ∧ regarde(garde, cible),
EFFECT: ¬Garde_present(Garde, x, y))

* Action(neutraliser_garde(Hitman, Garde, x, y, x, y-1),
PRECOND: Position(Hitman, x, y) ∧ Garde_present(Garde, x, y-1) ∧ ¬Regarde(Hitman, garde)
∧ Orientation(actuelle) = ouest ∧ regarde(garde, cible)
EFFECT: ¬Garde_present(Garde, x, y), ¬regarde(garde, cible))


* Action(neutraliser_civil(Hitman, Civil, x, y, x+1, y), 
PRECOND: Position(Hitman, x, y) ∧ Civil_present(Civil, x+1, y) ∧ ¬Regarde(Hitman, civil)
∧ Orientation(actuelle) = nord ∧ regarde(garde, cible),
EFFECT: ¬Civil_present(Civil, x, y), ¬regarde(garde, cible))

* Action(neutraliser_civil(Hitman, Civil, x, y, x-1, y),
PRECOND: Position(Hitman, x, y) ∧ Civil_present(Civil, x-1, y) ∧ ¬Regarde(Hitman, civil)
∧ Orientation(actuelle) = sud,
EFFECT: ¬Civil_present(Civil, x, y))

* Action(neutraliser_civil(Hitman, Civil, x, y, x, y+1),
PRECOND: Position(Hitman, x, y) ∧ Civil_present(Civil, x, y+1) ∧ ¬Regarde(Hitman, civil)
∧ Orientation(actuelle) = est,
EFFECT: ¬Civil_present(Civil, x, y))

* Action(neutraliser_civil(Hitman, Civil, x, y, x, y-1),
PRECOND: Position(Hitman, x, y) ∧ Civil_present(Civil, x, y-1) ∧ ¬Regarde(Hitman, civil)
∧ Orientation(actuelle) = ouest,
EFFECT: ¬Civil_present(Civil, x, y))


* Action(prendre_corde(Hitman, corde_de_piano, x, y), 
PRECOND: Position(Hitman, x, y) ∧ Sur_case(corde_de_piano, x, y), 
EFFECT: Possède(corde_de_piano) ∧ ¬Sur_case(corde_de_piano, x, y))


* Action(prendre_costume(Hitman, costume, x, y), 
PRECOND: Position(Hitman, x, y) ∧ Sur_case(costume, x, y), 
EFFECT: Possède(costume) ∧ ¬Sur_case(costume, x, y) )
```

## Avantages et inconvénients de notre programme

#### Avantages
Le nombre de rotation est optimisé afin de faire le nombre minimum de rotation pour se tourner vers la case où on veut aller.

##### Phase 1 :
La modélisation SAT permet d'être opérationnelle même sur des maps plus grande que la map actuelle (des maps de taille 10x10 par exemple).

Pour le choix du déplacement on prend en compte le coût du regard des gardes. 
On cherche la case inconnue la plus proche et on s'approche de cette case jusqu'à la voir. On ne va donc pas forcément jusqu'à aller sur cette case. Une fois qu'on la voit on recherche l'autre case inconnue la plus proche. Cette méthode permet de réduire les coûts car une fois qu'on connaît la case, on n'essaye pas d'aller dessus.

##### Phase 2 : 
On fait des simulations avec différents chemins pour savoir celui qui est le moins coûteux. Les coûts pris en compte sont : 
* les coûts de déplacements
* les coûts des rotations
* le nombre de fois qu'on est vu par un garde
* les coûts liés au costume (si on le prend)
* les coûts liés au meurtre de la cible
* les coûts liés au meutre d'un garde ou d'une cible


On neutralise des civils ou invités s'ils regardent la cible. Cela permet de réduire drastiquement le coût lorsqu'on tue la cible.


#### Inconvénients
##### Phase 1 : 
Pour se déplacer on cherche la case inconnue la plus proche. Cependant on cherche la case la plus proche avec une certaine préférence. Ce qui amène des fois à passer plusieurs fois sur une même case selon la configuration de la map. 

##### Phase 2 :
Ne fait des simulations qu'avec quelques chemins. Lorsqu'une action est faite le chemin n'est pas recalculé. Ce recalcule de chemin pourrait peut-être permettre de trouver un meilleur trajet.
