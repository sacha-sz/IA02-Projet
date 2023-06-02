from variables import *
import les_contraintes_clausales_en_cavales as cc
from hitman import *
from gophersat import *
from collections import deque

class Agent_Hitman:
    def __init__(self):
        self.oracle = HitmanReferee()  # On crée l'oracle / arbitre
        self.info_actuelle = self.oracle.start_phase1()  # On récupère les infos de départ

        # Taille de la map
        self.max_L = self.info_actuelle["m"]
        self.max_C = self.info_actuelle["n"]
        self.gophersat = Gophersat(self.max_L, self.max_C)

        # Position de départ
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]

        # Attributs pour les voisins et l'ouie
        self.MAX_VOISINS = self.getMAXVOISINS()

        self.nb_gardes = self.info_actuelle["guard_count"]
        self.nb_invites = self.info_actuelle["civil_count"]

        self.unknown = "."

        self.mat_connue = [[self.unknown for i in range(
            self.max_C)] for j in range(self.max_L)]

        self.mat_regard = [
            [0 for i in range(self.max_C)] for j in range(self.max_L)]

        self.loc_gardes = set()
        self.loc_invites = set()

    def __str__(self):
        """
            Affichage de l'agent
        """
        chaine = ""
        for i in range(self.max_L):
            for j in range(self.max_C):
                chaine += " " * \
                    min(3-len(self.mat_connue[i][j]),
                        2) + self.mat_connue[i][j]
            chaine += "\n"
        return chaine

    def entendre(self) -> None:
        """
            Entendre : méthode qui permet de générer les clauses
        """
        neighbors = self.generate_neighboors(
            self._x, self._y)  # On génère les voisins
        nb_ouie = self.info_actuelle["hear"]

        # Si on entend moins de BROUHAHA personnes, on regarde si on a déjà localisé des gens dans cette zone
        if nb_ouie < BROUHAHA:
            pos_neighbors = []
            for pos in neighbors:
                if self.mat_connue[pos[0]][pos[1]] == self.unknown:
                    pos_neighbors.append(pos)
                elif self.mat_connue[pos[0]][pos[1]] == Personne or self.mat_connue[pos[0]][pos[1]] == Garde or self.mat_connue[pos[0]][pos[1]] == Invite:
                    nb_ouie -= 1
            # On ajoute les clauses
            self.gophersat.ajout_clauses_entendre(pos_neighbors, nb_ouie)
        else:
            self.gophersat.ajout_clauses_entendre(neighbors, nb_ouie)

    def voir(self) -> None:
        """
            Voir : méthode qui permet de générer les clauses
        """
        vision = self.info_actuelle["vision"]
        certitudes = []
        for v in vision:
            pos_vision_x = v[0][1]
            pos_vision_y = v[0][0]
            
            if v[1] == HC.EMPTY:
                certitudes.append((pos_vision_x, pos_vision_y, "N"))
                self.ajout_info_mat(pos_vision_x, pos_vision_y, empty)
            elif v[1] in [HC.GUARD_N, HC.GUARD_S, HC.GUARD_E, HC.GUARD_W]:
                certitudes.append((pos_vision_x, pos_vision_y, "G"))
                self.loc_gardes.add((pos_vision_x, pos_vision_y))
                if v[1] == HC.GUARD_N:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, GardeNord)

                elif v[1] == HC.GUARD_S:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, GardeSud)

                elif v[1] == HC.GUARD_E:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, GardeEst)

                elif v[1] == HC.GUARD_W:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, GardeOuest)

            elif v[1] in [HC.CIVIL_N, HC.CIVIL_S, HC.CIVIL_E, HC.CIVIL_W]:
                certitudes.append((pos_vision_x, pos_vision_y, "I"))
                self.loc_invites.add((pos_vision_x, pos_vision_y))
                if v[1] == HC.CIVIL_N:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, InviteNord)

                elif v[1] == HC.CIVIL_S:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, InviteSud)

                elif v[1] == HC.CIVIL_E:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, InviteEst)

                elif v[1] == HC.CIVIL_W:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, InviteOuest)

            else:
                certitudes.append((pos_vision_x, pos_vision_y, "N"))
                if v[1] == HC.PIANO_WIRE:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, Corde)

                elif v[1] == HC.SUIT:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, Costume)
                elif v[1] == HC.WALL:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, wall)
        self.gophersat.ajout_clauses_voir(certitudes)

    def test(self, x: int, y: int) -> None:
        """
            Demande à gophersat s'il y a la présence d'une personne.
        """
        res = self.gophersat.test_personne((self._x, self._y, Personne))
        if res == 0:
            pass

        if res == -1:
            pass

        elif res == 1:
            self.ajout_info_mat(x, y, Personne)

        elif res == 2:
            self.ajout_info_mat(x, y, Garde)
            self.loc_gardes.add((x, y))

    def gardesTousTrouves(self):
        return len(self.loc_gardes) == self.nb_gardes

    def invitesTousTrouves(self):
        return len(self.loc_invites) == self.nb_invites

    def getMAXVOISINS(self) -> int:
        return (MAX_OUIE * 2 + 1) ** 2

    def generate_neighboors(self, Indice_ligne: int, Indice_colonne: int) -> LC:
        """
        Fonction qui genere les voisins d'une case donnee
        """
        liste_voisins = []

        for change_ligne in range(-MAX_OUIE, MAX_OUIE+1):
            for change_col in range(-MAX_OUIE, MAX_OUIE+1):
                if Indice_ligne + change_ligne < 0 or Indice_ligne + change_ligne >= self.max_L:
                    continue
                if Indice_colonne + change_col < 0 or Indice_colonne + change_col >= self.max_C:
                    continue

                liste_voisins.append(
                    [Indice_ligne + change_ligne, Indice_colonne + change_col])
        return liste_voisins

    def check_coord(self, ligne, colonne):
        if 0 <= ligne and ligne < self.max_L and 0 <= colonne and colonne < self.max_C:
            return True
        else:
            return False

    def translate_ligne(self, ligne):
        return self.max_L - 1 - ligne

    def ajout_info_mat(self, ligne, colonne, info):
        ligne = self.translate_ligne(ligne)
        if self.check_coord(ligne, colonne):
            self.mat_connue[ligne][colonne] = info

            # Si garde on ajoute sa vision
            if info.startswith("G"):
                self.add_vision_garde(ligne, colonne)

        else:
            print("Erreur : les coordonnées sont hors de la matrice")
            print("Aucune information n'a été ajoutée")

    def add_vision_garde(self, ligne, colonne):
        if self.check_coord(ligne, colonne):
            if self.mat_connue[ligne][colonne] == Garde:
                # On ne connait pas sa direction, il peut regarder dans n'importe quelle direction
                pass

            elif self.mat_connue[ligne][colonne] == GardeSud:
                for i in range(1, 3):
                    if ligne + i < self.max_L:
                        self.mat_regard[ligne + i][colonne] += 1

            elif self.mat_connue[ligne][colonne] == GardeNord:
                for i in range(1, 3):
                    if ligne - i >= 0:
                        self.mat_regard[ligne - i][colonne] += 1

            elif self.mat_connue[ligne][colonne] == GardeEst:
                for i in range(1, 3):
                    if colonne + i < self.max_C:
                        self.mat_regard[ligne][colonne + i] += 1

            elif self.mat_connue[ligne][colonne] == GardeOuest:
                for i in range(1, 3):
                    if colonne - i >= 0:
                        self.mat_regard[ligne][colonne - i] += 1
            else:
                print("Ce n'est pas un garde qui est en (" +
                      str(ligne) + ", " + str(colonne) + ")")
        else:
            print("Erreur : les coordonnées sont hors de la matrice")
            print("Aucune information n'a été ajoutée")
        self.verif_vision()

    def verif_vision(self):
        """
        Si un garde a un objet/mur/personne devant lui, son champ 
        de vision doit être réduit.
        """
        for i in range(self.max_L):
            for j in range(self.max_C):
                if self.mat_connue[i][j].startswith("G"):
                    vision_bloque = False
                    if self.mat_connue[i][j].endswith("S"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i + v < self.max_L:

                                if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i + v][j] = 0

                    elif self.mat_connue[i][j].endswith("N"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i - v >= 0:

                                if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i - v][j] = 0

                    elif self.mat_connue[i][j].endswith("E"):
                        for v in range(1, MAX_VISION_GARDE+1):
                            if j + v < self.max_C:

                                if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i][j + v] = 0

                    elif self.mat_connue[i][j].endswith("O"):
                        for v in range(1, MAX_VISION_GARDE+1):

                            if j - v >= 0:
                                # print(i, j-v,self.mat_connue[i][j - v])

                                if self.mat_connue[i][j - v] != empty and self.mat_connue[i][j - v] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i][j - v] = 0

                    else:
                        print("Erreur : le garde en (" + str(i) + ", " + str(j) + ") n'a pas de direction")

    def incomplete_mat(self) -> bool:
        """
        On regarde si la matrice est complète ou non, on recherche le premier élément inconnu
        """
        for i in range(self.max_L):
            for j in range(self.max_C):
                if self.mat_connue[i][j] == self.unknown:
                    return True
        return False

    def est_sur_bord(self, position : Tuple[int, int]):
        bord_haut = self.max_L-1
        bord_bas = 0
        bord_gauche = 0
        bord_droit = self.max_C-1
        x, y = position
        return x == bord_haut or x == bord_bas or y == bord_gauche or y == bord_droit


    def helicoptere(self):
        """
            On tourne autour de nous si ça vaut le coup
        """
    
        self.voir()
        self.info_actuelle = self.oracle.turn_clockwise()
        self.voir()
        self.info_actuelle = self.oracle.turn_clockwise()
        self.voir()
        self.info_actuelle = self.oracle.turn_clockwise()
        self.voir()
        self.info_actuelle = self.oracle.turn_clockwise()
        self.voir()
        
    def inconnue_plus_proche(self):
        """
        Methode pour trouver le unkown le plus proche.
        """

        deplacements = [(-1, 0), (0,1), (1,0), (0,-1)]

        file_attente = deque()
        visite = [[False] * self.max_C for _ in range(self.max_L)]

        x,y = self._x, self._y
        #print("x : ", x, "y : ", y)

        visite[x][y] = True

        file_attente.append((x, y, 0))  # (x, y, distance)

        # Recherche en largeur
        while file_attente:
            x, y, distance = file_attente.popleft()
            
            # Vérifier si la case actuelle est inconnue
            if self.mat_connue[self.translate_ligne(x)][y] == self.unknown:
                return (x, y), distance

            # Explorer les cases voisines
            for dx, dy in deplacements:
                nx, ny = x + dx, y + dy

                # Vérifier si la case voisine est valide et non visitée
                if self.check_coord(self.translate_ligne(nx),ny) and self.mat_connue[self.translate_ligne(x)][ny] != wall and not visite[nx][ny]:
                    #print("nx : ", nx, "ny : ", ny)
                    visite[nx][ny] = True
                    file_attente.append((nx, ny, distance + 1))

        # Aucun point trouvé
        return None
    
    def bfs_shortest_path(self, start, end):
        """
            Trouve un chemin pour aller jusqu'à end. 
            Ne fonctionne pas encore. Sûrement un problème lié 
            aux translations.
        """
        queue = deque()
        visited = [[False] * self.max_C for _ in range(self.max_L)]
        parent = [[None] * self.max_C for _ in range(self.max_L)]


        queue.append(start)
        visited[start[0]][start[1]] = True

        while queue:
            current = queue.popleft()
            
            if current == end:
                break

            row, col = current

            neighbors = [
                (row-1, col), 
                (row, col+1), 
                (row+1, col), 
                (row, col-1)
                ]
            
            for neighbor in neighbors:
                n_row, n_col = neighbor

                if self.check_coord(self.translate_ligne(n_row),n_col) and self.mat_connue[self.translate_ligne(n_row)][n_col] != wall and not visited[n_row][n_col]:
                    #print("n_row : ", n_row, "n_col : ", n_col)
                    visited[n_row][n_col] = True
                    parent[n_row][n_col] = current
                    queue.append(neighbor)


        if not visited[end[0]][end[1]]:
            return None
        
        path = []
        current = start
        while current is not None:
            path.append(current)
            current = parent[current[0]][current[1]]

        return list(reversed(path))
    
    def phase_1(self):
        """
        On fait un tour de jeu du hitman.
        Ce dernier se décompose en 3 temps :
        - temp 1 : on ajoute toutes les informations qu'on peut dans gophersat
        - temp 2 : on fait l'hélicoptère en se tournant vers les zones les plus intéressantes
        - temp 3 : on se déplace
        """
        print("--------------------")
        print("\tPhase 1")
        print("--------------------")
        print(self)
        
        # while self.incomplete_mat():

        # A indenter
        # Temp 1
        self.entendre()
        self.voir()
        
        
        print(self)
        print("penalties : ", self.info_actuelle["penalties"])

        # Temp 2
        self.helicoptere()
        print(self)
        self.voir()
        print("penalites : ", self.info_actuelle["penalties"])




        #Temp 3
        self.info_actuelle = self.oracle.move()
        self.voir()
        self.helicoptere()
        self.voir()

        print(self)
        print("penalites : ", self.info_actuelle["penalties"])
        self._x, self._y = self.info_actuelle["position"][1], self.info_actuelle["position"][0]
        pos, distance = self.inconnue_plus_proche()
        #print ("x : ", self._x, "y : ", self._y)
        #print("pos : ", pos, "distance : ", distance)
        #path = self.bfs_shortest_path((self._x, self._y), pos)
        #print("path : ", path)
        self.info_actuelle = self.oracle.turn_clockwise()
        print(self.info_actuelle["orientation"])
        self.info_actuelle = self.oracle.move()
        self.voir()
        self.info_actuelle = self.oracle.move()
        self.voir()
        print(self)
        self._x, self._y = self.info_actuelle["position"][1], self.info_actuelle["position"][0]
        print("x : ", self._x, "y : ", self._y)
        print("penalites : ", self.info_actuelle["penalties"])
        pos, distance = self.inconnue_plus_proche()
        print("pos : ", pos, "distance : ", distance)





def main():
    Hitman1 = Agent_Hitman()
    Hitman1.phase_1()


if __name__ == "__main__":
    main()
