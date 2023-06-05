from variables import *
from hitman import *
from gophersat import *
from collections import deque

class Agent_Hitman:
    def __init__(self):
        self.oracle = HitmanReferee() 
        self.info_actuelle = self.oracle.start_phase1()

        # Taille de la map
        self.max_L = self.info_actuelle["m"]
        self.max_C = self.info_actuelle["n"]
        self.gophersat = Gophersat(self.max_L, self.max_C)

        # Position de départ
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]

        self.nb_gardes = self.info_actuelle["guard_count"]
        self.nb_invites = self.info_actuelle["civil_count"]

        self.unknown = "?"

        self.mat_connue = [[self.unknown] * self.max_C for _ in range(self.max_L)]

        self.mat_regard = [[0] * self.max_C for _ in range(self.max_L)]

        self.loc_gardes = set()
        self.loc_invites = set()
        self.invitesTrouves = False
        self.gardesTrouves = False


    def __str__(self):
        """
        Affichage de la matrice des connaissances de l'agent
        """
        max_length = 4
        border = '+' + '-' * ((max_length + 2) * self.max_C + self.max_L) + '+'
        output = [border]

        for i in range(self.max_L):
            row_str = '|'
            for j in range(self.max_C):
                if self.translate_ligne(self._x) == i and self._y == j:
                    element = self.mat_connue[i][j] + " H"
                    if self.info_actuelle["orientation"] == HC.N:
                        element += "\u2191"
                    elif self.info_actuelle["orientation"] == HC.S:
                        element += "\u2193"
                    elif self.info_actuelle["orientation"] == HC.E:
                        element += "\u2192"
                    elif self.info_actuelle["orientation"] == HC.W:
                        element += "\u2190"
                    element_str = element.center(max_length)
                else:
                    element_str = self.mat_connue[i][j].center(max_length)
                row_str += f' {element_str} |'
            output.append(row_str)
            output.append(border)

        return '\n'.join(output)
    
    def generate_neighboors(self, Indice_ligne: int, Indice_colonne: int) -> LC:
        """
        Fonction qui genere les voisins d'une case donnee
        """
        liste_voisins = []

        for change_ligne in range(-MAX_OUIE, MAX_OUIE+1):
            for change_col in range(-MAX_OUIE, MAX_OUIE+1):
                if Indice_ligne + change_ligne < 0 or Indice_ligne + change_ligne >= self.max_L or \
                    Indice_colonne + change_col < 0 or Indice_colonne + change_col >= self.max_C:
                    continue
                
                liste_voisins.append([Indice_ligne + change_ligne, Indice_colonne + change_col])
                
        return liste_voisins
    
    def ajout_info_mat(self, ligne : int, colonne :int, info :str) -> None:
        """
        Ajoute une information dans la matrice de connaissance et convertit la ligne
        """
        
        ligne = self.translate_ligne(ligne)
        if self.check_coord(ligne, colonne):
            self.mat_connue[ligne][colonne] = info

            # Si garde on ajoute sa vision
            if info.startswith("G"):
                self.add_vision_garde(ligne, colonne)
            
        else:
            print("Erreur : les coordonnées sont hors de la matrice\nAucune information n'a été ajoutée")

    def gardesTousTrouves(self) -> bool:
        return len(self.loc_gardes) == self.nb_gardes

    def invitesTousTrouves(self) -> bool:
        return len(self.loc_invites) == self.nb_invites

    def check_coord(self, ligne, colonne) -> bool:
        """
        Vérifie si les coordonnées sont dans la matrice
        """
        return 0 <= ligne and ligne < self.max_L and 0 <= colonne and colonne < self.max_C

    def translate_ligne(self, ligne) -> int:
        """
        Permet de faire en sorte que la ligne 0 soit en bas de la matrice
        """
        return self.max_L - 1 - ligne

    
    def entendre(self) -> None:
        """
        Méthode qui ajoute les clauses pour l'ouie
        
        Légère optimisation: si on entend moins de BROUHAHA personnes, on regarde si on a déjà localisé des gens dans cette zone
        """
        
        neighbors = self.generate_neighboors(self.translate_ligne(self._x), self._y)
        nb_ouie = self.info_actuelle["hear"]

        # Si on entend moins de BROUHAHA personnes, on regarde si on a déjà localisé des gens dans cette zone
        if nb_ouie < BROUHAHA:
            unknown_pos = []
            for pos in neighbors:
                if self.mat_connue[pos[0]][pos[1]] == self.unknown:
                    unknown_pos.append(pos)
                elif self.mat_connue[pos[0]][pos[1]] == Personne or \
                    self.mat_connue[pos[0]][pos[1]] == Garde or \
                    self.mat_connue[pos[0]][pos[1]] == Invite:
                    nb_ouie -= 1
            
            self.gophersat.ajout_clauses_entendre(unknown_pos, nb_ouie)
        else:
            self.gophersat.ajout_clauses_entendre(neighbors, nb_ouie)

    def voir(self) -> None:
        """
        Méthode qui ajoute les clauses pour la vision
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
                elif v[1] == HC.TARGET:
                    self.ajout_info_mat(pos_vision_x, pos_vision_y, Target)
                    
        self.gophersat.ajout_clauses_voir(certitudes)

    def test(self, x: int, y: int) -> None:
        """
        Demande à gophersat s'il y a la présence d'une personne.
        """
        res = self.gophersat.test_personne((x,y, Personne))
        if res == 0:
            pass

        if res == -1:
            pass

        elif res == 1:
            self.ajout_info_mat(x, y, Personne)

        elif res == 2:
            self.ajout_info_mat(x, y, Garde)
            self.loc_gardes.add((x, y))

    def add_vision_garde(self, ligne: int, colonne: int) -> None:
        if self.check_coord(ligne, colonne):
            if self.mat_connue[ligne][colonne] == Garde:
                # On ne connait pas sa direction, il peut regarder dans n'importe quelle direction
                pass

            elif self.mat_connue[ligne][colonne] == GardeSud:
                for i in range(1, 3):
                    if ligne + i < self.max_L:
                        self.mat_regard[ligne + i][colonne] += 5

            elif self.mat_connue[ligne][colonne] == GardeNord:
                for i in range(1, 3):
                    if ligne - i >= 0:
                        self.mat_regard[ligne - i][colonne] += 5

            elif self.mat_connue[ligne][colonne] == GardeEst:
                for i in range(1, 3):
                    if colonne + i < self.max_C:
                        self.mat_regard[ligne][colonne + i] += 5

            elif self.mat_connue[ligne][colonne] == GardeOuest:
                for i in range(1, 3):
                    if colonne - i >= 0:
                        self.mat_regard[ligne][colonne - i] += 5
            else:
                print("Ce n'est pas un garde qui est en (" + str(ligne) + ", " + str(colonne) + ")")
        else:
            print("Erreur : les coordonnées sont hors de la matrice\nAucune information n'a été ajoutée")
        self.verif_vision()

    def verif_vision(self) -> None:
        """
        Si un garde a un objet/mur/personne devant lui, son champ 
        de vision doit être réduit.
        """
        for i in range(self.max_L):
            for j in range(self.max_C):
                if self.mat_connue[i][j].startswith("G"):
                    vision_bloque = False
                    if self.mat_connue[i][j] == GardeSud:
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i + v < self.max_L:

                                if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i + v][j] = 0

                    elif self.mat_connue[i][j] == GardeNord:
                        for v in range(1, MAX_VISION_GARDE+1):
                            if i - v >= 0:

                                if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i - v][j] = 0

                    elif self.mat_connue[i][j] == GardeEst:
                        for v in range(1, MAX_VISION_GARDE+1):
                            if j + v < self.max_C:

                                if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != self.unknown:
                                    vision_bloque = True

                                if vision_bloque:
                                    self.mat_regard[i][j + v] = 0

                    elif self.mat_connue[i][j] == GardeOuest:
                        for v in range(1, MAX_VISION_GARDE+1):

                            if j - v >= 0:
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
        return any(self.unknown in row for row in self.mat_connue)

    def est_sur_bord(self, position : PS) -> bool:
        bord_haut = self.max_L-1
        bord_bas = 0
        bord_gauche = 0
        bord_droit = self.max_C-1
        x, y = position
        return x in (bord_haut, bord_bas) or y in (bord_gauche, bord_droit)


    def helicoptere(self) -> None:
        """
            On tourne autour de nous si ça vaut le coup
        """     

        for _ in range(4):
            self.voir()
            self.info_actuelle = self.oracle.turn_clockwise()
            print(self)
        
        
    def inconnue_plus_proche(self) -> Tuple[int, int, int]:
        """
        Methode pour trouver le unkown le plus proche.
        """

        deplacements = [(-1, 0), (0,1), (1,0), (0,-1)]

        file_attente = deque()
        visite = [[False] * self.max_C for _ in range(self.max_L)]

        x,y = self.translate_ligne(self._x), self._y
        visite[x][y] = True

        file_attente.append((x, y, 0))  # (x, y, distance)

        # Recherche en largeur
        while file_attente:
            x, y, distance = file_attente.popleft()
            
            # Vérifier si la case actuelle est inconnue
            if self.mat_connue[x][y] == self.unknown:
                return (x, y, distance)

            # Explorer les cases voisines
            for dx, dy in deplacements:
                nx, ny = x + dx, y + dy

                # Vérifier si la case voisine est valide et non visitée
                if self.check_coord(nx,ny) and self.mat_connue[nx][ny] != wall and not visite[nx][ny]:
                    visite[nx][ny] = True
                    file_attente.append((nx, ny, distance + 1))

        # Aucun point trouvé
        return None
    
    def bfs_shortest_path(self, start, end) -> LP:
        visited = [[False] * self.max_C for _ in range(self.max_L)]
        queue = deque([(start, [])])
        
        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        while queue:
            current, path = queue.popleft()
            row, col = current
            
            if current == end:
                return path + [current]
            
            if not visited[row][col] and self.mat_connue[row][col] != wall and \
                self.mat_connue[row][col] != Garde and \
                self.mat_connue[row][col] != GardeEst and \
                self.mat_connue[row][col] != GardeNord and \
                self.mat_connue[row][col] != GardeOuest and \
                self.mat_connue[row][col] != GardeSud : 
                    
                visited[row][col] = True
                    
                for delta in deltas:
                    new_row, new_col = row + delta[0], col + delta[1]
                    if self.check_coord(new_row, new_col):
                        queue.append(((new_row, new_col), path + [current]))
                        
        return None
    
    def coords_case_devant_nous(self) -> PS:
        """
            Renvoie les coords de la case devant nous selon notre direction.
        """

        direction = self.info_actuelle["orientation"]
        if direction == HC.N:
            return self.translate_ligne(self._x)-1, self._y
        
        elif direction == HC.S:
            return self.translate_ligne(self._x)+1, self._y
        
        elif direction == HC.E:
            return self.translate_ligne(self._x), self._y+1
        
        elif direction == HC.W:
            return self.translate_ligne(self._x), self._y-1
        

    def rotation(self, next : PS) -> None:
        """
            Tourne dans la direction donnée pour qu'on puisse avancer sur la case next.
        """
        case_devant_nous = self.coords_case_devant_nous()
        if case_devant_nous[0] == next[0] and case_devant_nous[1] == next[1]:
            return
        
        while case_devant_nous[0] != next[0] or case_devant_nous[1] != next[1]:
            self.info_actuelle = self.oracle.turn_clockwise()
            self.voir()
            case_devant_nous = self.coords_case_devant_nous()                
    
    def first_move(self) -> None:
        """
        Hitman se déplace pour la première fois vers un emplacement empty.
        """
        self.entendre()
        self.voir()
        
        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        pos_x = self.translate_ligne(self._x)
        pos_possible = []
        
        for delta in deltas:
            if self.check_coord(pos_x + delta[0], self._y + delta[1]) and self.mat_connue[pos_x + delta[0]][self._y + delta[1]] == empty:
                pos_possible.append((pos_x + delta[0], self._y + delta[1]))
        # On se tourne en sens horaire jusqu'à ce qu'on trouve une case empty
        while len(pos_possible) == 0:
            print("On tourne")
            self.info_actuelle = self.oracle.turn_clockwise()
            self.voir()
            for delta in deltas:
                if self.check_coord(pos_x + delta[0], self._y + delta[1]) and self.mat_connue[pos_x + delta[0]][self._y + delta[1]] == empty:
                    pos_possible.append((pos_x + delta[0], self._y + delta[1]))
        
        # On est bien tourné vers une case empty
        self.move()    
        
    def move(self) -> None:
        """
        Gère le déplacement d'Hitman
        """
        self.info_actuelle = self.oracle.move()
        self.entendre()
        self.voir()
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]
        print(self)
        
    def convert(self, var) -> HC:
        if var == empty:
            return HC.EMPTY
        elif var == wall:
            return HC.WALL
        elif var == GardeEst:
            return HC.GUARD_E
        elif var == GardeNord:
            return HC.GUARD_N
        elif var == GardeOuest:
            return HC.GUARD_W
        elif var == GardeSud:
            return HC.GUARD_S
        elif var == InviteEst:
            return HC.CIVIL_E
        elif var == InviteNord:
            return HC.CIVIL_N
        elif var == InviteOuest:
            return HC.CIVIL_W
        elif var == InviteSud:
            return HC.CIVIL_S
        elif var == Costume:
            return HC.SUIT
        elif var == Target:
            return HC.TARGET
        elif var == Corde:
            return HC.PIANO_WIRE
        else:
            raise ValueError("Valeur inconnue : " + str(var))
            
        
    def conversion_mat_connue(self) -> Dict[Tuple[int, int], HC]:
        """
        Convertit la matrice connue en matrice de HC.
        """
        mat = {}
        for i in range(self.max_L):
            for j in range(self.max_C):
                convert_x = self.max_L - i -1                
                mat[(j, convert_x)] = self.convert(self.mat_connue[i][j])
        return mat
    
    def phase_1(self) -> None:
        """
        On fait un tour de jeu du hitman.
        """
        print("--------------------")
        print("\tPhase 1")
        print("--------------------")
        print(self)
        

        # Phase 1 : on fait l'hélicoptère puis on se déplace sur une case empty
        self.first_move()
        
        
        queue_action = deque()
        actual_target = None

        while self.incomplete_mat():
            if len(queue_action) == 0:
                nearest_unknown = self.inconnue_plus_proche()
                actual_target = (nearest_unknown[0], nearest_unknown[1])
                path_temp = self.bfs_shortest_path((self.translate_ligne(self._x), self._y), (nearest_unknown[0], nearest_unknown[1]))
                path_temp.pop(0) # On enlève la case sur laquelle on est
                for coord in path_temp:
                    queue_action.append(coord)
            else:
                # On vérifie si on n'a pas déjà vu la case d'objectif
                if self.mat_connue[actual_target[0]][actual_target[1]] == self.unknown: 
                    # On regarde la prochaine action à faire
                    next_action = queue_action.popleft()
                    
                    if next_action[0] == actual_target[0] and next_action[1] == actual_target[1]:
                        # On est arrivé à la case cible
                        self.voir()
                        self.info_actuelle = self.oracle.turn_clockwise()
                        self.voir()

                    else:
                        # On s'y dirige
                        case_devant_nous = self.coords_case_devant_nous()
                        while case_devant_nous[0] != next_action[0] or case_devant_nous[1] != next_action[1]:
                            self.info_actuelle = self.oracle.turn_clockwise()
                            self.voir()
                            case_devant_nous = self.coords_case_devant_nous()
                            
                        self.move()
                else:
                    queue_action.clear()

                if not self.gardesTrouves and self.gardesTousTrouves():
                    self.gardesTrouves = True
                    self.gophersat.garde_max_trouve()
                    if self.invitesTrouves:
                        self.gophersat.personne_max_trouve()
                
                if not self.invitesTrouves and self.invitesTousTrouves():
                    self.gardesTrouves = True
                    self.gophersat.invite_max_trouve()
                    if self.gardesTrouves:
                        self.gophersat.personne_max_trouve()

                    
        print(self)
        print("penalites : ", self.info_actuelle["penalties"])
        if self.oracle.send_content(self.conversion_mat_connue()):
            print("Victoire !")
            print("--------------------")
            print("\tFin de la phase 1")
            print("--------------------")
        else:
            print("Défaite !Mais c'est impossible !")        
