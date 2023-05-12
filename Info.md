IA02 Projet
===

[Sujet](https://hackmd.io/@ia02/S1LNF3CMn)

**Date limite : 25 juin**

### Phases

#### Phase 1

- ==Objectif== :
    - Repérer les lieux :
        - les gardes + la direction du regard
        - les civils + la direction du regard
        - position corde [UNIQUE + OBLIGATOIRE] 
        - position costume [UNIQUE + FACULTATIF]
        - les murs
- ==Déductions possibles== :
    - Regarder => Certitudes 
        - Hitman = 3 cases
        - Gardes = 2 cases
        - Civils = 1 case
        - Cible = 0 case
    - Ecoute => Possibilités
        - Si on entend moins de 5 personnes
            - Certitude du nombre
        - Sinon
            - nombre compris entre 5 et 9 
            
        - Pas certain de distinguer qui sont les gardes ou les civils
- ==Déplacement de Hitman== :
    - Mur => impossible
    - Garde => impossible
    - Reste => OK
        - Invité nous protège de la vision du garde



#### Phase 2



Idées : 
* 
Difficultés : 
* Comment déplacer le personnage en SAT


Modélisation logique propositionnelle : 
* **p(i,j)**: il y a une personne en position (i,j), où i et j sont des entiers représentant les coordonnées du monde rectangulaire.
* **g(i,j,d)**: il y a un garde en position (i,j) qui regarde dans la direction d (N, S, E ou O).
* **c(i,j)**: la cible est en position (i,j).
* **ci(i,j)**: il y a un civil en position (i,j).
* **o(i,j)**: il y a un objet en position (i,j).
* **m(i,j)**: il y a un mur en position (i,j).
* **h(i,j,d)**: Hitman est en position (i,j) et regarde dans la direction d.
* **t**: Hitman a la corde de piano sur lui.
* **c**: Hitman est déguisé avec le costume.