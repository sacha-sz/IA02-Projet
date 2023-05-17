import les_contraintes_clausales_en_cavales as cc
import les_axiomes_universels as au
from hitman import Hitman

def main():
    Hitman1 = Hitman(3, 3, 0, 0)
    print(Hitman1)
    """
    print(Hitman1)
    Hitman1.ajout_info_mat(1, 1, "GN")
    print(Hitman1)
    Hitman1.ajout_info_mat(2, 0, "GE")
    print(Hitman1)
    Hitman1.ajout_info_mat(2, 1, "GO")
    
    print(Hitman1)
    """
    au.add_to_file(au.entendre_voisins(Hitman1.x, Hitman1.y, 0))
    


if __name__ == "__main__":
    main()