from gophersat import *
from collections import deque
import copy
import heapq


class Agent_Hitman:
    def __init__(self):
        self.unknown = "?"
        self.oracle = HitmanReferee()
        self.info_actuelle = self.oracle.start_phase1()

        # Taille de la map
        self.max_L = self.info_actuelle["m"]
        self.max_C = self.info_actuelle["n"]

        # SAT
        self.gophersat = Gophersat(self.max_L, self.max_C)
        self.sat = False
        self.sat_connue = [[self.unknown] * self.max_C for _ in range(self.max_L)]
        self.sat_regard = [[0] * self.max_C for _ in range(self.max_L)]

        # Position de départ
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]

        self.nb_gardes = self.info_actuelle["guard_count"]
        self.nb_invites = self.info_actuelle["civil_count"]

        self.mat_connue = [[self.unknown] * self.max_C for _ in range(self.max_L)]
        self.mat_connue[self.translate_ligne(self._x)][self._y] = empty
        self.sat_connue[self.translate_ligne(self._x)][self._y] = SAT_NP

        self.mat_regard = [[0] * self.max_C for _ in range(self.max_L)]
        self.mat_regard_invite = [[0] * self.max_C for _ in range(self.max_L)]

        self.loc_gardes = set()
        self.loc_invites = set()
        self.invitesTrouves = False
        self.gardesTrouves = False
        self.phase1 = True

    def __str__(self):
        """
        Affichage de la matrice des connaissances de l'agent
        """
        max_length = 4
        border = '-' * (len(str(self.max_L)) + 1)
        border += '+' + '-' * ((max_length + 2) * self.max_C + self.max_L) + '+'
        output = [border]

        for i in range(self.max_L):
            row_str = f'{str(self.translate_ligne(i)).rjust(len(str(self.max_L)))} |'
            for j in range(self.max_C):
                element = self.mat_connue[i][j]
                # element = self.sat_connue[i][j]
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

        ligne_col = ' ' * (len(str(self.max_L)) + 1) + '|'
        for i in range(self.max_C):
            ligne_col += f' {str(i).center(max_length)} |'
        output.append(ligne_col)
        output.append("\n")

        # On affiche la matrice sat_regard qui contient des nombres flottant
        border = '-' * (len(str(self.max_L)) + 1)
        border += '+' + '-' * ((max_length + 2) * self.max_C + self.max_L) + '+'
        output += [border]

        for i in range(self.max_L):
            row = f'{str(self.translate_ligne(i)).rjust(len(str(self.max_L)))} |'
            for j in range(self.max_C):
                # self.sat_regard[i][j] = round(self.sat_regard[i][j], 2)
                val = self.sat_regard[i][j]
                row += f' {str(val).center(max_length)} |'
            output.append(row)
            output.append(border)

        ligne_col = ' ' * (len(str(self.max_L)) + 1) + '|'
        for i in range(self.max_C):
            ligne_col += f' {str(i).center(max_length)} |'
        output.append(ligne_col)
        output.append("\n")

        return '\n'.join(output)

    def check_coord(self, ligne, colonne) -> bool:
        """
        Vérifie si les coordonnées sont dans la matrice
        """
        return 0 <= ligne < self.max_L and 0 <= colonne < self.max_C

    def translate_ligne(self, ligne) -> int:
        """
        Permet de faire en sorte que la ligne 0 soit en bas de la matrice
        """
        return self.max_L - 1 - ligne

    def entendre(self) -> None:
        """
        Méthode qui ajoute les clauses pour l'ouie

        Légère optimisation: si on entend moins de BROUHAHA personnes, on regarde si on a déjà localisé des gens dans
        cette zone
        """
        if not self.sat:
            return
        nb_ouie = self.info_actuelle["hear"]
        pos_ngb = [(x[0], x[1]) for x in self.generate_neighboors(self.translate_ligne(self._x), self._y)]

        # Si on entend moins de BROUHAHA personnes, on regarde si on a déjà localisé des gens dans cette zone
        if nb_ouie < BROUHAHA:
            unknown_pos = []
            for pos in self.generate_neighboors(self.translate_ligne(self._x), self._y):
                if self.mat_connue[pos[0]][pos[1]] == self.unknown:
                    unknown_pos.append((pos[0], pos[1]))
                elif self.mat_connue[pos[0]][pos[1]] in [GardeEst, GardeOuest, GardeNord, GardeSud,
                                                         InviteEst, InviteOuest, InviteNord, InviteSud]:
                    nb_ouie -= 1
            self.gophersat.ajout_clauses_entendre(unknown_pos, nb_ouie)
        else:
            self.gophersat.ajout_clauses_entendre(pos_ngb, nb_ouie)

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

            elif v[1] in [HC.GUARD_N, HC.GUARD_S, HC.GUARD_E, HC.GUARD_W] and (
                    pos_vision_x, pos_vision_y) not in self.loc_gardes:
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

            elif v[1] in [HC.GUARD_N, HC.GUARD_S, HC.GUARD_E, HC.GUARD_W]:
                certitudes.append((pos_vision_x, pos_vision_y, "G"))

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

        if self.sat:
            new_certitudes = [(self.translate_ligne(x[0]), x[1], x[2]) for x in certitudes]
            self.gophersat.ajout_clauses_voir(new_certitudes)

    def generate_neighboors(self, indice_ligne: int, indice_colonne: int) -> LC:
        """
        Fonction qui genere les voisins d'une case donnee
        """
        liste_voisins = []

        for change_ligne in range(-MAX_OUIE, MAX_OUIE + 1):
            for change_col in range(-MAX_OUIE, MAX_OUIE + 1):
                liste_voisins.append(
                    [indice_ligne + change_ligne, indice_colonne + change_col])

        liste_voisins = [voisin for voisin in liste_voisins if self.check_coord(voisin[0], voisin[1])]
        return liste_voisins

    def add_vision_sat(self, ligne: int, colonne: int, newtype: str, oldtype: str) -> None:
        """
        Ajoute la vision d'un type dans la matrice de vision SAT :
        - P? : + 0.1
        - P : + 1
        - G : + 5
        - NP : + 0
        """
        if not self.sat:
            return
        dict_valeur = {
            self.unknown: 0.0,
            SAT_NP: 0,
            SAT_INVITE: 0,
            SAT_PROBA_PERSONNE: 1,
            SAT_PERSONNE: 5,
            SAT_GARDE: 10
        }

        if self.check_coord(ligne, colonne) and newtype != oldtype and \
                newtype in [SAT_NP, SAT_PROBA_PERSONNE, SAT_PERSONNE, SAT_GARDE] and \
                oldtype in [SAT_NP, SAT_PROBA_PERSONNE, SAT_PERSONNE, SAT_GARDE, self.unknown]:
            print("Avant : ", oldtype, "->", end=" ")
            print("Newtype : ", newtype, " en : ", ligne, colonne)

            difference = dict_valeur[newtype] - dict_valeur[oldtype]

            if difference != 0:
                deltas = [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (0, 2), (0, -2), (2, 0), (-2, 0)]

                for delta in deltas:
                    if self.check_coord(ligne + delta[0], colonne + delta[1]):
                        val = self.sat_regard[ligne + delta[0]][colonne + delta[1]] + difference
                        self.sat_regard[ligne + delta[0]][colonne + delta[1]] = max(0, val)

    def verif_vision_sat(self) -> None:
        """
        On limite la vision de la matrice de vision SAT
        """
        if not self.sat:
            return

        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 2), (0, -2), (2, 0), (-2, 0)]

        for i in range(self.max_L):
            for j in range(self.max_C):
                vision_bloque = False

                if self.sat_connue[i][j] == SAT_GARDE and (i, j) not in self.loc_gardes:
                    # Nous n'avons pas encore vu ce garde nous ne l'avons que déduit
                    # On ne connaît pas son orientation donc nous vérifions en croix
                    for delt in deltas:
                        if self.check_coord(i + delt[0], j + delt[1]) and \
                                self.mat_connue[i + delt[0]][j + delt[1]] != empty and \
                                self.mat_connue[i + delt[0]][j + delt[1]] != self.unknown:
                            vision_bloque = True

                        if vision_bloque and self.check_coord(i + delt[0], j + delt[1]):
                            self.sat_regard[i + delt[0]][j + delt[1]] = max(0, self.sat_regard[i + delt[0]][
                                j + delt[1]] - 10)

                elif self.sat_connue[i][j] == SAT_GARDE and (i, j) in self.loc_gardes:
                    # On connaît son orientation donc on vérifie en ligne
                    # On récupère l'orientation du garde
                    type = self.mat_connue[i][j]

                    for v in range(1, MAX_VISION_GARDE + 1):
                        if type == GardeNord:
                            if self.check_coord(i - v, j) and \
                                    self.mat_connue[i - v][j] != empty and \
                                    self.mat_connue[i - v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque and self.check_coord(i - v, j):
                                self.sat_regard[i - v][j] = max(0, self.sat_regard[i - v][j] - 10)

                        elif type == GardeSud:
                            if self.check_coord(i + v, j) and \
                                    self.mat_connue[i + v][j] != empty and \
                                    self.mat_connue[i + v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque and self.check_coord(i + v, j):
                                self.sat_regard[i + v][j] = max(0, self.sat_regard[i + v][j] - 10)

                        elif type == GardeEst:
                            if self.check_coord(i, j + v) and \
                                    self.mat_connue[i][j + v] != empty and \
                                    self.mat_connue[i][j + v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque and self.check_coord(i, j + v):
                                self.sat_regard[i][j + v] = max(0, self.sat_regard[i][j + v] - 10)

                        elif type == GardeOuest:
                            if self.check_coord(i, j - v) and \
                                    self.mat_connue[i][j - v] != empty and \
                                    self.mat_connue[i][j - v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque and self.check_coord(i, j - v):
                                self.sat_regard[i][j - v] = max(0, self.sat_regard[i][j - v] - 10)

                elif self.sat_connue[i][j] == SAT_PROBA_PERSONNE:
                    for delt in deltas:
                        if self.check_coord(i + delt[0], j + delt[1]) and \
                                self.mat_connue[i + delt[0]][j + delt[1]] != empty and \
                                self.mat_connue[i + delt[0]][j + delt[1]] != self.unknown:
                            vision_bloque = True

                        if vision_bloque and self.check_coord(i + delt[0], j + delt[1]):
                            self.sat_regard[i + delt[0]][j + delt[1]] = max(0, self.sat_regard[i + delt[0]][
                                j + delt[1]] - 1)

                elif self.sat_connue[i][j] == SAT_PERSONNE:
                    for delt in deltas:
                        if self.check_coord(i + delt[0], j + delt[1]) and \
                                self.mat_connue[i + delt[0]][j + delt[1]] != empty and \
                                self.mat_connue[i + delt[0]][j + delt[1]] != self.unknown:
                            vision_bloque = True

                        if vision_bloque and self.check_coord(i + delt[0], j + delt[1]):
                            self.sat_regard[i + delt[0]][j + delt[1]] = max(0, self.sat_regard[i + delt[0]][
                                j + delt[1]] - 5)

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

            if info.startswith("I"):
                self.add_vision_invite(ligne, colonne)

            # On ajoute sur la matrice SAT
            if self.sat:
                avant = self.sat_connue[ligne][colonne]
                if info.startswith("G"):
                    self.sat_connue[ligne][colonne] = SAT_GARDE
                    self.add_vision_sat(ligne, colonne, SAT_GARDE, avant)
                elif info.startswith("I"):
                    self.sat_connue[ligne][colonne] = SAT_INVITE
                    self.add_vision_sat(ligne, colonne, SAT_INVITE, avant)
                else:
                    self.sat_connue[ligne][colonne] = SAT_NP
                    self.add_vision_sat(ligne, colonne, SAT_NP, avant)
                self.verif_vision_sat()

            self.verif_vision()
            self.verif_vision_invite()

    def add_vision_invite(self, ligne: int, colonne: int) -> None:
        if self.check_coord(ligne, colonne):
            if self.mat_connue[ligne][colonne] == InviteSud:
                for i in range(1, MAX_VISION_INVITE + 1):
                    if ligne + i < self.max_L:
                        self.mat_regard_invite[ligne + i][colonne] += 1
            elif self.mat_connue[ligne][colonne] == InviteNord:
                for i in range(1, MAX_VISION_INVITE + 1):
                    if ligne - i >= 0:
                        self.mat_regard_invite[ligne - i][colonne] += 1
            elif self.mat_connue[ligne][colonne] == InviteEst:
                for i in range(1, MAX_VISION_INVITE + 1):
                    if colonne + i < self.max_C:
                        self.mat_regard_invite[ligne][colonne + i] += 1
            elif self.mat_connue[ligne][colonne] == InviteOuest:
                for i in range(1, MAX_VISION_INVITE + 1):
                    if colonne - i >= 0:
                        self.mat_regard_invite[ligne][colonne - i] += 1
            else:
                print("Ce n'est pas un invite qui est en (" + str(ligne) + ", " + str(colonne) + ")")

    def verif_vision_invite(self):
        for i in range(len(self.mat_regard_invite)):
            for j in range(len(self.mat_regard_invite)):
                if self.mat_connue[i][j].startswith("I"):
                    vision_bloque = False
                    for v in range(1, MAX_VISION_INVITE + 1):
                        if self.mat_connue[i][j] == InviteSud and i + v < self.max_L:
                            if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard_invite[i + v][j] = max(0, self.mat_regard_invite[i + v][j] - 1)

                        elif self.mat_connue[i][j] == InviteNord and i - v >= 0:

                            if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard_invite[i - v][j] = max(0, self.mat_regard_invite[i - v][j] - 1)

                        elif self.mat_connue[i][j] == InviteEst and j + v < self.max_C:

                            if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard_invite[i][j + v] = max(0, self.mat_regard_invite[i][j + v] - 1)

                        elif self.mat_connue[i][j] == InviteOuest and j - v >= 0:
                            if self.mat_connue[i][j - v] != empty and self.mat_connue[i][j - v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                self.mat_regard_invite[i][j - v] = max(0, self.mat_regard_invite[i][j - v] - 1)

    def gardes_tous_trouves(self) -> bool:
        """
        On vérifie si on a trouvé tous les gardes
        """
        return len(self.loc_gardes) == self.nb_gardes

    def invites_tous_trouves(self) -> bool:
        """
        On vérifie si on a trouvé tous les invités
        """
        return len(self.loc_invites) == self.nb_invites

    def add_vision_garde(self, ligne: int, colonne: int) -> None:
        if self.check_coord(ligne, colonne):
            if self.mat_connue[ligne][colonne] == GardeSud:
                for i in range(1, MAX_VISION_GARDE + 1):
                    if ligne + i < self.max_L:
                        self.mat_regard[ligne + i][colonne] += 5

            elif self.mat_connue[ligne][colonne] == GardeNord:
                for i in range(1, MAX_VISION_GARDE + 1):
                    if ligne - i >= 0:
                        self.mat_regard[ligne - i][colonne] += 5

            elif self.mat_connue[ligne][colonne] == GardeEst:
                for i in range(1, MAX_VISION_GARDE + 1):
                    if colonne + i < self.max_C:
                        self.mat_regard[ligne][colonne + i] += 5

            elif self.mat_connue[ligne][colonne] == GardeOuest:
                for i in range(1, MAX_VISION_GARDE + 1):
                    if colonne - i >= 0:
                        self.mat_regard[ligne][colonne - i] += 5
            else:
                print("Ce n'est pas un garde qui est en (" + str(ligne) + ", " + str(colonne) + ")")

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
                    for v in range(1, MAX_VISION_GARDE + 1):
                        if self.mat_connue[i][j] == GardeSud and i + v < self.max_L:
                            if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                # Sur la case de la target on ne reduit pas le cout car on peut la tuer
                                # Et si on est vu sur cette case en train de tuer on prend une pénalité.
                                if self.mat_connue[i + v][j] == Target:
                                    continue
                                self.mat_regard[i + v][j] = max(0, self.mat_regard[i + v][j] - 5)


                        elif self.mat_connue[i][j] == GardeNord and i - v >= 0:

                            if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                if self.mat_connue[i - v][j] == Target:
                                    continue
                                self.mat_regard[i - v][j] = max(0, self.mat_regard[i - v][j] - 5)

                        elif self.mat_connue[i][j] == GardeEst and j + v < self.max_C:

                            if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                if self.mat_connue[i][j + v] == Target:
                                    continue
                                self.mat_regard[i][j + v] = max(0, self.mat_regard[i][j + v] - 5)

                        elif self.mat_connue[i][j] == GardeOuest and j - v >= 0:
                            if self.mat_connue[i][j - v] != empty and self.mat_connue[i][j - v] != self.unknown:
                                vision_bloque = True

                            if vision_bloque:
                                if self.mat_connue[i][j - v] == Target:
                                    continue
                                self.mat_regard[i][j - v] = max(0, self.mat_regard[i][j - v] - 5)

    def incomplete_mat(self) -> bool:
        """
        On regarde si la matrice est complète ou non, on recherche le premier élément inconnu
        """
        return any(self.unknown in row for row in self.mat_connue)

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

        return nearest_unknown

    def get_neighbours(self, position):
        neighbours = []
        # Right, Left, Down, Up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for direction in directions:
            new_row = position[0] + direction[0]
            new_col = position[1] + direction[1]

            if self.check_coord(new_row, new_col) and self.mat_connue[new_row][new_col] != wall and \
                    self.mat_connue[new_row][new_col] != GardeEst and \
                    self.mat_connue[new_row][new_col] != GardeNord and \
                    self.mat_connue[new_row][new_col] != GardeOuest and \
                    self.mat_connue[new_row][new_col] != GardeSud:
                neighbours.append((new_row, new_col))
        return neighbours

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int], costume: bool = False):
        """
            Algorithme A_star. Prend la postion de départ et la position d'arrivée.
            Renvoie le chemin à suivre pour aller de la position de départ à la position d'arrivée.
            Suppose que start et goal on déjà eu leur translate_ligne.
        """
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: calculate_heuristic(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return reconstruct_path(came_from, current)

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if self.sat:
                    cost = self.sat_regard[neighbour[0]][neighbour[1]]
                else:
                    cost = self.mat_regard[neighbour[0]][neighbour[1]]
                if costume:
                    cost = 0
                tentative_g_score = g_score[current] + cost

                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + calculate_heuristic(neighbour, goal)
                    heapq.heappush(open_list, (f_score[neighbour], neighbour))

        return None

    def coords_case_devant_nous(self) -> PS:
        """
            Renvoie les coords de la case devant nous selon notre direction.
        """

        direction = self.info_actuelle["orientation"]
        if direction == HC.N:
            return self.translate_ligne(self._x) - 1, self._y

        elif direction == HC.S:
            return self.translate_ligne(self._x) + 1, self._y

        elif direction == HC.E:
            return self.translate_ligne(self._x), self._y + 1

        elif direction == HC.W:
            return self.translate_ligne(self._x), self._y - 1

    def first_move(self) -> None:
        """
        Hitman se déplace pour la première fois vers un emplacement empty.
        """
        self.entendre()
        self.voir()
        if self.sat:
            self.sat_utilisation()

        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        pos_x = self.translate_ligne(self._x)
        pos_possible = []

        # On se tourne en sens horaire jusqu'à ce qu’on trouve une case empty
        while len(pos_possible) == 0:
            self.turn()
            for delta in deltas:
                if self.check_coord(pos_x + delta[0], self._y + delta[1]) and \
                        self.mat_connue[pos_x + delta[0]][self._y + delta[1]] == empty:
                    pos_possible.append((pos_x + delta[0], self._y + delta[1]))

        # On est bien tourné vers une case empty
        self.move()

    def move(self) -> None:
        """
        Gère le déplacement d'Hitman
        """
        self.info_actuelle = self.oracle.move()
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]
        self.voir()
        self.entendre()

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

    def conversion_mat_connue(self) -> Dict[Tuple[int, int], HC]:
        """
        Convertit la matrice connue en matrice de HC.
        """
        mat = {}
        for i in range(self.max_L):
            for j in range(self.max_C):
                convert_x = self.max_L - i - 1
                mat[(j, convert_x)] = convert(self.mat_connue[i][j])
        return mat

    def orientation_case_from_pos(self, case_cible: Tuple[int, int]) -> HC:
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

    def best_turn(self, x: int, y: int) -> None:
        """
        On s’oriente vers la case (x, y) en tournant dans le sens le plus court.
        """

        current_orientation = self.info_actuelle["orientation"]
        clockwise_orientation = [HC.N, HC.E, HC.S, HC.W]
        anti_clockwise_orientation = [HC.N, HC.W, HC.S, HC.E]

        get_orientation_target = self.orientation_case_from_pos((x, y))

        clockwise_distance = clockwise_orientation.index(get_orientation_target) - clockwise_orientation.index(
            current_orientation)
        anti_clockwise_distance = anti_clockwise_orientation.index(
            get_orientation_target) - anti_clockwise_orientation.index(current_orientation)

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

    def sat_utilisation(self) -> None:
        """
        On récupère toutes les positions des cases inconnues. On test si ce sont des personnees.
        Si c'est le cas, on ajoute le coût dans sat_regard.
        On update dans tous les cas sat_connue
        """
        if self.gardes_tous_trouves() and not self.invites_tous_trouves():
            self.gophersat.garde_max_trouve()

        if self.invites_tous_trouves() and not self.gardes_tous_trouves():
            self.gophersat.invite_max_trouve()

        if self.gardes_tous_trouves() and self.invites_tous_trouves():
            self.gophersat.personne_max_trouve()

        for i in range(self.max_L):
            for j in range(self.max_C):
                avant = self.sat_connue[i][j]
                if avant in [SAT_PERSONNE or self.sat_connue[i][j] == SAT_PROBA_PERSONNE, self.unknown]:
                    res = self.gophersat.test_personne((i, j))
                    if res == 1:
                        res_p = self.gophersat.test_type((i, j, "G"))
                        if res_p == 1:
                            self.sat_connue[i][j] = SAT_GARDE
                            self.add_vision_sat(i, j, SAT_GARDE, avant)
                        else:
                            res_p = self.gophersat.test_type((i, j, "I"))
                            if res_p == 1:
                                self.sat_connue[i][j] = SAT_INVITE
                                self.add_vision_sat(i, j, SAT_INVITE, avant)
                            else:
                                self.sat_connue[i][j] = SAT_PERSONNE
                                self.add_vision_sat(i, j, SAT_PERSONNE, avant)
                    elif res == 0:
                        self.sat_connue[i][j] = SAT_PROBA_PERSONNE
                        self.add_vision_sat(i, j, SAT_PROBA_PERSONNE, avant)
                    else:
                        self.sat_connue[i][j] = SAT_NP
                        self.add_vision_sat(i, j, SAT_NP, avant)

        self.verif_vision_sat()

    def phase_1(self, sat: bool = False) -> None:
        """
        On fait un tour de jeu du hitman.
        """
        print("--------------------")
        print("\tPhase 1")
        print("--------------------")
        print(self)

        self.sat = sat

        self.first_move()

        queue_action = deque()
        actual_target = None

        while self.incomplete_mat():
            if self.sat:
                self.sat_utilisation()

            for ngb in self.get_neighbours((self.translate_ligne(self._x), self._y)):
                if self.mat_connue[ngb[0]][ngb[1]] == self.unknown:
                    self.best_turn(ngb[0], ngb[1])

            if len(queue_action) == 0:
                nearest_unknown = self.inconnue_plus_proche()
                pos_nu = []
                for nu in nearest_unknown:
                    pos_nu.append((nu[0], nu[1]))
                actual_target = pos_nu[0]
                # print("actual target : ", actual_target)

                a_star_path = self.a_star((self.translate_ligne(self._x), self._y), (pos_nu[0]))

                for coord in a_star_path:
                    queue_action.append(coord)

            else:
                if self.mat_connue[actual_target[0]][actual_target[1]] != self.unknown:
                    queue_action.clear()
                else:
                    next_action = queue_action.popleft()
                    self.best_turn(next_action[0], next_action[1])
                    self.move()

            print(self)
            if not self.incomplete_mat():
                break

        self.oracle.send_content(self.conversion_mat_connue())
        _, score, history, true_map = self.oracle.end_phase1()
        print(score)
        self.phase1 = False

    """
    --------------------------------------------------------------------------------------------------------------------
    
    -------------------------------------------------- PHASE 2 ---------------------------------------------------------
    
    --------------------------------------------------------------------------------------------------------------------
    """

    def find_stg(self, stg: str) -> Tuple[int, int]:
        for i in range(len(self.mat_connue)):
            for j in range(len(self.mat_connue[i])):
                if self.mat_connue[i][j] == stg:
                    return i, j

    def cost_path(self, path: List[Tuple[int, int]], x: int, y: int, direction_hitman: HC) -> int:

        """

            Methode pour calculer le cout d'un chemin. On prend en compte :
            - Le cout de chaque déplacement
            - Le cout des rotations
            - Le cout lorsqu'on est vu en train de mettre le costume
            - Le cout lorsqu'on passe devant un garde sans costume
            - Le cout lorsqu'on tue la cible sans costume et qu'on est vu
            
        """
        cost = 0
        has_suit = False
        suit_on = False
        # print("path : ", path)
        if direction_hitman:
            direction = direction_hitman

        x_simu = x
        y_simu = y

        mat_regard_copie = copy.deepcopy(self.mat_regard)
        mat_regarde_invite_copie = copy.deepcopy(self.mat_regard_invite)
        mat_connue_copie = copy.deepcopy(self.mat_connue)

        for id, coord in enumerate(path):
            # print("coord : ", coord)
            if case_devant_nous(x_simu, y_simu, direction) != coord:
                # print("case devant nous : ", self.case_devant_nous(x_simu, y_simu, direction))
                clockwise_orientation = [HC.N, HC.E, HC.S, HC.W]
                anti_clockwise_orientation = [HC.N, HC.W, HC.S, HC.E]
                if coord[0] == x_simu:
                    if coord[1] > y_simu:
                        get_orientation_target = HC.E
                    else:
                        get_orientation_target = HC.W
                else:
                    if coord[0] > x_simu:
                        get_orientation_target = HC.S
                    else:
                        get_orientation_target = HC.N
                clockwise_distance = clockwise_orientation.index(get_orientation_target) - clockwise_orientation.index(
                    direction)
                anti_clockwise_distance = anti_clockwise_orientation.index(
                    get_orientation_target) - anti_clockwise_orientation.index(direction)

                if clockwise_distance < 0:
                    clockwise_distance += 4
                if anti_clockwise_distance < 0:
                    anti_clockwise_distance += 4

                if clockwise_distance <= anti_clockwise_distance:
                    while case_devant_nous(x_simu, y_simu, direction) != (coord[0], coord[1]):
                        if direction == HC.N:
                            direction = HC.E
                        elif direction == HC.E:
                            direction = HC.S
                        elif direction == HC.S:
                            direction = HC.W
                        elif direction == HC.W:
                            direction = HC.N

                        cost += 1

                else:
                    while case_devant_nous(x_simu, y_simu, direction) != (coord[0], coord[1]):
                        if direction == HC.N:
                            direction = HC.W
                        elif direction == HC.W:
                            direction = HC.S

                        elif direction == HC.S:
                            direction = HC.E

                        elif direction == HC.E:
                            direction = HC.N

                        cost += 1

            cost += 1  # Coût pour se déplacer
            if not suit_on:
                cost += mat_regard_copie[coord[0]][coord[1]]  # Cout des regards des gardes

            if mat_connue_copie[coord[0]][coord[1]] == Corde:
                cost += 1
                mat_connue_copie[coord[0]][coord[1]] = empty

            if mat_connue_copie[coord[0]][coord[1]] == Costume:
                has_suit = True
                cost += 1
                mat_connue_copie[coord[0]][coord[1]] = empty

            # On passe à côté d'un garde ou civil. S'il regarde la cible, on le tue.
            # Générer les voisins et ensuite regarder si un des voisins est un garde et si ce garde regarde la cible.
            neighbours = [(coord[0] + 1, coord[1]), (coord[0] - 1, coord[1]), (coord[0], coord[1] + 1),
                          (coord[0], coord[1] - 1)]
            for neighbour in neighbours:
                if self.check_coord(neighbour[0], neighbour[1]) and mat_connue_copie[neighbour[0]][
                    neighbour[1]].startswith("G"):
                    vision = self.get_vision_guard(neighbour, mat_connue_copie)
                    target_pos = self.find_stg(Target)
                    for v in vision:
                        if v == target_pos:
                            cost += 20
                            cost += 100 * ((mat_regard_copie[coord[0]][coord[1]] // 5) +
                                           mat_regarde_invite_copie[coord[0]][coord[1]])
                            cost += 1  # On Tue donc un cout en plus
                            mat_connue_copie[neighbour[0]][neighbour[1]] = empty
                            for v2 in vision:
                                mat_regard_copie[v2[0]][v2[1]] -= 5
                if self.check_coord(neighbour[0], neighbour[1]) and mat_connue_copie[neighbour[0]][
                    neighbour[1]].startswith("I"):
                    vision = self.get_vision_invite(neighbour, mat_connue_copie)
                    target_pos = self.find_stg(Target)
                    for v in vision:
                        if v == target_pos:
                            cost += 20
                            cost += 100 * ((mat_regard_copie[coord[0]][coord[1]] // 5) +
                                           mat_regarde_invite_copie[coord[0]][coord[1]])
                            cost += 1
                            mat_connue_copie[neighbour[0]][neighbour[1]] = empty
                            for v2 in vision:
                                mat_regarde_invite_copie[v2[0]][v2[1]] -= 1

            if self.mat_regard[coord[0]][coord[1]] == 0:
                # On met uniquement si on n'est pas vu.
                if has_suit:
                    suit_on = True
                    cost += 1

            if self.mat_connue[coord[0]][coord[1]] == Target:
                cost += (self.mat_regard[coord[0]][coord[1]] // 5) * 100
                cost += 1  # On Tue donc un cout en plus
                mat_connue_copie[coord[0]][coord[1]] = empty

            x_simu = coord[0]
            y_simu = coord[1]
            # print("cost : ", cost)

        return cost

    def get_shortest_path_phase2(self):
        x_init, y_init = self.translate_ligne(self._x), self._y

        target_pos = self.find_stg(Target)
        costume_pos = self.find_stg(Costume)
        corde_pos = self.find_stg(Corde)

        couts_chemins = {i: 0 for i in range(1, 4)}

        # Listing des différents chemin pour aller jusqu'à la cible
        # - 1 : init -> costume -> corde -> cible -> init
        # - 2 : init -> corde -> costume -> cible -> init
        # - 3 : init -> corde -> cible -> costume -> init
        # - 4 : init -> corde -> cible -> init

        # A prendre en compte :
        # - Si on nous voit passer le costume on prend cher
        # - Si on nous prend en train de tuer la cible sans costume on prend cher.

        # ---------------------------- 1 ----------------------------

        path_init_costume = self.a_star((x_init, y_init), (costume_pos[0], costume_pos[1]))

        path_cos_to_cord = self.a_star((costume_pos[0], costume_pos[1]), (corde_pos[0], corde_pos[1]))
        path_cord_to_cib = self.a_star((corde_pos[0], corde_pos[1]), (target_pos[0], target_pos[1]))
        path_cib_to_init = self.a_star((target_pos[0], target_pos[1]), (x_init, y_init))
        chemin_1 = path_init_costume + path_cos_to_cord + path_cord_to_cib + path_cib_to_init
        # couts_chemins[1] = len(chemin_1)
        couts_chemins[1] = self.cost_path(chemin_1, x_init, y_init, self.info_actuelle["orientation"])

        # ---------------------------- 2 ----------------------------
        path_init_corde = self.a_star((x_init, y_init), (corde_pos[0], corde_pos[1]))
        path_corde_cos = self.a_star((corde_pos[0], corde_pos[1]), (costume_pos[0], costume_pos[1]))
        path_cos_cib = self.a_star((costume_pos[0], costume_pos[1]), (target_pos[0], target_pos[1]))
        chemin_2 = path_init_corde + path_corde_cos + path_cos_cib + path_cib_to_init
        # couts_chemins[2] = len(chemin_2)
        couts_chemins[2] = self.cost_path(chemin_2, x_init, y_init, self.info_actuelle["orientation"])

        # ---------------------------- 3 ----------------------------
        path_cord_cib = self.a_star((corde_pos[0], corde_pos[1]), (target_pos[0], target_pos[1]))
        path_cib_cos = self.a_star((target_pos[0], target_pos[1]), (costume_pos[0], costume_pos[1]))
        path_cos_init = self.a_star((costume_pos[0], costume_pos[1]), (x_init, y_init))
        chemin_3 = path_init_corde + path_cord_cib + path_cib_cos + path_cos_init
        # couts_chemins[3] = len(chemin_3)
        couts_chemins[3] = self.cost_path(chemin_3, x_init, y_init, self.info_actuelle["orientation"])

        # ---------------------------- 4 ----------------------------
        path_cord_cib = self.a_star((corde_pos[0], corde_pos[1]), (target_pos[0], target_pos[1]))
        path_cib_to_init = self.a_star((target_pos[0], target_pos[1]), (x_init, y_init))
        chemin_4 = path_init_corde + path_cord_cib + path_cib_to_init
        # couts_chemins[4] = len(chemin_4)
        couts_chemins[4] = self.cost_path(chemin_4, x_init, y_init, self.info_actuelle["orientation"])

        # ---------------------------- INFO ----------------------------

        # On prend le chemin le plus court
        chemin = min(couts_chemins, key=couts_chemins.get)
        # print("Shortest path : ", chemin)

        if chemin == 1:
            return chemin_1
        elif chemin == 2:
            return chemin_2
        elif chemin == 3:
            return chemin_3
        elif chemin == 4:
            return chemin_4

    def is_seen(self) -> bool:
        """

        Permet de savoir si nous sommes dans le champ de vision d'un garde ou d'un invité

        """

        for loc in self.loc_invites:  # Une case
            ngb = self.get_neighbours((loc[0], loc[1]))
            if (self.translate_ligne(self._x), self._y) in ngb:
                return True

        for loc in self.loc_gardes:  # Deux cases dans sa direction
            vision_bloque = False
            i = loc[0]
            j = loc[1]

            for v in range(1, MAX_VISION_GARDE + 1):
                if self.mat_connue[i][j] == GardeSud and i + v < self.max_L:
                    if self.mat_connue[i + v][j] != empty and self.mat_connue[i + v][j] != self.unknown:
                        vision_bloque = True

                    if (self.translate_ligne(self._x), self._y) == (i + v, j) and not vision_bloque:
                        return True

                if self.mat_connue[i][j] == GardeNord and i - v >= 0:
                    if self.mat_connue[i - v][j] != empty and self.mat_connue[i - v][j] != self.unknown:
                        vision_bloque = True

                    if (self.translate_ligne(self._x), self._y) == (i - v, j) and not vision_bloque:
                        return True

                if self.mat_connue[i][j] == GardeEst and j + v < self.max_C:
                    if self.mat_connue[i][j + v] != empty and self.mat_connue[i][j + v] != self.unknown:
                        vision_bloque = True

                    if (self.translate_ligne(self._x), self._y) == (i, j + v) and not vision_bloque:
                        return True

                if self.mat_connue[i][j] == GardeOuest and j - v >= 0:
                    if self.mat_connue[i][j - v] != empty and self.mat_connue[i][j - v] != self.unknown:
                        vision_bloque = True

                    if (self.translate_ligne(self._x), self._y) == (i, j - v) and not vision_bloque:
                        return True

        return False

    def get_vision_invite(self, invite: Tuple[int, int], mat: List[List] = None) -> List[Tuple[int, int]]:
        """
        Renvoie la liste des cases que l'invite voit.
        """
        vision = []
        i = invite[0]
        j = invite[1]

        if mat:
            mat_connue = mat

        else:
            mat_connue = self.mat_connue

        for v in range(1, MAX_VISION_INVITE + 1):
            if mat_connue[i][j] == InviteSud and i + v < self.max_L:
                if self.mat_connue[i + v][j] == empty or mat_connue[i + v][j] == Target:
                    vision.append((i + v, j))
                else:

                    return vision

            if self.mat_connue[i][j] == InviteNord and i - v >= 0:
                if mat_connue[i - v][j] == empty or mat_connue[i - v][j] == Target:

                    vision.append((i - v, j))

                else:

                    return vision

            if mat_connue[i][j] == InviteEst and j + v < self.max_C:
                if mat_connue[i][j + v] == empty or mat_connue[i][j + v] == Target:
                    vision.append((i, j + v))

                else:
                    return vision

            if mat_connue[i][j] == InviteOuest and j - v >= 0:
                if mat_connue[i][j - v] == empty or mat_connue[i][j - v] == Target:

                    vision.append((i, j - v))
                else:
                    return vision

        return vision

    def get_vision_guard(self, guard: Tuple[int, int], mat: List[List] = None) -> List[Tuple[int, int]]:
        """
        Renvoie la liste des cases que le garde voit.
        """
        vision = []
        i = guard[0]
        j = guard[1]

        if mat:
            mat_connue = mat

        else:
            mat_connue = self.mat_connue

        for v in range(1, MAX_VISION_GARDE + 1):
            if mat_connue[i][j] == GardeSud and i + v < self.max_L:
                if self.mat_connue[i + v][j] == empty or mat_connue[i + v][j] == Target:
                    vision.append((i + v, j))

                return vision

            if self.mat_connue[i][j] == GardeNord and i - v >= 0:
                if mat_connue[i - v][j] == empty or mat_connue[i - v][j] == Target:
                    vision.append((i - v, j))

                return vision

            if mat_connue[i][j] == GardeEst and j + v < self.max_C:
                if mat_connue[i][j + v] == empty or mat_connue[i][j + v] == Target:
                    vision.append((i, j + v))

                else:
                    return vision

            if mat_connue[i][j] == GardeOuest and j - v >= 0:
                if mat_connue[i][j - v] == empty or mat_connue[i][j - v] == Target:

                    vision.append((i, j - v))
                else:
                    return vision

        return vision

    def phase_2(self):
        print("--------------------")
        print("\tPhase 2")
        print("--------------------")
        # Correction temporaire
        self.sat = False  # Si le sat est à True les trajets d'a_start sont modifiés.

        self.info_actuelle = self.oracle.start_phase2()
        # print("direction : ", self.info_actuelle["orientation"])
        # print("penalites : ", self.info_actuelle["penalties"])
        self._x = self.info_actuelle["position"][1]
        self._y = self.info_actuelle["position"][0]
        print(self)

        # print("penalites : ", self.info_actuelle["penalties"])

        chemin = self.get_shortest_path_phase2()
        print("chemin : ", chemin)
        if not chemin:
            return

        possede_costume = False

        queue_action = deque()
        for coord in chemin:
            queue_action.append(coord)

        while len(queue_action) != 0:
            # print("penalites : ", self.info_actuelle["penalties"])
            next_action = queue_action.popleft()
            self.best_turn(next_action[0], next_action[1])
            self.info_actuelle = self.oracle.move()
            # print("penalites : ", self.info_actuelle["penalties"])
            self._x = self.info_actuelle["position"][1]
            self._y = self.info_actuelle["position"][0]

            if self.mat_connue[self.translate_ligne(self._x)][self._y] == Corde:
                self.info_actuelle = self.oracle.take_weapon()
                # print("penalites : ", self.info_actuelle["penalties"])
                self.mat_connue[self.translate_ligne(self._x)][self._y] = empty

            elif self.mat_connue[self.translate_ligne(self._x)][self._y] == Costume:
                self.info_actuelle = self.oracle.take_suit()
                # print("penalites : ", self.info_actuelle["penalties"])
                possede_costume = True
                self.mat_connue[self.translate_ligne(self._x)][self._y] = empty

            elif self.mat_connue[self.translate_ligne(self._x)][self._y] == Target:
                self.info_actuelle = self.oracle.kill_target()
                # print("penalites : ", self.info_actuelle["penalties"])
                self.mat_connue[self.translate_ligne(self._x)][self._y] = DEAD

            if possede_costume and not self.is_seen():
                self.info_actuelle = self.oracle.put_on_suit()

            neighbours = [(self.translate_ligne(self._x) + 1, self._y), (self.translate_ligne(self._x) - 1, self._y),
                          (self.translate_ligne(self._x), self._y + 1), (self.translate_ligne(self._x), self._y - 1)]

            for ngb in neighbours:
                # print("case ngb : ", self.mat_connue[ngb[0]][ngb[1]])

                if not self.check_coord(ngb[0], ngb[1]):
                    continue
                if self.mat_connue[ngb[0]][ngb[1]] == GardeEst or self.mat_connue[ngb[0]][ngb[1]] == GardeNord or \
                        self.mat_connue[ngb[0]][ngb[1]] == GardeOuest or self.mat_connue[ngb[0]][ngb[1]] == GardeSud:
                    # Regarder si ce garde regarde la cible : 
                    # Si oui, on le tue
                    # Sinon on passe devant lui

                    regards_garde = self.get_vision_guard(ngb)

                    for rg in regards_garde:
                        target_pos = self.find_stg(Target)
                        if rg == target_pos:

                            self.best_turn(ngb[0], ngb[1])
                            if self.mat_connue[ngb[0]][ngb[1]] == GardeEst or self.mat_connue[ngb[0]][
                                ngb[1]] == GardeNord or self.mat_connue[ngb[0]][ngb[1]] == GardeOuest or \
                                    self.mat_connue[ngb[0]][ngb[1]] == GardeSud:
                                self.info_actuelle = self.oracle.neutralize_guard()
                                # print("penalites : ", self.info_actuelle["penalties"])

                            self.mat_connue[ngb[0]][ngb[1]] = empty

                if self.mat_connue[ngb[0]][ngb[1]] == InviteEst or self.mat_connue[ngb[0]][ngb[1]] == InviteNord or \
                        self.mat_connue[ngb[0]][ngb[1]] == InviteOuest or self.mat_connue[ngb[0]][ngb[1]] == InviteSud:
                    # Regarder si cet invité regarde la cible :
                    # Si oui, on le tue
                    # Sinon on passe devant lui

                    regards_invite = self.get_vision_invite(ngb)

                    for rg in regards_invite:
                        target_pos = self.find_stg(Target)
                        if rg == target_pos:

                            self.best_turn(ngb[0], ngb[1])
                            if self.mat_connue[ngb[0]][ngb[1]] == InviteEst or self.mat_connue[ngb[0]][
                                ngb[1]] == InviteNord or self.mat_connue[ngb[0]][ngb[1]] == InviteOuest or \
                                    self.mat_connue[ngb[0]][ngb[1]] == InviteSud:
                                self.info_actuelle = self.oracle.neutralize_invite()
                                # print("penalites : ", self.info_actuelle["penalties"])

                            self.mat_connue[ngb[0]][ngb[1]] = empty

            print(self)

        _, score, history = self.oracle.end_phase2()
        print("score : ", score)
        # print("history : ", history)
