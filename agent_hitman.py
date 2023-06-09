from variables import *
from hitman import *
from gophersat import *
from collections import deque
import heapq


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
                element = self.mat_connue[i][j]
                if self.translate_ligne(self._x) == i and self._y == j:
                    element += " H"
                    orientation_dict = {
                        HC.N: "\u2191",
                        HC.S: "\u2193",
                        HC.E: "\u2192",
                        HC.W: "\u2190"
                    }
                    element += orientation_dict.get(self.info_actuelle["orientation"], "")
                element_str = element.center(max_length)
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

                liste_voisins.append(
                    [Indice_ligne + change_ligne, Indice_colonne + change_col])

        return liste_voisins

    def ajout_info_mat(self, ligne: int, colonne: int, info: str) -> None:
        """
        Ajoute une information dans la matrice de connaissance et convertit la ligne
        """

        ligne = self.translate_ligne(ligne)
        if self.check_coord(ligne, colonne):
            self.mat_connue[ligne][colonne] = info

            # Si garde on ajoute sa vision
            if info.startswith("G"):
                self.add_vision_garde(ligne, colonne)
            
            self.verif_vision()

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
        x = self.translate_ligne(self._x)
        neighbors = self.generate_neighboors(x, self._y)
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
                    self.ajout_info_mat(
                        pos_vision_x, pos_vision_y, InviteOuest)

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
        res = self.gophersat.test_personne((x, y, Personne))
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
                print("Ce n'est pas un garde qui est en (" +
                      str(ligne) + ", " + str(colonne) + ")")

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
                    for v in range(1, MAX_VISION_GARDE+1):
                        if self.mat_connue[i][j] == GardeSud and i + v < self.max_L:
                            if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard[i + v][j] = 0

                        elif self.mat_connue[i][j] == GardeNord and i - v >= 0:

                            if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard[i - v][j] = 0

                        elif self.mat_connue[i][j] == GardeEst and j + v < self.max_C:

                            if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != self.unknown:
                                vision_bloque = True
                            
                            if vision_bloque:
                                self.mat_regard[i][j + v] = 0

                        elif self.mat_connue[i][j] == GardeOuest and j - v >= 0:
                            if self.mat_connue[i][j - v] != empty and self.mat_connue[i][j - v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard[i][j - v] = 0

    def incomplete_mat(self) -> bool:
        """
        On regarde si la matrice est complète ou non, on recherche le premier élément inconnu
        """
        return any(self.unknown in row for row in self.mat_connue)

    def est_sur_bord(self, position: PS) -> bool:
        bord_haut = self.max_L-1
        bord_bas = 0
        bord_gauche = 0
        bord_droit = self.max_C-1
        x, y = position
        return x in (bord_haut, bord_bas) or y in (bord_gauche, bord_droit)

    def inconnue_plus_proche(self) -> List[Tuple[int, int, int]]:
        """
        Methode pour trouver le unkown le plus proche.
        """

        deplacements = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        file_attente = deque()
        visite = [[False] * self.max_C for _ in range(self.max_L)]

        x, y = self.translate_ligne(self._x), self._y
        visite[x][y] = True

        file_attente.append((x, y, 0))
        nearest_unknown = []

        # Recherche en largeur
        while file_attente:
            x, y, distance = file_attente.popleft()

            # Vérifier si la case actuelle est inconnue
            if self.mat_connue[x][y] == self.unknown:
                nearest_unknown.append((x, y, distance))
                continue

            # Explorer les cases voisines
            for dx, dy in deplacements:
                nx, ny = x + dx, y + dy

                # Vérifier si la case voisine est valide et non visitée
                if self.check_coord(nx, ny) and self.mat_connue[nx][ny] != wall and not visite[nx][ny]:
                    visite[nx][ny] = True
                    file_attente.append((nx, ny, distance + 1))

        sorted_unknown = sorted(nearest_unknown, key=lambda x: x[2])
        
        # On retourne tous les unkown ayant la même distance
        nearest_distance = sorted_unknown[0][2]
        nearest_unknown = [unknown for unknown in sorted_unknown if unknown[2] == nearest_distance]
        print(nearest_unknown)
        return nearest_unknown
        
    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def calculate_heuristic(self, current, goal):
        # Manhattan distance heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbours(self, position):
        neighbours = []
        # Right, Left, Down, Up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for direction in directions:
            new_row = position[0] + direction[0]
            new_col = position[1] + direction[1]

            if self.check_coord(new_row, new_col) and self.mat_connue[new_row][new_col] != wall and \
                    self.mat_connue[new_row][new_col] != Garde and \
                    self.mat_connue[new_row][new_col] != GardeEst and \
                    self.mat_connue[new_row][new_col] != GardeNord and \
                    self.mat_connue[new_row][new_col] != GardeOuest and \
                    self.mat_connue[new_row][new_col] != GardeSud:
                neighbours.append((new_row, new_col))

        return neighbours

    def A_star(self, start: Tuple[int, int], goal: Tuple[int, int]):
        """
            Algorithme A_star. Prend la postion de départ et la position d'arrivée.
            Renvoie le chemin à suivre pour aller de la position de départ à la position d'arrivée.
            Suppose que start et goal on déjà eu leur translate_ligne.
        """
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.calculate_heuristic(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                cost = self.mat_regard[neighbour[0]][neighbour[1]]
                tentative_g_score = g_score[current] + cost

                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + \
                        self.calculate_heuristic(neighbour, goal)
                    heapq.heappush(open_list, (f_score[neighbour], neighbour))

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
                    self.mat_connue[row][col] != GardeSud:

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
            self.turn()
            for delta in deltas:
                if self.check_coord(pos_x + delta[0], self._y + delta[1]) and self.mat_connue[pos_x + delta[0]][self._y + delta[1]] == empty:
                    pos_possible.append((pos_x + delta[0], self._y + delta[1]))

        # On est bien tourné vers une case empty
        self.move()
        
        
        pos_x = self.translate_ligne(self._x)
                
        unknown_neighours = self.get_neighbours((pos_x, self._y))
        for neighbour in unknown_neighours:
            self.best_turn(neighbour[0], neighbour[1])

    def move(self) -> None:
        """
        Gère le déplacement d'Hitman
        """
        self.info_actuelle = self.oracle.move()
        self.entendre()
        self.voir()
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]

    def turn(self, clockwise: bool = True) -> None:
        """
        Gère la rotation d'Hitman
        
        Par défaut on tourne dans le sens horaire (False pour le sens anti-horaire)
        """
        if clockwise:
            self.info_actuelle = self.oracle.turn_clockwise()
        else:
            self.info_actuelle = self.oracle.turn_anti_clockwise()

        self.voir()
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
                convert_x = self.max_L - i - 1
                mat[(j, convert_x)] = self.convert(self.mat_connue[i][j])
        return mat

    def orientation_case_from_pos (self, case_cible : Tuple[int, int]) -> HC:
        """
        On retourne l'orientation de la case cible par rapport à notre position actuelle.
        """
    
        if case_cible[0] == self.translate_ligne(self._x):
            if case_cible[1] > self._y:
                return HC.E
            else:
                return HC.W
        else:
            if case_cible[0] > self.translate_ligne(self._x):
                return HC.S
            else:
                return HC.N

    def best_turn (self, x: int, y: int) -> None:
        """
        On s'oriente vers la case (x, y) en tournant dans le sens le plus court.
        """
        
        current_orientation = self.info_actuelle["orientation"]
        clockwise_orientation = [HC.N, HC.E, HC.S, HC.W]
        anti_clockwise_orientation = [HC.N, HC.W, HC.S, HC.E]
        
        get_orientation_target = self.orientation_case_from_pos((x, y))
        
        clockwise_distance = clockwise_orientation.index(get_orientation_target) - clockwise_orientation.index(current_orientation)
        anti_clockwise_distance = anti_clockwise_orientation.index(get_orientation_target) - anti_clockwise_orientation.index(current_orientation)
        
        if clockwise_distance < 0:
            clockwise_distance += 4
        if anti_clockwise_distance < 0:
            anti_clockwise_distance += 4
                
        if clockwise_distance <= anti_clockwise_distance:
            while self.coords_case_devant_nous() != (x, y):
                self.turn()
        else:
            while self.coords_case_devant_nous() != (x, y):
                self.turn(False)
                
        
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
            for ngb in self.get_neighbours((self.translate_ligne(self._x), self._y)):
                if self.mat_connue[ngb[0]][ngb[1]] == self.unknown:
                    self.best_turn(ngb[0], ngb[1])
            
            if len(queue_action) == 0:
                nearest_unknown = self.inconnue_plus_proche() 
                pos_nu = []
                for nu in nearest_unknown:
                    pos_nu.append((nu[0], nu[1]))
                print("Inconnue la plus proche : " + str(pos_nu))
                actual_target = pos_nu[0]
                    
                print("Target : " + str(actual_target))
                    
                a_star_path = self.A_star((self.translate_ligne(self._x), self._y), (pos_nu[0]))
                
                print("A* : " + str(a_star_path))
                for coord in a_star_path:
                    queue_action.append(coord)                
                
            else:
                if self. mat_connue[actual_target[0]][actual_target[1]] != self.unknown:
                    queue_action.clear()
                else:
                    next_action = queue_action.popleft()
                    self.best_turn(next_action[0], next_action[1])
                    self.move()

                """ if not self.gardesTrouves and self.gardesTousTrouves():
                    self.gardesTrouves = True
                    self.gophersat.garde_max_trouve()
                    if self.invitesTrouves:
                        self.gophersat.personne_max_trouve()

                if not self.invitesTrouves and self.invitesTousTrouves():
                    self.gardesTrouves = True
                    self.gophersat.invite_max_trouve()
                    if self.gardesTrouves:
                        self.gophersat.personne_max_trouve() """
                        
            if not self.incomplete_mat():
                break

        print("penalites : ", self.info_actuelle["penalties"])

        self.oracle.send_content(self.conversion_mat_connue())
        _, score, history, true_map = self.oracle.end_phase1()
        print(score)
    